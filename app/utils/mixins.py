import datetime
import re

from sqlalchemy import BIGINT, Column, DateTime
from sqlalchemy.orm import declarative_base, declarative_mixin, declared_attr

# declarative base class
Base = declarative_base()


@declarative_mixin
class CommonMixin:
    """define a series of common elements that may be applied to mapped
    classes using this class as a mixin class."""

    __name__: str
    __table_args__ = {"mysql_engine": "InnoDB"}
    __mapper_args__ = {"eager_defaults": True}

    id: int = Column(BIGINT, primary_key=True, autoincrement=True)

    @declared_attr
    def __tablename__(cls) -> str:
        split_cap = re.findall("[A-Z][^A-Z]*", cls.__name__)
        table_name = (
            "".join(map(lambda word: word.lower() + "_", split_cap[:-1]))
            + split_cap[-1].lower()
        )
        return table_name


class TimestampMixin:
    creation_date: datetime = Column(
        DateTime, default=datetime.datetime.utcnow()
    )
    modified_date: datetime = Column(DateTime)
