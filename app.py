from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import os
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return PlainTextResponse("Hello World from Cloud Run!")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
