#!/usr/bin/env python3
"""
Dashboard module for ECLI Metadata Database.
Provides web-based visualization of corpus statistics and metadata.
"""

import os
import sqlite3
import json
from datetime import datetime
import pandas as pd
from flask import Flask, render_template, jsonify, request, Response, send_from_directory
import plotly
import plotly.express as px
import plotly.graph_objects as go

# Initialize Flask app
app = Flask(__name__)

# Configuration
DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ecli_test.db')
print(f"Using database at: {DEFAULT_DB_PATH}")
print(f"Current working directory: {os.getcwd()}")
print(f"Database exists: {os.path.exists(DEFAULT_DB_PATH)}")

def get_db_connection(db_path=None):
    """
    Get a connection to the database.
    
    Args:
        db_path (str, optional): Path to the database file
        
    Returns:
        sqlite3.Connection: Database connection
    """
    if db_path is None:
        db_path = DEFAULT_DB_PATH
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_corpus_stats():
    """
    Get the latest corpus statistics.
    
    Returns:
        dict: Corpus statistics
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query the corpus_stats table
    cursor.execute('''
    SELECT * FROM corpus_stats
    ORDER BY id DESC
    LIMIT 1
    ''')
    
    row = cursor.fetchone()
    if row:
        # Convert row to dictionary
        stats = dict(row)
        
        # Parse JSON fields with error handling
        if stats.get('courts'):
            try:
                stats['courts'] = json.loads(stats['courts'])
            except json.JSONDecodeError:
                stats['courts'] = {}
        
        if stats.get('years'):
            try:
                stats['years'] = json.loads(stats['years'])
            except json.JSONDecodeError:
                stats['years'] = {}
        
        conn.close()
        return stats
    
    # If no stats found, generate basic stats from documents table
    cursor.execute('SELECT COUNT(*) FROM documents')
    total_documents = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(page_count) FROM document_metrics')
    total_pages = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT SUM(file_size) FROM document_metrics')
    total_size = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT court, COUNT(*) as count FROM documents GROUP BY court')
    courts = {row[0]: row[1] for row in cursor.fetchall() if row[0]}
    
    cursor.execute('SELECT year, COUNT(*) as count FROM documents GROUP BY year')
    years = {str(row[0]): row[1] for row in cursor.fetchall() if row[0]}
    
    stats = {
        'total_documents': total_documents,
        'total_pages': total_pages,
        'total_size_bytes': total_size,
        'courts': courts,
        'years': years,
        'generated_date': datetime.now().isoformat()
    }
    
    conn.close()
    return stats

def get_documents_by_court():
    """
    Get the number of documents by court.
    
    Returns:
        pd.DataFrame: DataFrame with court and count columns
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT court, COUNT(*) as count
    FROM documents
    WHERE court IS NOT NULL
    GROUP BY court
    ORDER BY count DESC
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    if rows:
        df = pd.DataFrame(rows, columns=['court', 'count'])
        return df
    
    return pd.DataFrame(columns=['court', 'count'])

def get_documents_by_year():
    """
    Get the number of documents by year.
    
    Returns:
        pd.DataFrame: DataFrame with year and count columns
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT year, COUNT(*) as count
    FROM documents
    WHERE year IS NOT NULL
    GROUP BY year
    ORDER BY year
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    if rows:
        df = pd.DataFrame(rows, columns=['year', 'count'])
        return df
    
    return pd.DataFrame(columns=['year', 'count'])

def get_document_metrics():
    """
    Get document metrics (page count, file size).
    
    Returns:
        pd.DataFrame: DataFrame with document metrics
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT d.ecli_id, d.court, d.year, m.page_count, m.file_size
    FROM documents d
    JOIN document_metrics m ON d.id = m.document_id
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    if rows:
        df = pd.DataFrame(rows, columns=['ecli_id', 'court', 'year', 'page_count', 'file_size'])
        return df
    
    return pd.DataFrame(columns=['ecli_id', 'court', 'year', 'page_count', 'file_size'])

def get_recent_documents(limit=10):
    """
    Get the most recently added documents.
    
    Args:
        limit (int): Maximum number of documents to return
        
    Returns:
        list: List of document dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # First try with added_date field
        cursor.execute('''
        SELECT d.id, d.ecli_id, d.court, d.year, d.added_date, m.page_count, m.file_size
        FROM documents d
        LEFT JOIN document_metrics m ON d.id = m.document_id
        ORDER BY d.added_date DESC
        LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        
        # If no rows or added_date is NULL, try with document ID as fallback
        if not rows:
            cursor.execute('''
            SELECT d.id, d.ecli_id, d.court, d.year, d.added_date, m.page_count, m.file_size
            FROM documents d
            LEFT JOIN document_metrics m ON d.id = m.document_id
            ORDER BY d.id DESC
            LIMIT ?
            ''', (limit,))
            rows = cursor.fetchall()
        
        documents = []
        for row in rows:
            doc = dict(row)
            # Ensure all required fields have at least a default value
            if doc.get('ecli_id') is None:
                doc['ecli_id'] = f"ECLI_UNKNOWN_{doc.get('id', 'UNKNOWN')}"
            if doc.get('court') is None:
                doc['court'] = 'Unknown'
            if doc.get('year') is None:
                doc['year'] = 'Unknown'
            if doc.get('added_date') is None:
                doc['added_date'] = 'Unknown'
            documents.append(doc)
        
        conn.close()
        return documents
    except Exception as e:
        print(f"Error getting recent documents: {e}")
        conn.close()
        return []

def search_documents(query):
    """
    Search for documents matching the query.
    
    Args:
        query (dict): Search query parameters
        
    Returns:
        list: Matching documents
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build the query
    sql = '''
    SELECT d.ecli_id, d.court, d.year, d.added_date, m.page_count, m.file_size
    FROM documents d
    LEFT JOIN document_metrics m ON d.id = m.document_id
    WHERE 1=1
    '''
    params = []
    
    # Add query parameters
    if 'court' in query and query['court']:
        sql += ' AND d.court = ?'
        params.append(query['court'])
    
    if 'year' in query and query['year']:
        sql += ' AND d.year = ?'
        params.append(query['year'])
    
    if 'min_pages' in query and query['min_pages']:
        sql += ' AND m.page_count >= ?'
        params.append(int(query['min_pages']))
    
    if 'max_pages' in query and query['max_pages']:
        sql += ' AND m.page_count <= ?'
        params.append(int(query['max_pages']))
    
    # Add order by
    sql += ' ORDER BY d.added_date DESC'
    
    # Execute the query
    cursor.execute(sql, params)
    
    rows = cursor.fetchall()
    conn.close()
    
    if rows:
        documents = [dict(row) for row in rows]
        return documents
    
    return []

# Routes
@app.route('/')
def index():
    """Render the dashboard home page."""
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    """API endpoint for corpus statistics."""
    stats = get_corpus_stats()
    return jsonify(stats)

@app.route('/api/courts')
def get_courts():
    """API endpoint for documents by court."""
    df = get_documents_by_court()
    
    # Create a bar chart
    fig = px.bar(df, x='court', y='count', title='Documents by Court')
    fig.update_layout(xaxis_title='Court', yaxis_title='Number of Documents')
    
    # Convert to JSON
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Return with proper content type
    return Response(graph_json, mimetype='application/json')

@app.route('/api/years')
def get_years():
    """API endpoint for documents by year."""
    df = get_documents_by_year()
    
    # Create a line chart
    fig = px.line(df, x='year', y='count', title='Documents by Year')
    fig.update_layout(xaxis_title='Year', yaxis_title='Number of Documents')
    
    # Convert to JSON
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Return with proper content type
    return Response(graph_json, mimetype='application/json')

@app.route('/api/metrics')
def get_metrics():
    """API endpoint for document metrics."""
    df = get_document_metrics()
    
    # Create a scatter plot
    fig = px.scatter(df, x='page_count', y='file_size', color='court',
                    title='Document Metrics', hover_data=['ecli_id', 'year'])
    fig.update_layout(xaxis_title='Page Count', yaxis_title='File Size (bytes)')
    
    # Convert to JSON
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Return with proper content type
    return Response(graph_json, mimetype='application/json')

@app.route('/api/recent')
def get_recent():
    """API endpoint for recent documents."""
    documents = get_recent_documents()
    return jsonify(documents)

@app.route('/api/document/<ecli_id>')
def get_document(ecli_id):
    """API endpoint for document details."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query the documents table
    cursor.execute('''
    SELECT d.*, m.page_count, m.file_size, m.document_date, m.judge, m.pdf_metadata
    FROM documents d
    LEFT JOIN document_metrics m ON d.id = m.document_id
    WHERE d.ecli_id = ?
    ''', (ecli_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        # Convert row to dictionary
        doc = dict(row)
        
        # Parse PDF metadata if available
        if doc.get('pdf_metadata'):
            try:
                pdf_metadata = json.loads(doc['pdf_metadata'])
                doc.update(pdf_metadata)
            except:
                pass
            del doc['pdf_metadata']
        
        return jsonify(doc)
    
    return jsonify({'error': 'Document not found'}), 404

@app.route('/api/search')
def search():
    """API endpoint for document search."""
    query = {
        'court': request.args.get('court'),
        'year': request.args.get('year'),
        'min_pages': request.args.get('min_pages'),
        'max_pages': request.args.get('max_pages')
    }
    
    documents = search_documents(query)
    return jsonify(documents)

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """API endpoint for submitting user feedback."""
    feedback_data = request.json
    
    if not feedback_data:
        return jsonify({'error': 'No feedback data provided'}), 400
    
    # Add timestamp to feedback
    feedback_data['timestamp'] = datetime.now().isoformat()
    
    # Store feedback in the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create feedback table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        feedback_type TEXT,
        rating INTEGER,
        comment TEXT,
        document_id TEXT,
        user_agent TEXT,
        timestamp TEXT
    )
    ''')
    
    # Insert feedback
    cursor.execute('''
    INSERT INTO user_feedback 
    (feedback_type, rating, comment, document_id, user_agent, timestamp)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        feedback_data.get('type'),
        feedback_data.get('rating'),
        feedback_data.get('comment'),
        feedback_data.get('document_id'),
        feedback_data.get('user_agent'),
        feedback_data.get('timestamp')
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Feedback submitted successfully'})

# Run the app if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
