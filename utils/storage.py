from utils.singleton import Singleton


class Storage:
    __metaclass__ = Singleton

    def __init__(self):
        pass

    def download_file(self, key):
        raise NotImplementedError
