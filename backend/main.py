from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

if __name__ == "__main__":
    import uvicorn
    # Use the PORT from environment variables if available, default to 8000
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)