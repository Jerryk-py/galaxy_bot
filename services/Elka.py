class ElkaService:
    def __init__(self) -> dict:
        self.all = []


    def add(self, id, type, status):
        if id in self.all:
            return False
        else:
            data ={
                'id': id,
                'type': type,
                'status': status,
            }
            self.all.append(data)
            return True
    def clear (self):
        self.all = []
        
    def list(self):
        return self.all
    
    def get(self, id):
        for i in self.all:
            if i['id'] == id:
                return i
        return False 
    
    def set(self,id, status):
        for i in self.all:
            if i['id'] == id:
                i['status']=status
        
    
    def run_good(self):
        for i in self.all:
            if i['status'] == 6:
                return f"OBJ_ACT {i['type']} {i['id']} 11 present_off"
        return False

    def update(self, id, status) -> None:
        for i in self.all:
            if i['id'] == id:
                i['status'] = status