from utils import randbool

# Создаём облака и грозы
class Clouds():
    def __init__(self, mapX, mapY):    # вводим размены нашей карты
        self.mapX = mapX
        self.mapY = mapY
        self.cells = [[0 for i in range(mapX)] for j in range(mapY)]    # создаём каркас собственной карты облаков

    # заполняем каркас карты облаков
    def update_clouds(self, rndMin = 2, rndMax = 20, groz = 1, rndGroz = 20):   # вводим параметры для функции рандома. Первые две для простых облаков, последние две для грозы.
        for i in range(self.mapY):
            for j in range(self.mapX):
                if randbool(rndMin, rndMax):    # определяем с помощью функции рандома будет ли эта клетка облаком или нет
                    self.cells[i][j] = 1    
                    if randbool(groz, rndGroz):     # определяем с помощью функции рандома будет ли это облако грозой или нет
                        self.cells[i][j] = 2
                else:
                    self.cells[i][j] = 0

    # собираем карту облаков в словарь для сохранения 
    def export_data(self):
        return {"cells":self.cells}
    
    # переприсваеваем нашу карту облаков той что из словаря (сохранения)
    def import_data(self, data):
        self.cells = data["cells"] or [[0 for i in range(self.mapX)] for j in range(self.mapY)]
