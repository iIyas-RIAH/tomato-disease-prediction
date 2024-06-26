from fastapi import FastAPI, File, UploadFile
import numpy as np
import uvicorn
from io import BytesIO
import tensorflow as tf
import PIL from Image

app = FastAPI()

MODEL = tf.keras.models.load_model("../Tomato_model.h5")
Class_Names = [
    'Tomato_Bacterial_spot',
    'Tomato_Early_blight',
    'Tomato_Late_blight',
    'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite',
    'Tomato__Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus',
    'Tomato__Tomato_mosaic_virus',
    'Tomato_healthy']


def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image


@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expend_dims(image, 0)

    prediction = MODEL.predict(img_batch)

    predicted_class = Class_Names[np.argmax(prediction[0])]
    confidence = np.max(prediction[0])

    return {
        'class' = predicted_class,
        'confidence' = float(confidence)
    }



if __name__ = "__main__":
    uvicorn.run(app, host='localhost', port=8000)
