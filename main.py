import logging
import sys
import os
from fastapi import FastAPI
from endpoints.questions import router as questions_router
from endpoints.answers import router as answers_router

if not os.environ.get("UVICORN_RELOADER"):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler("/app/logs/app.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

logger = logging.getLogger("app")

app = FastAPI(title="Q&A API", version="1.0.0")
app.include_router(questions_router)
app.include_router(answers_router)

if not os.environ.get("UVICORN_RELOADER"):
    logger.info("Starting application...")
    logger.info("Routers included")

if __name__ == "__main__":
    import uvicorn
    import subprocess

    if not os.environ.get("UVICORN_RELOADER"):
        logger.info("Applying database migrations...")
        try:
            result = subprocess.run(
                ["alembic", "-c", "/app/alembic.ini", "upgrade", "head"],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info("Migrations applied successfully")
            logger.debug(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error("Failed to apply migrations")
            logger.error(e.stderr)
            sys.exit(1)

        os.makedirs("/app/logs", exist_ok=True)

    logger.info("Starting Uvicorn server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )