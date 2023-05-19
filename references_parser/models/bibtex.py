from enum import Enum
from typing import List, Optional, Tuple, Union

import bibtexparser as p
from pydantic import BaseModel, root_validator, validator


class Bibtex(BaseModel):
    class Types(str, Enum):
        Article = "article"
        Proceedings = "inproceedings"
        Website = "online"

    ENTRYTYPE: Types
    title: str
    year: str

    doi: Optional[str]
    journal: Optional[str]
    author: Optional[Union[str, List[str]]]
    number: Optional[str]
    volume: Optional[str]
    pages: Optional[str]
    booktitle: Optional[str]
    # Proceedings-related
    organization: Optional[str]
    # Website-related
    address: Optional[str]
    base: Optional[str]
    origin: Optional[str]
    url: Optional[str]
    date: Optional[str]
    # Books-related
    issn: Optional[str]

    # Calculated fields
    pages_list: List[str] = []

    @root_validator
    def initialize_and_validate(cls, values):
        """
        Since pydantic does not support computed fields yet
        this method provides a workaround
        """
        pages = values["pages"]
        values["pages_list"] = [] if pages is None else pages.split("--")
        return values

    @validator("title")
    def title_rules(cls, title: str):
        """
        Sometimes the title contains '.' in the end.
        Dot in the end is prohibited

        Args:
            title (str): title to be sanitized

        Returns:
            str: sanitized title
        """
        if title.endswith("."):
            return title[:-1]
        return title
