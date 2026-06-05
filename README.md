# WealthFact: Mutual Fund RAG Assistant

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg?logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-0.3-orange.svg)
![ChromaDB](https://img.shields.io/badge/Chroma-Vector_DB-purple.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**WealthFact** is an intelligent, RAG-powered (Retrieval-Augmented Generation) API and Web Interface designed to answer factual questions about **HDFC Mutual Funds**. 

The system strictly adheres to providing *facts only*, pulling real-time data from official fund pages and automatically refusing to provide financial advice or process personally identifiable information (PII).

---

## 🎯 Key Features

- **Automated Daily Ingestion**: An integrated **GitHub Actions Cron Job** triggers the `/api/ingest` endpoint every day at 10:00 AM IST to scrape 19 HDFC Mutual Fund pages and keep the vector database up-to-date, saving memory on the backend host.
- **Strict Guardrails**: Advanced query classification blocks any questions seeking financial advice (e.g., "Should I buy this fund?") and detects/blocks PII.
- **Verifiable Citations**: Every factual answer includes the exact source URL and the timestamp of when the data was last ingested.
- **Decoupled Architecture**: A modern **Next.js 15 (React)** interface that seamlessly communicates with the robust FastAPI Python backend.

---

## 🏗️ Architecture Overview

The system uses a Retrieval-Augmented Generation (RAG) approach:
1. **Scraping & Chunking**: `requests` and `BeautifulSoup4` scrape fund data, which is then semantically chunked into sections (Metrics, Objective, Exit Load, Fund Managers).
2. **Embedding & Vector Storage**: Chunks are embedded using `sentence-transformers` and stored in a local `ChromaDB` vector database.
3. **Retrieval**: User queries are embedded and matched against the vector store to fetch the Top-K relevant facts.
4. **Generation**: The retrieved context is passed to the **Groq LLM** (using `llama-3.3-70b-versatile`) with a strict system prompt to synthesize a factual response without hallucinating.

---

## ⚙️ Environment Setup & Installation

### Prerequisites
- Python 3.9 or higher
- [Groq API Key](https://console.groq.com/) (Required for the LLM)

### 1. Local Setup
Clone the repository and install the dependencies in a virtual environment:

```bash
git clone https://github.com/shreyashf80/MutualFund-RAG-Chatbot.git
cd MutualFund-RAG-Chatbot

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory by copying the example template:
```bash
cp .env.example .env
```
Add your Groq API key to the `.env` file:
```ini
GROQ_API_KEY="gsk_your_groq_api_key_here"
```

### 3. Run the Backend Locally
Start the FastAPI server:
```bash
uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
```
*(Note: On first boot, the system will check for vector data. If none exists, you can manually trigger the ingestion via the API below).*

### 4. Run the Frontend Locally
Open a new terminal, navigate to the `frontend/` directory, and start the Next.js development server:
```bash
cd frontend
npm install
npm run dev
```
The frontend UI will be available at `http://localhost:3000/`.

---

## 🚀 Deployment Guide

This repository is pre-configured to be deployed across two platforms:

### Backend (Railway)
The backend is Dockerized for reliable deployment on Railway (which requires specific `sqlite3` libraries for ChromaDB).
1. Create a new Railway project and connect your GitHub repo.
2. Railway will automatically detect the `Dockerfile` and build the image.
3. **Important**: Add your `GROQ_API_KEY` to the Railway Environment Variables.
4. Set the internal `PORT` variable if necessary (defaults to 8000).
5. Railway provides a persistent volume for ChromaDB storage so you don't lose data on restarts.

### Frontend (Vercel)
The UI is a Next.js application designed to be hosted seamlessly on Vercel.
1. Create a new Vercel project and connect the repo.
2. Ensure the **Framework Preset** is set to "Next.js".
3. Set the "Root Directory" to `frontend`.
4. **Important**: Add a new Environment Variable in the Vercel dashboard:
   - Name: `NEXT_PUBLIC_API_BASE_URL`
   - Value: `https://your-app.up.railway.app` (Your deployed Railway backend URL).

---

## 📚 API Documentation

Once the server is running, the interactive Swagger UI is available at `/docs`.

### Core Endpoints

#### `POST /api/query`
Main endpoint for the chatbot.
**Request**:
```json
{ "query": "What is the expense ratio of HDFC Top 100 fund?" }
```
**Response**:
```json
{
  "status": "success",
  "type": "factual",
  "answer": "The expense ratio for HDFC Top 100 Fund is 1.63%.",
  "citation": "https://groww.in/mutual-funds/hdfc-top-200-fund",
  "last_updated": "2023-10-25"
}
```

#### `POST /api/ingest`
Manually triggers the scraping, chunking, and embedding pipeline. Useful for first-time setup or forced refreshes.
*Warning: This is a synchronous process and may take 1-2 minutes.*

#### `GET /api/schemes`
Returns a list of all currently indexed mutual fund schemes.

---

## ⚠️ Disclaimer

**Facts-only. No investment advice.**
This tool is for educational and informational purposes only. The LLM is strictly prompted to avoid offering financial advice, predictions, or recommendations. Always consult a registered financial advisor before making investment decisions.

---
*Built for the NextLeap Groww Milestone.*