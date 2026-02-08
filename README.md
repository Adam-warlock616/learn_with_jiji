Learn with Jiji - Backend API
FastAPI backend for the VeidaLabs "Learn with Jiji" assignment - an AI learning companion that retrieves relevant learning resources based on user queries.

🚀 Features
FastAPI backend with async support

Supabase integration (PostgreSQL, Storage, Auth)

Row Level Security (RLS) implemented

RESTful API with clean request/response contracts

Input validation using Pydantic models

Error handling with proper HTTP status codes

📁 Project Structure
text
learn-with-jiji-backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration & settings
│   ├── routes/
│   │   └── ask.py           # API endpoints
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   └── utils/
│       ├── supabase_client.py  # Supabase connection
│       └── auth.py          # Authentication middleware
├── supabase/
│   └── schema.sql           # Database schema with RLS
├── requirements.txt         # Python dependencies
├── run.py                  # Application entry point
├── test_api.py             # API test suite
└── .env.example            # Environment template
🛠️ Setup
1. Clone and Install
bash
git clone <repository-url>
cd learn-with-jiji-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
2. Configure Supabase
Create a project at supabase.com

Run the SQL from supabase/schema.sql in Supabase SQL Editor

Create a Storage bucket named files (public)

Upload sample PPT/video files

Get your credentials from Settings → API

3. Configure Environment
bash
cp .env.example .env
# Edit .env with your Supabase URL and anon key
4. Run the API
bash
python run.py
Server starts at http://localhost:8000

📡 API Endpoints
POST /api/ask-jiji
Main endpoint for asking questions about AI topics.

Request:

json
{
  "query_text": "Explain RAG"
}
Response:

json
{
  "answer": "Here's what I found about 'Explain RAG'...",
  "resources": [
    {
      "id": 1,
      "title": "Introduction to RAG",
      "description": "Slides on Retrieval-Augmented Generation",
      "type": "ppt",
      "file_url": "https://.../rag-intro.pptx",
      "tags": ["AI", "RAG", "NLP"]
    }
  ]
}
GET /api/health
Health check endpoint to verify API and Supabase connection.

GET /docs
Interactive API documentation (Swagger UI).

🗄️ Database Schema
Three main tables with RLS policies:

profiles: User profiles (linked to Supabase Auth)

queries: Log of user queries

resources: Learning materials (PPT/video files)

Row Level Security ensures:

Users can only access their own profiles and queries

Learning resources are publicly readable

Authenticated users can upload files

🧪 Testing
Run the test suite:

bash
python test_api.py
Tests include:

Health check

Query processing with different topics

Input validation (empty queries)

Supabase connection verification

🔧 One Improvement with More Time
Given more time, I would implement full-text search using PostgreSQL's tsvector for better resource matching, and add caching with Redis to reduce database load for frequent queries.

📝 Assignment Requirements Checklist
FastAPI backend with /api/ask-jiji endpoint

Supabase integration (DB, Storage, Auth)

Row Level Security policies

Clean request/response contracts

Basic input validation

Error handling

README with setup instructions

Working demo

📄 License
MIT License - Created for VeidaLabs Software Developer Hiring Assignment

