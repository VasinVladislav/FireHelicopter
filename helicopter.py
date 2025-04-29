from utils import randcell
import os

# Создаём вертолёт
class Helicopter:

    # Инициальзируем класс вертолёт, вводим размер карты
    def __init__(self, mapX, mapY):
        rc = randcell(mapX, mapY)   # появляемся в рандомном месте в пределах карты
        rx, ry = rc[0], rc[1]
        self.mapX, self.mapY = mapX, mapY   # призваиваем размеры карты переменным внутри нашего класса т.к. они нам понадобятся в будущем 
        self.hx, self.hy = rx, ry   # наши координаты вертолёта
        self.tank = 0   # количество воды в баке
        self.maxtank = 1    # вместимость бака с водой
        self.score = 0     # очки за тушение/сгорание дерева
        self.hp = 2    # количество жизней
        self.maxhp = 3     # максимальное здоровье
        self.save_tree = 0     # спасённые деревья
        self.burn_tree = 0     # потерянные деревья
        
    # функция перемещения вертолёта
    def move(self, dx, dy):    # принемает на вход координаты смещения (вверх вниз влево вправо)
        nx = self.hx + dx   # получаем новые координаты
        ny = self.hy + dy
        if (0 <= nx < self.mapX) and (0 <= ny < self.mapY):  # если новые координаты не выходят за приделы карты...
            self.hx = nx    # ...то переприсваеваем старые координаты вертолёта новыми
            self.hy = ny

    # информационный блок
    def print_stats(self):        
        print("💧 ", self.tank, "/ ", self.maxtank, sep = "", end = " | ")
        print("🏆 ", self.score, sep = "", end = " | ")
        print("❤️" * self.hp, end = "")
        print("🖤" * (self.maxhp - self.hp), end = " | ")
        print("Сохранение: R | Загрузка: G")

    # "Экран смерти"
    def you_dead(self):
        print("⬛" * 13)
        print("⬛", "ИГРА ОКОНЧЕНА") 
        print("⬛", "критические повреждения") if self.hp == 0 else print("⬛", "плохая результативность")
        print("⬛" * 13)   
        print("⬛", "Спасено деревьев 🌳:", self.save_tree)
        print("⬛", "Сгорело деревьев 🔥:", self.burn_tree)
        print("⬛" * 13)
        if self.score > 0:
            print("⬛","Итоговые очки 🏆:", self.score)
            print("⬛" * 13)          
        exit(0)    # завершаем программу
 
    # собираем данные в словарь для сохранения
    def export_data(self):
        return {
            "score": self.score, "save_tree": self.save_tree, "burn_tree": self.burn_tree,
            "hp":  self.hp,
            "hx": self.hx, "hy": self.hy,
            "tank": self.tank, "maxtank": self.maxtank
            }
    
    # переприсваиваем данные из словаря (сохранения)
    def import_data(self, data):
        self.hx = data["hx"] or 0
        self.hy = data["hy"] or 0
        self.hp = data["hp"] or 2
        self.tank = data["tank"] or 0
        self.maxtank = data["maxtank"] or 1
        self.score = data["score"] or 0
        self.save_tree = data["save_tree"] or 0
        self.burn_tree = data["burn_tree"] or 0