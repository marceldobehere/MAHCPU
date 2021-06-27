# Importieren der Pygame-Bibliothek
import pygame
import tkinter as tk
import numpy
import keyboard


# initialisieren von pygame
pygame.init()

# genutzte Farbe
ORANGE  = ( 255, 140, 0)
ROT     = ( 255, 0, 0)
GRUEN   = ( 0, 255, 0)
SCHWARZ = ( 0, 0, 0)
WEISS   = ( 255, 255, 255)

# Fenster öffnen
screen = pygame.display.set_mode((300, 340))

screen.fill(SCHWARZ)
pygame.display.set_caption("TEST-CPU")




font = pygame.font.Font('freesansbold.ttf', 28)
text = font.render('Screen', True, WEISS, SCHWARZ)
textRect = text.get_rect()
textRect.center = (150, 25)
screen.blit(text, textRect)
 


pygame.display.flip()

from tkinter import filedialog
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
print(file_path)

from numpy import loadtxt
file1 = open(file_path, 'r')
lines = file1.readlines()

debug_out = False

maxlen = 0
for line in lines:
    lines[maxlen] = line.strip().ljust(52, '0')
    if (debug_out):
        print(lines[maxlen])
    maxlen += 1

# solange die Variable True ist, soll das Spiel laufen
spielaktiv = True
ENDE = True

# Bildschirm Aktualisierungen einstellen
clock = pygame.time.Clock()





REG = [0] * 16
RAM = [0] * 1000000




REG[0] = -1


while spielaktiv:
    # Überprüfen, ob Nutzer eine Aktion durchgeführt hat

    REG[0] += 1

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            spielaktiv = False
            ENDE = False

    cmd = lines[REG[0]][0:4]
    cmd_arg_1 = int("0" + lines[REG[0]][4:36], 2)
    cmd_arg_2 = int("0" + lines[REG[0]][36:68], 2)
    cmd_arg_3 = int("0" + lines[REG[0]][68:100], 2)

    
    # print(str(REG[0]) + " | " + cmd + " | "  + str(lines[REG[0]][4:20]) + " | "  + str(lines[REG[0]][20:36]) + " | "  + str(lines[REG[0]][36:52]))
    if (debug_out):
        print(str(REG[0]) + " | " + cmd + " | "  + str(cmd_arg_1) + " | "  + str(cmd_arg_2) + " | "  + str(cmd_arg_3))

    if (cmd == '0001'):
        REG[cmd_arg_1] = cmd_arg_2

    if (cmd == '0010'):
        REG[RAM[cmd_arg_1]] = RAM[RAM[cmd_arg_2]]

    if (cmd == '0011'):
        RAM[cmd_arg_1] = REG[cmd_arg_2]

    if (cmd == '0100'):
        RAM[RAM[cmd_arg_1]] = REG[RAM[cmd_arg_2]]

    if (cmd == '0101'):
        val = REG[7]

        int_diff = val%3
        x = (val//3)%100
        y = (val//3)//100

        col = tuple(screen.get_at((x * 3, y * 3 + 40)))
        col_temp = list(col)
        col_temp[int_diff] = RAM[REG[8]]
        col = tuple(col_temp)
        # screen.set_at((x, y), col)
        if (debug_out):
            print("Setting pixel at " + str(x) + " | " + str(y) + "(" + str(val) + ") to " + str(col_temp[0]) + " | " + str(col_temp[1]) + " | " + str(col_temp[2]))
        pygame.draw.rect(screen, col, pygame.Rect(x * 3, y * 3 + 40, 3, 3))


    if (cmd == '0110'):
        val = REG[8]
        int_diff = val%3
        x = (val//3)%100
        y = (val//3)//100

        col = tuple(screen.get_at((x * 3, y * 3 + 40)))

        col_temp = list(col)
        RAM[REG[7]] = col_temp[int_diff]


    if (cmd == '0111'):
        REG[1] = RAM[REG[7]] + RAM[REG[8]]

    if (cmd == '1000'):
        REG[1] = RAM[REG[7]] - RAM[REG[8]]

    if (cmd == '1001'):
        REG[2] = 1 * (RAM[REG[7]] + RAM[REG[8]] == 2)

    if (cmd == '1010'):
        REG[2] = 1 * (RAM[REG[7]] + RAM[REG[8]] > 0)

    if (cmd == '1011'):
        REG[2] = 1 * (RAM[REG[7]] == 0)

    if (cmd == '1100'):
        if (debug_out):
            print("Jumping to " + str(RAM[REG[8]]) + " if " + str(RAM[REG[7]]) + " != 0")
        if (RAM[REG[7]] != 0):
            REG[0] = RAM[REG[8]]
            if (debug_out):
                print("Jumping to " + str(RAM[REG[8]]) + "... (" + str(REG[0]) + ")")

    if (cmd == '1110'):

        print("Enter key...")
        inp = keyboard.read_key()

        if (debug_out):
            print(ord(inp[0]))
        RAM[cmd_arg_1] = ord(inp[0])


    if (cmd == '1101'):
        pygame.display.flip()

    if (cmd == '1111'):
        print("Debug out REG[" + str(cmd_arg_1) + "] = " + str(REG[cmd_arg_1]))

    # screen.set_at((counter, 40), WEISS)
    # pygame.display.flip()

    
    # clock.tick(30)




    if REG[0] >= maxlen - 1:
        spielaktiv = False


pygame.display.flip()

'''
    y = 0
    while (y < 340):
        x = 0
        while (x < 300):
            col = tuple(screen.get_at((x, y)))
            # print("PIXEL: " + str(screen.get_at((x, y))))
            col_temp = list(col)
            # col_temp[0] = 50
            col_temp[1] = 150
            col = tuple(col_temp)
        
            screen.set_at((x, y), col)
            x += 1
        y += 1
        pygame.display.flip()
'''



print("Waiting to exit...")

while ENDE:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            ENDE = False

pygame.quit()