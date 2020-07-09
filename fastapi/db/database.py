import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

mysql_config = {
    'u': os.environ['MYSQL_USER'],
    'ps': os.environ['MYSQL_PASSWORD'],
    'h': os.environ['MYSQL_CONTAINER_HOST'],
    'db': os.environ['MYSQL_DATABASE'],
    'cs': os.environ['MYSQL_CHARACTER']
}

url = 'mysql+mysqldb://{u}:{ps}@{h}/{db}?charset={cs}'.format(**mysql_config)

# The file will be located at the same directory in the file sql_app.db.
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    # this is needed only for SQLite. It's not needed for other databases.
    url, isolation_level='SERIALIZABLE'
)
# The class itself is not a database session yet, so we create an instance of the SessionLocal class.
# this instance will be the actual database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Later we will inherit from this class to create each of the database models or classes (the ORM models)
Base = declarative_base()
