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
    UploaderWorkers.add(uploader.dict())
    PersistUploader(uploader.dict())
    return uploader


def PersistUploader(item):
    import pickle
    filename = "persist_picklefile"
    with open(filename, "ab") as fp:
        pickle.dump(item, fp)

    #To load from pickle file
    data = []
    with open(filename, 'rb') as fr:
        try:
            while True:
                data.append(pickle.load(fr))
        except EOFError:
            pass

    print(len(data))
    print(data)
