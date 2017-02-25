import time
class A():
    def __init__(self):
        self.a = "Doneeee"

    def run(self):
        time.sleep(12)
        return self.a

a = A()
def run(cls):
    print dir(cls)
