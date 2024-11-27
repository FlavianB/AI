class OutputFile:

    def __init__(self, path):
        self.path = path
        self.file = open(self.path, 'w')

    def close(self):
        self.file.close()

    def write_and_log(self, *data):
        self.write(*data)
        print(*data)

    def write(self, *data):
        self.file.write(' '.join(map(str, data)) + '\n')
