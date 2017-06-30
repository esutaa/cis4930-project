#!/usr/bin/env python3

import pygame as pg

pg.init()

res_width  = 800
res_height = 600
gameDisplay = pg.display.set_mode((res_width, res_height))
pg.display.set_caption('Test Caption')

clock = pg.time.Clock()

# Loading graphics assets
# If this gives you some BS about it not being a BMP, update your Python Version
imgAsset = pg.image.load('imgAsset.png')
imgAssetWidth = 64

def robotnik(x, y):
  gameDisplay.blit(imgAsset, (x, y))

x = (res_width * 0.45)
y = (res_height * 0.8)

crashed = False

x_change = 0

# This is the main game loop
while not crashed:

  for event in pg.event.get():
    if event.type == pg.QUIT:
      crashed = True
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_LEFT:
        x_change = -5
      elif event.key == pg.K_RIGHT:
        x_change = 5
    if event.type == pg.KEYUP:
      if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
        x_change = 0
  print(event)
  
  x += x_change
  
  # This effectively wipes the display so that it can be re-written
  gameDisplay.fill((0,0,0))
  robotnik(x, y)
  
  pg.display.update()
  clock.tick(60)


pg.quit()
quit()
