# AI Chatbot Application

A simple chatbot application with a FastAPI backend and vanilla JavaScript frontend that integrates with Azure OpenAI.

## Project Structure

```
chatbot/
├── backend/
│   └── main.py              # FastAPI backend server
├── frontend/
│   ├── index.html           # Main HTML file
│   ├── style.css            # Styling
│   └── script.js            # JavaScript functionality
├── .env                     # Environment variables
├── start_backend.sh         # Backend startup script
├── start_frontend.sh        # Frontend startup script
├── pyproject.toml           # Python dependencies
└── README.md               # This file
```

## Features

- **Real-time Chat**: Interactive chat interface with message history
- **Azure OpenAI Integration**: Uses Azure OpenAI service for intelligent responses
- **Responsive Design**: Works on desktop and mobile devices
- **Message History**: Maintains conversation context throughout the session
- **Error Handling**: Graceful error handling with user-friendly messages
- **Loading States**: Visual feedback during API calls

## Setup Instructions

### Prerequisites

- Python 3.8+
- Azure OpenAI resource and API key

### Installation

1. **Install Python dependencies:**
   ```bash
   uv install
   ```

2. **Set up your Azure OpenAI configuration:**
   
   Edit the `.env` file and update the Azure OpenAI settings:

   ```env
   AZURE_OPENAI_API_KEY=your-azure-openai-api-key
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   AZURE_OPENAI_API_VERSION=2024-02-01
   AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
   ```

### Running the Application

You'll need to run both the backend and frontend servers:

#### Option 1: Using the startup scripts

1. **Start the backend server:**
   ```bash
   chmod +x start_backend.sh
   ./start_backend.sh
   ```
   The backend will run on `http://localhost:8000`

2. **Start the frontend server (in a new terminal):**
   ```bash
   chmod +x start_frontend.sh
   ./start_frontend.sh
   ```
   The frontend will run on `http://localhost:3000`

#### Option 2: Manual startup

1. **Start the backend:**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the frontend (in a new terminal):**
   ```bash
   cd frontend
   python3 -m http.server 3000
   ```

### Usage

1. Open your web browser and navigate to `http://localhost:3000`
2. Type your message in the input field and press Enter or click Send
3. The chatbot will respond using Azure OpenAI service
4. Your conversation history is maintained throughout the session

## API Endpoints

- `GET /` - Health check endpoint
- `POST /chat` - Main chat endpoint
  - Request body: `{"message": "your message", "history": [...]}`
  - Response: `{"response": "ai response", "success": true}`

## Troubleshooting

1. **Backend connection error**: Make sure the backend server is running on port 8000
2. **Azure OpenAI API error**: Verify your API key, endpoint, and deployment name are correct
3. **CORS issues**: The backend includes CORS middleware for development. In production, update the `allow_origins` setting

## Development

- Backend uses FastAPI with automatic API documentation at `http://localhost:8000/docs`
- Frontend is pure HTML/CSS/JavaScript for simplicity
- The application maintains chat history in memory (resets on page reload)
