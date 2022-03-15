"""Main Mind map leaf API."""
from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.applications import ReadMindMapApps, ReadMindMapApp, \
    CreateMindMapApp, ReadMindMapAppsPrettyFormat, AddMindMapLeaf
from src.models import MindMapApp, MindMapLeaf
from src.providers import MindMapDBProvider

# Define provider for dependency injection
DB_PROVIDER = MindMapDBProvider()
# Define jinja template directory
templates = Jinja2Templates(directory="templates")

tags_metadata = [
    {
        "name": "Mind map apps",
        "description": "A Mind map API for testing",
        "externalDocs": {
            "description": "Mind map items external docs",
            "url": "https://127.0.0.1",
        },
    },
]

description = """
This API aims to do something but what ???.
"""
app = FastAPI(
    title="Mind map API",
    description=description,
    version="0.0.1",
    terms_of_service="https://127.0.0.1/terms/",
    contact={
        "name": "Arnaud SENE",
        "url": "https://127.0.0.1/contact/",
        "email": "arnaud.sene@pm.me",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata,
)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Read all apps in html."""
    mind_map_items = ReadMindMapAppsPrettyFormat(db_provider=DB_PROVIDER)()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "apps": mind_map_items,
        }
    )


@app.get("/apps", response_model=List[MindMapApp], tags=["items"])
async def read_apps() -> List[MindMapApp]:
    """
    Read apps.

    Returns:
        List of MindMapApp DTO.
    """
    mind_map_items = ReadMindMapApps(db_provider=DB_PROVIDER)()
    return mind_map_items


@app.get("/apps/{app_id}", response_model=MindMapApp, tags=["items"])
async def read_app(app_id: str) -> MindMapApp:
    """
    Read an app by id.

    Args:
        app_id: An app id.

    Returns:
        A MindMapApp DTO.
    """
    return ReadMindMapApp(db_provider=DB_PROVIDER)(id=app_id)


@app.post("/apps/", response_model=MindMapApp, tags=["items"])
async def create_app(mind_map_app: MindMapApp) -> MindMapApp:
    """
    Create an app.

    Args:
        mind_map_app: A MindMapApp DTO.

    Returns:
        A MindMapApp DTO.

    Raises:
        HTTPException
    """
    try:
        return CreateMindMapApp(db_provider=DB_PROVIDER)(
            mind_map_app=mind_map_app)

    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@app.put("/apps/{app_id}", response_model=MindMapApp, tags=["items"])
async def add_leaf(app_id: str, mind_map_leaf: MindMapLeaf) -> MindMapApp:
    """
    Add a leaf in app.

    Args:
        app_id: An app id
        mind_map_leaf: A MindMapLeaf DTO.

    Returns:
        A MindMapApp DTO.

    Raises:
        HTTPException
    """
    try:
        # add leaf to app
        return AddMindMapLeaf(db_provider=DB_PROVIDER)(
            id=app_id,
            mind_map_leaf=mind_map_leaf)

    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc))
