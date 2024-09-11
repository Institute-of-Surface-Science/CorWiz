from typing import Optional, List
from datetime import datetime

from .creator import Creator


class File:
    """
    A class to represent a file with its associated metadata.

    Attributes:
        checksum (str): The checksum of the file.
        created_at (datetime): The timestamp when the file was created.
        creator (Creator): The creator of the file.
        description (str): A description of the file.
        file_id (str): The unique identifier of the file.
        last_modified (datetime): The timestamp when the file was last modified.
        magic_mimetype (str): The magic MIME type of the file.
        mimetype (str): The MIME type of the file.
        name (str): The name of the file.
        size (int): The size of the file in bytes.
    """

    def __init__(self,
                 checksum: str,
                 created_at: str,
                 creator: dict,
                 description: str,
                 id: str,
                 last_modified: str,
                 magic_mimetype: str,
                 mimetype: str,
                 name: str,
                 size: int):
        self.checksum = checksum
        self.created_at = datetime.fromisoformat(created_at)
        self.creator = Creator(**creator)
        self.description = description
        self.id = id
        self.last_modified = datetime.fromisoformat(last_modified)
        self.magic_mimetype = magic_mimetype
        self.mimetype = mimetype
        self.name = name
        self.size = size

    def __repr__(self):
        return (f"File(name={self.name}, size={self.size}, mimetype={self.mimetype}, "
                f"checksum={self.checksum}, created_at={self.created_at}, last_modified={self.last_modified}, "
                f"creator={self.creator})")