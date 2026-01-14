

from fastapi import FastAPI
from routes.upload import router as upload_router

app = FastAPI(title="Project_2")

app.include_router(upload_router)

@app.get("/")
def health():
    return {"status": "running"}
