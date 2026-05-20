import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings

settings = get_settings()

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()

app = FastAPI(
    title="CV Generator API",
    description="AI-powered ATS-optimized CV generator using Word templates",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    logger.info("cv_generator_startup", env=settings.app_env, ai_provider=settings.ai_provider)


@app.on_event("shutdown")
async def shutdown():
    logger.info("cv_generator_shutdown")


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}


from app.routers import auth, profiles, experiences, education, skills, certifications, projects, languages, job_offers, matching, generate

app.include_router(auth.router)
app.include_router(profiles.router)
app.include_router(experiences.router)
app.include_router(education.router)
app.include_router(skills.router)
app.include_router(certifications.router)
app.include_router(projects.router)
app.include_router(languages.router)
app.include_router(job_offers.router)
app.include_router(matching.router)
app.include_router(generate.router)
