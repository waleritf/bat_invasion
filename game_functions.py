import sys
import pygame

from bullet import Bullet
from bat import Bat

def check_keydown_events(event, ai_settings, screen, ship, bullets):
  if event.key == pygame.K_RIGHT:
    ship.moving_right = True
  if event.key == pygame.K_LEFT:
    ship.moving_left = True
  if event.key == pygame.K_SPACE:
    fire_bullet(ai_settings, screen, ship, bullets)
  if event.key == pygame.K_q:
    sys.exit()

def check_keyup_events(event, ship):
  if event.key == pygame.K_RIGHT:
    ship.moving_right = False
  if event.key == pygame.K_LEFT:
    ship.moving_left = False

def check_events(ai_settings, screen, ship, bullets):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == pygame.KEYDOWN:
      check_keydown_events(event, ai_settings, screen, ship, bullets)
    elif event.type == pygame.KEYUP:
      check_keyup_events(event, ship)

def update_screen(ai_settings, screen, ship, bats, bullets):
  screen.fill(ai_settings.bg_color)

  ship.blitme()
  bats.draw(screen)

  for bullet in bullets.sprites():
    bullet.draw_bullet()

  pygame.display.flip()

def update_bullets(bats, bullets):
  collisions = pygame.sprite.groupcollide(bullets, bats, True, True)

  bullets.update()

  for bullet in bullets.copy():
      if bullet.rect.bottom <= 0:
        bullets.remove(bullet)

def fire_bullet(ai_settings, screen, ship, bullets):
  if len(bullets) < ai_settings.bullets_allowed:
    new_bullet = Bullet(ai_settings, screen, ship)
    bullets.add(new_bullet)

def get_numbers_bats_x(ai_settings, bat_width):
  available_space_x = ai_settings.screen_width - (2 * bat_width)
  number_bats_x = int(available_space_x / (2 * bat_width))

  return number_bats_x

def get_numbers_rows(ai_settings, ship_height, bat_height):
  available_space_y = (ai_settings.screen_height
    - (3 * bat_height) - ship_height)
  number_rows = int(available_space_y / (2 * bat_height))

  return number_rows

def create_bat(ai_settings, screen, bats, bat_number, row_number):
  bat = Bat(ai_settings, screen)
  bat_width = bat.rect.width
  bat.x = bat_width + 2 * bat_width * bat_number
  bat.rect.x = bat.x
  bat.rect.y = bat.rect.height + 2 * bat.rect.height * row_number
  bats.add(bat)

def create_fleet(ai_settings, screen, ship, bats):
  bat = Bat(ai_settings, screen)
  number_bats_x = get_numbers_bats_x(ai_settings, bat.rect.width)
  number_rows = get_numbers_rows(ai_settings, ship.rect.height, bat.rect.height)

  for row_number in range(number_rows):
    for bat_number in range(number_bats_x):
      create_bat(ai_settings, screen, bats, bat_number, row_number)

def update_bats(ai_settings, bats):
  check_fleet_edges(ai_settings, bats)
  bats.update()

def check_fleet_edges(ai_settings, bats):
  for bat in bats.sprites():
    if bat.check_edges():
      change_fleet_direction(ai_settings, bats)
      break

def change_fleet_direction(ai_settings, bats):
  for bat in bats.sprites():
    bat.rect.y += ai_settings.fleet_drop_speed
  ai_settings.feet_direction *= -1