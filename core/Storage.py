class Storage:
    def __init__(self):
        self.data = {}
        self.objects = []

    def set(self, key, value):
        if type(value) == object:
            self.objects.append(value)
        else:
            self.data[key] = value

    def get(self, key, default=None):
        return self.data.get(key, default)
    

    def get_objects(self):
        return self.objects
    
    def exists(self, key):
        if key in self.data:
            return True
        else:
            return False