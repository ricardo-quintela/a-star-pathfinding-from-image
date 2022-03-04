from player import *
from node import *
from interface import *
from settings import *
import pygame
import tkinter as tk
from tkinter import filedialog
from PIL import Image

vector2 = pygame.Vector2

class game:
    def __init__(self):
        info = pygame.display.Info()
        self.screenres = vector2(info.current_w, info.current_h)
        (self.w, self.h) = SIZE
        self.center = vector2(self.w / 2, self.h / 2)
        self.win = pygame.display.set_mode(SIZE)
        pygame.display.set_caption(TITLE)



        # main variables
        self.clock = pygame.time.Clock()

        # !MENU
        self.inMain = True
        self.menu_sprites = pygame.sprite.Group()
        self.play = Button(x=self.center[0], y=self.center[1], color=orange, text='Import')
        self.menu_sprites.add(self.play)

        # !Gaem
        self.inGame = True
        self.game_sprites = pygame.sprite.Group()

        #player

        self.player = Player()
        self.game_sprites.add(self.player)
        self.call_coords = self.player.rect.center
        self.path = []

        player_coords = self.player.rect.center




    def events(self):
        #checks for window events and key presses
        self.mouse_click = False
        
        for event in pygame.event.get():
            #quit
            if event.type == pygame.QUIT:
                self.inMain = False
                self.inGame = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_click = True

##############################
#      general functions
##############################
    def mouse(self):
        #returns mouse pos
        m = pygame.mouse.get_pos()
        return m[0], m[1]

    def center_coords(self, object, coords):
        #returns the coordinates of an object correctly centered with the given coordinates
        obj_size = object.rect.width, object.rect.height
        return coords[0] - obj_size[0] / 2, coords[1] - obj_size[1]

    def calculate_cell(self, coords):
        #calculates the current code center
        return [coords[0] // 30 * 30 + 15, coords[1] // 30 * 30 + 15]


    ##############################
    #   create the map matrixes
    ##############################
    def read_level(self, image):
        map =[]
        #reads the level file and returns a tilemap matrix
        for y in range(image.height):
            line = []
            for x in range(image.width):
                r,g,b = image.getpixel((x,y))
                if not r and not g and not b:
                    line.append("1")
                else:
                    line.append("0")
            map.append(line)
        return map



    def create_map(self, tilemap):
        #iterates from the tilemap matrix and creates an image for optimized rendering
        playerset = False
        call_coords_set = False
        for line in range(len(tilemap)):
            for node in range(len(tilemap[line])):
                if (line == 0 or line == len(tilemap) - 1) or (node == 0 or node == len(tilemap[line]) - 1):
                    if tilemap[line][node] == "0":
                        if not playerset:
                            self.player.setpos(node * tilesize, line * tilesize)
                            playerset = True
                        else:
                            self.call_coords = self.calculate_cell((node * tilesize, line * tilesize))
                            call_coords_set = True
                            break
            if call_coords_set:
                break
                            

                

        map_surface = pygame.Surface(SIZE)
        map_surface.fill(white)

        for y in range(len(tilemap)):
            for x in range(len(tilemap[y])):
                if tilemap[y][x] == "1":
                    pygame.draw.rect(map_surface, black, (x*tilesize, y*tilesize, tilesize, tilesize))

        return map_surface

    def add_colliders(self, tilemap):
        # iterates from the tilemap and creates a list with the tile individual hitboxes
        colliders = []
        for y in range(len(tilemap)):
            for x in range(len(tilemap[y])):
                if tilemap[y][x] == "1":
                    hitbox = pygame.Rect(x * tilesize, y * tilesize, tilesize, tilesize)
                    colliders.append(hitbox)
        coords = [list(coord.center) for coord in colliders]
        return colliders, coords


    ################################
    #PATHFINDING
    ################################
    def create_path(self, last_node):
        # generates a list with the coordinates of all parents of the end node
        node = last_node
        path = [node.coords]
        while node.parent != 'NULL':
            path.append(node.parent.coords)
            node = node.parent
        return path[::-1]

    def pathfind(self, start_pos, end_pos, tilemap):
        # algorithm to find a path to the given node

        open = [Node(start_pos, start_pos, end_pos)]
        closed = []

        while True:
            self.clock.tick()
            Fcosts = [node.Fcost for node in open]
            current = open[Fcosts.index(min(Fcosts))]

            open.pop(open.index(current))
            closed.append(current.coords)

            test = current.coords, current.Fcost

            if current.coords == end_pos:
                print("Caminho encontrado.")
                return self.create_path(current)

            current.neighbors = current.calculate_neigbors(current.coords)
            for neighbor in current.neighbors:
                if (neighbor.coords in tilemap or neighbor.coords in closed):
                    continue
                if neighbor not in open:
                    neighbor.parent = current
                    open.append(neighbor)







    ##############################
    #           GaEm
    ##############################
    def update_game(self, map):
        #updates the game window
        self.win.blit(map, (0,0))
        
        self.game_sprites.update()
        self.game_sprites.draw(self.win)

        pygame.draw.rect(self.win, green, (self.call_coords[0] - tilesize / 2, self.call_coords[1] - tilesize / 2, tilesize, tilesize))

        pygame.display.update()


    def gameloop(self, converted):
        # create the map
        tilemap = self.read_level(converted)
        map = self.create_map(tilemap)
        colliders, wall_coords = self.add_colliders(tilemap)

        # pathfinding variables
        index = 0

        if self.call_coords not in wall_coords:
            index = 0
            self.path = self.pathfind(self.calculate_cell(self.player.rect.center), self.call_coords, wall_coords)
            self.path.append(self.call_coords)

        #runs the main game loop
        while self.inGame:
            self.events()
            self.clock.tick(FPS)

        
            # player movement
            if self.mouse_click:
                self.call_coords = self.calculate_cell(self.mouse())
                player_coords = self.calculate_cell(self.player.rect.center)

                if self.call_coords not in wall_coords:
                    index = 0
                    self.path = self.pathfind(player_coords, self.call_coords, wall_coords)
                    self.path.append(self.call_coords)

            if index != len(self.path) and len(self.path) != 0:
                move = self.player.movement(self.path[index])
                index += 1 if move else 0


            self.update_game(map)


##############################
#           MENU
##############################
    def update_menu(self):
        #updates the menu screen
        self.win.fill(light_gray)

        
        self.menu_sprites.update()
        self.menu_sprites.draw(self.win)

        pygame.display.update()

    def mainloop(self):
        #runs the mainloop
        while self.inMain:
            self.events()
            self.clock.tick(FPS)

            self.play.rect.topleft = self.center_coords(self.play, self.center)
            if self.play.click(self.mouse(), self.mouse_click):
                start = False
                try:
                    root = tk.Tk()
                    path = filedialog.askopenfilename(title='Import image', filetypes=(("PNG Files", "*.png"),("JPEG Files", "*.jpg"),("All Files", "*.*")))
                    root.destroy()
                    image = Image.open(path)
                    converted = image.convert("RGB")
                    start = True
                except:
                    start = False
                if start:
                    self.inGame = True
                    self.gameloop(converted)

            self.update_menu()

pygame.init()


g = game()
g.mainloop()

pygame.quit()
