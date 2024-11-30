import random
import keras
from keras.layers import Input
from keras.models import Model
from keras.applications.resnet50 import preprocess_input, decode_predictions
import os
from PIL import Image
import numpy as np
from tensorflow.compat.v1 import ConfigProto, InteractiveSession

# Настройка для GPU (если используется CPU, можно пропустить этот блок)
config = ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.7
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

height, width = 224, 224  # Размер входного изображения
nh, nw, ncol = 224, 224, 3  # Размеры и количество цветовых каналов

visible2 = Input(shape=(nh, nw, ncol), name='imginp')
resnet = keras.applications.resnet_v2.ResNet50V2(
    include_top=True,
    weights='imagenet',
    input_tensor=visible2,
    input_shape=None,
    pooling=None,
    classes=1000
)

def read_image_files(files_max_count, dir_name):
    files = [item.name for item in os.scandir(dir_name) if item.is_file()]
    files_count = min(files_max_count, len(files))
    image_box = []
    
    for file_name in files[:files_count]:
        try:
            img_path = os.path.join(dir_name, file_name)
            image_box.append(Image.open(img_path))
        except Exception as e:
            print(f"Ошибка при чтении файла {file_name}: {e}")
            continue

    return files_count, image_box

def getresult(image_box):
    files_count = len(image_box)
    images_resized = []

    # Преобразуем изображения в формат numpy и нормализуем
    for i in range(files_count):
        try:
            resized_image = np.array(image_box[i].resize((height, width))) / 255.0
            images_resized.append(resized_image)
        except Exception as e:
            print(f"Ошибка при обработке изображения: {e}")

    images_resized = np.array(images_resized)

    # Передаем изображения в сеть и получаем результаты
    out_net = resnet.predict(images_resized)
    decode = decode_predictions(out_net, top=1)  # Декодируем классы
    return decode

# Пример прединициализации сети (опционально):
# fcount, fimage = read_image_files(1, './static')
# decode = getresult(fimage)
