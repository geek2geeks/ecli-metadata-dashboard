# ECLI Metadata Dashboard

A comprehensive web dashboard for visualizing and exploring Portuguese ECLI (European Case Law Identifier) Judicial Decisions metadata.

![Dashboard Preview](https://via.placeholder.com/800x450?text=ECLI+Metadata+Dashboard)

## Overview

The ECLI Metadata Dashboard is a component of the Portuguese ECLI Judicial Decisions RAG (Retrieval Augmented Generation) System. It provides an intuitive, interactive web interface for exploring metadata extracted from ECLI documents, visualizing corpus statistics, and searching for specific documents.

### What is ECLI?

The European Case Law Identifier (ECLI) is a uniform identifier format for case law from European and national courts. This dashboard specifically focuses on Portuguese judicial decisions that have been assigned ECLI identifiers.

## Features

- **Corpus Statistics**: View total documents, pages, and size with intuitive stat cards
- **Court Distribution**: Interactive bar chart visualizing documents by court
- **Year Distribution**: Interactive line chart visualizing documents by year
- **Document Metrics**: Interactive scatter plot exploring page count and file size distribution
- **Document Search**: Advanced search for documents by court, year, and page count with real-time results
- **Recent Documents**: View and interact with the most recently added documents
- **Document Preview**: View detailed document metadata with organized sections for document info, PDF metadata, and system info
- **User Feedback**: Provide feedback on document metadata and UI experience
- **Responsive Design**: Fully responsive interface that works on desktop and mobile devices
- **Help System**: Comprehensive help documentation accessible from the navigation bar

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Visualization**: Plotly.js
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome

## Repository Structure

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
├── .gitignore                  # Git ignore file
├── LICENSE                     # License file
├── README.md                   # This file
└── requirements.txt            # Python dependencies
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/geek2geeks/ecli-metadata-dashboard.git
   cd ecli-metadata-dashboard
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python scripts/init_database.py
   ```

4. Run the dashboard:
   ```bash
   python dashboard/dashboard.py
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## API Endpoints

The dashboard provides the following API endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/stats` | GET | Get corpus statistics |
| `/api/courts` | GET | Get document distribution by court |
| `/api/years` | GET | Get document distribution by year |
| `/api/metrics` | GET | Get document metrics (page count, file size) |
| `/api/recent` | GET | Get recent documents |
| `/api/document/<ecli_id>` | GET | Get document details by ECLI ID |
| `/api/search` | GET | Search for documents |
| `/api/feedback` | POST | Submit user feedback |

## Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Setting Up Development Environment

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the dashboard in debug mode:
   ```bash
   python dashboard/dashboard.py
   ```

### Database Schema

The dashboard uses a SQLite database with the following tables:

- `documents`: Stores document metadata
- `document_metrics`: Stores document metrics (page count, file size, etc.)
- `corpus_stats`: Stores corpus statistics
- `user_feedback`: Stores user feedback

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Plotly.js](https://plotly.com/javascript/)
- [Font Awesome](https://fontawesome.com/)
- [jQuery](https://jquery.com/)