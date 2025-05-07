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
import json
import sqlite3
import sys

def main():
    # Журналирование
    logging.basicConfig(
        format='[%(asctime)s]: %(levelname)s: %(message)s',
        level=logging.INFO,
        datefmt='%Y/%m/%d %H:%M:%S'
    )

    # Путь к БД
    mediaDir = None
    
    # Путь к базе данных
    databaseFile = None

    # Парсинг аргументов командной строки
    # Файл настроек получен?
    configArgFilled = "-c" in sys.argv or "--config" in sys.argv
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-m", "--mediadir",
        required=not configArgFilled,
        help="Путь к директории изображений для сканирования"
    )
    ap.add_argument(
        "-db", "--database",
        required=not configArgFilled,
        help="Путь к базе данных"
    )
    ap.add_argument(
        "-c", "--config",
        required=False,
        help="Путь к файлу настроек"
    )
    args = vars(ap.parse_args())

    # Если пользователь указал файл настроек, берём их
    if args['config'] != None:
        try:
            with open(args["config"]) as configFile:
                config = json.load(configFile)
                mediaDir = config["media-dir"]
                databaseFile = config["database-file"]
        except FileNotFoundError:
            logging.error("Файл настроек по указанному пути не найден")
            return 1
        except KeyError as ex:
            logging.error("Ключ настроек не найден:", ex)
            return 2
        except json.decoder.JSONDecodeError:
            logging.error("Файл настроек содержит неверный JSON")
            return 3
    
    # Приоритет аргументов командной строки над файлом настроек
    if args["mediadir"] != None:
        mediaDir = args["mediadir"]
    if args["database"] != None:
        databaseFile = args["database"]

    # Подключение к базе данных
    try:
        db = Database.DB(databaseFile)
    except sqlite3.OperationalError:
        logging.error("Не удалось открыть файл базы данных")
        return 4

    # Сканирование изображений
    try:
        files = os.listdir(mediaDir)
    except FileNotFoundError:
        logging.error(f"Каталог {mediaDir} не найден")
        return 5
    newFound        = False
    isFirstFound    = True
    storage         = FaceCoding.FaceStorage.FaceStorage()

    for filename in files:
        fullPath = os.path.realpath(os.path.join(mediaDir, filename))
        if db.isPhotoExists(fullPath):
            continue
        newFound = True

        # Если это первый раз когда нашли новую фотографию, 
        # заполняем хранилище лиц
        if isFirstFound:
            isFirstFound = False
            allFaces = db.getStudentFaces()
            storage.fill(allFaces)
        
        FaceCoding.EncodeFaces.processImage(fullPath, db, storage)
        db.commit()

    if not newFound:
        logging.info("Не обнаружено новых изображений")

    db.close()

if __name__ == "__main__":
    main()