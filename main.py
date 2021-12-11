from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

from persist import PersistUploader
from worker import init_workers, UploaderWorkers

app = FastAPI()
workers = init_workers()
persist = PersistUploader()

class Uploader(BaseModel):
    Upload_id: str
    Source_folder: str
    Destination_bucket: str
    Regex: Optional[str] = None


@app.post("/uploader/")
async def create_upload(uploader: Uploader):
    UploaderWorkers.add(uploader.dict())
    persist.add_new_item(uploader.dict())
    return uploader

