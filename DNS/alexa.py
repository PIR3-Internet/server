import random

class Alexa:
    def __init__(self, file):
        self.file = file

    def retrieve_top(self, number):
        with open(self.file, 'r') as f:
            return [f.readline().rstrip() for _ in range(number)]

    def retrieve_random(self, number):
        with open(self.file, 'r') as f:
            lines = f.readlines()
            numbers = [random.randint(0, len(lines)-1) for _ in range(number)]
            return [lines[i].rstrip() for i in numbers]

    def retrieve_bottom(self, number):
        with open(self.file, 'r') as f:
            lines = f.readlines()
            return [lines[i].rstrip() for i in range(len(lines)-number, len(lines))]
