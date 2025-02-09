# accept-face.py
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
import logging
import face_recognition
import numpy as np
import FaceCoding.FaceStorage as FaceStorage

# Выводит ошибку в std
def fail(message):
    return {"ok": False, "description": message}

def success(photoIds):
    output = []
    for item in photoIds:
        output.append(item[0])
    obj = {"ok": True, "photoIds": output}
    return obj

def process(dbManager, faceEncoding):
    # Хранилище
    storage = FaceStorage.FaceStorage()
    allFaces = dbManager.getStudentFaces()
    storage.fill(allFaces)

    # Узнаём что это за студент
    result = storage.compare(faceEncoding)
    if not result.found:
        return fail("Нет связанных с тобой фотографий")

    # Собираем все фотографии, которые есть с этим студентом
    photoIds = dbManager.getPhotosByStudentId(result.foundStudentId)
    return success(photoIds)

def accept(filename, db):
    # Загрузка фотографии
    image = face_recognition.load_image_file(filename)

    # Поиск лиц
    faceEncodings = face_recognition.face_encodings(image, model='cnn')
    logging.info("Найдено лиц: {}".format(len(faceEncodings)))
    if (len(faceEncodings) == 0):
        return fail("На фотографии не обнаружено ни одного лица")
    if (len(faceEncodings) > 1):
        return fail("На фотографии обнаружено больше одного лица")
    faceEncoding = faceEncodings[0]

    return process(db, faceEncoding)