from sqlalchemy import (FetchedValue, Integer, String, DateTime, Column)
from v1.config.database_conf import Base
from sqlalchemy.sql import text

# The rest of the imports remain the same


class RegionsRussiaModel(Base):
    __tablename__ = 'regions_russia'

    id = Column(Integer, primary_key=True,
                server_default=FetchedValue(), default=None)
    name = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, server_default=text("NOW()"))
    updated_at = Column(DateTime, nullable=False, server_default=text("NOW()"))
