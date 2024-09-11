from typing import Optional


class Creator:
    """
    A class to represent the creator of a file.

    Attributes:
        displayname (str): The display name of the creator.
        id (int): The ID of the creator.
        orcid (Optional[str]): The ORCID identifier of the creator, if available.
    """
    def __init__(self, displayname: str, id: int, orcid: Optional[str] = None):
        self.displayname = displayname
        self.id = id
        self.orcid = orcid

    def __repr__(self):
        return f"Creator(displayname={self.displayname}, id={self.id}, orcid={self.orcid})"
