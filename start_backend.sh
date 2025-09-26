# Backend startup script
echo "Starting FastAPI backend server..."
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000