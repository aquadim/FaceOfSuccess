#!/usr/bin/python3
# Файл для работы с БД
import sqlite3
import io

class DB:
    def __init__(self, dbPath):
        self.con = sqlite3.connect(dbPath)
        self.cur = self.con.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS "photo" (
            "id"	INTEGER,
            "path"	TEXT UNIQUE,
            PRIMARY KEY("id" AUTOINCREMENT)
        )""")

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS "face" (
            "id"	INTEGER,
            "encoding"	BLOB,
            "photo_id"	INTEGER,
            "student_id"	INTEGER,
            FOREIGN KEY("photo_id") REFERENCES "photo"("id"),
            FOREIGN KEY("student_id") REFERENCES "student"("id"),
            PRIMARY KEY("id" AUTOINCREMENT)
        )""")
        
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS "student" (
            "id"	INTEGER,
            PRIMARY KEY("id" AUTOINCREMENT)
        )""")

    # Добавляет фотографию
    def addPhoto(self, path):
        self.cur.execute('INSERT INTO photo (path) VALUES (?)', (path,))
        return self.cur.lastrowid

    # Добавляет студента
    def addStudent(self):
        self.cur.execute('INSERT INTO student (id) VALUES (NULL)')
        return self.cur.lastrowid

    # Связывает лицо со студентом
    def addStudentFace(self, studentId, faceId):
        self.cur.execute('INSERT INTO student_face (face_id,student_id) VALUES (?, ?)', (faceId,studentId))
        return self.cur.lastrowid

    # Добавляет лицо
    def addFace(self, studentId, byteData, photoId):
        self.cur.execute('INSERT INTO face (student_id, encoding, photo_id) VALUES (?, ?, ?)', (studentId, byteData, photoId))
        return self.cur.lastrowid

    # Возвращает все фотографии студентов с данными и ID студентов
    def getStudentFaces(self):
        self.cur.execute(
        """
        SELECT face.student_id, face.encoding
        FROM face
        """)
        return self.cur.fetchall()

    # Возвращает true если фотография существует
    def isPhotoExists(self, filePath):
        self.cur.execute(
        """
        SELECT COUNT(*)
        FROM photo
        WHERE path=?
        """, (filePath,))
        return self.cur.fetchone()[0] > 0

    # Возвращает фотографии по ID студента
    def getPhotosByStudentId(self, studentId):
        self.cur.execute(
        """
        SELECT face.photo_id
        FROM face
        WHERE face.student_id = ?
        """, (studentId,))
        return self.cur.fetchall()

    # Возвращает путь к фотографии по ID
    def getPhotoPath(self, photoId):
        self.cur.execute(
        """
        SELECT path
        FROM photo
        WHERE id = ?
        """, (photoId,))
        return self.cur.fetchone()[0]

    # Возвращает путь к фотографиям по их ID
    def getPathsByIds(self, photoIds):
        strings = (str(item) for item in photoIds)
        inStatement = ",".join(strings)
        self.cur.execute(
        """
        SELECT path
        FROM photo
        WHERE id IN (%s)
        """ % inStatement)
        return self.cur.fetchall()

    # Подтверждает транзакцию
    def commit(self):
        self.con.commit()

    # Закрывает подключение
    def close(self):
        self.con.commit()
        self.con.close()