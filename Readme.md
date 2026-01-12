# GenAI Workflow Builder

A **Low-Code / No-Code GenAI Workflow Engine** that lets users visually design AI-powered workflows using a drag-and-drop UI. Built with modern web technologies and fully containerized for a frictionless developer experience.

This project integrates **LLMs + RAG pipelines** into a configurable workflow system — no heavy setup, no manual infrastructure work.

---

## Table of Contents

- [Features](#-features)
- [What This Project Does](#-what-this-project-does)
- [Tech Stack](#️-tech-stack)
- [Quick Start](#-quick-start-easy-mode)
- [Project Structure](#-project-structure)
- [Environment Variables](#-environment-variables)
- [API Documentation](#-api-documentation)
- [Workflow Demo](#-recommended-demo-flow)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## Features

- **Visual Workflow Designer** - Drag-and-drop interface for building AI workflows
- **Modular Components** - Pre-built nodes for User Query, Knowledge Base, LLM, and Output
- **Real-time Execution** - Run workflows and see results instantly
- **Fully Dockerized** - One-command deployment with Docker Compose
- **Async Processing** - Fast and efficient workflow execution
- **RESTful API** - Clean API design with automatic documentation
- **Persistent Storage** - PostgreSQL database for workflow persistence

---

## What This Project Does

GenAI Workflow Builder allows you to:

1. **Design AI Workflows Visually** - Connect AI components without writing code
2. **Orchestrate LLM Pipelines** - Chain together query processing, knowledge retrieval, and generation
5. **Iterate Quickly** - Hot-reload enabled for both frontend and backend development
---

## Tech Stack

### Frontend
- **React 18** - Modern UI framework
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first styling
- **React Flow** - Interactive node-based editor
- **Axios** - HTTP client for API calls

### Backend
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy 2.0** - Async ORM for database operations
- **Pydantic** - Data validation and settings management
- **LangChain** - LLM orchestration framework
- **Python 3.11** - Latest stable Python runtime

### Database
- **PostgreSQL 15** - Production-ready relational database
- **Alembic** - Database migration tool

### Infrastructure
- **Docker** - Container runtime
- **Docker Compose** - Multi-container orchestration
- **Nginx** - (Optional) Reverse proxy for production

---

## Quick Start (Easy Mode)

> **Prerequisites:** Docker Desktop installed ([Download here](https://www.docker.com/products/docker-desktop))  
> No need to install Python, Node.js, or PostgreSQL separately

### Clone the Repository

```bash
git clone <YOUR_REPO_URL_HERE>
cd genai-workflow-builder
```

### Configure Environment Variables

Navigate to the backend directory and set up your environment file:

```bash
cd backend
cp .env.example .env
```

Open `.env` in your text editor and add your API keys:

```env
API_PORT=8000
PROJECT_BASE_DIR=<project root directory absolute path>
CORS_ORIGINS=http://localhost:5173
# AI Provider Keys
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

### Launch the Application

Return to the project root and start all services:

```bash
cd ..
docker-compose up --build
```

Docker will:
- Build frontend and backend containers
- Start PostgreSQL database
- Run database migrations
- Launch all services

**Wait for:** `Application startup complete` in the logs

### Access the Application

Once running, open your browser:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend UI** | http://localhost:5173 | Workflow builder interface |
| **Backend API** | http://localhost:8000 | FastAPI REST endpoints |
| **API Docs (Swagger)** | http://localhost:8000/docs | Interactive API documentation |
| **API Docs (ReDoc)** | http://localhost:8000/redoc | Alternative API documentation |

---

## Project Structure

```
genai-workflow-builder/
├── frontend/                  # React + Vite application
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API service layer
│   │   └── App.jsx           # Main app component
│   ├── Dockerfile
│   └── package.json
│
├── backend/                   # FastAPI application
│   ├── app/
│   │   ├── api/              # API routes
│   │   ├── core/             # Core configurations
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   └── main.py           # FastAPI entry point
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── docker-compose.yml         # Multi-container setup
├── .gitignore
└── README.md
```

---

## Environment Variables

### Backend Configuration (`backend/.env`)

```env

# ============================================
# AI Provider API Keys (REQUIRED)
# ============================================
OPENAI_API_KEY=sk-your-openai-key-here

# ============================================
# Security (Change in Production!)
# ============================================
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Getting API Keys

**OpenAI:**
1. Visit https://platform.openai.com/api-keys
2. Create a new secret key
3. Copy and paste into `.env`
---

## API Documentation

Once the backend is running, explore the interactive API documentation:

### Swagger UI
Visit http://localhost:8000/docs to:
- View all available endpoints
- Test API calls directly from your browser
- See request/response schemas
- Download OpenAPI specification

### Key API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/workflows` | List all workflows |
| `POST` | `/api/v1/workflows` | Create new workflow |
| `GET` | `/api/v1/workflows/{id}` | Get workflow details |
| `PUT` | `/api/v1/workflows/{id}` | Update workflow |
| `DELETE` | `/api/v1/workflows/{id}` | Delete workflow |
| `POST` | `/api/v1/workflows/{id}/execute` | Run workflow |
| `GET` | `/api/v1/health` | Health check |

---

## Recommended Demo Flow

Try this workflow to see the system in action:

### Step 1: Create a New Workflow
1. Open http://localhost:5173
2. Click **"New Workflow"**
3. Name it "AI Research Assistant"

### Step 2: Add Nodes
Drag and drop these components onto the canvas:

1. **User Query Node**
   - Accepts user input
   - Example: "Explain quantum computing"

2. **Knowledge Base Node**
   - Retrieves relevant context
   - Configure with your document source

3. **LLM Node**
   - Processes query with context
   - Select model: GPT-4 or Llama

4. **Output Node**
   - Formats and displays results

### Step 3: Connect Nodes
- Draw edges between nodes to define the flow
- User Query → Knowledge Base → LLM → Output

### Step 4: Execute Workflow
1. Click **"Run Workflow"**
2. Enter your test query
3. Observe the structured AI-generated response
4. Review execution logs in the console

---

## Troubleshooting

### Port Already in Use
If ports 5173, 8000, or 5432 are occupied:

```bash
# Stop conflicting services or modify docker-compose.yml
docker-compose down
docker-compose up --build
```

### Database Connection Issues
Reset the database:
```bash
docker-compose down -v
docker-compose up --build
```

### Frontend Can't Reach Backend
Verify CORS settings in `backend/app/core/config.py`:
```python
CORS_ORIGINS = ["http://localhost:5173"]
```

### API Keys Not Working
- Ensure `.env` file exists in `backend/` directory
- Check for extra spaces or quotes in key values
- Restart containers after updating `.env`:
  ```bash
  docker-compose restart backend
  ```

### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```


## Acknowledgments

- **React Flow** - For the amazing node-based UI library
- **FastAPI** - For the blazing-fast Python framework
- **LangChain** - For LLM orchestration patterns
- **OpenAI & Hugging Face** - For AI model APIs

---
