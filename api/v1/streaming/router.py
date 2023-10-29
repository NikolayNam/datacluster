from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from fastapi import Request, Response
from fastapi import Header
from fastapi.templating import Jinja2Templates

streaming_router = APIRouter(prefix="/streams")
templates = Jinja2Templates(directory="/api/v1/streaming/templates")
video_file = '/api/videos/almata_semei.mp4'


@streaming_router.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@streaming_router.get("/video")
async def video():
    def file_upload():  #
        with open(video_file, mode="rb") as file:
            yield from file
    return StreamingResponse(file_upload(), media_type="video/mp4")
