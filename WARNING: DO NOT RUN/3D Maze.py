import pygame as pg
from pygame.locals import *
import numpy as np

class App:
    def __init__(self):
        """Main application class for running the game.

        This class initializes the Pygame environment and manages the main game loop. 
        It handles events, updates game state, and renders graphics to the window at a consistent frame rate.
        """
        pg.init()

        self.map_num = np.random.randint(0,100)
        self.r = 0
        self.l = 0
        self.lock = [False, False, False, False]
        
        self.windowsize = (1600, 800)
        self.window = pg.display.set_mode(self.windowsize)
        self.clock = pg.time.Clock()

        self.mainloop()

    def mainloop(self):
        """Runs the main loop of the application, handling events and updating the game state.

    This method continuously processes user input, updates the position of the character, 
    draws the game map and character, casts rays for collision detection, and refreshes the display. 
    The loop continues until the application is closed.

    Args:
        None

    Returns:
        None

    Examples:
        app_instance.mainloop()
    """
        running = True
        cords = np.array([400, 400], dtype=np.float64)
        self.lock_cords = np.array([400, 400], dtype=np.float64)
        random_map = np.random.randint(5, size=256)
        while running:
            for event in pg.event.get():
                if event.type == QUIT:
                    running = False
# sourcery skip: merge-nested-ifs
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        cords = np.array([400, 400], dtype=np.float64)
                    if event.key == K_UP:
                        random_map = np.random.randint(5, size=256)
                        self.map_num += 1
                    if event.key == K_DOWN:
                        random_map = np.random.randint(5, size=256)
                        self.map_num -= 1
            cords = movement().move(cords, self.l, self.lock, self.lock_cords)
            hitboxes, mnum = drawmap().draw(self.window, self.map_num, random_map)
            cords, self.lock, self.lock_cords = character().char(self.window, cords, hitboxes, self.lock, self.lock_cords, mnum)
            dist, self.r, self.l, n = rays().cast(self.window, cords, hitboxes, self.r)
            bg(self.window, dist, n)
            pg.display.flip()
            self.clock.tick(45)
        pg.quit()
class drawsquare:
    def draw(self, window, cords, value):
        points = np.array([((cords[0] - 24, cords[1] - 24), (cords[0] - 24, cords[1] + 24), (cords[0] + 24, cords[1] + 24), (cords[0] + 24, cords[1] - 24)), ((cords[0] - 25, cords[1] - 25), (cords[0] - 25, cords[1] + 25), (cords[0] + 25, cords[1] + 25), (cords[0] + 25, cords[1] - 25))])
        if value == 1:
            return pg.draw.polygon(window, pg.Color("white"), points[1])
        pg.draw.polygon(window, pg.Color("black"), points[0])
class drawmap:
    def draw(self, window, map_num, random_map):
        window.fill(pg.Color("dimgray"))
        hitboxes = []
        map = np.array([(
            1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
            1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,
            1,1,1,1,1,1,0,0,1,1,1,0,0,1,0,1,
            1,1,0,0,0,1,0,0,0,0,0,0,1,1,0,1,
            1,0,0,1,0,1,0,0,1,1,1,0,0,1,0,1,
            1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,
            1,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,
            1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,
            1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,1,
            1,0,1,1,0,0,1,1,1,1,0,1,1,1,0,1,
            1,0,0,1,0,0,0,0,0,0,0,1,0,1,0,1,
            1,0,0,0,0,1,1,1,1,0,0,1,0,1,0,1,
            1,0,1,0,0,1,0,0,1,0,0,1,0,1,0,1,
            1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,
            1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
            (
            1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,1,1,1,0,0,0,0,0,0,1,1,1,0,1,
            1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,
            1,0,1,0,1,1,1,0,0,1,1,1,0,1,0,1,
            1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,
            1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,
            1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,
            1,0,1,0,1,1,1,0,0,1,1,1,0,1,0,1,
            1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,
            1,0,1,1,1,0,0,0,0,0,0,1,1,1,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
            (
            1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
            (
            1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,1,0,0,1,1,0,1,1,0,0,0,0,0,1,
            1,0,1,0,1,0,0,1,0,0,1,0,0,0,0,1,
            1,0,1,0,1,0,0,0,0,0,1,0,0,0,0,1,
            1,0,1,0,0,1,0,0,0,1,0,0,0,0,0,1,
            1,0,1,0,0,0,1,0,1,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,1,0,0,0,0,0,1,0,1,1,1,0,1,
            1,0,1,1,0,0,0,0,1,0,0,1,0,1,0,1,
            1,0,0,1,0,0,0,1,0,0,0,1,0,1,0,1,
            1,0,1,1,1,0,1,0,0,0,0,1,1,1,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
            random_map
            ])
        m = 0
        x = 25
        y = 25
        map_num = map_num % len(map)
        for _ in range(16):
            for _ in range(16):
                if rect := drawsquare().draw(window, (x, y), map[map_num][m]):
                    hitboxes.append(rect)
                x += 50
                m += 1
            x = 25
            y += 50
        return hitboxes, map_num

class character:
    def char(self, window, cords, hitboxes, lock, lock_cords, mnum):
        self.cords = cords
        self.lock = lock
        self.lock_cords = lock_cords
        if mnum == 4:
            self.cords[0] = max(self.cords[0], 5)
            self.cords[1] = max(self.cords[1], 5)
            self.cords[0] = min(self.cords[0], 795)
            self.cords[1] = min(self.cords[1], 795)
        elif max(self.cords[0], 5) == 5 or max(self.cords[1], 5) == 5 or min(self.cords[0], 795) == 795 or min(self.cords[1], 795) == 795:
            self.cords = np.array([400, 400], dtype=np.float64)
        self.rect = pg.draw.circle(window, pg.Color("red"), self.cords, 5)
        if collisions := self.rect.collideobjectsall(hitboxes):
            for self.collision in collisions:
                self.check_right()
                self.check_left()
                self.check_top()
                self.check_bottom()
        else:
            self.lock = [False, False, False, False]
        return self.cords, self.lock, self.lock_cords
    def check_right(self):
        if self.collision.left <= self.rect.right and self.rect.centery <= self.collision.bottom and self.rect.centery >= self.collision.top and self.collision.centerx > self.rect.right:
            self.cords[0] = self.collision.left - 4
            self.lock[0] = True
            self.lock_cords[0] = self.cords[0]
        else:
            self.lock[0] = False
    def check_left(self):
        if self.collision.right >= self.rect.left and self.rect.centery <= self.collision.bottom and self.rect.centery >= self.collision.top and self.collision.centerx < self.rect.left:
            self.cords[0] = self.collision.right + 4
            self.lock[1] = True
            self.lock_cords[0] = self.cords[0]
        else:
            self.lock[1] = False
    def check_top(self):
        if self.collision.bottom >= self.rect.top and self.rect.centerx <= self.collision.right and self.rect.centerx >= self.collision.left and self.collision.centery < self.rect.top:
            self.cords[1] = self.collision.bottom + 4
            self.lock[2] = True
            self.lock_cords[1] = self.cords[1]
        else:
            self.lock[2] = False
    def check_bottom(self):
        if self.collision.top <= self.rect.bottom and self.rect.centerx <= self.collision.right and self.rect.centerx >= self.collision.left and self.collision.centery > self.rect.bottom:
            self.cords[1] = self.collision.top - 4
            self.lock_cords[1] = self.cords[1]
            self.lock[3] = True
        else:
            self.lock[3] = False
class movement:
    def move(self, cords, l, lock, lock_cords):
        keys = pg.key.get_pressed()
        s = 2
        if keys[K_w]:
            cords[1] += s * np.sin(l)
            cords[0] += s * np.cos(l)
        if keys[K_s]:
            cords[1] -= s * np.sin(l)
            cords[0] -= s * np.cos(l)
        if keys[K_a]:
            cords[1] -= s * np.cos(l)
            cords[0] += s * np.sin(l)
        if keys[K_d]:
            cords[1] += s * np.cos(l)
            cords[0] -= s * np.sin(l)
        if True in lock:
            if lock[0] and cords[0] > lock_cords[0]:
                cords[0] = lock_cords[0]
            if lock[1] and cords[0] < lock_cords[0]:
                cords[0] = lock_cords[0]
            if lock[2] and cords[1] < lock_cords[1]:
                cords[1] = lock_cords[1]
            if lock[3] and cords[1] > lock_cords[1]:
                cords[1] = lock_cords[1]
        return cords
class rays:
    def cast(self, window, cords, hitboxes, r):
        n = 400
        fov = 3
        directions = np.arange(0, np.pi / fov, np.pi / (n * fov))
        dist = [(0, "") for _ in range(n)]
        pos = []
        keys = pg.key.get_pressed()
        if keys[K_RIGHT]:
            r += 0.04
        if keys[K_LEFT]:
            r -= 0.04
        l = np.pi / (fov * 2) + r
        for a in directions:
            y = np.sin(a + r) * 800 + cords[1]
            x = np.cos(a + r) * 800 + cords[0]
            pos.append((x, y))
        for index, p in enumerate(pos):
            for hitbox in hitboxes:
                if hitbox.clipline(cords, p):
                    start, end = hitbox.clipline(cords, p)
                    p = start
            rect = pg.Rect(0, 0, 800, 800)
            stuffing, p = rect.clipline(cords, p)
            c = "green" if p[1] % 50 == 0 else "darkgreen"
            dist[index] = ((cords[0] - p[0]) ** 2 + (cords[1] - p[1]) ** 2, c)
            pg.draw.aaline(window, pg.Color(c), cords, p)
        return dist, r, l, n
class bg:
    def __init__(self, window, dist, n):
        rect = pg.Rect(800, 0, 800, 400)
        pg.draw.rect(window, pg.Color("blue"), rect)
        x = 800 / len(dist)
        player_height = 2
        for _ in range(len(dist)):
            h = 1 / np.sqrt(dist[_][0]) * 35000
            pg.draw.line(window,
                            dist[_][1],
                            (x * _ + 800, 400 - h/player_height),
                            (x * _ + 800, 400 + h/player_height),
                            width= 800 // n
                            )
if __name__ == "__main__":
    App()
