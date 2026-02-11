"""
Base repository class with common JSON file operations.
Provides shared functionality for all repository implementations.
"""
import json
import logging
from pathlib import Path
from typing import List, TypeVar, Generic, Type
from pydantic import BaseModel

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)


class BaseRepository(Generic[T]):
    """
    Base repository class with common JSON file operations.
    Subclasses should specify the model type and file path.
    """
    
    def __init__(self, file_path: Path, model_class: Type[T]):
        """
        Initialize the repository.
        
        Args:
            file_path: Path to the JSON file
            model_class: Pydantic model class for this repository
        """
        self.file_path = file_path
        self.model_class = model_class
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Ensure the data directory and file exist."""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not self.file_path.exists():
                self.file_path.write_text("[]", encoding="utf-8")
                logger.info(f"Created file: {self.file_path}")
        except Exception as e:
            logger.error(f"Failed to create file {self.file_path}: {e}", exc_info=True)
            raise
    
    def _load_all(self) -> List[T]:
        """
        Load all items from the JSON file.
        
        Returns:
            List of model instances
        """
        try:
            content = self.file_path.read_text(encoding="utf-8")
            data = json.loads(content)
            items = [self.model_class(**item) for item in data]
            logger.debug(f"Loaded {len(items)} items from {self.file_path.name}")
            return items
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON in {self.file_path}: {e}", exc_info=True)
            return []
        except Exception as e:
            logger.error(f"Error loading from {self.file_path}: {e}", exc_info=True)
            return []
    
    def _save_all(self, items: List[T]) -> None:
        """
        Save all items to the JSON file.
        
        Args:
            items: List of model instances to save
        """
        try:
            data = [item.model_dump(mode='json') for item in items]
            content = json.dumps(data, indent=2, ensure_ascii=False)
            self.file_path.write_text(content, encoding="utf-8")
            logger.debug(f"Saved {len(items)} items to {self.file_path.name}")
        except Exception as e:
            logger.error(f"Failed to save to {self.file_path}: {e}", exc_info=True)
            raise
