"""Mind map leaf provider."""
from typing import List, Optional, Dict, Any

from src.interfaces import MindMapAppDBInterface
from src.models import MindMapAppCreateError, \
    MindMapApp, MindMapLeaf, MindMapAppAddError


db = [
    {
        "id": "app-0",
        "data": [
            {
                "path": "i/like/potatoes",
                "text": "Because reasons"
            },
            {
                "path": "/this/is/a/path/1",
                "text": "This is a sample topic 1"
            }
        ]
    },
    {
        "id": "app-1",
        "data": [
            {
                "path": "i/like/potatoes",
                "text": "Because reasons"
            },
            {
                "path": "/this/is/a/path/1",
                "text": "This is a sample topic 1"
            }
        ]

    },
]


class MindMapDBProvider(MindMapAppDBInterface):
    """Mind map providers for data."""

    def __init__(self):
        """Init DB."""
        self.db: List[Dict[str, Any]] = db

    def read_mind_map_apps(self) -> List[MindMapApp]:
        """
        Read all mind map apps.

        Returns:
            A list of MindMapApp
        """
        return [MindMapApp(**item) for item in self.db]

    def read_mind_map_app(self, id: str) -> Optional[MindMapApp]:
        """
        Read an app by app id.

        Args:
            id: An app id

        Returns:
            A MindMapApp or None
        """
        for item in self.db:
            if item['id'] == id:
                return MindMapApp(**item)
        return None

    def create_mind_map_app(self, mind_map_app: MindMapApp) -> MindMapApp:
        """
        Create a mind map app.

        Args:
            mind_map_app: A MindMapApp DTO.

        Returns:
            A MindMapApp DTO.
        """
        for item in self.db:
            if mind_map_app.id == item['id']:
                raise MindMapAppCreateError(
                    f"App with id: {mind_map_app.id} "
                    f"already exists in database.")

        self.db.append(mind_map_app.dict())
        return mind_map_app

    def add_mind_map_leaf(
            self,
            id: str,
            mind_map_leaf: MindMapLeaf
    ) -> MindMapApp:
        """
        Add a leaf to a mind map app.

        Args:
            id: An app id
            mind_map_leaf: A MindMapLeaf DTO.

        Returns:
            A MindMapApp DTO.
        """
        for item in self.db:
            if item['id'] == id:
                item['data'].append(mind_map_leaf.dict())
                return self.read_mind_map_app(id=id)

        raise MindMapAppAddError(
            f"App with id: {id} does not exist in database.")
