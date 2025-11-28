import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from .routers import index as indexRoute
from .models import model_loader
from .dependencies.config import conf


app = FastAPI(
    title="Sandwich Maker API",
    description="API for managing a sandwich shop",
    version="1.0.0"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)


@app.get("/")
def root():
    """Root endpoint - redirects to API documentation"""
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)