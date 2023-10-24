from heapq import *
import pygame as pg
from PIL import Image

c, p, X, Y = 16, 17, 2, 15
maze = ['%%%%%%%%%%%%%%%%',
        '%# @    ----#--%',
        '%#****#*    #  %',
        '%#****#* #% # %%',
        '%#    #* #  #  %',
        '%#    #* #%%#%%%',
        '%#%%%*#* #  #  %',
        '%#       #* #  %',
        '%#          #  %',
        '%#          #  %',
        '%#****#%%%**#%%%',
        '%#**  #   * #  %',
        '%#    #   # #  %',
        '%# * %#%**%%#%%%',
        '%#    #     #  %',
        '%#    #     #  %',
        '%%%%%%%%%%%%%%%%']

class Program:

    weights =   {
#             direction | start | end     :   time
            ( "D",        " ",    " " )   :   1,
            ( "L",        " ",    " " )   :   1,
            ( "R",        " ",    " " )   :   1,
            ( "L",        "-",    "-" )   :   1,
            ( "R",        "-",    "-" )   :   1,
            ( "D",        "-",    " " )   :   1,
            ( "L",        "-",    " " )   :   1,
            ( "R",        "-",    " " )   :   1,
            ( "L",        " ",    "-" )   :   1,
            ( "R",        " ",    "-" )   :   1,
            ( "U",        "#",    "#" )   :   100,
            ( "D",        "#",    "#" )   :   1,
            ( "L",        "#",    " " )   :   1,
            ( "U",        "#",    " " )   :   1,
            ( "R",        "#",    " " )   :   1,
            ( "L",        " ",    "#" )   :   1,
            ( "R",        " ",    "#" )   :   1,
            ( "D",        " ",    "#" )   :   1,
            ( "L",        "#",    "-" )   :   1,
            ( "R",        "#",    "-" )   :   1,
            ( "L",        "-",    "#" )   :   1,
            ( "R",        "-",    "#" )   :   1,
            ( "D",        " ",    "@" )   :   1,
            ( "L",        " ",    "@" )   :   1,
            ( "R",        " ",    "@" )   :   1,
            ( "L",        "-",    "@" )   :   1,
            ( "R",        "-",    "@" )   :   1,
            ( "D",        "-",    "@" )   :   1,
            ( "L",        "#",    "@" )   :   1,
            ( "R",        "#",    "@" )   :   1
            }
    
    def __init__(self, labyrinth, weights):
        graph = {}

        for y in range(1, len(labyrinth)-1):
            for x in range(1, len(labyrinth[y])-1):
                start = labyrinth[y][x]
                graph[x,y] = []
                start_bottom = labyrinth[y+1][x]
                

                try:
                    direction = "D"
                    end = labyrinth[y+1][x]
                    time = weights[direction, start, end]
                    graph[x,y].append([(x, y+1), time])
                except:
                    pass

                try:
                    direction = "U"
                    end = labyrinth[y-1][x]
                    if (start == " " and start_bottom == " "):
                        pass
                    else: 
                        time = weights[direction, start, end]
                        graph[x,y].append([(x, y-1), time])
                except:
                    pass
                
                

                try:
                    direction = "L"
                    end = labyrinth[y][x-1]
                    end_bottom = labyrinth[y+1][x-1]
                    if (start == " " and start_bottom == " "):
                        pass
                    else: 
                        time = weights[direction, start, end]
                        graph[x,y].append([(x-1, y), time])
                except:
                    pass

                try:
                    direction = "R"
                    end = labyrinth[y][x+1]
                    end_bottom = labyrinth[y+1][x+1]
                    if (start == " " and start_bottom == " "):
                        pass
                    else:          
                        time = weights[direction, start, end]
                        graph[x,y].append([(x+1, y), time])
                except:
                    pass
                            
                # print((x, y), graph[x,y])
                x = x + 1
            
            
            y = y + 1

        self.graph = graph

    def find_chest(labyrinth):

        for y in range(1, len(labyrinth) - 1):
            for x in range(1, len(labyrinth[y]) - 1):
                if labyrinth[y][x] == "@":
                    return (x, y)

    def get_neighbors(self, v):
        return self.graph[v]

    def h(self, n, goal):
        return abs(n[0] - goal[0]) + abs(n[1] - goal[1])

    def a_star_algorithm(self, start_node, stop_node):
        open_list = set([start_node])
        closed_list = set([])

        g = {}

        g[start_node] = 0

        parents = {}
        parents[start_node] = start_node

        while len(open_list) > 0:
            n = None

            for v in open_list:
                if n == None or g[v] + self.h(v, stop_node) < g[n] + self.h(n, stop_node):
                    n = v;

            if n == None:
                print('Path does not exist!')
                return None

            if n == stop_node:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start_node)

                reconst_path.reverse()

                return reconst_path

            for (m, weight) in self.get_neighbors(n):
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

    def backtrace(parent, start, end):
        path = [end]
        while path[-1] != start:
            path.append(parent[path[-1]])
        path.reverse()
        return path
            
    def bfs(self, start, end):
        parent = {}
        queue = []
        queue.append(start)
        while queue:
            node = queue.pop(0)
            if node == end:
                return Program.backtrace(parent, start, end)
            for adjacent in self.graph.get(node, []):
                if node not in queue :
                    parent[adjacent[0]] = node # <<<<< record its parent 
                    queue.append(adjacent[0])

    def path_counter(path):
        pressed_buttons = ""
        all_weight = 0
        for i in range(len(path)-1):
            x = path[i][0]
            y = path[i][1]
            next_x = path[i+1][0]
            next_y = path[i+1][1]

            start = maze[y][x]
            end = maze[next_y][next_x]
            
            if(x - next_x == -1):
                direction = 'R'
            if(x - next_x == 1):
                direction = 'L'
            if(y - next_y == -1):
                direction = 'D'
            if(y - next_y == 1):
                direction = 'U'

            pressed_buttons += direction
            # print(Program.weights[direction, start, end])
            all_weight += Program.weights[direction, start, end]


        return [pressed_buttons, all_weight]

    def bg_image(maze, c, p):
        img = Image.new('RGBA', (50*c, 50*p)) # (256, 256*3) - размер полотна, соответственно ширина,высота. 'white' - цвет background'a.

        chest = Image.open('textures/chest.png')
        rope = Image.open('textures/rope.png')
        brick = Image.open('textures/brick-wall.png')
        wood = Image.open('textures/wood-wall.png')
        ladder = Image.open('textures/ladder.png')


        for i in range(len(maze)):
            for j in range(len(maze[i])):

                if maze[i][j] == '#':
                    img.paste(ladder, (50*j, 50*i))

                if maze[i][j] == '@':
                    img.paste(chest, (50*j, 50*i))
                    
                if maze[i][j] == '*':
                    img.paste(wood, (50*j, 50*i))

                if maze[i][j] == '%':
                    img.paste(brick, (50*j, 50*i))

                if maze[i][j] == '-':
                    img.paste(rope, (50*j, 50*i))

                j += 1

            i += 1
                
        img.save("out.png")

    def get_circle(x, y, TILE):
        return (x * TILE + TILE // 2, y * TILE + TILE // 2), TILE // 6

    def draw(a_star_path, bfs_path, maze, c, p):
        try:
            a_star_pressed_buttons, a_star_all_weight = Program.path_counter(a_star_path)
            print(a_star_all_weight, a_star_path, sep=" ", end='\n')
            print(a_star_pressed_buttons, end='\n')
            
            bfs_pressed_buttons, bfs_all_weight = Program.path_counter(bfs_path)
            print(bfs_all_weight, bfs_path, sep=" ", end='\n')
            print(bfs_pressed_buttons, end='\n')
            Program.bg_image(maze, c, p)

            common_coords = []
            for i in a_star_path:
                if i in bfs_path:
                    common_coords.append(i)
                    
            TILE = 50
            pg.init()
            sc = pg.display.set_mode([c * TILE, p * TILE])
            pg.display.set_caption("Game")
            clock = pg.time.Clock()
            bg = pg.image.load('out.png')
            bg = pg.transform.scale(bg, (c * TILE, p * TILE))

            while True:

                sc.blit(bg, (0, 0))
                for coords in bfs_path:
                    pg.draw.circle(sc, pg.Color('blue'), *Program.get_circle(*coords, TILE))
                for coords in a_star_path:
                    pg.draw.circle(sc, pg.Color('red'), *Program.get_circle(*coords, TILE))
                
                for coords in common_coords:
                    pg.draw.circle(sc, pg.Color('blue'), *Program.get_circle(*coords, TILE), False, False, True, True)

                pg.draw.circle(sc, pg.Color('magenta'), *Program.get_circle(*(bfs_path[0]), TILE))
                pg.draw.circle(sc, pg.Color('magenta'), *Program.get_circle(*(bfs_path[-1:][0]), TILE))
                
                [exit() for event in pg.event.get() if event.type == pg.QUIT]
                pg.display.flip()
                clock.tick(30)
        except:
            pass
    
start = X, Y
end = Program.find_chest(maze)
# end = 14,15
game = Program(maze, Program.weights)
a_star_path = game.a_star_algorithm(start, end)
bfs_path = game.bfs(start, end)

Program.draw(a_star_path, bfs_path, maze, c, p)
