from tinydb  import TinyDB
from datetime import datetime

class PosicaodoRobo: 
    def __init__(self, db_path): 
        
        self.db = TinyDB(db_path)
        self.table = self.db.table('Posicaodorobo')

    def coordenadas_add(self, x, y, z, r):  
        self.table.insert({
            'x': x,
            'y': y,
            'z': z,
            'r': r,
            'hora': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    def valores(self): 
        return self.table.all()