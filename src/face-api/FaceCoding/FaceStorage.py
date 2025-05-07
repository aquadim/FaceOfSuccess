# face-storage.py
import face_recognition
import numpy as np
import io

class FaceSearchResult:
    def __init__(self, found, foundStudentId=None):
        self.found = found
        self.foundStudentId = foundStudentId

# Класс для хранения кодировок лиц и студентов в памяти
class FaceStorage:
    def __init__(self):
        self.faces = []
        self.ids = []

    # Добавляет соответствие лица и студента
    # array - numpy массив
    # studentId - число, id студента
    def add(self, array, studentId):
        self.faces.append(array)
        self.ids.append(studentId)

    # Заполняет лица. allFaces - результат работы database.DB.getStudentFaces
    def fill(self, allFaces):
        for item in allFaces:
            byte_io = io.BytesIO(item[1])
            self.add(np.load(byte_io), item[0])

    def compare(self, encoding):
        # Список из булевых значений, где matches[i] будет True, если faces,
        # и соответственно ids[i] будет похоже на studentFace
        matches = face_recognition.compare_faces(
            self.faces,
            encoding,
            tolerance=0.5
        )

        if not True in matches:
            # Совпадений не найдено
            return FaceSearchResult(False)

        # Узнаём какие индексы совпали
        matchedIndexes = [i for (i, matched) in enumerate(matches) if matched]

        # {student id: сколько совпадений}
        counts = {}
        for i in matchedIndexes:
            studentId = self.ids[i]
            counts[studentId] = counts.get(studentId, 0) + 1

        # Выбор студента с наибольшим количеством совпадений
        finalStudentId = max(counts, key=counts.get)

        return FaceSearchResult(True, finalStudentId)