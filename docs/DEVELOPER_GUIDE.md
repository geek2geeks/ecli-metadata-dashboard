# ECLI Metadata Dashboard Developer Guide

This guide provides information for developers who want to understand, modify, or extend the ECLI Metadata Dashboard.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Directory Structure](#directory-structure)
3. [Backend Implementation](#backend-implementation)
4. [Frontend Implementation](#frontend-implementation)
5. [Database Schema](#database-schema)
6. [Adding New Features](#adding-new-features)
7. [Testing](#testing)
8. [Deployment](#deployment)

## Architecture Overview

The ECLI Metadata Dashboard follows a simple client-server architecture:

- **Backend**: A Flask application that provides API endpoints for retrieving and manipulating data
- **Frontend**: HTML, CSS, and JavaScript that consume the API endpoints and render the UI
- **Database**: SQLite database that stores document metadata and statistics

### Key Components

- **API Layer**: RESTful API endpoints for retrieving data
- **Data Access Layer**: Functions for interacting with the database
- **Visualization Layer**: Plotly.js charts for visualizing data
- **UI Layer**: Bootstrap-based responsive interface

## Directory Structure

```
ecli-metadata-dashboard/
├── dashboard/                  # Main application directory
│   ├── __init__.py             # Package initialization
│   ├── dashboard.py            # Main Flask application with API endpoints
│   ├── run_dashboard.py        # Script to run the dashboard
│   └── templates/              # HTML templates
│       └── index.html          # Main dashboard template
├── scripts/                    # Utility scripts
│   └── init_database.py        # Database initialization script
├── docs/                       # Documentation
│   ├── API.md                  # API documentation
│   ├── USER_GUIDE.md           # User guide
│   └── DEVELOPER_GUIDE.md      # This file
├── .gitignore                  # Git ignore file
├── LICENSE                     # License file
├── README.md                   # Project overview
└── requirements.txt            # Python dependencies
```

## Backend Implementation

The backend is implemented in Python using the Flask framework. The main file is `dashboard/dashboard.py`.

### Key Components

#### Flask Application Initialization

```python
app = Flask(__name__)
```

#### Database Connection

```python
def get_db_connection(db_path=None):
    """Get a connection to the database."""
    if db_path is None:
        db_path = DEFAULT_DB_PATH
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
```

#### Data Retrieval Functions

These functions retrieve data from the database:

- `get_corpus_stats()`: Get corpus statistics
- `get_documents_by_court()`: Get document distribution by court
- `get_documents_by_year()`: Get document distribution by year
- `get_document_metrics()`: Get document metrics
- `get_recent_documents(limit)`: Get recent documents
- `search_documents(query)`: Search for documents

#### API Endpoints

The API endpoints are implemented as Flask routes:

- `@app.route('/')`: Render the dashboard home page
- `@app.route('/api/stats')`: Get corpus statistics
- `@app.route('/api/courts')`: Get document distribution by court
- `@app.route('/api/years')`: Get document distribution by year
- `@app.route('/api/metrics')`: Get document metrics
- `@app.route('/api/recent')`: Get recent documents
- `@app.route('/api/document/<ecli_id>')`: Get document details
- `@app.route('/api/search')`: Search for documents
- `@app.route('/api/feedback', methods=['POST'])`: Submit feedback

## Frontend Implementation

The frontend is implemented in HTML, CSS, and JavaScript, with the main template in `dashboard/templates/index.html`.

### Key Components

#### HTML Structure

The HTML structure follows a standard Bootstrap layout:

- Navigation bar
- Statistics cards
- Chart containers
- Search form
- Recent documents table
- Modals for document details and feedback

#### JavaScript Functions

The JavaScript functions handle data retrieval and UI updates:

- `loadStats()`: Load corpus statistics
- `loadCharts()`: Load all charts
- `loadCourtChart()`: Load court distribution chart
- `loadYearChart()`: Load year distribution chart
- `loadMetricsChart()`: Load document metrics chart
- `showDocumentDetails(ecliId)`: Show document details modal
- `loadRecentDocuments()`: Load recent documents table

#### CSS Styling

The CSS styling is based on Bootstrap with custom styles for:

- Statistics cards
- Chart containers
- Tables
- Modals
- Loading indicators

## Database Schema

The database schema consists of four tables:

### documents

Stores document metadata:

```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ecli_id TEXT UNIQUE NOT NULL,
    court TEXT,
    year TEXT,
    case_number TEXT,
    file_path TEXT,
    added_date TEXT,
    last_updated TEXT
)
```

### document_metrics

Stores document metrics:

```sql
CREATE TABLE document_metrics (
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
```

### corpus_stats

Stores corpus statistics:

```sql
CREATE TABLE corpus_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_documents INTEGER,
    total_pages INTEGER,
    total_size_bytes INTEGER,
    courts TEXT,
    years TEXT,
    generated_at TEXT
)
```

### user_feedback

Stores user feedback:

```sql
CREATE TABLE user_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id TEXT,
    type TEXT,
    rating INTEGER,
    comment TEXT,
    user_agent TEXT,
    submitted_at TEXT
)
```

## Adding New Features

### Adding a New API Endpoint

To add a new API endpoint:

1. Add a new function to retrieve the data from the database
2. Add a new route in `dashboard.py`
3. Update the frontend to consume the new endpoint

Example:

```python
def get_document_languages():
    """Get document languages."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT language, COUNT(*) as count
    FROM document_metrics
    GROUP BY language
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

@app.route('/api/languages')
def get_languages():
    """API endpoint for document languages."""
    languages = get_document_languages()
    return jsonify(languages)
```

### Adding a New Visualization

To add a new visualization:

1. Add a new container in `index.html`
2. Add a new JavaScript function to load the data and create the chart
3. Call the function when the page loads

Example:

```javascript
function loadLanguageChart() {
    fetch('/api/languages')
        .then(response => response.json())
        .then(data => {
            const chartData = [{
                values: data.map(item => item.count),
                labels: data.map(item => item.language),
                type: 'pie'
            }];
            
            const layout = {
                title: 'Documents by Language'
            };
            
            Plotly.newPlot('language-chart', chartData, layout);
        })
        .catch(error => console.error('Error loading language chart:', error));
}
```

## Testing

The dashboard does not currently have automated tests. When implementing tests, consider:

### Backend Tests

Use `pytest` to test the Flask application:

```python
def test_get_stats():
    """Test the stats endpoint."""
    response = app.test_client().get('/api/stats')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'total_documents' in data
```

### Frontend Tests

Use a framework like Jest to test the JavaScript functions:

```javascript
test('loadStats updates the UI correctly', () => {
    // Mock the fetch API
    global.fetch = jest.fn().mockImplementation(() => {
        return Promise.resolve({
            json: () => Promise.resolve({
                total_documents: 50,
                total_pages: 1250,
                total_size_bytes: 62500000
            })
        });
    });
    
    // Call the function
    loadStats();
    
    // Check that the UI was updated correctly
    expect(document.getElementById('total-documents').textContent).toBe('50');
});
```

## Deployment

The dashboard can be deployed in various ways:

### Local Deployment

For local deployment, simply run:

```bash
python dashboard/dashboard.py
```

### Production Deployment

For production deployment, consider:

1. Using a production WSGI server like Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 dashboard:app
```

2. Using a reverse proxy like Nginx:

```nginx
server {
    listen 80;
    server_name ecli-dashboard.example.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. Using Docker:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "dashboard:app"]
```

### Database Considerations

For production, consider:

1. Using a more robust database like PostgreSQL
2. Implementing proper backup and recovery procedures
3. Optimizing database queries for performance

## Conclusion

This developer guide provides an overview of the ECLI Metadata Dashboard implementation. For more detailed information, refer to the code comments and other documentation files.