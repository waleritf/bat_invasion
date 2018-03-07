import sys
import pygame

from bullet import Bullet
from bat import Bat
from time import sleep

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

def check_events(ai_settings, screen, ship, bullets, bats, stats, play_button):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == pygame.KEYDOWN:
      check_keydown_events(event, ai_settings, screen, ship, bullets)
    elif event.type == pygame.KEYUP:
      check_keyup_events(event, ship)
    elif event.type == pygame.MOUSEBUTTONDOWN:
      mouse_x, mouse_y = pygame.mouse.get_pos()
      check_play_button(ai_settings, screen, stats, ship, bullets, bats, play_button, mouse_x, mouse_y)

def update_screen(ai_settings, screen, stats, ship, bats, bullets, play_button):
  screen.fill(ai_settings.bg_color)

  ship.blitme()
  bats.draw(screen)

  for bullet in bullets.sprites():
    bullet.draw_bullet()

  if not stats.game_active:
    play_button.draw()

  pygame.display.flip()

def update_bullets(ai_settings, screen, ship, bats, bullets):
  check_bullet_bat_collisions(ai_settings, screen, ship, bats, bullets)

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

def ship_hit(ai_settings, stats, screen, ship, bats, bullets):
  if stats.ships_left > 0:
    stats.ships_left -= 1

    bats.empty()
    bullets.empty()

    create_fleet(ai_settings, screen, ship, bats)
    ship.center_ship()

    sleep(0.5)
  else:
    stats.game_active = False
    pygame.mouse.set_visible(True)

def update_bats(ai_settings, stats, screen, ship, bats, bullets):
  check_fleet_edges(ai_settings, bats)
  bats.update()

  if pygame.sprite.spritecollideany(ship, bats):
    ship_hit(ai_settings, stats, screen, ship, bats, bullets)
  
  check_bats_bottom(ai_settings, stats, screen, ship, bats, bullets)

def check_fleet_edges(ai_settings, bats):
  for bat in bats.sprites():
    if bat.check_edges():
      change_fleet_direction(ai_settings, bats)
      break

def change_fleet_direction(ai_settings, bats):
  for bat in bats.sprites():
    bat.rect.y += ai_settings.fleet_drop_speed
  ai_settings.fleet_direction *= -1

def check_bullet_bat_collisions(ai_settings, screen, ship, bats, bullets):
  pygame.sprite.groupcollide(bullets, bats, True, True)

  if len(bats) == 0:
    bullets.empty()
    ai_settings.increase_speed()
    create_fleet(ai_settings, screen, ship, bats)

def check_bats_bottom(ai_settings, stats, screen, ship, bats, bullets):
  screen_rect = screen.get_rect()
  for bat in bats.sprites():
    if bat.rect.bottom >= screen_rect.bottom:
      ship_hit(ai_settings, stats, screen, ship, bats, bullets)
      break

def check_play_button(ai_settings, screen, stats, ship, bullets, bats, play_button, mouse_x, mouse_y):
  button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
  if button_clicked and not stats.game_active:
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    stats.game_active = True
    bats.empty()
    bullets.empty()
    create_fleet(ai_settings, screen, ship, bats)
    ship.center_ship()