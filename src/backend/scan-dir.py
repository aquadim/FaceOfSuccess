# scan-dir.py
# Использование: python3 scan-dir.py <путь к папке с изображениями> <путь к БД>
# Сканирует папку изображений, находит на фотографиях лица студентов и сохраняет
# их в кодированном виде в базу данных.
import argparse
import os
import logging
import Database
import FaceCoding.FaceStorage
import FaceCoding.EncodeFaces

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
    db = Database.DB(args['database'])

    # Сканирование изображений
    imageDir = args['mediadir']
    files = os.listdir(imageDir)
    newFound = False
    isFirstFound = True

    # Создание хранилища лиц
    storage = FaceCoding.FaceStorage.FaceStorage()

    for filename in files:
        fullPath = os.path.realpath(os.path.join(imageDir, filename))
        if db.isPhotoExists(fullPath):
            continue
        newFound = True

        # Если это первый раз когда нашли новую фотографию, загружаем
        # данные из BLOB в np массив
        if isFirstFound:
            isFirstFound = False
            allFaces = db.getStudentFaces()
            storage.fill(allFaces)
        
        FaceCoding.EncodeFaces.processImage(fullPath, db, storage)

    if not newFound:
        logging.info("Не обнаружено новых изображений")

    db.close()

if __name__ == "__main__":
    main()