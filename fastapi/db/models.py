from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import Base from database (the file database.py from above).
from .database import Base

# Inherit Base class we created before to create the SQLAlchemy models on the file database.py
# The __tablename__ attribute tells SQLAlchemy the name of the table
# to use in the database for each of these models..


# The __tablename__ attribute tells SQLAlchemy the name of the table
# to use in the database for each of these models.
class Document(Base):
    __tablename__ = "document"  # this means `document` in Elasticsearch.

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
    # owner_id = Column(Integer, ForeignKey("users.id"))
    # owner = relationship("User", back_populates="items")


class Keyword(Base):
    __tablename__ = "keyword"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    freq = Column(Integer, index=True)
    category = Column(String(255), index=True)
    description = Column(String(255), index=True)
