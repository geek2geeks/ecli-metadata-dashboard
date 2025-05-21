#!/usr/bin/env python3
"""
Initialize the SQLite database for the ECLI Metadata Dashboard.
Creates necessary tables and populates them with sample data.
"""

import os
import sqlite3
import json
from datetime import datetime

# Database path
DB_PATH = os.environ.get('ECLI_DB_PATH', 'ecli_test.db')

def init_database():
    """Initialize the database with tables and sample data."""
    print(f"Initializing database at: {os.path.abspath(DB_PATH)}")
    
    # Connect to database (will create it if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create documents table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ecli_id TEXT UNIQUE NOT NULL,
        court TEXT,
        year TEXT,
        case_number TEXT,
        file_path TEXT,
        added_date TEXT,
        last_updated TEXT
    )
    ''')
    
    # Create document_metrics table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS document_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        page_count INTEGER,
        file_size INTEGER,
        document_date TEXT,
        language TEXT,
        judge TEXT,
        pdf_metadata TEXT,
        FOREIGN KEY (document_id) REFERENCES documents (id)
    )
    ''')
    
    # Create corpus_stats table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS corpus_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total_documents INTEGER,
        total_pages INTEGER,
        total_size_bytes INTEGER,
        courts TEXT,
        years TEXT,
        generated_at TEXT
    )
    ''')
    
    # Create user_feedback table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id TEXT,
        type TEXT,
        rating INTEGER,
        comment TEXT,
        user_agent TEXT,
        submitted_at TEXT
    )
    ''')
    
    # Commit changes
    conn.commit()
    
    # Check if we need to add sample data
    cursor.execute('SELECT COUNT(*) FROM documents')
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("Adding sample data...")
        add_sample_data(conn)
    else:
        print(f"Database already contains {count} documents. Skipping sample data.")
    
    # Generate corpus statistics
    generate_corpus_stats(conn)
    
    # Close connection
    conn.close()
    print("Database initialization complete.")

def add_sample_data(conn):
    """Add sample data to the database."""
    cursor = conn.cursor()
    
    # Sample courts
    courts = ['STJ', 'TRL', 'TRP', 'TRC', 'TRE', 'TRG', 'STA', 'TCA', 'TCN', 'TCS']
    
    # Sample years
    years = ['1966', '1991', '1998', '2000', '2008', '2011', '2012', '2018', '2020', '2022', '2023', '2024', '2025']
    
    # Sample documents
    documents = []
    for court in courts:
        for i in range(1, 6):  # 5 documents per court
            year = years[i % len(years)]
            case_number = f"{i:06d}"
            ecli_id = f"ECLI_PT_{court}_{year}_{case_number}"
            
            documents.append({
                'ecli_id': ecli_id,
                'court': court,
                'year': year,
                'case_number': case_number,
                'file_path': f"examples/sample_documents/{ecli_id}.pdf",
                'added_date': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            })
    
    # Insert documents
    for doc in documents:
        cursor.execute('''
        INSERT INTO documents (ecli_id, court, year, case_number, file_path, added_date, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            doc['ecli_id'],
            doc['court'],
            doc['year'],
            doc['case_number'],
            doc['file_path'],
            doc['added_date'],
            doc['last_updated']
        ))
        
        # Get the document ID
        doc_id = cursor.lastrowid
        
        # Add document metrics
        page_count = (int(doc['case_number']) % 30) + 1  # 1-30 pages
        file_size = page_count * 50 * 1024  # ~50KB per page
        
        # Sample PDF metadata
        pdf_metadata = {
            'pdf_creator': 'TCPDF 6.4.2',
            'pdf_producer': 'TCPDF 6.4.2 (http://www.tcpdf.org)',
            'pdf_title': doc['ecli_id'],
            'pdf_author': 'Portuguese Judicial System',
            'pdf_creation_date': doc['added_date'],
            'pdf_mod_date': doc['added_date']
        }
        
        cursor.execute('''
        INSERT INTO document_metrics (document_id, page_count, file_size, document_date, language, judge, pdf_metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            doc_id,
            page_count,
            file_size,
            doc['added_date'],
            'Portuguese',
            'N° do Documento',
            json.dumps(pdf_metadata)
        ))
    
    # Commit changes
    conn.commit()
    print(f"Added {len(documents)} sample documents.")

def generate_corpus_stats(conn):
    """Generate corpus statistics."""
    cursor = conn.cursor()
    
    # Get total documents
    cursor.execute('SELECT COUNT(*) FROM documents')
    total_documents = cursor.fetchone()[0]
    
    # Get total pages
    cursor.execute('SELECT SUM(page_count) FROM document_metrics')
    total_pages = cursor.fetchone()[0] or 0
    
    # Get total size
    cursor.execute('SELECT SUM(file_size) FROM document_metrics')
    total_size_bytes = cursor.fetchone()[0] or 0
    
    # Get court distribution
    cursor.execute('SELECT court, COUNT(*) as count FROM documents GROUP BY court')
    courts = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Get year distribution
    cursor.execute('SELECT year, COUNT(*) as count FROM documents GROUP BY year')
    years = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Insert corpus stats
    cursor.execute('''
    INSERT INTO corpus_stats (total_documents, total_pages, total_size_bytes, courts, years, generated_at)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        total_documents,
        total_pages,
        total_size_bytes,
        json.dumps(courts),
        json.dumps(years),
        datetime.now().isoformat()
    ))
    
    # Commit changes
    conn.commit()
    print(f"Generated corpus statistics: {total_documents} documents, {total_pages} pages, {total_size_bytes/1024/1024:.2f} MB")

if __name__ == '__main__':
    init_database()
