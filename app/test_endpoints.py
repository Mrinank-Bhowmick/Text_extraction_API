import io
from app.main import app,BASE_DIR,UPLOAD_DIR
from fastapi.testclient import TestClient
import shutil
import time
from PIL import Image,ImageChops

client=TestClient(app)        # This is similer to python requests module



def test_get():
    response=client.get("/")
    assert response.status_code==200
    assert "text/html" in response.headers['content-type']


def test_upload():
    img_save_path=BASE_DIR/"images"

    for path in img_save_path.glob("*"):

        try:
            img=Image.open(path)
        except:
            img=None

        response=client.post("/img/",files={"file":open(path,'rb')})
        file_extension=str(path.suffix).replace(".",'')

        if img is None:
            assert response.status_code==400
        else:
            assert response.status_code==200
            #assert file_extension in response.headers['content-type']
            r_stream=io.BytesIO(response.content)
            echo_img=Image.open(r_stream)
            difference=ImageChops.difference(echo_img,img).getbbox()
            assert difference is None

    time.sleep(3)       # To see what is happening
    shutil.rmtree(UPLOAD_DIR)


def test_prediction_upload():
    img_save_path=BASE_DIR/"images"

    for path in img_save_path.glob("*"):

        try:
            img=Image.open(path)
        except:
            img=None

        response=client.post("/",files={"file":open(path,'rb')})
        file_extension=str(path.suffix).replace(".",'')

        if img is None:
            assert response.status_code==400
        else:
            assert response.status_code==200
            data=response.json()
            print(data)
            print(len(data.keys()))
            assert len(data.keys())==2