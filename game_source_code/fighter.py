import math
import pygame

class Fighter():
  def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
    self.player = player #check player being controlled
    # self.size = data[0]
    self.width = data[0]
    self.height = data[1]
    self.image_scale = data[2]
    self.offset = data[3]
    self.flip = flip #for horizontal orientation of player
    self.animation_list = self.load_images(sprite_sheet, animation_steps) #all images of player
    self.action = 0 #0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
    self.frame_index = 0
    self.image = self.animation_list[self.action][self.frame_index] #current image of player to be rendered
    self.update_time = pygame.time.get_ticks()
    self.rect = pygame.Rect((x, y, 80, 180)) #placeholder rect for handling all player movements
    self.vel_y = 0
    self.running = False
    self.jump = False
    self.attacking = False
    self.attack_type = 0
    self.attack_cooldown = 0 #ensure some gap between two attacks
    self.attack_sound = sound
    self.hit = False
    self.health = 100
    self.alive = True
    self.attack2_cooldown=0
    self.supuse=0
    self.invincible = False
    self.invincible_duration = 5000  # Time in milliseconds
    self.invincible_end_time = 0
    self.health_boost=False
    self.health_boost_duration=2000
    self.health_boost_endtime=0

  def load_images(self, sprite_sheet, animation_steps):
    #extract images from spritesheet
    animation_list = []
    for y, animation in enumerate(animation_steps):
      temp_img_list = []
      for x in range(animation):
        temp_img = sprite_sheet.subsurface(x * self.width, y * self.height, self.width, self.height)
        temp_img_list.append(pygame.transform.scale(temp_img, (self.width * self.image_scale, self.height * self.image_scale)))
      animation_list.append(temp_img_list)
    return animation_list


  def move(self, screen_width, screen_height, target, round_over, custom_data):
    SPEED = 15
    GRAVITY = 2
    dx = 0
    dy = 0
    self.attack_type = 0
    if self.attack2_cooldown>0:
      self.attack2_cooldown-=1
    #can only perform other actions if not currently attacking
    if self.attacking == False and self.alive == True and round_over == False:
      #check player 1 controls
      if self.player == 1:
        #movement
        if custom_data[0]:
          dx = -SPEED
          self.running = True
        if custom_data[1]:
          dx = SPEED
          self.running = True
        #jump
        if custom_data[2] and self.jump == False:
          self.vel_y = -35
          self.jump = True
        #attack
        if custom_data[3] or custom_data[4]:
          
          #determine which attack type was used
          if custom_data[3]:
            self.attack_type = 1
          if custom_data[4]:
            self.attack_type = 2
          self.attack(target,self.attack_type)
        if custom_data[10] and self.supuse==0 and self.health<50:
           self.health=50
           self.health_boost=True
           self.health_boost_endtime=pygame.time.get_ticks() + self.health_boost_duration
           self.supuse=1
        if custom_data[12] and self.supuse==0:
           self.invincible=True
           self.invincible_end_time = pygame.time.get_ticks() + self.invincible_duration
           self.supuse=1

      #check player 2 controls
      if self.player == 2:
        #movement
        if custom_data[5]:
          dx = -SPEED
          self.running = True
        if custom_data[6]:
          dx = SPEED
          self.running = True
        #jump
        if custom_data[7] and self.jump == False:
          self.vel_y = -35
          self.jump = True
        #attack
        if custom_data[8] or custom_data[9]:
          
          #determine which attack type was used
          if custom_data[8]:
            self.attack_type = 1
          if custom_data[9]:
            self.attack_type = 2
          self.attack(target,self.attack_type)
        if custom_data[11] and self.supuse==0 and self.health<50:
           self.health=50
           self.health_boost=True
           self.health_boost_endtime=pygame.time.get_ticks() + self.health_boost_duration
           self.supuse=1
        if custom_data[13] and self.supuse==0:
           self.invincible=True
           self.invincible_end_time = pygame.time.get_ticks() + self.invincible_duration
           self.supuse=1

    #apply gravity
    self.vel_y += GRAVITY
    dy += self.vel_y
    if self.invincible and pygame.time.get_ticks() >= self.invincible_end_time:
            self.invincible = False
    if self.health_boost and pygame.time.get_ticks() >= self.health_boost_endtime:
            self.health_boost  = False
    #ensure player stays on screen
    if self.rect.left + dx < 0:
      dx = -self.rect.left
    if self.rect.right + dx > screen_width:
      dx = screen_width - self.rect.right
    if self.rect.bottom + dy > screen_height - 110:
      self.vel_y = 0
      self.jump = False
      dy = screen_height - 110 - self.rect.bottom

    #ensure players face each other
    if target.rect.centerx > self.rect.centerx:
      self.flip = False
    else:
      self.flip = True

    #apply attack cooldown
    if self.attack_cooldown > 0:
      self.attack_cooldown -= 1

    #update player position
    self.rect.x += dx
    self.rect.y += dy


  #handle animation updates
  def update(self):
    #check what action the player is performing
    if self.health <= 0:
      self.health = 0
      self.alive = False
      self.update_action(6)#6:death
    elif self.hit == True:
      self.update_action(5)#5:hit
    elif self.attacking == True:
      if self.attack_type == 2:
        self.update_action(4)#4:attack2
      elif self.attack_type == 1:
        self.update_action(3)#3:attack1
    elif self.jump == True:
      self.update_action(2)#2:jump
    elif self.running == True:
      self.update_action(1)#1:run
    else:
      self.update_action(0)#0:idle

    animation_cooldown = 50
    #update image
    self.image = self.animation_list[self.action][self.frame_index]
    #check if enough time has passed since the last update
    if pygame.time.get_ticks() - self.update_time > animation_cooldown:
      self.frame_index += 1
      self.update_time = pygame.time.get_ticks()
    #check if the animation has finished
    if self.frame_index >= len(self.animation_list[self.action]):
      #if the player is dead then end the animation
      if self.alive == False:
        self.frame_index = len(self.animation_list[self.action]) - 1
      #else if running animation is over => back to idle
      elif self.action == 1:
        self.running = False
        self.update_action(0)
      #else restart the animation
      else:
        self.frame_index = 0
        #check if an attack was executed
        if self.action == 3 or self.action == 4:
          self.attacking = False
          self.attack_cooldown = 20
        #check if damage was taken
        if self.action == 5:
          self.hit = False
          #if the player was in the middle of an attack, then the attack is stopped
          self.attacking = False
          self.attack_cooldown = 20
      


  def attack(self, target,attack_type):
    attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height - 5)
    if attack_type==1:
          if self.attack_cooldown == 0:
          #execute attack
              self.attacking = True
              self.attack_sound.play()
              attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height - 5)
              if attacking_rect.colliderect(target.rect) and not target.invincible:
                target.health -= 5
                target.hit = True
    elif attack_type == 2 and self.attack2_cooldown == 0:
          if self.attack_cooldown == 0:
          #execute attack
              self.attacking = True
              self.attack_sound.play()
              attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height - 5)
              self.attack2_cooldown = 1500
              if attacking_rect.colliderect(target.rect) and not target.invincible:
                target.health -= 20
                target.hit = True
                


  def update_action(self, new_action):
    #check if the new action is different to the previous one
    if new_action != self.action:
      self.action = new_action
      #update the animation settings
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()

  def draw(self, surface):
    #draw image of character on screen
    img = pygame.transform.flip(self.image, self.flip, False)
    surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
    if self.invincible:
       circle_radius = max(self.rect.width, self.rect.height) * 0.6  # Adjust multiplier as needed    # Calculate center of the circle
       circle_center = (self.rect.centerx, self.rect.centery)
       pygame.draw.circle(surface, (255, 165, 0), circle_center, int(circle_radius), 2)
  def draw_timer(self, surface, x, y, radius):
        # Calculate percentage of cooldown completed
        percentage_completed = 1 - (self.attack2_cooldown / 1500)  # Assuming 1500 ticks cooldown

        # Calculate angle to fill based on percentage
        angle = 360 * percentage_completed

        # Draw the unfilled portion of the timer
        pygame.draw.circle(surface, (100, 100, 100), (x, y), radius)
        # Check if the timer is completely filled
        if percentage_completed >= 1:
            alpha = math.sin(pygame.time.get_ticks() / 200)  # Adjust the division factor to control pulsation speed
        # Adjust the alpha value range to [100, 255] for visibility
            brightness = abs(math.sin(pygame.time.get_ticks() / 2000))  # Adjust the division factor to control pulsation speed
            # Adjust the brightness value range to [100, 255] for visibility
            brightness = int(155 * brightness + 100)

            # Fill the entire circle with glowing yellow color
            glowing_yellow = (255, 255, 0, brightness)  # Set yellow color with pulsating brightness
            pygame.draw.circle(surface, glowing_yellow, (x, y), radius)
        else:
            # Draw the filled portion of the timer without glowing effect
            fill_color = (255, 0, 0)  # Red fill color
            pygame.draw.arc(surface, fill_color, (x - radius, y - radius, 2 * radius, 2 * radius),math.radians(-90), math.radians(-90 + angle), 10)