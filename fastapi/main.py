# -*- coding: utf-8 -*-
"""NIMSPARQList: Routing of FastAPI to Elasticsearch

Requirements:
     * python3.7+
     * `pip install fastapi uvicorn elastic-apm elasticsearch[async]`

Todo:
   TODOリストを記載
    * conf.pyの``sphinx.ext.todo`` を有効にしないと使用できない
    * conf.pyの``todo_include_todos = True``にしないと表示されない

"""

# cf. https://github.com/elastic/elasticsearch-py/tree/master/examples/fastapi-apm

import os
import json
import datetime
from typing import List
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

# elastic modules
from elasticsearch import AsyncElasticsearch, NotFoundError  # with async
# from elasticsearch import Elasticsearch, NotFoundError # not async
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client

# local modules
from db import crud, models, schemas
from db.database import SessionLocal, engine


# settings for Elastic ----------------------------------------------------
apm = make_apm_client(
    {
        "SERVICE_NAME": "NIMSPARQList",
        "SERVER_URL": os.environ["APM_SERVER_URL"]
    }
)
es = AsyncElasticsearch(os.environ["ELASTICSEARCH_URL"])  # with async
# es = Elasticsearch(os.environ["ELASTICSEARCH_URL"])

# -------------------------------------------------------------------------


models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.add_middleware(ElasticAPM, client=apm)

# cf. https://fastapi.tiangolo.com/tutorial/cors/
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # Indicate that cookies should be supported for cross-origin requests.
    allow_credentials=True,
    # A list of HTTP methods that should be allowed for cross-origin requests.
    allow_methods=["*"],
    # A list of HTTP request headers that should be supported for cross-origin requests.
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("shutdown")
async def app_shutdown():
    """FastAPIサーバーが終了したときの処理

        いきなりブチッと接続が切れると例外処理が怖い．
        Elasticsearchとの接続を切り，Glacefullyに処理を終えたい

    Yields:
        es.close(): elasticsearchとの接続を切る

    Note:
        `es` はグローバル変数

    """
    await es.close()


@app.get("/")
async def index():
    """
    cf. https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.create
    """
    if not (await es.indices.exists(index="sparqlets")):
        return await es.indices.create(index="sparqlets")
    else:
        return await es.cluster.health()

# -------------------------------------------------------------------

# `response_model` ---->  responseの取りうるべき型


@app.post("/create/sparqlet", response_model=schemas.Document)
async def create_sparqlet(sparqlet: schemas.SPARQLet, db: Session = Depends(get_db)):
    """
    args: sparqlet expectec JSON
    - SPARQLet is defined as a Markdown document.
      SPARQLet consists of parameterized SPARQL queries and
      JavaScript glue codes that integrate the queries.
      It can also have rich documentation about the SPARQLet itself.
      cf. https://github.com/dbcls/sparqlist/blob/master/doc/GUIDE.md
    """

    doc_attrs: dict = {
        "name": sparqlet.name,
        "title": sparqlet.title,
        "description": sparqlet.description
    }

    # `.dict()` is Pydantic method ----> cf. https://fastapi.tiangolo.com/tutorial/extra-models/#pydantics-dict
    document = crud.create_document(
        db=db,
        document=schemas.DocCreate(**doc_attrs)
    )

    req: dict = sparqlet.dict()
    req.update({
        "created": datetime.datetime.now(),
        "updated": datetime.datetime.now(),
    })

    # if You need to specify id, use `create` instead of `index`
    # cf. https://bit.ly/2Y2V5Ub
    await es.create(index="sparqlets", id=document.id, body=req)

    return document


@app.get("/list/sparqlet")
async def list_sparqlet(keyword: List[str] = Query(None), prefix: bool = Query(None)):
    """
    cf. https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#query-parameter-list-multiple-values
    expect `keyword` is like ... '?keyword=hoge&keyword=huga&keyword=haga'
    """
    if keyword:
        if prefix:
            # prefix 検索（前方一致検索）
            result = await crud.prefixSearch_sparqlet_by_keyword(es, keyword)
        else:
            # TODO: AND検索 => operation をフラグで変える？
            result = await crud.search_sparqlet_by_keyword(es, keyword)
    else:
        result = await crud.getAllSparqlet(es, size=200)
    return result  # type should be `List[schemas.SPARQLet]`


@app.post("/create/keyword", response_model=schemas.Keyword)
async def create_keyword(keyword: schemas.KeywordCreate, db: Session = Depends(get_db)):
    keyword = crud.create_keyword(db=db, keyword=keyword)
    return keyword


@app.post("/create-bulk/keyword", response_model=List[schemas.Keyword])
async def create_keyword_bulk(keywordList: List[schemas.KeywordCreate], db: Session = Depends(get_db)):
    keywordList = crud.create_keyword_bulk(db=db, keywords=keywordList)
    return keywordList


@app.get("/list/keywords/", response_model=List[schemas.Keyword])
async def list_keywords(skip: int = 0, limit: int = 10000, db: Session = Depends(get_db)):
    keywords = crud.get_keywords(db, skip=skip, limit=limit)
    return keywords
