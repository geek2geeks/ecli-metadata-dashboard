# ECLI Metadata Dashboard

A comprehensive web dashboard for visualizing and exploring Portuguese ECLI (European Case Law Identifier) Judicial Decisions metadata.

## Overview

The ECLI Metadata Dashboard is a component of the Portuguese ECLI Judicial Decisions RAG (Retrieval Augmented Generation) System. It provides an intuitive, interactive web interface for exploring metadata extracted from ECLI documents, visualizing corpus statistics, and searching for specific documents.

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

## License

This project is licensed under the MIT License - see the LICENSE file for details.
