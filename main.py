import time
import os
import msvcrt
from random import randint


class Snake:

    def __init__(self, x, y):
        self.parts = [[1, 1]]
        self.length = 1
        self.dir = 'd'
        self.skins = ['O']
        self.fruit = [randint(2, x), randint(2, y)]
        self.size = [x, y]
        self.print_in_coords()

    def get_opposites(self):
        return {"w": "s", "s": "w", "d": "a", "a":"d"}

    def set_skins(self):
        skins = ['O']
        coords_subtraction = lambda a, b: [x1 - x2 for (x1, x2) in zip(a, b)]
        for i in range(1, len(self.parts)):
            if i == len(self.parts)-1:
                a = self.parts[-2]
                b = self.parts[-1]
            else:
                b = self.parts[i+1]
                a = self.parts[i-1]
            diff = coords_subtraction(a, b)
            if diff[0] == 0:
                skins.append('│')
            elif diff[1] == 0:
                skins.append('─')
            else:
                a = self.parts[i-1]
                b = self.parts[i]
                diff2 = coords_subtraction(a, b)
                if sum(diff) == 0:
                    if sum(diff2) == 1:
                        skins.append('└')
                    else:
                        skins.append('┐')
                else:
                    if diff2[1] == -1 or diff2[0] == 1:
                        skins.append('┌')
                    else:
                        skins.append('┘')

            self.skins = skins

    def print_in_coords(self):
        coords = self.parts
        os.system('cls')
        for i in range(self.size[1], 0, -1):
            for j in range(1, self.size[0]+1):
                if [j, i] in coords:
                    print(self.skins[coords.index([j, i])], end=' ')
                elif [j, i] == self.fruit:
                    print('X', end=' ')
                else:
                    print('·', end=' ')
            print('')

    def update_coors(self):

        for i in range(len(self.parts)-1, 0, -1):
            self.parts[i] = self.parts[i-1][:]

        if self.dir == 'w':
            self.parts[0][1] += 1
        elif self.dir == 'd':
            self.parts[0][0] += 1
        elif self.dir == 's':
            self.parts[0][1] -= 1
        elif self.dir == 'a':
            self.parts[0][0] -= 1

    def check_fruit(self):
        if self.parts[0] == self.fruit:
            self.grow()
            self.generate_fruit()

    def alive(self):
        head = self.parts[0]
        if (head in self.parts[1:]) or (not(0 < head[0] <= self.size[0])) or (not(0 < head[1] <= self.size[1])):
            return False
        return True

    def get_action(self, character):
        if (character in 'wasd') and (self.get_opposites()[character] != self.dir or len(self.parts) == 1):
            self.dir = character
        self.update_coors()
        self.check_fruit()
        self.set_skins()
        self.print_in_coords()
        return self.alive()

    def generate_fruit(self):
        new_coords = [randint(1,self.size[0]), randint(1,self.size[1])]
        if new_coords in self.parts:
            self.generate_fruit()
        else:
            self.fruit = new_coords

    def grow(self):
        if len(self.parts) > 1:
            last = self.parts[-1]
            sec_last = self.parts[-2]
            diff = [x1 - x2 for (x1, x2) in zip(sec_last, last)]
            if diff[0] == 0:
                if diff[1] > 0:
                    self.parts.append([last[0], last[1]-1])
                else:
                    self.parts.append([last[0], last[1]+1])
            elif diff[0] > 0:
                self.parts.append([last[0]-1, last[1]])
            else:
                self.parts.append([last[0]+1, last[1]])
        else:
            head = self.parts[0]
            if self.dir == 'w':
                self.parts.append([head[0], head[1]-1])
            elif self.dir == 'd':
                self.parts.append([head[0]-1, head[1]])
            elif self.dir == 's':
                self.parts.append([head[0], head[1]+1])
            elif self.dir == 'a':
                self.parts.append([head[0]+1, head[1]])
        self.length += 1


def main():
    snake = Snake(15, 10)
    update_time = .125
    keep_playing = True
    while keep_playing:
        t = 0
        key_stroke = b' '
        while t < update_time:
            start = time.time()
            if msvcrt.kbhit():
                key_stroke = msvcrt.getch()
            end = time.time()
            t += end - start

        keep_playing = snake.get_action(key_stroke.decode('utf-8'))
    print('Score:', snake.length)
    while True:
        again = input('Keep playing? (y/n)')
        if again.lower() == 'y':
            main()
            break
        elif again.lower() == 'n':
            print('Bye')
            break
        else:
            print('Input a valid answer')


if __name__ == "__main__":
    main()
