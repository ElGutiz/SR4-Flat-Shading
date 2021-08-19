from zFunctions import glInit, load, glFinish

width = 800
height = 600

glInit(width, height)

load('./models/pumpkin.obj', (0.9, 0.4, 0), (450, 450, 150))

glFinish("PruebaPumpkinV2.bmp", width, height)