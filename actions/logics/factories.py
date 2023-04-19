from theormsearch import *
class factory:
    def __init__(self):
        pass
    def create(self):
        raise NotImplementedError("this and abstracted class")
class theorm_finder_factory(factory):
    def __init__(self,theorm_path):
        super().__init__()
        self.theorm_path=theorm_path
    def create(self):
        return theorm_finder(self.theorm_path)
