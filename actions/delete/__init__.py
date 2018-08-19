from .delete_albums import delete_albums
from .delete_fave import delete_fave
from .delete_messages import delete_messages
from .delete_profile import delete_profile
from .delete_videos import delete_videos
from .delete_wall import delete_wall
from .delete_docs import delete_docs

__all__ = [
    'delete_messages', 'delete_wall', 'delete_fave', 'delete_albums', 'delete_videos', 'delete_profile',
    'delete_docs'
]