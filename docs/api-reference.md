# BioForge API Reference

This document provides a reference for the BioForge API endpoints.

## Base URLs

- **Development**: `http://localhost:8000`
- **Production**: `https://api.bioforge.org`

## Authentication

Most API endpoints require authentication. BioForge uses Firebase Authentication and JWT tokens.

To authenticate:

1. Obtain a Firebase ID token
2. Include the token in the `Authorization` header: `Authorization: Bearer YOUR_TOKEN`

## API Gateway Endpoints

### Authentication

#### Login

\`\`\`
POST /token
\`\`\`

Request body:
\`\`\`json
{
  "username": "user@example.com",
  "password": "password"
}
\`\`\`

Response:
\`\`\`json
{
  "access_token": "YOUR_TOKEN",
  "token_type": "bearer"
}
\`\`\`

### DNA Parts

#### Get DNA Parts

\`\`\`
GET /api/parts
\`\`\`

Query parameters:
- `category` (optional): Filter by category (promoter, gene, terminator, rbs, operator)
- `query` (optional): Search query

Response:
\`\`\`json
[
  {
    "id": "genbank_ABC123",
    "name": "LacI promoter",
    "type": "promoter",
    "sequence": "ATCG...",
    "description": "LacI repressible promoter",
    "source": "GenBank",
    "metadata": {
      "accession": "ABC123",
      "organism": "Escherichia coli",
      "taxonomy": ["Bacteria", "Proteobacteria"],
      "references": ["LacI promoter characterization"]
    }
  }
]
\`\`\`

### DNA Designs

#### Create Design

\`\`\`
POST /api/designs
\`\`\`

Request body:
\`\`\`json
{
  "name": "GFP Expression System",
  "description": "A simple GFP expression system",
  "parts": [
    {
      "id": "genbank_ABC123",
      "name": "LacI promoter",
      "type": "promoter",
      "sequence": "ATCG..."
    },
    {
      "id": "genbank_DEF456",
      "name": "GFP",
      "type": "gene",
      "sequence": "ATCG..."
    }
  ]
}
\`\`\`

Response:
\`\`\`json
{
  "id": "design_123",
  "name": "GFP Expression System",
  "description": "A simple GFP expression system",
  "parts": [...],
  "user_id": "user_123",
  "created_at": "2023-05-01T12:00:00Z",
  "updated_at": "2023-05-01T12:00:00Z"
}
\`\`\`

#### Get Designs

\`\`\`
GET /api/designs
\`\`\`

Response:
\`\`\`json
[
  {
    "id": "design_123",
    "name": "GFP Expression System",
    "description": "A simple GFP expression system",
    "parts": [...],
    "user_id": "user_123",
    "created_at": "2023-05-01T12:00:00Z",
    "updated_at": "2023-05-01T12:00:00Z"
  }
]
\`\`\`

#### Get Design

\`\`\`
GET /api/designs/{design_id}
\`\`\`

Response:
\`\`\`json
{
  "id": "design_123",
  "name": "GFP Expression System",
  "description": "A simple GFP expression system",
  "parts": [...],
  "user_id": "user_123",
  "created_at": "2023-05-01T12:00:00Z",
  "updated_at": "2023-05-01T12:00:00Z"
}
\`\`\`

#### Update Design

\`\`\`
PUT /api/designs/{design_id}
\`\`\`

Request body:
\`\`\`json
{
  "name": "Updated GFP Expression System",
  "description": "An updated GFP expression system",
  "parts": [...]
}
\`\`\`

Response:
\`\`\`json
{
  "id": "design_123",
  "name": "Updated GFP Expression System",
  "description": "An updated GFP expression system",
  "parts": [...],
  "user_id": "user_123",
  "created_at": "2023-05-01T12:00:00Z",
  "updated_at": "2023-05-02T12:00:00Z"
}
\`\`\`

#### Delete Design

\`\`\`
DELETE /api/designs/{design_id}
\`\`\`

Response: 204 No Content

### AI Service

#### Validate Sequence

\`\`\`
POST /api/ai/validate
\`\`\`

Request body:
\`\`\`json
{
  "sequence": "ATCG..."
}
\`\`\`

Response:
\`\`\`json
{
  "valid": true,
  "sequence_length": 100,
  "gc_content": 0.5,
  "orfs": 1,
  "issues": [],
  "warnings": ["Low GC content (0.50)"],
  "suggestions": ["Consider increasing GC content for stability"]
}
\`\`\`

#### Predict Function

\`\`\`
POST /api/ai/predict
\`\`\`

Request body:
\`\`\`json
{
  "sequence": "ATCG..."
}
\`\`\`

Response:
\`\`\`json
{
  "prediction": "Green Fluorescent Protein (GFP)",
  "confidence": 0.95,
  "possible_functions": ["Fluorescent reporter", "Protein tagging"],
  "protein_domains": ["GFP beta-barrel"],
  "notes": ["High confidence match to GFP sequence"]
}
\`\`\`

### Simulation

#### Run Simulation

\`\`\`
POST /api/simulate
\`\`\`

Request body:
\`\`\`json
{
  "id": "design_123",
  "name": "GFP Expression System",
  "description": "A simple GFP expression system",
  "parts": [...]
}
\`\`\`

Response:
\`\`\`json
{
  "growth_rate": 0.75,
  "protein_expression": 0.82,
  "metabolic_burden": 0.35,
  "stability": 0.91,
  "time_series": {
    "time": [0, 1, 2, ...],
    "growth": [0.1, 0.2, 0.3, ...],
    "protein": [0, 0.1, 0.3, ...],
    "metabolite": [0, 0.05, 0.1, ...]
  },
  "notes": []
}
\`\`\`

### Safety

#### Check Safety

\`\`\`
POST /api/safety/check
\`\`\`

Request body:
\`\`\`json
{
  "id": "design_123",
  "name": "GFP Expression System",
  "description": "A simple GFP expression system",
  "parts": [...]
}
\`\`\`

Response:
\`\`\`json
{
  "overall": 0.88,
  "toxicity": 0.05,
  "environmental_risk": 0.12,
  "biocontainment": 0.95,
  "dangerous_sequences": 0,
  "recommendations": [
    "Consider adding a kill switch for additional biocontainment",
    "The current design has minimal environmental risk"
  ]
}
\`\`\`

### Blockchain

#### Mint Token

\`\`\`
POST /api/blockchain/mint
\`\`\`

Request body:
\`\`\`json
{
  "id": "design_123",
  "name": "GFP Expression System",
  "description": "A simple GFP expression system",
  "parts": [...]
}
\`\`\`

Response:
\`\`\`json
{
  "success": true,
  "token_id": "1",
  "transaction_hash": "0x...",
  "block_number": 12345678,
  "token_uri": "https://bioforge.example.com/metadata/abc123",
  "design_hash": "abc123"
}
\`\`\`

#### Get Tokens

\`\`\`
GET /api/blockchain/tokens
\`\`\`

Response:
\`\`\`json
[
  {
    "token_id": "1",
    "token_uri": "https://bioforge.example.com/metadata/abc123",
    "name": "GFP Expression System",
    "description": "A simple GFP expression system",
    "image": "https://bioforge.example.com/nft-image.png"
  }
]
\`\`\`

## Error Responses

BioForge API uses standard HTTP status codes to indicate the success or failure of an API request.

Common error responses:

- `400 Bad Request`: The request was invalid
- `401 Unauthorized`: Authentication is required
- `403 Forbidden`: The authenticated user doesn't have permission
- `404 Not Found`: The requested resource was not found
- `500 Internal Server Error`: An error occurred on the server

Error response body:
\`\`\`json
{
  "detail": "Error message"
}
\`\`\`

## Rate Limiting

The API is rate limited to prevent abuse. The current limits are:

- 100 requests per minute per IP address
- 1000 requests per hour per user

When rate limited, the API will return a `429 Too Many Requests` response.
