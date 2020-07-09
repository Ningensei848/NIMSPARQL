"""
To avoid confusion between the SQLAlchemy models and the Pydantic models,
we will have the file models.py with the SQLAlchemy models,
and the file schemas.py with the Pydantic models.
These Pydantic models define more or less a "schema" (a valid data shape).
So this will help us avoiding confusion while using both.
cf. https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-pydantic-models
"""
from datetime import datetime
from typing import List, Dict, Union

from pydantic import BaseModel


# Create Pydantic models (or let's say "schemas")
# to have common attributes while creating or reading data.
class Param(BaseModel):
    name: str
    description: str
    default: Union[str, float]
    example: List[str] = []


class SPARQLet(BaseModel):
    name: str  # Character restricted (expect for use into path)
    title: str  # length limited
    description: str = None  # short desc. (length limited)
    src: str   # markdown
    html: str  # html
    endpoint: str  # TODO: 複数のエンドポイントに投げたい場合もある？（高度で複雑なクエリの場合）
    params: List[Param] = []


class DocBase(BaseModel):
    name: str
    title: str
    description: str = None


class DocCreate(DocBase):
    pass


class Document(DocBase):
    id: int

    class Config:
        """
        This Config class is used to provide configurations to Pydantic.
        This mode will tell the Pydantic model to read the data even if it is not a dict,
        but an ORM model (or any other arbitrary object with attributes).
        cf. https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode
        """
        orm_mode = True


class KeywordBase(BaseModel):
    """
    id, name, freq, category, description だけの簡単なテーブル
    """
    name: str
    category: str = None
    description: str = None


class KeywordCreate(KeywordBase):
    freq: int = 0


class Keyword(KeywordBase):
    id: int

    class Config:
        orm_mode = True
