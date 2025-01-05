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

    def addPhoto(self, path):
        self.cur.execute('INSERT INTO photo (path) VALUES (?)', (path,))
        return self.cur.lastrowid

    def addStudent(self):
        self.cur.execute('INSERT INTO student (id) VALUES (NULL)')
        return self.cur.lastrowid
        
    def addStudentFace(self, studentId, faceId):
        self.cur.execute('INSERT INTO student_face (face_id,student_id) VALUES (?, ?)', (faceId,studentId))
        return self.cur.lastrowid

    # encoding - 128-размерный массив кодировки лица
    def addFace(self, studentId, byteData, photoId):
        self.cur.execute('INSERT INTO face (student_id, encoding, photo_id) VALUES (?, ?, ?)', (studentId, byteData, photoId))
        return self.cur.lastrowid

    def getStudentFaces(self):
        self.cur.execute(
        """
        SELECT face.student_id, face.encoding
        FROM face
        """)
        return self.cur.fetchall()

    def isPhotoExists(self, filePath):
        self.cur.execute(
        """
        SELECT COUNT(*)
        FROM photo
        WHERE path=?
        """, (filePath,))
        return self.cur.fetchone()[0] > 0

    def getPhotosByStudentId(self, studentId):
        self.cur.execute(
        """
        SELECT face.photo_id
        FROM face
        WHERE face.student_id = ?
        """, (studentId,))
        return self.cur.fetchall()

    def commit(self):
        self.con.commit()

    def close(self):
        self.con.commit()
        self.con.close()