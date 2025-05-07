import face_recognition
import FaceCoding.FaceStorage
import logging
import io
import numpy as np

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