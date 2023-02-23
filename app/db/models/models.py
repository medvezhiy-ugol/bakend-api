# pylint: disable=R0903
from sqlalchemy import CheckConstraint, Column, ForeignKey, MetaData
from sqlalchemy.dialects.postgresql import (
    BOOLEAN,
    CHAR,
    INTEGER,
    JSONB,
    TIMESTAMP,
    VARCHAR,
    FLOAT,
)
from sqlalchemy.orm import declarative_base
from enum import Enum
from app.db import convention


metadata = MetaData(naming_convention=convention)
DeclarativeBase = declarative_base(metadata=metadata)


class User_type(Enum):
    Admin = 1
    User = 2


class Users(DeclarativeBase):
    __tablename__ = "users"

    id = Column(
        "id", INTEGER, primary_key=True, unique=True, autoincrement=True, nullable=False
    )
    nickname = Column("nickname", VARCHAR(30), nullable=False)
    name = Column("name", VARCHAR(15), nullable=False)
    user_type = Column("user_type", VARCHAR(15), nullable=False)
    surname = Column("surname", VARCHAR(20), nullable=False)
    phone = Column("phone", CHAR(12), nullable=False)
