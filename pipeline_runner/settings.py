import os
DEBUG = os.getenv("PIPELINE_DEBUG", "").lower() in ("1", "true")
LOG_LEVEL = os.getenv("PIPELINE_LOG_LEVEL", "INFO")
CORS_ORIGINS = os.getenv("PIPELINE_CORS_ORIGINS", "*")
