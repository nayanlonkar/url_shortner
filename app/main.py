import hashlib
import models
from starlette.responses import RedirectResponse
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_md5(data: str):
    data = hashlib.md5(data.encode())
    return data.hexdigest()


@app.get("/{shortcut}", tags=["url"], status_code=status.HTTP_200_OK)
def get_url(shortcut: str, db: Session = Depends(get_db)):
    shortcut_exists = models.get_shortcut(db, shortcut=shortcut)

    # if shortcut is not present, raise exception
    if not shortcut_exists:
        raise HTTPException(status_code=400, detail="Shortcut is not present")

    # redirect response
    return RedirectResponse(url=shortcut_exists.url)


@app.post("/url", tags=["url"], status_code=status.HTTP_201_CREATED)
def create_shortcut(shortcut: str, url: str, db: Session = Depends(get_db)):
    md5 = get_md5(url)
    # check if url is already present or not
    url_exists = models.get_mdfive(db, md5)
    # if it is already present then return the shortcut
    if url_exists:
        return url_exists

    # check if shortcut is already present or not
    shortcut_exists = models.get_shortcut(db, shortcut=shortcut)
    # if shortcut is already present then raise exception
    if shortcut_exists:
        raise HTTPException(
            status_code=400,
            detail="Shortcut is already present. Please use different shortcut",
        )

    return models.create_db_entry(db, shortcut=shortcut, mdfive=md5, url=url)
