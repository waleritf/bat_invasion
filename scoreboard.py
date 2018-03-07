import pygame.font

class Scoreboard():
  def __init__(self, ai_settings, screen, stats):
    self.screen = screen
    self.screen_rect = screen.get_rect()
    self.ai_settings = ai_settings
    self.stats = stats

    self.text_color = (127, 127, 127)
    self.font = pygame.font.SysFont(None, 48)

    self.prepare_score()
    self.prepare_high_score()

  def prepare_score(self):
    score_str = str(self.stats.score)
    self.score_image = self.font.render(score_str, True, self.text_color,
      self.ai_settings.bg_color)

    self.score_rect = self.score_image.get_rect()
    self.score_rect.right = self.screen_rect.right - 20
    self.score_rect.top = 20

  def show_score(self):
    self.screen.blit(self.score_image, self.score_rect)
    self.screen.blit(self.high_score_image, self.high_score_rect)
  
  def prepare_high_score(self):
    high_score_str = str(self.stats.high_score)

    self.high_score_image = self.font.render(high_score_str, True,
      self.text_color, self.ai_settings.bg_color)

    self.high_score_rect = self.high_score_image.get_rect()
    self.high_score_rect.centerx = self.screen_rect.centerx
    self.high_score_rect.top = self.score_rect.top