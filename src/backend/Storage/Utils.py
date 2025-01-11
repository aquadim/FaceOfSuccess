#!/usr/bin/env python
# Определяет есть ли подключенное USB хранилище.
# Если есть, возвращает путь к корню первого найденного раздела
import pyudev
import psutil

def ok(mountPoint):
    return {"ok": True, "path": mountPoint}

def fail():
    return {"ok": False}

def main():
    found = False
    
    # https://unix.stackexchange.com/a/294690
    context = pyudev.Context()

    # Поиск внешних дисковых устройств
    removable = [device for device in context.list_devices(subsystem='block', DEVTYPE='disk') if device.attributes.asstring('removable') == "1"]
    for device in removable:
        # Поиск разделов дисков на внешних устройствах
        partitions = [device.device_node for device in context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
        for p in psutil.disk_partitions():
            if p.device in partitions:
                return ok(p.mountpoint)

    return fail()

if __name__ == "__main__":
    main()