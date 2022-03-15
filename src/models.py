"""Mind map leaf models."""
from typing import Optional, List

from pydantic import BaseModel, Field


class MindMapLeaf(BaseModel):
    """A MindMapLeaf DTO."""

    path: Optional[str] = None
    text: Optional[str] = None


class MindMapApp(BaseModel):
    """A MindMapApp DTO."""

    id: str
    data: List[MindMapLeaf] = Field(default_factory=list)


class MindMapAppExceptions(Exception):
    """Base exceptions for MindMapItem."""


class MindMapAppCreateError(MindMapAppExceptions):
    """Raise when trying to create an app in database."""


class MindMapAppAddError(MindMapAppExceptions):
    """Raise when trying to add a leaf in database."""
