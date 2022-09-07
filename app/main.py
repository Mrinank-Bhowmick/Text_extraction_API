import io
import pathlib
from functools import lru_cache
from PIL import Image
import uuid
from fastapi import FastAPI, Depends, Request,UploadFile,File,HTTPException
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings
import pytesseract

class Settings(BaseSettings):
    debug: bool = False
    echo_active:bool = False

    class Config:
        env_file=".env"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
DEBUG=settings.debug

BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR=BASE_DIR/"uploads"


app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
# REST API

print(DEBUG)
@app.get("/", response_class=HTMLResponse) # http GET -> JSON
def home_view(request: Request, settings:Settings = Depends(get_settings)):
    print(settings.debug)
    return templates.TemplateResponse("home.html", {"request": request, "abc": 123})

@app.post("/")   # Same as HTTP post
async def prediction(file:UploadFile=File(...),settings:Settings = Depends(get_settings)):      # Using ellipsis in File(...) will give it an arbitrary length

    bytes_str=io.BytesIO(await file.read())
    try:
        img=Image.open(bytes_str)
    except:
        raise HTTPException(detail="Invalid image",status_code=400)

    prediction=pytesseract.image_to_string(img)
    return {"Text":prediction}



@app.post("/img/",response_class=FileResponse)
async def img_view(file:UploadFile=File(...),settings:Settings = Depends(get_settings)):      # Using ellipsis in File(...) will give it an arbitrary length
    if not settings.echo_active:
        raise HTTPException(detail="Invalid endpoint",status_code=400)

    UPLOAD_DIR.mkdir(exist_ok=True)     # To delete UPLOAD_DIR after we run the test
    bytes_str=io.BytesIO(await file.read())
    try:
        img=Image.open(bytes_str)
    except:
        raise HTTPException(detail="Invalid image",status_code=400)

    file_name=pathlib.Path(file.filename)
    file_extension=file_name.suffix     # This will give us file extenion like .jpg , .png etc
    destination=UPLOAD_DIR/f'{uuid.uuid1()}{file_extension}'  # declaring this to create unique filenames

    img.save(destination)

    return destination
