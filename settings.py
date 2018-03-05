class Settings():
  def __init__(self):
    self.screen_width = 1200
    self.screen_height = 800
    self.bg_color = (60, 60, 60)
    self.ship_speed_factor = 1.5
    self.ship_limit = 3

    self.bullet_speed_factor = 3
    self.bullet_width = 5
    self.bullet_height = 15
    self.bullet_color = 170, 00, 00
    self.bullets_allowed = 3

    self.bat_speed_factor = 1
    self.fleet_drop_speed = 10
    self.fleet_direction = 1