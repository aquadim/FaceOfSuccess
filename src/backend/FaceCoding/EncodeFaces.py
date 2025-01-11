# encode-faces.py
# Использование: python3 encode-faces.py <путь к папке с изображениями> <путь к БД>
# Сканирует папку изображений, находит на фотографиях лица студентов и сохраняет
# их в кодированном виде в базу данных.
import argparse
import os
import logging
import face_recognition
import Database
import sqlite3
import io
import numpy as np
import FaceStorage

# Обрабатывает изображение
def processImage(filePath, dbManager, storage):
    # Загрузка изображения
    image = face_recognition.load_image_file(filePath)
    logging.info("Обработка изображения " + filePath)

    # Поиск лиц
    faceEncodings = face_recognition.face_encodings(image, model='cnn')
    logging.info("Найдено лиц: {}".format(len(faceEncodings)))

    # Добавляем в базу фотографию
    try:
        photoId = dbManager.addPhoto(filePath)
    except sqlite3.IntegrityError:
        logging.error("Фотография уже существует в базе данных")
        return

    # Каждое лицо на фотографии добавляем в базу
    for encoding in faceEncodings:
        # Преобразование лица из 128-размерного массива в байты
        byteIO = io.BytesIO()
        np.save(byteIO, encoding)
        byteData = byteIO.getvalue()

        # Сверяем лицо с базой существующих
        result = storage.compare(encoding)
        if not result.found:
            logging.info("Лицо студента не распознано. Создаю нового студента.")
            studentId = dbManager.addStudent()
            logging.info("Студент создан, id: {0}.".format(studentId))
        else:
            logging.info("Студент распознан. (id: {0}) ".format(result.foundStudentId))
            studentId = result.foundStudentId

        storage.add(encoding, studentId)
        dbManager.addFace(studentId, byteData, photoId)
        dbManager.commit()

def main():
    # Журналирование
    logging.basicConfig(
        format='[%(asctime)s]: %(levelname)s: %(message)s',
        level=logging.INFO,
        datefmt='%Y/%m/%d %H:%M:%S'
    )

    # Парсинг аргументов командной строки
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-m", "--mediadir",
        required=True,
        help="Путь к директории изображений для сканирования"
    )
    ap.add_argument(
        "-db", "--database",
        required=True,
        help="Путь к базе данных"
    )
    args = vars(ap.parse_args())

    # БД
    dbManager = database.DB(args['database'])

    # Сканирование изображений
    imageDir = args['mediadir']
    files = os.listdir(imageDir)
    newFound = False
    isFirstFound = True

    # Создание хранилища лиц
    storage = FaceStorage.FaceStorage()

    for filename in files:
        fullPath = os.path.join(imageDir, filename)
        if dbManager.isPhotoExists(fullPath):
            continue
        newFound = True

        # Если это первый раз когда нашли новую фотографию, загружаем
        # данные из BLOB в np массив
        if isFirstFound:
            isFirstFound = False
            allFaces = dbManager.getStudentFaces()
            storage.fill(allFaces)
        
        processImage(fullPath, dbManager, storage)

    if not newFound:
        logging.info("Не обнаружено новых изображений")

    dbManager.close()

main()