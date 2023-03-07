from ml_logic.APIs import SpoonAPIcall
from ml_logic.model_roboflow import Recognition

image = "input_image.jpg"

if __name__ == '__main__':

    result = SpoonAPIcall(Recognition(image))
    print("Recomended Dish:", result[0][0])
    print("Dish Recipe:", result[0][1])
