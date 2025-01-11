# accept-face.py
# Использование: python3 accept-face.py -i <путь к изображению> -db <путь к БД>
# Загружает изображение, возвращает список из id студентов, которые были
# найдены в БД
# Выводит ответ в стандартный вывод в формате JSON
# Пример ошибки
#{
#    "ok": false,
#    "description": "Перефотографируйтесь"
#}
# Пример успеха
#{
#    "ok": true,
#    "photoIds": [1, 2, 3, 4]
#}

import argparse
import os
import logging
import face_recognition
import Database
import sqlite3
import io
import numpy as np
import FaceStorage
import json

# Выводит ошибку в std
def fail(message):
    obj = {"ok": False, "description": message}
    print(json.dumps(obj))

def success(photoIds):
    output = []
    for item in photoIds:
        output.append(item[0])
    obj = {"ok": True, "photoIds": output}
    print(json.dumps(obj))

def process(dbManager, faceEncoding):
    # Хранилище
    storage = FaceStorage.FaceStorage()
    allFaces = dbManager.getStudentFaces()
    storage.fill(allFaces)

    # Узнаём что это за студент
    result = storage.compare(faceEncoding)
    if not result.found:
        fail("Нет связанных с тобой фотографий")
        return

    # Собираем все фотографии, которые есть с этим студентом
    photoIds = dbManager.getPhotosByStudentId(result.foundStudentId)
    success(photoIds)

def main():
    # Парсинг аргументов командной строки
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-i", "--image",
        required=True,
        help="Путь к изображению"
    )
    ap.add_argument(
        "-db", "--database",
        required=True,
        help="Путь к базе данных"
    )
    ap.add_argument(
        '--quiet',
        action="store_true",
        help="Не выводить сообщения журнала"
    )
    args = ap.parse_args()

    # Журналирование
    if not args.quiet:
        logging.basicConfig(
            format='[%(asctime)s]: %(levelname)s: %(message)s',
            level=logging.INFO,
            datefmt='%Y/%m/%d %H:%M:%S'
        )
    
    # Загрузка фотографии
    image = face_recognition.load_image_file(args.image)
    logging.info("Загружено изображение: {0}".format(args.image))

    # Поиск лиц
    faceEncodings = face_recognition.face_encodings(image, model='cnn')
    logging.info("Найдено лиц: {}".format(len(faceEncodings)))
    if (len(faceEncodings) == 0):
        fail("На фотографии не обнаружено ни одного лица")
        return
    if (len(faceEncodings) > 1):
        fail("На фотографии обнаружено больше одного лица")
        return
    faceEncoding = faceEncodings[0]

    # БД
    dbManager = database.DB(args.database)
    process(dbManager, faceEncoding)
    dbManager.close()
main()