
category_index = {1: {'id': 1, 'name': 'buffalo'}, 2: {'id': 2, 'name': 'elephant'}, 3: {'id': 3, 'name': 'giraffe'}, 4: {'id': 4, 'name': 'human'}, 5: {'id': 5, 'name': 'leopard'}, 6: {'id': 6, 'name': 'lion'}, 7: {'id': 7, 'name': 'rhinoceros'}, 8: {'id': 8, 'name': 'zebra'}}
models_folder = "classification/models/"

mobilenet = "MOBILENET"
mobilenet_lite = "MOBILENET_LITE"
mobilenet_q = "MOBILENET_Q"
inception = "INCEPTION"
MODEL = mobilenet # ENTER MODEL HERE

relevant_class = [4,7]

if MODEL == mobilenet:
    model_filename = models_folder + "mobilenet_0416_adam.tflite"

elif MODEL == mobilenet_lite:
    model_filename = models_folder + "mobilenet_lite_0416_adam.tflite"

elif MODEL == mobilenet_q:
    model_filename = models_folder + "mobilenet_0420_adam_q.tflite"

elif MODEL == inception:
    model_filename = models_folder + "inception_0416_adam.tflite"
