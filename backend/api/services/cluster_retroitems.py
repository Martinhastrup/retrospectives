from api.models import Retrospective, RetrospectiveItem, User
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
import numpy.typing as npt
from api.schemas import RetroItem, RetroItemList, DEFAULT_SENTENCE_TRANSFORMER


class ClusteringService:
    """Service for clustering retrospective items."""
    def __init__(self, transformer: str = DEFAULT_SENTENCE_TRANSFORMER):
        self.transformer = SentenceTransformer(transformer)
    
    def get_retrospective_items(self, retrospective_id: int, category: str) -> list[RetroItem]:
        """Get all items from a retrospective."""
        try:
            retrospective_items = RetrospectiveItem.objects.filter(
                retrospective_id=retrospective_id,
                category=category
            )

            return [
                RetroItem(
                    category=item.category,
                    content=item.content,
                    cluster_id=item.cluster_id,
                )
                for item in retrospective_items
            ]
        except Retrospective.DoesNotExist:
            raise ValueError(f"Retrospective with id {retrospective_id} not found")
    
    def encode_retrospective_items(self, items: list[RetroItem]) -> npt.NDArray[float]:
        """Transform retrospective items."""
        return self.transformer.encode([item.content for item in items])
    
    def find_clusters(self, items: npt.NDArray[float]) -> DBSCAN:
        """Fit cluster model."""
        return DBSCAN(eps=1.1, min_samples=1).fit(items).labels_
    
    def cluster_retrospective_items(self, retrospective_id: int, category: str):
        """Cluster retrospective items."""
        items = self.get_retrospective_items(retrospective_id, category)
        items_encoded = self.encode_retrospective_items(items)
        cluster_ids = self.find_clusters(items_encoded)
        
        return cluster_ids