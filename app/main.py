from fastapi import FastAPI

from app.api.routers import main_router
from app.containers import Container
from app.core.config import settings

app = FastAPI(
    title=settings.app_title,
    description=settings.description
)

container = Container()
container.config.from_dict({
    'database_url': settings.database_url,
    'app_title': settings.app_title,
})

container.wire(modules=[
    'app.api.endpoints.charity_project',
    'app.api.endpoints.donation',
    'app.api.validators',
    'app.services.investment',
])

app.container = container
app.include_router(main_router)
