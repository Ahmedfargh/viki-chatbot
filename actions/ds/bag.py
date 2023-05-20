class bag:
    def __init__(self):
        self._data=[]
    def append(self,data):
        self._data.append(data)
    def pop(self,index=None):
        if index:
            return self._data.pop(index)
        else:
            return self._data.pop()
    def get_data(self):
        return self._data