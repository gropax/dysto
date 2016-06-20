class Logger(object):
    def __init__(self, streams=[]):
        self.streams = streams

    def log(self, string):
        for stream in self.streams:
            stream.write(string.rstrip() + "\n")
