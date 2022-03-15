"""Mind map leaf applications."""

from typing import List, Optional, Dict

from src.interfaces import MindMapAppDBInterface
from src.models import MindMapApp, MindMapLeaf


class ReadMindMapApps:
    """Read all mind map apps."""

    def __init__(
            self,
            db_provider: MindMapAppDBInterface
    ):
        """Init."""
        self.db_provider = db_provider

    def __call__(self) -> List[MindMapApp]:
        """
        Read all mind map apps.

        Returns:
            A list of MindMapApp DTO.
        """
        return self.db_provider.read_mind_map_apps()


class ReadMindMapApp:
    """Read an app by app id."""

    def __init__(
            self,
            db_provider: MindMapAppDBInterface
    ):
        """Init."""
        self.db_provider = db_provider

    def __call__(self, id: str) -> Optional[MindMapApp]:
        """
        Read an app by app id.

        Args:
            id: An app id

        Returns:
            A MindMapApp or None
        """
        return self.db_provider.read_mind_map_app(id=id)


class ReadMindMapAppsPrettyFormat:
    """Read all mind map apps for a pretty format output."""

    def __init__(
            self,
            db_provider: MindMapAppDBInterface
    ):
        """Init."""
        self.db_provider = db_provider

    def __call__(self) -> List[Dict[str, str]]:
        """
        Read all mind map apps for a pretty format output.

        Split the path string in order to get a tree view in html view.

        Returns:
            A list of apps as a dict
        """
        result = self.db_provider.read_mind_map_apps()
        apps_tree = []

        for app in result:
            for d in app.data:
                d.path = d.path.lstrip("/").split('/')
            app_tree = app.dict()
            apps_tree.append(app_tree)

        return apps_tree


class CreateMindMapApp:
    """Create a mind map app."""

    def __init__(
            self,
            db_provider: MindMapAppDBInterface
    ):
        """Init."""
        self.db_provider = db_provider

    def __call__(self, mind_map_app: MindMapApp) -> MindMapApp:
        """
        Create a mind map app.

        Args:
            mind_map_app: A MindMapApp DTO.

        Returns:
            A MindMapApp DTO.
        """
        return self.db_provider.create_mind_map_app(
            mind_map_app=mind_map_app)


class AddMindMapLeaf:
    """Add a leaf to a mind map app."""

    def __init__(
            self,
            db_provider: MindMapAppDBInterface
    ):
        """Init."""
        self.db_provider = db_provider

    def __call__(
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
        return self.db_provider.add_mind_map_leaf(
            id=id,
            mind_map_leaf=mind_map_leaf)
