import uvicorn
from fastapi import FastAPI

from flatlandasp.core.log_config import get_logger
from flatlandasp.features.router import router as feature_router

logger = get_logger()

app = FastAPI(title="FlatlandASP", version="0.01")
app.include_router(feature_router)


def main():
    uvicorn.run("flatlandasp.main:app",
                host='0.0.0.0',
                port=8000, reload=True)


if __name__ == "__main__":
    main()
