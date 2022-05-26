'''
'
'
'
'       FUNÇÕES AUXILIARES
'
'
'
'
'''

WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
X, Y = 0, 1

class NODE:
    def __init__(self):
        self.set = '0'
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None

    def __str__(self):
        return str(self.set)

def createEdgeList(width, height):
    edge_list = []
    for y in range(height):
        for x in range(width):
            if x > 0: #tem aresta na esquerda
                #LEFT
                edge_a = (x - 1, y)
                edge_b = (x, y)
                edge_list.append((edge_a, edge_b))

            if x < width - 2: #tem aresta na direita
                #RIGHT
                edge_a = (x, y)
                edge_b = (x + 1, y)
                edge_list.append((edge_a, edge_b))

            if y > 0: #tem aresta pra cima
                #UP
                edge_a = (x, y - 1)
                edge_b = (x, y)
                edge_list.append((edge_a, edge_b))

            if y < height - 2: #tem aresta pra baixo
                #DOWN
                edge_a = (x, y)
                edge_b = (x, y + 1)
                edge_list.append((edge_a, edge_b))
    
    return edge_list

def printGrid(grid):
    for l in grid:
        for cell in l:
            print(cell, end=', ')
        print("")

def drawBoard(grid):
    #desenha tudo
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell.bottom != 1:
                drawBottom(x, y, WHITE)
            if cell.right != 1:
                drawRight(x, y, WHITE)

'''
'
'
'
'       FUNÇÃO PRINCIPAL
'
'
'
'
'''

# Import and initialize the pygame library
import pygame, random
pygame.init()

def drawTop(x, y, color, offset_x=0,offset_y=0):
    pygame.draw.rect(screen, color, pygame.Rect(x * 32 + offset_x, y * 32 + offset_y, 32 - offset_x, 1 - offset_y))

def drawLeft(x, y, color, offset_x=0,offset_y=0):
    pygame.draw.rect(screen, color, pygame.Rect(x * 32 + offset_x, y * 32 + offset_y, 1 - offset_x, 32 - offset_y))

def drawBottom(x, y, color, offset_x=0,offset_y=0):
    pygame.draw.rect(screen, color, pygame.Rect(x * 32 + offset_x, (y + 1) * 32 + offset_y, 32 - offset_x, 1 - offset_y))

def drawRight(x, y, color, offset_x=0,offset_y=0):
    pygame.draw.rect(screen, color, pygame.Rect((x + 1) * 32 + offset_x, y * 32 + offset_y, 1 - offset_x, 32 - offset_y))

# Set up the drawing window
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# criando grid 2D
width, height = (WIDTH // 32, HEIGHT // 32)
grid = [[NODE() for i in range(width)] for j in range(height)]

edge_list = createEdgeList(width, height)
#random.seed(42)
random.shuffle(edge_list)

clock = pygame.time.Clock()
running = True
it = 0

printGrid(grid)

countSet = 1
while running:
    #apertou fechar ou apertou ESC?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Fill the background with black
    screen.fill((0, 0, 0))

    #check if exists empty set
    flag = True
    for l in grid:
        for cell in l:
            if cell.set == '0':
                flag = False

    #não terminou?
    if flag == False:

        #monta uma peça do labirinto
        edge = edge_list.pop(0)
        node_a, node_b = edge[0], edge[1]
        print("aresta:", edge)
        print("a:", node_a)
        print("b:", node_b)
        print(node_a[X] - node_b[X], node_a[Y] - node_b[Y])
        print("-----------")

        if grid[node_a[Y]][node_a[X]].set == '0' and grid[node_b[Y]][node_b[X]].set == '0':
            grid[node_a[Y]][node_a[X]].set = str(countSet)
            grid[node_b[Y]][node_b[X]].set = str(countSet)
            countSet+=1

            if node_a[X] - node_b[X] == -1: #esquerda pra direita
                grid[node_a[Y]][node_a[X]].right = 1
                grid[node_b[Y]][node_b[X]].left = 1

            if node_a[Y] - node_b[Y] == -1: #cima pra baixo
                grid[node_a[Y]][node_a[X]].bottom = 1
                grid[node_b[Y]][node_b[X]].top = 1
        else:
            if grid[node_a[Y]][node_a[X]].set == '0': #node_b já está no grafo
                grid[node_a[Y]][node_a[X]].set = grid[node_b[Y]][node_b[X]].set
                if node_a[Y] - node_b[Y] == -1: #cima pra baixo
                    grid[node_a[Y]][node_a[X]].bottom = 1
                    grid[node_b[Y]][node_b[X]].top = 1

                if node_a[X] - node_b[X] == -1: #esquerda pra direita
                    grid[node_a[Y]][node_a[X]].right = 1
                    grid[node_b[Y]][node_b[X]].left = 1

            elif grid[node_b[Y]][node_b[X]].set == '0': #node_a já está no grafo
                grid[node_b[Y]][node_b[X]].set = grid[node_a[Y]][node_a[X]].set
                if node_a[Y] - node_b[Y] == -1: #cima pra baixo
                    grid[node_a[Y]][node_a[X]].bottom = 1
                    grid[node_b[Y]][node_b[X]].top = 1

                if node_a[X] - node_b[X] == -1: #esquerda pra direita
                    grid[node_a[Y]][node_a[X]].right = 1
                    grid[node_b[Y]][node_b[X]].left = 1

            elif grid[node_a[Y]][node_a[X]].set != grid[node_b[Y]][node_b[X]].set:
                #atualizando o rótulo entre as 2 árvores
                temp_set = grid[node_b[Y]][node_b[X]].set
                for y, l in enumerate(grid):
                    for x, cell in enumerate(l):
                        if cell.set == temp_set:
                            grid[y][x].set = grid[node_a[Y]][node_a[X]].set

                if node_a[X] - node_b[X] == -1: #esquerda pra direita
                    grid[node_a[Y]][node_a[X]].right = 1
                    grid[node_b[Y]][node_b[X]].left = 1

                if node_a[Y] - node_b[Y] == -1: #cima pra baixo
                    grid[node_a[Y]][node_a[X]].bottom = 1
                    grid[node_b[Y]][node_b[X]].top = 1

        printGrid(grid)

    drawBoard(grid)

    # Flip the display
    pygame.display.flip()

    clock.tick()
    #print(clock.get_fps())
    it += 1

# Done! Time to quit.
pygame.quit()