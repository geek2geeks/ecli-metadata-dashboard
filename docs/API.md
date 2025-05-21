# ECLI Metadata Dashboard API Documentation

This document provides detailed information about the API endpoints available in the ECLI Metadata Dashboard.

## Base URL

All API endpoints are relative to the base URL of your dashboard installation. By default, this is:

```
http://localhost:5000
```

## Authentication

Currently, the API does not require authentication. This is suitable for local development and internal use. For production deployment, consider implementing appropriate authentication mechanisms.

## API Endpoints

### 1. Get Corpus Statistics

Retrieves overall statistics about the document corpus.

**Endpoint:** `/api/stats`

**Method:** GET

**Response:**

```json
{
  "total_documents": 50,
  "total_pages": 1250,
  "total_size_bytes": 62500000,
  "courts": {
    "STJ": 10,
    "TRL": 8,
    "TRP": 7,
    "TRC": 5,
    "TRE": 5,
    "TRG": 5,
    "STA": 4,
    "TCA": 2,
    "TCN": 2,
    "TCS": 2
  },
  "years": {
    "2020": 15,
    "2021": 10,
    "2022": 12,
    "2023": 8,
    "2024": 5
  },
  "generated_at": "2025-05-21T12:00:00.000Z"
}
```

### 2. Get Court Distribution

Retrieves the distribution of documents by court with visualization data.

**Endpoint:** `/api/courts`

**Method:** GET

**Response:**

```json
{
  "data": [
    {"court": "STJ", "count": 10},
    {"court": "TRL", "count": 8},
    {"court": "TRP", "count": 7},
    {"court": "TRC", "count": 5},
    {"court": "TRE", "count": 5},
    {"court": "TRG", "count": 5},
    {"court": "STA", "count": 4},
    {"court": "TCA", "count": 2},
    {"court": "TCN", "count": 2},
    {"court": "TCS", "count": 2}
  ],
  "plot": {
    // Plotly.js JSON data for the chart
  }
}
```

### 3. Get Year Distribution

Retrieves the distribution of documents by year with visualization data.

**Endpoint:** `/api/years`

**Method:** GET

**Response:**

```json
{
  "data": [
    {"year": "2020", "count": 15},
    {"year": "2021", "count": 10},
    {"year": "2022", "count": 12},
    {"year": "2023", "count": 8},
    {"year": "2024", "count": 5}
  ],
  "plot": {
    // Plotly.js JSON data for the chart
  }
}
```

### 4. Get Document Metrics

Retrieves document metrics (page count, file size) with visualization data.

**Endpoint:** `/api/metrics`

**Method:** GET

**Response:**

```json
{
  "data": [
    {"ecli_id": "ECLI_PT_STJ_2020_000001", "court": "STJ", "year": "2020", "page_count": 25, "file_size": 1250000},
    {"ecli_id": "ECLI_PT_TRL_2021_000002", "court": "TRL", "year": "2021", "page_count": 18, "file_size": 900000},
    // More documents...
  ],
  "plot": {
    // Plotly.js JSON data for the scatter plot
  }
}
```

### 5. Get Recent Documents

Retrieves the most recently added documents.

**Endpoint:** `/api/recent`

**Method:** GET

**Response:**

```json
[
  {
    "ecli_id": "ECLI_PT_STJ_2024_000050",
    "court": "STJ",
    "year": "2024",
    "added_date": "2025-05-20T14:30:00.000Z",
    "page_count": 22,
    "file_size": 1100000
  },
  {
    "ecli_id": "ECLI_PT_TRL_2024_000049",
    "court": "TRL",
    "year": "2024",
    "added_date": "2025-05-19T10:15:00.000Z",
    "page_count": 15,
    "file_size": 750000
  },
  // More documents...
]
```

### 6. Get Document Details

Retrieves detailed information about a specific document.

**Endpoint:** `/api/document/<ecli_id>`

**Method:** GET

**Parameters:**
- `ecli_id` (path parameter): The ECLI ID of the document

**Response:**

```json
{
  "id": 50,
  "ecli_id": "ECLI_PT_STJ_2024_000050",
  "court": "STJ",
  "year": "2024",
  "case_number": "000050",
  "file_path": "examples/sample_documents/ECLI_PT_STJ_2024_000050.pdf",
  "added_date": "2025-05-20T14:30:00.000Z",
  "last_updated": "2025-05-20T14:30:00.000Z",
  "page_count": 22,
  "file_size": 1100000,
  "document_date": "2024-12-15T00:00:00.000Z",
  "language": "Portuguese",
  "judge": "N° do Documento",
  "pdf_metadata": {
    "pdf_creator": "TCPDF 6.4.2",
    "pdf_producer": "TCPDF 6.4.2 (http://www.tcpdf.org)",
    "pdf_title": "ECLI_PT_STJ_2024_000050",
    "pdf_author": "Portuguese Judicial System",
    "pdf_creation_date": "2024-12-15T00:00:00.000Z",
    "pdf_mod_date": "2025-05-20T14:30:00.000Z"
  }
}
```

### 7. Search Documents

Searches for documents based on various criteria.

**Endpoint:** `/api/search`

**Method:** GET

**Query Parameters:**
- `ecli` (optional): Partial ECLI ID to search for
- `court` (optional): Court identifier
- `year` (optional): Year of publication
- `min_pages` (optional): Minimum number of pages
- `max_pages` (optional): Maximum number of pages
- `limit` (optional): Maximum number of results to return (default: 50)

**Example Request:**
```
/api/search?court=STJ&year=2024&min_pages=20
```

**Response:**

```json
[
  {
    "ecli_id": "ECLI_PT_STJ_2024_000050",
    "court": "STJ",
    "year": "2024",
    "added_date": "2025-05-20T14:30:00.000Z",
    "page_count": 22,
    "file_size": 1100000
  },
  {
    "ecli_id": "ECLI_PT_STJ_2024_000045",
    "court": "STJ",
    "year": "2024",
    "added_date": "2025-05-15T09:45:00.000Z",
    "page_count": 25,
    "file_size": 1250000
  },
  // More documents...
]
```

### 8. Submit Feedback

Submits user feedback about a document or the dashboard.

**Endpoint:** `/api/feedback`

**Method:** POST

**Request Body:**

```json
{
  "document_id": "ECLI_PT_STJ_2024_000050",
  "type": "metadata",
  "rating": 4,
  "comment": "The metadata is accurate but could include more details about the case."
}
```

**Parameters:**
- `document_id` (required): The ECLI ID of the document
- `type` (required): Type of feedback (e.g., "metadata", "ui", "general")
- `rating` (required): Rating from 1 to 5
- `comment` (optional): Additional comments

**Response:**

```json
{
  "success": true
}
```

## Error Handling

All API endpoints return appropriate HTTP status codes:

- `200 OK`: The request was successful
- `400 Bad Request`: The request was invalid (e.g., missing required parameters)
- `404 Not Found`: The requested resource was not found
- `500 Internal Server Error`: An error occurred on the server

Error responses include a JSON object with an `error` field describing the error:

```json
{
  "error": "Document not found"
}
```

## Rate Limiting

Currently, there are no rate limits implemented. For production deployment, consider implementing rate limiting to prevent abuse.

## Versioning

The current API is considered v1. Future versions will be announced with appropriate deprecation notices for any breaking changes.