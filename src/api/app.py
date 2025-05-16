from dotenv import load_dotenv
import uvicorn

from api.api_routes import router as backend_router
from api.history_routes import router as history_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()


def create_app() -> FastAPI:

    app = FastAPI(title="Conversation Knowledge Mining Solution Accelerator", version="1.0.0")

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(backend_router, prefix="/api", tags=["backend"])
    app.include_router(history_router, prefix="/history", tags=["history"])

    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {"status": "healthy"}

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
