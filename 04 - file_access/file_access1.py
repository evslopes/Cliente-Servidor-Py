import eel, os, psutil, time

eel.init('web')

@eel.expose
def CPU():
    while True:
        eel.sleep(1.0)
        return psutil.cpu_percent(percpu=True)

eel.start('file_access1.html')
