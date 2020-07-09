"""
In this file we will have reusable functions to interact with the data in the database.
CRUD comes from: Create, Read, Update, and Delete.
"""

# Import Session from sqlalchemy.orm, this will allow you to declare the type of the db parameters
# and have better type checks and completion in your functions.
from sqlalchemy.orm import Session

from typing import List
from . import models, schemas

def get_document_by_id(db: Session, doc_id: int):
    """
    `models.Document` モデルの `id` を走査して，`doc_id` に一致したもののうち先頭要素を返す
    """
    return db.query(models.Document).filter(models.Document.id == doc_id).first()


def get_documents(db: Session, skip: int = 0, limit: int = 10000):  # max で1万件まで取得
    return db.query(models.Document).offset(skip).limit(limit).all()


def create_document(db: Session, document: schemas.DocCreate):
    """
    cf. https://fastapi.tiangolo.com/tutorial/sql-databases/#create-data
    """
    doc = models.Document(**document.dict())
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

    # TODO:      raise HTTP_EXCEPTIONS.get(status_code, TransportError)(
    # elasticsearch.exceptions.ConflictError: ConflictError(409, 'version_conflict_engine_exception', '[1]: version conflict, document already exists (current version [1])')


def get_keywords(db: Session, skip: int = 0, limit: int = 10000):
    return db.query(models.Keyword).offset(skip).limit(limit).all()


def create_keyword(db: Session, keyword: schemas.KeywordCreate):
    """
    cf. https://fastapi.tiangolo.com/tutorial/sql-databases/#create-data
    """
    word = models.Keyword(**keyword.dict())
    db.add(word)
    db.commit()
    db.refresh(word)
    return word


def create_keyword_bulk(db: Session, keywords: List[schemas.KeywordCreate]):
    """
    cf. https://fastapi.tiangolo.com/tutorial/sql-databases/#create-data
    """

    # cf. https://bit.ly/2Ni8G3O
    keyword_list = [models.Keyword(**k.dict()) for k in keywords]
    # db.execute(models.Keyword.__table__.insert(), keyword_list)
    db.bulk_save_objects(keyword_list, return_defaults=True)
    db.commit()
    return keyword_list


# ---------------------------------------------------------------------
# Elasticsearch operation ---------------------------------------------
# ---------------------------------------------------------------------

async def getAllSparqlet(es, size):
    query = {
        'size': size,
        'query': {
            'match_all': {}
        }
    }
    return await es.search(index="sparqlets", body=query, filter_path=['hits.hits._*'])


async def search_sparqlet_by_keyword(es, keyword_list, size=1000):
    """
    # compund queries: cf. https://www.elastic.co/guide/en/elasticsearch/reference/current/compound-queries.html
    # query DSL - Bool: cf. https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html
    """

    match_list = []  # init
    # init <= ref to `schemas.SPARQLet`
    fieldname_list = ["title", "description", "src"]

    for field in fieldname_list:
        # dsl object for `query.match` (this is a part of `bool.query`)

        query_dsl_match = {
            "match": {
                field: {
                    "query": " ".join(keyword_list),
                    # querying method: cf. https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html#match-field-params
                    "operator": "or"
                }
            }
        }
        match_list.append(query_dsl_match)
    # end of for-loop -------------------------------------------------

    # クエリのORではなく，DSLのORを示す(?)
    query_dsl = {
        "should": match_list
    }
    compound_query_bool = {"query": {"bool": query_dsl}}
    # The `filter_path` parameter is used to reduce the response returned by elasticsearch.
    # cf. https://bit.ly/3hLWJlb
    result = await es.search(index="sparqlets", body=compound_query_bool, filter_path=['hits.hits._*'])
    return result


async def prefixSearch_sparqlet_by_keyword(es, keyword_list, size=1000):

    match_list = []  # init
    # init <= ref to `schemas.SPARQLet`
    fieldname_list = ["title", "description", "src"]

    for field in fieldname_list:
        for keyword in keyword_list:
            query_dsl_match = {
                "prefix": {
                    field: {
                        "value": keyword
                    }
                }
            }
            match_list.append(query_dsl_match)
    # end of for-loop -------------------------------------------------

    # クエリのORではなく，DSLのORを示す(?)
    query_dsl = {
        "should": match_list
    }
    compound_query_bool = {"query": {"bool": query_dsl}}
    # The `filter_path` parameter is used to reduce the response returned by elasticsearch.
    # cf. https://bit.ly/3hLWJlb
    result = await es.search(index="sparqlets", body=compound_query_bool, filter_path=['hits.hits._*'])
    return result
