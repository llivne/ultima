from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from worker import init_workers, UploaderWorkers

app = FastAPI()
workers = init_workers()


class Uploader(BaseModel):
    Upload_id: str
    Source_folder: str
    Destination_bucket: str
    Regex: Optional[str] = None


@app.post("/uploader/")
async def create_upload(uploader: Uploader):
    UploaderWorkers.add(uploader)
    return uploader
