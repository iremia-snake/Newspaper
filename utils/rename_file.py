import uuid
from os import path


def uuid_file_path(instance, filepath, filename):
    # уникальное имя файла
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex}.{ext}'
    return path.join(filepath, filename)