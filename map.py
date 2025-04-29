from utils import randbool
from utils import randcell
from utils import randcell2
# 0 - поле
# 1 - дерево
# 2 - река
# 3 - вертолётная площадка
# 4 - мастерская
# 5 - огонь

CELL_TYPES = "🟫🌳🌊🔥🔧🏥"
THREE_REWARD = 100
THREE_PENALTY = 100
UPGRADE_COST = 500
HP_COST = 1000

class Map():

    # тут инициализируем каркас карты и её заполнение
    def __init__(self, mapX, mapY):
        self.mapX = mapX  # задаём размер карты по горизонтали
        self.mapY = mapY  # задаём размер карты по вертикали
        self.cells = [[0 for i in range(mapX)] for j in range(mapY)]  # генерация каркаса карты состоящих из нулей 
        self.generate_forest()
        self.generate_river(mapX, mapY)      
        self.upgrade_station()
        self.helipad()

    # тут заполняем каркас карты и обводим её рамкой
    def print_map(self, heli, clouds):
        print("⬛" * (self.mapX + 2))   # верхняя линия рамки, печатаем символы в количестве размера горизонтали карты(mapX) и по одному символу с каждой стороны(+2)
        for i in range(self.mapY):  # i - индекс (листа) на вертикальной оси(y) в каркасе карты, начинаем с 0 и с каждой новой итерацией идём вниз по оси пока не заполним
            print("⬛", end ="")    # элемент левой стороны рамки в строчке № i, на следующую строку не переходим
            for j in range(self.mapX):    # j - индекс (элемента) на горизонтальной оси(x) 
                cell = self.cells[i][j]
                if (clouds.cells[i][j] == 1):
                    print("💨", end ="")
                elif (clouds.cells[i][j] == 2):
                    print("⚡", end ="")
                elif (heli.hy == i and heli.hx == j):
                    print("🚁", end ="")
                elif (cell >= 0 and cell <= len(CELL_TYPES)):                                  
                    print(CELL_TYPES[cell], end = "")   # возвращаем элемент из списка констант(CELL_TYPES) по номеру элемента в cell (все элементы в cell, как и в cells являются нулями)
            print("⬛")  # строчка № i заканчивается элементом правой стороны рамки, переходим на следующую строку
        print("⬛" * (self.mapX + 2))   # нижняя линия рамки, аналогична верхней

    # функция проверяет является ли заданная точка частью карты
    def check_bounds(self, x, y):
        if (x < 0 or y < 0 or x >= self.mapX or y >= self.mapY):
            return False
        return True
    
    # заполняем карту деревьями
    def generate_forest(self, rndMin = 1, rndMax = 2):  # вводим соотношение клеток деревьев по отношению к остальной карте
        for i in range(self.mapY):    # проходим по каждой строке под номером i на вертикальной оси
            for j in range(self.mapX):    # проходим по каждому элементу в строке под номером j на горизонтальной оси
                if randbool(rndMin, rndMax):    # с помощью функции определяем вероятность "вырастания" дерева
                    self.cells[i][j] = 1    # меняем клетку на 1(дерево) из списка констант CELL_TYPES

    # рандомное дерево
    def generate_tree(self):
        rc = randcell(self.mapX, self.mapY) 
        rx, ry = rc[0], rc[1]
        if (self.cells[ry][rx]) == 0:   # если на клетке поле
            self.cells[ry][rx] = 1     # заменяем его на дерево

    # мастерская
    def upgrade_station(self):
        rc = randcell(self.mapX, self.mapY) 
        rx, ry = rc[0], rc[1]
        self.cells[ry][rx] = 4

    # вертолётная площадка
    def helipad(self):
        rc = randcell(self.mapX, self.mapY) 
        rx, ry = rc[0], rc[1]
        if self.cells[ry][rx] != 4:    # проверяем не занята ли клетка мастерской
            self.cells[ry][rx] = 5
        else:
            self.helipad()

    # заполняем карту реками, водоёмами
    def generate_river(self, mapX, mapY, length = 5):   # вводим размеры карты, длину реки (количество элементов)
        map_size = mapX * mapY
        while map_size > 0:    # создаём реки каждые 50 клеток карты
            rc = randcell(self.mapX, self.mapY)   # вводим размеры карты, метод возвращает рандомные координаты в пределах карты
            rx, ry = rc[0], rc[1]   # присваиваем рандомные координаты переменным
            self.cells[ry][rx] = 2  # меняем клетку по заданным координатам на значение 2(река) из списка констант CELL_TYPES
            length2 =  length
            while length2 - 1 > 0:   # повторяем цикл пока полностью не отработаем длинну реки
                rc2 = randcell2(rx, ry)    # функция для нахождения соседней клетки 
                rx2, ry2 = rc2[0], rc2[1]   # присваиваем координаты соседней клетки переменным
                if self.check_bounds(rx2, ry2):    # проверяем находится ли эта клетка на карте
                    if self.cells[ry2][rx2] != 2:   # проверяем не является ли клетка рекой 
                        self.cells[ry2][rx2] = 2    # меняем клетку по заданным координатам на значение 2(река) из списка констант CELL_TYPES
                        rx, ry = rx2, ry2   # переприсваиваем координаты для следующего цисла
                        length2 -= 1    # если клетка реки создана уменьшаем количество циклов
            map_size -= 50    

    # создаём огонь
    def add_fire(self):
        rc = randcell(self.mapX, self.mapY)
        rx, ry = rc[0], rc[1]
        if self.cells[ry][rx] == 1:    # если на клетке дерево
            self.cells[ry][rx] = 3     # заменяем его на огонь

    # создаём пожар
    def update_fires(self, heli):
        for i in range(self.mapY):
            for j in range(self.mapX):
                if self.cells[i][j] == 3:   # если на клетке огонь
                    self.cells[i][j] = 0    # заменяем его на поле
                    heli.score -= THREE_PENALTY
                    heli.burn_tree += 1
        for k in range(10):    # создаём несколько очагов возгорания
            self.add_fire()

    # функционал вертолёта, забор воды, тушение пожаров
    def process_helicopter(self, heli, clouds):
        wc = self.cells[heli.hy][heli.hx]   # WorkCoordinate
        sc = clouds.cells[heli.hy][heli.hx]    # StormCoordinate
        if wc == 2:
            heli.tank = heli.maxtank
        if wc == 3 and heli.tank > 0:
            heli.tank -= 1
            self.cells[heli.hy][heli.hx] = 1
            heli.score += THREE_REWARD
            heli.save_tree += 1
        if wc == 4 and heli.score >= UPGRADE_COST:
            heli.maxtank += 1
            heli.score -= UPGRADE_COST
        if wc == 5 and heli.score >= HP_COST and heli.hp < heli.maxhp:
            heli.hp += 1
            heli.score -= HP_COST
        if sc == 2:
            heli.hp -= 1
            clouds.cells[heli.hy][heli.hx] = 1 
        if heli.hp == 0 or heli.score < 0:  
            heli.you_dead()    

    # Информация по стоимости апгрейда и ремонта
    def print_info(self):
        print("Вместимость 🔧:", UPGRADE_COST, " | ", "Ремонт 🏥:", HP_COST)

    # собираем карту в словарь для сохранения
    def export_data(self):
        return {"cells":self.cells}
    
    # переприсваиваем карту той что из словаря (сохранения)
    def import_data(self, data):
        self.cells = data["cells"] or [[0 for i in range(self.mapX)] for j in range(self.mapY)]