#!/usr/bin/env python
# Определяет есть ли подключенное USB хранилище.
# Если есть, возвращает путь к корню первого найденного раздела
import pyudev
import psutil
import datetime
import os

# Возвращает точку установки раздела первого попавшегося устройства съёмного хранилища
# Возвращает None если не удалось найти таких устройств
def getMountPoint():
    # https://unix.stackexchange.com/a/294690
    context = pyudev.Context()
    
    # Поиск внешних дисковых устройств
    removable = [device for device in context.list_devices(subsystem='block', DEVTYPE='disk') if device.attributes.asstring('removable') == "1"]
    for device in removable:
        # Поиск разделов дисков на внешних устройствах
        partitions = [device.device_node for device in context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
        for p in psutil.disk_partitions():
            if p.device in partitions:
                return p.mountpoint
    return None

# Возвращает имя файла в который следует сохранить вывод лица успеха.
# В конце сразу добавляет .zip
# Например /media/vadim/KOR/ЛицоУспеха_2024_02_09_19_40.zip
def generateZipName(mountPoint):
    now = datetime.datetime.now()
    return os.path.join(
        mountPoint,
        "ЛицоУспеха_" + now.strftime("%Y_%m_%d_%H_%M_%S") + ".zip"
    )