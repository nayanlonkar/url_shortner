from sqlalchemy import Column, String
from sqlalchemy.orm import Session
from database import Base


class Urls(Base):
    __tablename__ = "urls"

    shortcut = Column(String, primary_key=True, index=True)
    mdfive = Column(String, unique=True, index=True)
    url = Column(String, unique=True)


def create_db_entry(db: Session, shortcut: str, mdfive: str, url: str):
    db_entry = Urls(shortcut=shortcut, mdfive=mdfive, url=url)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def get_shortcut(db: Session, shortcut: str):
    return db.query(Urls).filter(Urls.shortcut == shortcut).first()


def get_mdfive(db: Session, mdfive: str):
    return db.query(Urls).filter(Urls.mdfive == mdfive).first()
