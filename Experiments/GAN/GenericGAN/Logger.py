from datetime import datetime

class Logger:
    def __init__(self):
        pass

    def log(self, msg):
        now = datetime.now()
        print(f"{now}: {msg}")
