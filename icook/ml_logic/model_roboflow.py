from roboflow import Roboflow
import os
import sys

def model_Roboflow():
    sys.stdout = open(os.devnull, "w")

    rf = Roboflow(api_key=os.environ.get('ROBO_API_KEY'))
    project = rf.workspace().project("icook")

    sys.stdout = sys.__stdout__
    return project.version(5).model

def Recognition(image):
    '''Object Recognition Model predicts input image, saves output image and returns the list of ingredients'''
    model=model_Roboflow()
    prediction = model.predict(image)

    preds_class = []
    for result in prediction.json()['predictions']:
        preds_class.append(result['class'])

    prediction.save(output_path="icook/img/image_with_labels.jpg")

    return preds_class
