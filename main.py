from map import Map
from helicopter import Helicopter
import time
import os
import math
import json
import platform
from pynput import keyboard
from clouds import Clouds

MAP_X, MAP_Y = 25, 15   # размер карты задаётся здесь
TICK_SLEEP = 0.01    # "fps"

# экземпляры наших классов
map = Map(MAP_X, MAP_Y)
heli = Helicopter(MAP_X, MAP_Y)
clouds = Clouds(MAP_X, MAP_Y)

# управление с клавиатуры
# координаты смещения в зависимости от нажатой клавиши
MOVES_EN = {'w': (-1, 0), 'd': (0, 1), 's': (1, 0), 'a': (0, -1)}
MOVES_RU = {'ц': (-1, 0), 'в': (0, 1), 'ы': (1, 0), 'ф': (0, -1)}

# функция для обработки нажатия клавиш
def key_control(key):
    global heli, clouds, map, tick
    try:
        
        c = key.char.lower()    # переводим нажатую клавишу к единому стандарту
        if c in MOVES_EN.keys():
            dx, dy = MOVES_EN[c][1], MOVES_EN[c][0]     # в зависимости от нажатой клавиши выибираем ключ в словаре MOVES и присваиваем значение координатам смещения вертолёта
            heli.move(dx, dy)
        elif c in MOVES_RU.keys():
            dx, dy = MOVES_RU[c][1], MOVES_RU[c][0]
            heli.move(dx, dy)
        
        elif c == 'r' or c == 'к':      # кнопка сохранения
            # словарь хранит в себе функции export(функция хранит словарь с игровыми данными)
            data = {"helicopter": heli.export_data(), "clouds": clouds.export_data(), "map": map.export_data(), "tick": tick}   
            with open("level.json", "w") as lvl:    # функция для записи в файл
                json.dump(data, lvl)    # запись data в lvl(level.json)
        
        elif c == 'g' or c == 'п':      # кнопка загрузки
            with open("level.json", "r") as lvl:    # функция для чтения
                data = json.load(lvl)   # переприсваиваем данные из файла lvl(level.json) в data
                tick = data["tick"] or 1
                heli.import_data(data["helicopter"])
                clouds.import_data(data["clouds"])
                map.import_data(data["map"])
    
    except AttributeError:     # Игнорирует случайные нажатия
        pass

listener = keyboard.Listener(on_press=None, on_release=key_control)
listener.start()

tick = 1
diferent = 1 / TICK_SLEEP   # введена для компенсации влияния быстроты тиков на геймплей
thee_update = math.ceil(10 * diferent / ((MAP_X * MAP_Y) / 100))
fire_update = 10 * diferent
cloud_update = 15 * diferent
clouds.update_clouds()  # добавляет облака с самого начала игры, дальнейшее обновление будет в цикле

def clear_screen():
    # Определяем операционную систему
    if platform.system() == "Windows":
        os.system("cls")  # Для Windows
    else:
        os.system("clear")  # Для Unix-подобных систем (Linux, macOS)

# работа программы
while True:
    clear_screen() 
    # print("TICK", tick)
    map.process_helicopter(heli, clouds)
    map.print_info()
    heli.print_stats()
    map.print_map(heli, clouds)
    tick += 1
    time.sleep(TICK_SLEEP)
    if (tick % thee_update) == 0:
        map.generate_tree()
    if (tick % fire_update) == 0:
        map.update_fires(heli)
    if (tick % cloud_update) == 0:
        clouds.update_clouds()  
    clear_screen()       