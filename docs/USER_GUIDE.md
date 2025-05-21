# ECLI Metadata Dashboard User Guide

This guide provides detailed instructions on how to use the ECLI Metadata Dashboard to explore and analyze Portuguese ECLI (European Case Law Identifier) Judicial Decisions metadata.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [Exploring Corpus Statistics](#exploring-corpus-statistics)
4. [Searching for Documents](#searching-for-documents)
5. [Viewing Document Details](#viewing-document-details)
6. [Providing Feedback](#providing-feedback)
7. [Troubleshooting](#troubleshooting)

## Getting Started

After installing and running the dashboard as described in the [README.md](../README.md), open your web browser and navigate to:

```
http://localhost:5000
```

The dashboard will load automatically and display the main interface with corpus statistics and visualizations.

## Dashboard Overview

The dashboard is organized into several sections:

### Navigation Bar

Located at the top of the page, the navigation bar provides:
- Dashboard title and logo
- Help button that opens a comprehensive help modal
- Feedback button for providing general feedback about the dashboard

### Statistics Cards

The top section displays key statistics about the document corpus:
- Total Documents: The number of documents in the corpus
- Total Pages: The combined page count of all documents
- Total Size: The total size of all documents in the corpus

### Visualization Section

The middle section contains interactive charts:
- Court Distribution: Bar chart showing the number of documents by court
- Year Distribution: Line chart showing the number of documents by year
- Document Metrics: Scatter plot showing the relationship between page count and file size

### Recent Documents

The bottom section displays a table of the most recently added documents, including:
- ECLI ID
- Court
- Year
- Added Date
- Page Count
- File Size

### Search Section

A dedicated search section allows you to find specific documents based on various criteria.

## Exploring Corpus Statistics

### Viewing Statistics Cards

The statistics cards at the top of the dashboard provide a quick overview of the corpus:
- **Total Documents**: Hover over this card to see when the last document was added
- **Total Pages**: Hover over this card to see the average number of pages per document
- **Total Size**: Hover over this card to see the average file size per document

### Interacting with Charts

All charts are interactive:

#### Court Distribution Chart
- Click on a bar to filter the recent documents table by that court
- Hover over a bar to see the exact number of documents for that court
- Use the toolbar in the top-right corner of the chart to:
  - Download the chart as an image
  - Zoom in/out
  - Pan across the chart
  - Reset the view

#### Year Distribution Chart
- Click on a point to filter the recent documents table by that year
- Hover over a point to see the exact number of documents for that year
- Use the toolbar for additional options

#### Document Metrics Chart
- Each point represents a document
- Points are colored by court
- Hover over a point to see details about the document
- Click on a point to open the document details modal
- Use the toolbar for additional options

## Searching for Documents

The search section allows you to find specific documents based on various criteria:

1. **ECLI ID**: Enter a partial or complete ECLI ID
2. **Court**: Select a court from the dropdown menu
3. **Year**: Select a year from the dropdown menu
4. **Page Count Range**: Specify minimum and maximum page counts
5. **Click "Search"**: The results will appear in a table below the search form

### Search Results

The search results table displays:
- ECLI ID
- Court
- Year
- Added Date
- Page Count
- File Size

Click on any row to view detailed information about that document.

### Clearing Results

To clear the search results and start a new search, click the "Clear Results" button.

## Viewing Document Details

To view detailed information about a document:
1. Click on a row in the Recent Documents table, or
2. Click on a row in the Search Results table, or
3. Click on a point in the Document Metrics chart

### Document Details Modal

The document details modal displays comprehensive information about the selected document, organized into tabs:

#### Document Info Tab
- ECLI ID
- Court
- Year
- Case Number
- Added Date
- Last Updated

#### Metrics Tab
- Page Count
- File Size
- Document Date
- Language
- Judge

#### PDF Metadata Tab
- PDF Creator
- PDF Producer
- PDF Title
- PDF Author
- PDF Creation Date
- PDF Modification Date

## Providing Feedback

The dashboard allows you to provide feedback in two ways:

### General Feedback

To provide general feedback about the dashboard:
1. Click the "Provide Feedback" link in the footer
2. In the feedback modal:
   - Select the feedback type (UI, Performance, Feature Request, etc.)
   - Provide a rating from 1 to 5 stars
   - Add optional comments
   - Click "Submit Feedback"

### Document-Specific Feedback

To provide feedback about a specific document:
1. Open the document details modal
2. Click the "Provide Feedback" button
3. In the feedback modal:
   - Select the feedback type (Metadata, Content, etc.)
   - Provide a rating from 1 to 5 stars
   - Add optional comments
   - Click "Submit Feedback"

## Troubleshooting

### Charts Not Loading

If the charts are not loading:
1. Check your internet connection
2. Ensure JavaScript is enabled in your browser
3. Try refreshing the page
4. Clear your browser cache and try again

### Search Not Working

If the search functionality is not working:
1. Ensure you are using valid search criteria
2. Try using fewer search parameters
3. Check if the database is properly initialized

### Document Details Not Displaying

If document details are not displaying:
1. Ensure the document exists in the database
2. Try accessing the document through the Recent Documents table
3. Check the browser console for any error messages

### General Issues

For general issues:
1. Restart the dashboard application
2. Ensure all dependencies are installed correctly
3. Check the application logs for error messages
4. Verify that the database file exists and is accessible

If problems persist, please report them through the feedback system or by creating an issue on the GitHub repository.