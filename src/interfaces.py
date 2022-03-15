"""Mind map leaf interfaces."""
import abc
from typing import List, Optional

from src.models import MindMapApp, MindMapLeaf


class MindMapAppDBInterface(abc.ABC):
    """Abstract class for MindMapApp."""

    @abc.abstractmethod
    def read_mind_map_apps(self) -> List[MindMapApp]:
        """
        Read all mind map apps.

        Returns:
            A list of MindMapApp
        """
        raise NotImplementedError

    @abc.abstractmethod
    def read_mind_map_app(self, id: str) -> Optional[MindMapApp]:
        """
        Read an app by app id.

        Args:
            id: An app id

        Returns:
            A MindMapApp or None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def create_mind_map_app(self, mind_map_app: MindMapApp) -> MindMapApp:
        """
        Create a mind map app.

        Args:
            mind_map_app: A MindMapApp DTO.

        Returns:
            A MindMapApp DTO.
        """
        raise NotImplementedError

    @abc.abstractmethod
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
        raise NotImplementedError
