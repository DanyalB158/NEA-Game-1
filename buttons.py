class Buttons:
  def __init__(self, image, pos, text_input, font, base_colour):
    self.image = image
    self.x_pos = pos[0]
    self.y_pos = pos[1]
    self.font = font
    self.base_colour = base_colour
    self.text_input = text_input
    self.text = self.font.render(self.text_input, True, self.base_colour)
    if self.image is None:
      self.image = self.text
    self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
    self.text_rect = self.text.get_rect(center = (self.x_pos,self.y_pos))

  def update(self,screen):
    if self.image is not None:
      screen.blit(self.image,self.rect)
    else:
      screen.blit(self.text,self.text_rect)

  def check_for_input(self,position):
    if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,self.rect.bottom):
      return True
    else: return False
    
