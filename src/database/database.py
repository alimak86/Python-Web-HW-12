from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:567234@195.201.150.230:5433/a_makusheva_fa"
SQLALCHEMY_DATABASE_URL_FOR_WORK = "postgresql+psycopg2://postgres:567234@195.201.150.230:5433/a_makusheva_fa"


class Connect_db:

  def __init__(self, url: str):
    self.url = url
    self.engine = create_engine(url)
    self.session = sessionmaker(autocommit=False,
                                autoflush=False,
                                bind=self.engine)

  def __call__(self):
    db = self.session()
    try:
      yield db
    finally:
      db.close()
