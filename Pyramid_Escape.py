####################################################################
#################################################################### 초기 설정

import pygame, sys, random, time
from pygame.locals import *

pygame.init() #파이게임 초기화

#화면 크기 설정
screen_width = 1280 # 가로크기
screen_height = 720 # 세로크기

#게임 크기
screen = pygame.display.set_mode((screen_width, screen_height))

#게임이름
pygame.display.set_caption('Pyramid_Escape')

#FPS
clock = pygame.time.Clock()

#각종 이미지 불러오기
homescreen_image = pygame.image.load('images/homescreen.png').convert()

one_image = pygame.image.load('images/1.png').convert()
one_image.set_colorkey((0, 0, 0))
two_image = pygame.image.load('images/2.png').convert()
two_image.set_colorkey((0, 0, 0))
three_image = pygame.image.load('images/3.png').convert()
three_image.set_colorkey((0, 0, 0))

clearscreen_image = pygame.image.load('images/clear.png').convert()
howtoplay_image = pygame.image.load('images/How_to_play.png').convert()

start_image = pygame.image.load('images/start.png').convert()
start_rect = start_image.get_rect()

end_image = pygame.image.load('images/end.png').convert()
end_rect = end_image.get_rect()

replay_image = pygame.image.load('images/replay.png').convert()
replay_rect = replay_image.get_rect()

how_to_butten_image = pygame.image.load('images/how_to_butten.png').convert()
how_to_butten_rect = how_to_butten_image.get_rect()

badguy_image = pygame.image.load('images/E_missile.png').convert()
badguy_image.set_colorkey((255, 255, 255))

boss_small_missile = pygame.image.load('images/B_missile.png').convert()
boss_small_missile.set_colorkey((255, 255, 255))

boss_missile_image = pygame.image.load('images/boss_missile.png').convert()
boss_missile_image.set_colorkey((255, 255, 255))

enemy_image = pygame.image.load('images/vhxkq.png').convert()
enemy_image.set_colorkey((0, 0, 0))

boss_image = pygame.image.load('images/boss.png').convert()
boss_image.set_colorkey((255, 255, 255))

wall_normal = pygame.image.load('images/wall_normal.png').convert()
wall_broken = pygame.image.load('images/wall_broken.png').convert()
wall_broken.set_colorkey((255, 255, 255))

character_image = pygame.image.load('images/character_top.png').convert()
character_image.set_colorkey((255, 255, 255))
character_size = character_image.get_rect().size
character_width = character_size[0]
character_height = character_size[1]

missile_image = pygame.image.load('images/missile.png').convert()
missile_image.set_colorkey((255, 255, 255))

portal_image = pygame.image.load('images/test.png').convert()
portal_image.set_colorkey((255, 255, 255))
un_portal_image = pygame.image.load('images/un_act_portal.png').convert()
un_portal_image.set_colorkey((255, 255, 255))
boss_portal_image = pygame.image.load('images/boss_portal.png').convert()
boss_portal_image.set_colorkey((255, 255, 255))

treasure_image = pygame.image.load('images/tkdwk.png').convert()
treasure_image.set_colorkey((0, 0, 0))

GAME_OVER = pygame.image.load('images/gameover.png').convert()

#폰트들 설정
font = pygame.font.Font(None, 25)
font2 = pygame.font.Font(None, 30)
font3 = pygame.font.Font(None, 50)

#변수들 초기화
stage = 0
stop = 0
rewards = 0
high_score = 0
mapcounter = 1 #스테이지가 계속 호출되는 것을 막기 위한 변수

missile_speed = 10 #캐릭터 샷스피드
e_missile_speed = 4 #포탑 샷스피드
fire_range = 50 #포탑 공격 사거리

#사운드 불러오기
shot_sound = pygame.mixer.Sound('sounds/shot.wav')
walk_sound = pygame.mixer.Sound('sounds/walk.wav')
treasure_sound = pygame.mixer.Sound('sounds/treasure.wav')
portal_sound = pygame.mixer.Sound('sounds/portal.wav')
Boss_music = pygame.mixer.Sound('sounds/boss_music.wav')
stage_music = pygame.mixer.Sound('sounds/stage_music.wav')
clear_sound = pygame.mixer.Sound('sounds/clear_sound.wav')

####################################################################
#################################################################### 클래스

class Character: #플레이어 클래스
    def __init__(self):
        self.x = 640
        self.y = 690
        self.range = 0
        self.stop = 0.0
        self.lastInput = 0 #벽에 닿기 직전 사용자가 어떤 방향키를 누르고 벽에 닿았는지 좌우상하 순으로 1, 2, 3, 4로 저장
        self.canMove_L = True #추가
        self.canMove_R = True #추가
        self.canMove_U = True #추가
        self.canMove_D = True #추가

        self.attac_speed = 0.6 #캐릭터 공격 속도(작을 수록 빨라짐)
        self.character_speed = 5 #캐릭터 이동 속도(클 수록 빨라짐)
        self.damage = 0 #캐릭터 공격 추가 데미지(클 수록 강해짐)
        self.hp = 3 #캐릭터 체력

    def respawn(self): #플레이어 리스폰 위치
        self.x =640
        self.y = 690
        self.range = 0

    def move(self, walls): #플레이어 이동 함수 + 벽을 지나갈 수 없게 하는 함수
        self.character_rect_R = pygame.Rect(self.x+32, self.y+7, 5, 25) #추가
        self.character_rect_L = pygame.Rect(self.x+2, self.y+7, 5, 25) #추가
        self.character_rect_T = pygame.Rect(self.x+7, self.y+2, 25, 5) #추가
        self.character_rect_B = pygame.Rect(self.x+7, self.y+32, 25, 5) #추가
        ##이 부분부터 판정 알고리즘 수정
        wallCount = 0
        for wallCount in range(len(walls)):
            if self.character_rect_R.colliderect(walls[wallCount].wall_rect) == True:
                self.canMove_R = False
                break
            else:
                self.canMove_R = True

        wallCount = 0
        for wallCount in range(len(walls)):
            if self.character_rect_L.colliderect(walls[wallCount].wall_rect) == True:
                self.canMove_L = False
                break
            else:
                self.canMove_L = True

        wallCount = 0
        for wallCount in range(len(walls)):
            if self.character_rect_T.colliderect(walls[wallCount].wall_rect) == True:
                self.canMove_U = False
                break
            else:
                self.canMove_U = True

        wallCount = 0
        for wallCount in range(len(walls)):
            if self.character_rect_B.colliderect(walls[wallCount].wall_rect) == True:
                self.canMove_D = False
                break
            else:
                self.canMove_D = True
                
        if len(walls) == 0: # 마지막 벽이 깨질 때 벽에 붙어 있으면 이후 위의 for문이 안돌아 다시 self.canMove를 True로 돌리는 코드가 없었음, 또 다른 버그 생길 수도 있음
            self.canMove_L = True
            self.canMove_R = True
            self.canMove_U = True
            self.canMove_D = True
        #여기까지 판단 알고리즘

        
        if pressed_keys[K_LEFT] and self.x > 0 and self.canMove_L == True: #세번째 조건 바뀜
            self.character_rect_T = pygame.Rect(self.x+32, self.y+7, 5, 25) #추가
            self.character_rect_B = pygame.Rect(self.x+2, self.y+7, 5, 25) #추가
            self.character_rect_L = pygame.Rect(self.x+7, self.y+2, 25, 5) #추가
            self.character_rect_R = pygame.Rect(self.x+7, self.y+32, 25, 5) #추가, 이하 나머지 방향키도 추가
            
            self.x -= self.character_speed
            self.lastInput = 1

            if (time.time() - self.stop)>0.4:
                pygame.mixer.Sound.play(walk_sound)
                self.stop = time.time()
            return
            
        if pressed_keys[K_RIGHT] and self.x < 1280 - 40 and self.canMove_R == True:
            self.character_rect_B = pygame.Rect(self.x+32, self.y+7, 5, 25)
            self.character_rect_T = pygame.Rect(self.x+2, self.y+7, 5, 25)
            self.character_rect_R = pygame.Rect(self.x+7, self.y+2, 25, 5)
            self.character_rect_L = pygame.Rect(self.x+7, self.y+32, 25, 5)
            
            self.x += self.character_speed
            self.lastInput = 2

            if (time.time() - self.stop)>0.4:
                pygame.mixer.Sound.play(walk_sound)
                self.stop = time.time()
            return

        if pressed_keys[K_UP] and self.y > 0 and self.canMove_U == True:
            self.character_rect_R = pygame.Rect(self.x+32, self.y+7, 5, 25)
            self.character_rect_L = pygame.Rect(self.x+2, self.y+7, 5, 25)
            self.character_rect_T = pygame.Rect(self.x+7, self.y+2, 25, 5)
            self.character_rect_B = pygame.Rect(self.x+7, self.y+32, 25, 5)
            
            self.y -= self.character_speed
            self.lastInput = 3

            if (time.time() - self.stop)>0.4:
                pygame.mixer.Sound.play(walk_sound)
                self.stop = time.time()
            return

        if pressed_keys[K_DOWN] and self.y < 720 - 40 and self.canMove_D == True:
            self.character_rect_L = pygame.Rect(self.x+32, self.y+7, 5, 25)
            self.character_rect_R = pygame.Rect(self.x+2, self.y+7, 5, 25)
            self.character_rect_B = pygame.Rect(self.x+7, self.y+2, 25, 5)
            self.character_rect_T = pygame.Rect(self.x+7, self.y+32, 25, 5)
            
            self.y += self.character_speed #이동 구현
            self.lastInput = 4

            if (time.time() - self.stop)>0.4:
                pygame.mixer.Sound.play(walk_sound)
                self.stop = time.time()
            return
    
    def draw(self): #그리기(각도에 따라 로테이션 해줌)

        if pressed_keys[K_LEFT]:
            self.range = 90
            rotated = pygame.transform.rotate(character_image, self.range)
            screen.blit(rotated, (self.x, self.y))
            return

        if pressed_keys[K_RIGHT]:
            self.range = 270
            rotated = pygame.transform.rotate(character_image, self.range)
            screen.blit(rotated, (self.x, self.y))
            return
        
        if pressed_keys[K_UP]:
            self.range = 0
            rotated = pygame.transform.rotate(character_image, self.range)
            screen.blit(rotated, (self.x, self.y))
            return

        if pressed_keys[K_DOWN]:
            self.range = 180
            rotated = pygame.transform.rotate(character_image, self.range)
            screen.blit(rotated, (self.x, self.y))
            return

        else:
            rotated = pygame.transform.rotate(character_image, self.range)
            screen.blit(rotated, (self.x, self.y))
    
    def fire(self): #미사일 발사(총구의 방향에서 발사되게 조정해놓음)
        if self.range == 90:
            missiles.append(Missile(self.x - 12, self.y + 8, self.range))

        if self.range == 270:
            missiles.append(Missile(self.x + 20, self.y + 26, self.range))

        if self.range == 0:
            missiles.append(Missile(self.x + 24, self.y - 4, self.range))

        if self.range == 180:
            missiles.append(Missile(self.x + 4, self.y + 20, self.range))
    
class Missile: # 미사일 클래스
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def move(self):
        if self.r == 0:
            self.y -= missile_speed # 총알 샷스피드가 높을수록 미사일의 샷스피드가 빨라짐

        if self.r == 90:
            self.x -= missile_speed

        if self.r == 270:
            self.x += missile_speed

        if self.r == 180:
            self.y += missile_speed

    def off_screen(self): #총알이 화면을 벗어났을 때 없애주는 함수
        if (self.y < -8):
            return True
        elif (self.y > 728):
            return True
        elif (self.x < -8):
            return True
        elif (self.x > 1288):
            return True

    def draw(self):
        
        if self.r == 0:
            rotated = pygame.transform.rotate(missile_image, self.r)
            screen.blit(rotated, (self.x, self.y))

        if self.r == 180:
            rotated = pygame.transform.rotate(missile_image, self.r)
            screen.blit(rotated, (self.x, self.y))

        if self.r == 90:
            rotated = pygame.transform.rotate(missile_image, self.r)
            screen.blit(rotated, (self.x, self.y))

        if self.r == 270:
            rotated = pygame.transform.rotate(missile_image, self.r)
            screen.blit(rotated, (self.x, self.y))

class Wall: #벽 클래스
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = stage * 6
        self.wall_state = wall_normal #기본은 기본 벽 텍스처
        self.wall_rect = pygame.Rect(self.x, self.y, 40, 40) #벽 범위

    def draw(self):
        screen.blit(self.wall_state, (self.x, self.y))

    def hit(self, missiles): #벽 피격 판정(미사일: 10*32, 벽: 40*40)
        if missiles.r == 0:
            return self.y < missiles.y + 26 and missiles.y < self.y + 40 and self.x < missiles.x + 8 and missiles.x < self.x + 40
        if missiles.r == 180:
            return self.y < missiles.y + 26 and missiles.y < self.y + 40 and self.x < missiles.x + 8 and missiles.x < self.x + 40
        if missiles.r == 90:
            return self.y < missiles.y + 8 and missiles.y < self.y + 40 and self.x < missiles.x + 26 and missiles.x < self.x + 40
        if missiles.r == 270:
            return self.y < missiles.y + 8 and missiles.y < self.y + 40 and self.x < missiles.x + 26 and missiles.x < self.x + 40

class Enemy: #포탑 클래스
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = stage
        self.last_badguy_spawn_time = time.time() 

    def draw(self):
        screen.blit(enemy_image, (self.x, self.y))

    def hit(self, missiles): #벽 피격 판정(미사일: 10*32, 포탑: 40*40)
        if missiles.r == 0:
            return self.y < missiles.y + 26 and missiles.y < self.y + 40 and self.x < missiles.x + 8 and missiles.x < self.x + 40
        if missiles.r == 180:
            return self.y < missiles.y + 26 and missiles.y < self.y + 40 and self.x < missiles.x + 8 and missiles.x < self.x + 40
        if missiles.r == 90:
            return self.y < missiles.y + 8 and missiles.y < self.y + 40 and self.x < missiles.x + 26 and missiles.x < self.x + 40
        if missiles.r == 270:
            return self.y < missiles.y + 8 and missiles.y < self.y + 40 and self.x < missiles.x + 26 and missiles.x < self.x + 40

    def fire(self): #십자방향으로 포탑 총알 발사
        badguys.append(Badguy_Down(self.x + 8, self.y + 5))
        badguys.append(Badguy_Up(self.x + 8, self.y + 15))
        badguys.append(Badguy_Left(self.x + 5, self.y + 8))
        badguys.append(Badguy_Right(self.x + 15, self.y + 8))

class Boss: #보스 클래스
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100
        self.last_badguy_spawn_time = time.time()
        self.last_badguy_spawn_time2 = time.time()

    def hit(self, missiles): #보스 피격 판정(미사일: 10*32, 보스: 360*360)
        return self.y < missiles.y + 26 and missiles.y < self.y + 360 and self.x < missiles.x + 8 and missiles.x < self.x + 360

    def draw(self):
        screen.blit(boss_image, (self.x, self.y))
        
    def fire_big(self): #무작위 패턴의 미사일 큰거 3발 + 미사일 작은거 2발 발사
        randome_one = random.randint(1,5)
        randome_two = random.randint(1,5)

        if randome_one == 1 or randome_two == 1:
            boss_missiles.append(Boss_Down1(self.x - 260, self.y))
        if randome_one == 2 or randome_two == 2:
            boss_missiles.append(Boss_Down1(self.x + 40, self.y + 300))
        if randome_one == 3 or randome_two == 3:
            boss_missiles.append(Boss_Down1(self.x + 360, self.y))

    def fire_small(self):
        randome_three = random.randint(1,5)
        randome_four = random.randint(1,5)

        if randome_three == 1 or randome_four == 1:
            boss_missiles.append(Boss_small_Down1(self.x - 10, self.y + 300))
            boss_missiles.append(Boss_small_Down1(self.x + 330, self.y + 300))

        if randome_three == 2 or randome_four == 2:
            boss_missiles.append(Boss_small_Down1(self.x + 20, self.y + 300))
            boss_missiles.append(Boss_small_Down1(self.x + 300, self.y + 300))


class Boss_Down1: #보스 미사일 큰거
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 0

    def move(self):
        self.y += e_missile_speed
             
    def draw(self):
        screen.blit(boss_missile_image, (self.x, self.y))

    def off_screen(self):
        if (self.y < -800):
            return True
        elif (self.y > 728):
            return True
        elif (self.x < -800):
            return True
        elif (self.x > 1288):
            return True

    def touching_c(self, caracter): #캐릭터와 충돌했을 떄
        return self.y + 40 < caracter.y + 40 and caracter.y < self.y + 180 and self.x + 40 < caracter.x + 30 and caracter.x < self.x + 220

class Boss_small_Down1: #보스 미사일 작은거
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 0

    def move(self):
        self.y += e_missile_speed
             
    def draw(self):
        screen.blit(boss_small_missile, (self.x, self.y))

    def off_screen(self):
        if (self.y < -800):
            return True
        elif (self.y > 728):
            return True
        elif (self.x < -800):
            return True
        elif (self.x > 1288):
            return True

    def touching_c(self, caracter):
        return self.y < caracter.y + 40 and caracter.y < self.y + 25 and self.x - 10 < caracter.x + 30 and caracter.x < self.x + 35

class Badguy_Down: #포탑 미사일(아래 방향)
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 0

    def move(self):
        self.y += e_missile_speed
             
    def draw(self):
        screen.blit(badguy_image, (self.x, self.y))

    def off_screen(self):
        if (self.y < -8):
            return True
        elif (self.y > 728):
            return True
        elif (self.x < -8):
            return True
        elif (self.x > 1288):
            return True

    def touching_m(self, missiles): #내 캐릭터의 미사일에 닿았을 때
        return self.y < missiles.y + 26 and missiles.y < self.y + 25 and self.x < missiles.x + 8 and missiles.x < self.x + 25

    def touching_c(self, caracter):
        return self.y < caracter.y + 40 and caracter.y < self.y + 25 and self.x < caracter.x + 30 and caracter.x < self.x + 25

class Badguy_Up: #포탑 미사일(위 방향)
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 0

    def move(self):
        self.y -= e_missile_speed
             
    def draw(self):
        screen.blit(badguy_image, (self.x, self.y))

    def off_screen(self):
        if (self.y < -8):
            return True
        elif (self.y > 728):
            return True
        elif (self.x < -8):
            return True
        elif (self.x > 1288):
            return True

    def touching_m(self, missiles):
        return self.y < missiles.y + 26 and missiles.y < self.y + 25 and self.x < missiles.x + 8 and missiles.x < self.x + 25

    def touching_c(self, caracter):
        return self.y < caracter.y + 30 and caracter.y < self.y + 25 and self.x < caracter.x + 30 and caracter.x < self.x + 25

class Badguy_Left: #포탑 미사일(왼쪽 방향)
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 0

    def move(self):
        self.x += e_missile_speed
             
    def draw(self):
        screen.blit(badguy_image, (self.x, self.y))

    def off_screen(self):
        if (self.y < -8):
            return True
        elif (self.y > 728):
            return True
        elif (self.x < -8):
            return True
        elif (self.x > 1288):
            return True

    def touching_m(self, missiles):
        return self.y < missiles.y + 26 and missiles.y < self.y + 25 and self.x < missiles.x + 8 and missiles.x < self.x + 25

    def touching_c(self, caracter):
        return self.y < caracter.y + 30 and caracter.y < self.y + 25 and self.x < caracter.x + 30 and caracter.x < self.x + 25

class Badguy_Right: #포탑 미사일(오른쪽 방향)
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 0

    def move(self):
        self.x -= e_missile_speed
             
    def draw(self):
        screen.blit(badguy_image, (self.x, self.y))

    def off_screen(self):
        if (self.y < -8):
            return True
        elif (self.y > 728):
            return True
        elif (self.x < -8):
            return True
        elif (self.x > 1288):
            return True

    def touching_m(self, missiles):
        return self.y < missiles.y + 26 and missiles.y < self.y + 25 and self.x < missiles.x + 8 and missiles.x < self.x + 25

    def touching_c(self, caracter):
        return self.y < caracter.y + 30 and caracter.y < self.y + 25 and self.x < caracter.x + 30 and caracter.x < self.x + 25

class Portal: #포탈 클래스
    def __init__(self):
        self.x = 640
        self.y = 20
        self.type = False #기본 타입은 False로

    def act_draw(self): #활성화 된 포탈 이미지 그리기
        if stage == 9:
            screen.blit(boss_portal_image, (self.x, self.y))

        else: 
            screen.blit(portal_image, (self.x, self.y))

    def un_act_draw(self): #비 활성화 된 포탈 이미지 그리기
        screen.blit(un_portal_image, (self.x, self.y))

    def touch(self): #포탈과 닿았을 때(캐릭터: 40*40, 포탈: 40*40)
        if (self.y < character.y + 40 and character.y < self.y + 40 and self.x < character.x + 40 and character.x < self.x + 40):
            return True

class Treasure: #보물상자 클래스
    def __init__(self):
        self.x = 800
        self.y = 20
        self.act = False #기본으로 False

    def draw(self):
        screen.blit(treasure_image, (self.x, self.y))

    def touch(self): #포탈과 닿았을 때(캐릭터: 40*40, 상자: 40*40)
        return (self.y < character.y + 40 and character.y < self.y + 40 and self.x < character.x + 40 and character.x < self.x + 40)

    def reward(self, rewards): #보물상자 보상
        global rewards_text
        global missile_speed

        if rewards == 1:
            character.hp += 3
            rewards_text = font2.render('hp 3 recovery', True, (0,0,0))

        if rewards == 2:
            rewards_text = font2.render('attac speed up', True, (0,0,0))
            character.attac_speed -= 0.2

        if rewards == 3:
            rewards_text = font2.render('damage up', True, (0,0,0))
            character.damage += 2

        if rewards == 4:
            rewards_text = font2.render('shot speed up', True, (0,0,0))
            missile_speed += 10


class Stage: #스테이지 클래스
    def __init__(self):
        self.x = 0
        self.y = 0

    def homescreen(self): #게임 메인화먄(시작화면)
        screen.blit(homescreen_image, (self.x, self.y))
        Button(start_image,780,520,313,97,start_image,780,530,'start')
        Button(how_to_butten_image,210,520,313,97,how_to_butten_image,210,530,'howto')

    def clearscreen(self): #게임 클리어 화면
        screen.blit(clearscreen_image, (self.x, self.y))
        Button(replay_image,210,520,313,97,replay_image,210,520,'replay')
        Button(end_image,780,520,313,97,end_image,780,520,'end')

    def howtoplayscreen(self): #게임 설명탭 화면
        screen.blit(howtoplay_image, (self.x, self.y))
        Button(start_image,880,520,313,97,start_image,880,530,'start')

    #스테이지 편하게 말들기 위한 함수들
    def makeWall_garo(self, x, y, i):
        for z in range (0, i+1):   
            walls.append(Wall(x + 40 * z, y))

    def makeWall_sero(self, x, y, i):
        for z in range (0, i+1):   
            walls.append(Wall(x, y + 40 * z))

    #각 스테이지들에서의 오브젝트 배치
    def stage1(self):

        Map.makeWall_garo(40*8,40*4,1)
        Map.makeWall_garo(40*8,40*5,1)
        Map.makeWall_garo(40*8,40*8,1)
        Map.makeWall_garo(40*8,40*9,1)
        Map.makeWall_garo(40*8,40*12,1)
        Map.makeWall_garo(40*8,40*13,1)
        
        Map.makeWall_garo(40*22,40*4,1)
        Map.makeWall_garo(40*22,40*5,1)
        Map.makeWall_garo(40*22,40*8,1)
        Map.makeWall_garo(40*22,40*9,1)
        Map.makeWall_garo(40*22,40*12,1)
        Map.makeWall_garo(40*22,40*13,1)
        
        Map.makeWall_garo(40*12,40*7,1)
        Map.makeWall_garo(40*17,40*10,1)
        Map.makeWall_garo(40*12,40*13,1)

        enemys.append(Enemy(40*13, 40*4))
        enemys.append(Enemy(40*17, 40*7))
        enemys.append(Enemy(40*13, 40*10))

    def stage2(self):
        
        Map.makeWall_garo(40*8,40*3,2)
        Map.makeWall_sero(40*8,40*4,3)
        Map.makeWall_sero(40*10,40*4,3)
        Map.makeWall_garo(40*4,40*7,3)
        Map.makeWall_sero(40*4,40*8,1)
        Map.makeWall_garo(40*5,40*9,3)
        Map.makeWall_sero(40*8,40*10,3)
        Map.makeWall_garo(40*9,40*13,1)
        Map.makeWall_sero(40*10,40*9,3)

        Map.makeWall_garo(40*21,40*3,2)
        Map.makeWall_sero(40*23,40*4,3)
        Map.makeWall_sero(40*21,40*4,3)
        Map.makeWall_garo(40*24,40*7,3)
        Map.makeWall_sero(40*27,40*8,1)
        Map.makeWall_garo(40*23,40*9,3)
        Map.makeWall_sero(40*23,40*10,3)
        Map.makeWall_garo(40*21,40*13,1)
        Map.makeWall_sero(40*21,40*9,3)

        Map.makeWall_garo(40*15,40*8,1)

        enemys.append(Enemy(40*9, 40*4))
        enemys.append(Enemy(40*5, 40*8))

        enemys.append(Enemy(40*26, 40*8))
        enemys.append(Enemy(40*22, 40*12))



    def stage3(self):

        Map.makeWall_sero(40*7,40*0,8)
        Map.makeWall_sero(40*24,40*0,8)
        Map.makeWall_sero(40*10,40*8,4)
        Map.makeWall_sero(40*21,40*8,4)
        Map.makeWall_garo(40*4,40*4,1)
        Map.makeWall_garo(40*26,40*4,1)
        Map.makeWall_garo(40*0,40*13,7)
        Map.makeWall_garo(40*24,40*13,7)
        Map.makeWall_garo(40*15,40*14,1)

        enemys.append(Enemy(40*5,40*2))
        enemys.append(Enemy(40*1,40*6))
        enemys.append(Enemy(40*4,40*12))
        enemys.append(Enemy(40*9,40*9))

        enemys.append(Enemy(40*15,40*9))
        enemys.append(Enemy(40*16,40*9))

        enemys.append(Enemy(40*22,40*9))
        enemys.append(Enemy(40*27,40*12))
        enemys.append(Enemy(40*26,40*2))
        enemys.append(Enemy(40*30,40*6))

        enemys.append(Enemy(40*10,40*4))
        enemys.append(Enemy(40*21,40*4))

    def stage4(self):

        Map.makeWall_garo(40*0,40*17,14)
        Map.makeWall_garo(40*18,40*17,13)
        
        Map.makeWall_garo(40*0,40*15,13)
        Map.makeWall_garo(40*15,40*15,5)
        Map.makeWall_garo(40*22,40*15,9)

        Map.makeWall_garo(40*0,40*13,3)
        Map.makeWall_garo(40*5,40*13,26)

        Map.makeWall_garo(40*1,40*11,20)
        Map.makeWall_garo(40*22,40*11,9)

        Map.makeWall_garo(40*0,40*9,31)

        Map.makeWall_garo(40*0,40*7,14)
        Map.makeWall_garo(40*16,40*7,15)

        Map.makeWall_garo(40*1,40*5,29)

        Map.makeWall_garo(40*0,40*3,14)
        Map.makeWall_garo(40*16,40*3,7)
        Map.makeWall_garo(40*25,40*3,6)

        enemys.append(Enemy(40*29,40*16))

        enemys.append(Enemy(40*8,40*14))

        enemys.append(Enemy(40*11,40*12))
        enemys.append(Enemy(40*18,40*12))
        enemys.append(Enemy(40*26,40*12))

        enemys.append(Enemy(40*15,40*8))

        enemys.append(Enemy(40*5,40*6))
        enemys.append(Enemy(40*20,40*6))
        enemys.append(Enemy(40*26,40*6))

        enemys.append(Enemy(40*9,40*4))
        

    def stage5(self):

        Map.makeWall_garo(40*14,40*13,3)
        Map.makeWall_garo(40*14,40*14,3)
        
        Map.makeWall_garo(40*4,40*12,0)

        Map.makeWall_garo(40*10,40*7,1)

        Map.makeWall_garo(40*7,40*4,3)

        Map.makeWall_sero(40*16,40*7,3)

        Map.makeWall_garo(40*22,40*7,0)

        Map.makeWall_sero(40*24,40*13,4)

        Map.makeWall_garo(40*27,40*13,0)

        Map.makeWall_sero(40*27,40*2,4)
        Map.makeWall_sero(40*29,40*2,4)

        enemys.append(Enemy(40*4,40*6))
        enemys.append(Enemy(40*4,40*8))
        enemys.append(Enemy(40*6,40*2))
        enemys.append(Enemy(40*10,40*12))
        enemys.append(Enemy(40*13,40*3))
        enemys.append(Enemy(40*13,40*4))
        enemys.append(Enemy(40*13,40*5))
        enemys.append(Enemy(40*13,40*6))
        enemys.append(Enemy(40*18,40*2))
        enemys.append(Enemy(40*18,40*3))
        enemys.append(Enemy(40*19,40*3))
        enemys.append(Enemy(40*22,40*2))
        enemys.append(Enemy(40*25,40*13))
        enemys.append(Enemy(40*28,40*2))
        enemys.append(Enemy(40*28,40*3))
        enemys.append(Enemy(40*28,40*4))
        enemys.append(Enemy(40*28,40*5))
        enemys.append(Enemy(40*28,40*6))

    def stage6(self):
        enemys.append(Enemy(640, 320))
        enemys.append(Enemy(640, 320))

        enemys.append(Enemy(1040, 320))
        enemys.append(Enemy(1040, 160))
        enemys.append(Enemy(240, 160))
        enemys.append(Enemy(240, 320))
        enemys.append(Enemy(1040, 480))
        enemys.append(Enemy(240, 480))
        
        Map.makeWall_garo(160,560,11)
        Map.makeWall_garo(680,560,11)
        Map.makeWall_garo(160,240,11)
        Map.makeWall_garo(680,240,11)
        Map.makeWall_garo(160,400,11)
        Map.makeWall_garo(680,400,11)
        Map.makeWall_garo(160,80,11)
        Map.makeWall_garo(680,80,11)
        Map.makeWall_sero(600,80,12)
        Map.makeWall_sero(680,80,12)
        

    def stage7(self):
        enemys.append(Enemy(1080, 200))
        enemys.append(Enemy(1080, 440))
        enemys.append(Enemy(160, 200))
        enemys.append(Enemy(160, 440))

        
        Map.makeWall_garo(0,160,3)
        Map.makeWall_garo(200,160,10)
        Map.makeWall_garo(0,240,3)
        Map.makeWall_garo(200,240,10)
        Map.makeWall_garo(720,160,8)
        Map.makeWall_garo(1120,160,5)
        Map.makeWall_garo(720,240,8)
        Map.makeWall_garo(1120,240,5)
        
        Map.makeWall_garo(0,400,3)
        Map.makeWall_garo(200,400,10)
        Map.makeWall_garo(0,480,3)
        Map.makeWall_garo(200,480,10)
        Map.makeWall_garo(720,400,8)
        Map.makeWall_garo(1120,400,5)
        Map.makeWall_garo(720,480,8)
        Map.makeWall_garo(1120,480,5)
        
        Map.makeWall_sero(600,480,5)
        Map.makeWall_sero(680,480,5)
        Map.makeWall_sero(600,240,4)
        Map.makeWall_sero(680,240,4)
        Map.makeWall_sero(600,0,4)
        Map.makeWall_sero(680,0,4)

    def stage8(self):
        enemys.append(Enemy(480, 200))
        enemys.append(Enemy(480, 320))
        enemys.append(Enemy(400, 240))
        enemys.append(Enemy(400, 280))
        enemys.append(Enemy(360, 240))
        enemys.append(Enemy(360, 280))
        enemys.append(Enemy(280, 200))
        enemys.append(Enemy(280, 320))
        
        enemys.append(Enemy(880, 240))
        enemys.append(Enemy(880, 280))
        enemys.append(Enemy(920, 240))
        enemys.append(Enemy(920, 280))
        enemys.append(Enemy(800, 200))
        enemys.append(Enemy(800, 320))
        enemys.append(Enemy(1000, 200))
        enemys.append(Enemy(1000, 320))

        Map.makeWall_garo(280,480,18)
        Map.makeWall_sero(640,120,9)
        Map.makeWall_sero(1120,320,9)
        Map.makeWall_sero(160,320,9)

    def stage9(self):
        enemys.append(Enemy(440, 200))
        enemys.append(Enemy(440, 440))
        enemys.append(Enemy(240, 200))
        enemys.append(Enemy(240, 440))
        enemys.append(Enemy(840, 200))
        enemys.append(Enemy(840, 440))
        enemys.append(Enemy(1040, 200))
        enemys.append(Enemy(1040, 440))

        Map.makeWall_garo(200,120,21)
        Map.makeWall_sero(600,120,3)
        Map.makeWall_sero(680,120,3)
        Map.makeWall_sero(400,120,3)
        Map.makeWall_sero(480,120,3)
        Map.makeWall_sero(200,120,3)
        Map.makeWall_sero(280,120,3)
        Map.makeWall_sero(800,120,3)
        Map.makeWall_sero(880,120,3)
        Map.makeWall_sero(1000,120,3)
        Map.makeWall_sero(1080,120,3)
        Map.makeWall_sero(600,360,9)
        Map.makeWall_sero(680,360,9)
        Map.makeWall_sero(400,360,9)
        Map.makeWall_sero(480,360,9)
        Map.makeWall_sero(200,360,9)
        Map.makeWall_sero(280,360,9)
        Map.makeWall_sero(800,360,9)
        Map.makeWall_sero(880,360,9)
        Map.makeWall_sero(1000,360,9)
        Map.makeWall_sero(1080,360,9)

    def stage10(self):
        Map.makeWall_sero(0,0,18)
        Map.makeWall_sero(40,0,18)
        Map.makeWall_sero(80,0,18)
        Map.makeWall_sero(120,0,18)
        Map.makeWall_sero(160,0,18)
        Map.makeWall_sero(200,0,18)
        Map.makeWall_garo(240,0,6)
        Map.makeWall_garo(240,40,6)

        Map.makeWall_sero(1240,0,18)
        Map.makeWall_sero(1200,0,18)
        Map.makeWall_sero(1160,0,18)
        Map.makeWall_sero(1120,0,18)
        Map.makeWall_sero(1080,0,18)
        Map.makeWall_sero(1040,0,18)
        Map.makeWall_garo(800,0,6)
        Map.makeWall_garo(800,40,6)

        boss.append(Boss(480, -50))

class Button: #버튼 클래스
    def __init__(self, img_in, x, y, width, height, img_act, x_act, y_act, type):
        mouse = pygame.mouse.get_pos()

        if type == 'start':
            start_rect.left = x
            start_rect.top = y

        elif type == 'end':
            end_rect.left = x
            end_rect.top = y

        elif type == 'replay':
            replay_rect.left = x
            replay_rect.top = y

        elif type == 'howto':
            how_to_butten_rect.left = x
            how_to_butten_rect.top = y

        if x + width > mouse[0] > x and y + height > mouse[1] > y: #이미지 위에 마우스를 올리면 이미지 좌표 바꿔주기
            screen.blit(img_act,(x_act, y_act))
                
        else:
            screen.blit(img_in,(x,y))

character = Character()
portal = Portal()
Map = Stage()
treasure = Treasure() #한번만 쓸것들

badguys = []
enemys = []
walls = []
boss = []
missiles = []
boss_missiles = [] #배열로 여러개 만들것들

####################################################################
#################################################################### 게임루프

while 1:
    dt = clock.tick(60) #초당 프레임수는 60이다.
    pressed_keys = pygame.key.get_pressed() # 코딩 편하게 할려고 미리 써 놓은거 (게임과는 상관 X)

    for event in pygame.event.get():

        if event.type == QUIT:
            sys.exit() # X 누르면 나가기

        if pressed_keys[K_SPACE] and (stage >= 1 and stage <11): #공격속도에 제한 두기

            if (time.time() - stop) > character.attac_speed:

                character.fire() # SPACE 누르면 총알 발사
                pygame.mixer.Sound.play(shot_sound)

                stop = time.time()

    #스테이지 설정들
    if stage == 0: #시작화면 스테이지 값: 0
        Map.homescreen()
        if pygame.mouse.get_pressed()[0] and start_rect.collidepoint(pygame.mouse.get_pos()):
            stage += 1
        elif pygame.mouse.get_pressed()[0] and how_to_butten_rect.collidepoint(pygame.mouse.get_pos()):
            stage = -1

    if stage == -1: #설명탭 스테이지 값: -1
        Map.howtoplayscreen()
        if pygame.mouse.get_pressed()[0] and start_rect.collidepoint(pygame.mouse.get_pos()):
            stage = 1

    if stage == 11 and mapcounter == 11: #클리어 화면 스테이지 값: 11
            enemys.clear()
            badguys.clear()
            walls.clear()
            Map.clearscreen()

            score = (character.hp * 100) - (int(start_time - time.time())) #점수 계산
            if high_score < score:
                    high_score = score

            #점수 화면에 띄우기
            c_txt2 = font3.render(str(int(score)), True, (0, 0, 0))
            c_txt3 = font3.render('Score: ', True, (0, 0, 0))
            c_txt4 = font3.render(str(int(high_score)), True, (0, 0, 0))
            c_txt5 = font3.render('High Score: ', True, (0, 0, 0))

            screen.blit(c_txt2, (325, 400))
            screen.blit(c_txt3, (210, 400))
            screen.blit(c_txt4, (980, 400))
            screen.blit(c_txt5, (780, 400))

            boss_music_loop.stop()
            pygame.mixer.Sound.play(clear_sound)
            mapcounter += 1
            while 1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        sys.exit() # X누르면 나가기

                if pygame.mouse.get_pressed()[0] and replay_rect.collidepoint(pygame.mouse.get_pos()):
                    last_fire = 0
                    stage = 0
                    score = 0
                    mapcounter = 1
                    missile_speed = 10
                    character = Character()
                    portal = Portal()
                    Map = Stage()
                    treasure = Treasure()
                    badguys = []
                    enemys = []
                    walls = []
                    boss = []
                    missiles = []
                    boss_missiles = []
                    Map.homescreen()
                    time.sleep(0.5)
                    break

                elif pygame.mouse.get_pressed()[0] and end_rect.collidepoint(pygame.mouse.get_pos()):
                    sys.exit()
                    
                pygame.display.update() #화면에 나타내기
    
    if stage > 0:
        screen.fill((239, 228, 176)) #화면 색 채우기
        character.move(walls)
        character.draw()

        if stage == 1 and mapcounter == 1:
            start_time = time.time()
            Map.stage1()
            treasure_txt = False
            mapcounter += 1

            #3..2..1 타이머
            while (time.time() - start_time <= 3):
                if time.time() - start_time <= 1 and time.time() - start_time >= 0:
                    screen.fill((239, 228, 176))
                    screen.blit(three_image, (500, 110))

                if time.time() - start_time <= 2 and time.time() - start_time >= 1:
                    screen.fill((239, 228, 176))
                    screen.blit(two_image, (500, 110))

                if time.time() - start_time <= 3 and time.time() - start_time >= 2:
                    screen.fill((239, 228, 176))
                    screen.blit(one_image, (500, 110))
                pygame.display.update()
            
            stage_music_loop = pygame.mixer.Sound(stage_music)
            stage_music_loop.play(-1) #음악 반복 재생

        if stage == 2 and mapcounter == 2:
            Map.stage2()
            mapcounter += 1
            character.hp += 1
            treasure.act = False
            treasure_txt = False

        if stage == 3 and mapcounter == 3:
            Map.stage3()
            mapcounter += 1
            character.hp += 1
            treasure.act = True #3배수 스테이지 마다 보물상자 출현
            treasure_txt = False

        if stage == 4 and mapcounter == 4:
            Map.stage4()
            mapcounter += 1
            character.hp += 1
            treasure.act = False
            treasure_txt = False

        if stage == 5 and mapcounter == 5:
            Map.stage5()
            mapcounter += 1
            character.hp += 1
            treasure.act = False
            treasure_txt = False

        if stage == 6 and mapcounter == 6:
            Map.stage6()
            mapcounter += 1
            character.hp += 1
            treasure.act = True
            treasure_txt = False

        if stage == 7 and mapcounter == 7:
            Map.stage7()
            mapcounter += 1
            character.hp += 1
            treasure.act = False
            treasure_txt = False

        if stage == 8 and mapcounter == 8:
            Map.stage8()
            mapcounter += 1
            character.hp += 1
            treasure.act = False
            treasure_txt = False

        if stage == 9 and mapcounter == 9:
            Map.stage9()
            mapcounter += 1
            character.hp += 1
            treasure.act = True
            treasure_txt = False

        if stage == 10 and mapcounter == 10:
            Map.stage10()
            mapcounter += 1
            character.hp += 1
            treasure.act = False
            treasure_txt = False

            stage_music_loop.stop() #보스전이 아닌 스테이지의 Bgm 끄기

            boss_music_loop = pygame.mixer.Sound(Boss_music)
            boss_music_loop.play(-1) #보스전 음악 반복재생

        #포탈 관련: 적들이 다 죽어야 포탈이 열림
        if len(enemys) != 0 or len(boss) != 0:
            portal.un_act_draw()

        if len(enemys) == 0 and len(boss) == 0:
            portal.type = True
            portal.act_draw()

        #포탈 관련: 닿으면 캐릭터를 리스폰 위치로 옮기고 스테이지 1 증가
        if portal.touch() and portal.type == True:
            pygame.mixer.Sound.play(portal_sound)
            stage += 1
            character.respawn()
            enemys.clear()
            badguys.clear()
            walls.clear()
            missiles.clear()
            portal.type = False

        #보물상자 관련: 적들이 다 죽고 보물상자 조건(3배수 스테이지)어야 생성
        if ((len(enemys) == 0) and (treasure.act == True)):
            treasure.draw()

            if treasure.touch():
                pygame.mixer.Sound.play(treasure_sound)
                rewards = (random.randint(1,4)) #보상 랜덤 뽑기
                treasure.reward(rewards)
                treasure.act = False
                treasure_txt = True
        
        #보물상자 관련: 3배수 스테이지일 때, 보물상자 보상 효과 띄우기
        if treasure_txt:
                screen.blit(rewards_text, (1130,0))

        e = 0 # 포탑 판단
        while e < len(enemys):
            m_ = 0
            enemys[e].draw()

            while m_ < len(missiles): #캐릭터의 미사일과 충돌하면 체력 1 감소
                if enemys[e].hit(missiles[m_]):
                    enemys[e].hp -= (1 + character.damage)
                    del missiles[m_]
                    j -= 1
                m_ += 1
            
            if time.time() - enemys[e].last_badguy_spawn_time > 1.5: #만약 포탑 사정거리 범위 내에 캐릭터가 있다면
                if (character.x - fire_range < enemys[e].x and character.x + fire_range + 40 > enemys[e].x + 40) or (character.y - fire_range < enemys[e].y and character.y + fire_range + 40 > enemys[e].y + 40):
                    
                    enemys[e].fire()
                    enemys[e].last_badguy_spawn_time = time.time()

            if enemys[e].hp <= 0: #체력이 0이하가 되면 삭제
                    del enemys[e]
            e += 1

        i = 0 #포탑 총알 판단: 그리기, 화면 넘어가면 삭제
        while i < len(badguys):
            badguys[i].move()
            badguys[i].draw()

            if badguys[i].off_screen():
                del badguys[i]
                i -= 1
            i += 1

        i = 0 #포탑 총알 판단: 미사일과 충돌했을 때 삭제
        while i < len(badguys):
            j = 0

            while j < len(missiles):

                if badguys[i].touching_m(missiles[j]):
                    del badguys[i]
                    del missiles[j]
                    i -= 1
                    break
                j += 1
            i += 1

        i = 0 #포탑 총알 판단: 캐릭터와 충돌 했을 때 hp감소, 삭제
        while i < len(badguys):
            if badguys[i].touching_c(character): #만약 포탑 총알과 캐릭터가 닿았다면
                del badguys[i]
                character.hp -= 1
                i -= 1
            i += 1

        b = 0 #보스 판단
        while b < len(boss):
            m_ = 0
            boss[b].draw()

            while m_ < len(missiles): #미사일과 보스가 닿으면 hp 1 감소
                if boss[b].hit(missiles[m_]):
                    boss[b].hp -= (1 + character.damage)
                    del missiles[m_]
                    j -= 1
                m_ += 1

            if time.time() - boss[b].last_badguy_spawn_time > 1:
                boss[b].fire_big()
                boss[b].fire_small()
                boss[b].last_badguy_spawn_time = time.time()

            if boss[b].hp <= 0: #보스 체력이 0 이하가 되면 삭제
                    del boss[b]
            b += 1

        ib = 0 #보스 총알 판단: 그리기, 화면 넘어가면 삭제
        while ib < len(boss_missiles):
            boss_missiles[ib].move()
            boss_missiles[ib].draw()
            if boss_missiles[ib].off_screen():
                del boss_missiles[ib]
                ib -= 1
            ib += 1
        
        ib = 0 #보스 총알 판단: 캐릭터와 충돌 했을 때 hp감소, 삭제
        while ib < len(boss_missiles):
            if boss_missiles[ib].touching_c(character):
                del boss_missiles[ib]
                character.hp -= 1
                ib -= 1
            ib += 1

        w = 0 # 벽 판단: 그리기, 캐릭터 미사일과 충돌 했을 대 hp 감소, 삭제
        while w < len(walls):
            m = 0
            index = 0
            walls[w].draw()
            
            while m < len(missiles): #미사일과 충돌했을 때 hp 감소
                if walls[w].hit(missiles[m]):
                    walls[w].hp -= (1 + character.damage)
                    del missiles[m]
                    j -= 1
                
                if walls[w].hp <= stage * 6 / 2: #벽의 체력(stage * 6)이 절반이 되면 금간 이미지로 변경
                    walls[w].wall_state=wall_broken
                m += 1

            if walls[w].hp <= 0: #벽 체력이 0 이하가 되면 삭제(밑에도 추가하면 리스트 오류남)
                del walls[w]
            w += 1

        w = 0 # 벽 판단: 그리기, 포탑 미사일과 충돌 했을 대 hp 감소, 삭제
        while w < len(walls):
            index = 0
            walls[w].draw()
            
            while index < len(badguys):
                if walls[w].hit(badguys[index]):
                    walls[w].hp -= 1
                    del badguys[index]
                    j -= 1
                
                if walls[w].hp <= stage * 6 / 2:
                    walls[w].wall_state=wall_broken
                index += 1
            w += 1

        j = 0 #캐릭터 미사일 판단: 그리기, 화면 밖으로 나가면 삭제하기
        while j < len(missiles):
            missiles[j].move()
            missiles[j].draw()
            if missiles[j].off_screen():
                del missiles[j]
                j -= 1
            j += 1

        #기본 인터페이스 정보
        if stage >= 1 and stage <= 10:
            stage_str_text = font3.render('Stage', True, (128,64,64))
            screen.blit(stage_str_text, (10,10))
            stage_text = font3.render(str(int(stage)), True, (128,64,64))
            screen.blit(stage_text, (110,10))

            hp_str_text = font3.render('HP', True, (255,128,128))
            screen.blit(hp_str_text, (10,60))
            hp_text = font3.render(str(int(character.hp)), True, (255,128,128))
            screen.blit(hp_text, (70,60))

        #캐릭터의 체력이 0이되어 게임 오버되었을 때 각종 게임 정보들 화면에 띄우기
        if character.hp <= 0:
            mapcounter = 13
            if mapcounter == 13:
                score = (character.hp * 100) - (int(start_time - time.time()))

                if high_score < score:
                    high_score = score

                screen.blit(GAME_OVER, (0, 230)) #게임 오버 이미지 띄우기
                txt = font2.render('Press R key to restart', True, (255, 0, 0))
                txt2 = font2.render(str(int(score)), True, (255, 0, 0))
                txt3 = font2.render('Score: ', True, (255, 0, 0))
                txt4 = font2.render(str(int(high_score)), True, (255, 0, 0))
                txt5 = font2.render('High Score: ', True, (255, 0, 0))

                screen.blit(txt, (1000, 450)) #R키를 누르면 재시작 합니다 띄우기, 점수 띄우기
                screen.blit(txt2, (170, 450))
                screen.blit(txt3, (100, 450))
                screen.blit(txt4, (370, 450))
                screen.blit(txt5, (250, 450))

                # 게임 오버 화면에서의 루프문
                while 1:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            sys.exit()
                    
                    again_key = pygame.key.get_pressed() #R키 누르면 각종 변수들 초기화 후 다시시작(게임오버 창 나가면 메인루프)
                    if again_key[K_r]:
                        if stage > 0 and stage < 10:
                            stage_music_loop.stop()

                        if stage == 10:
                            boss_music_loop.stop()
                        
                        last_fire = 0
                        stage = 0
                        score = 0
                        mapcounter = 1
                        missile_speed = 10
                        character = Character()
                        portal = Portal()
                        Map = Stage()
                        treasure = Treasure()
                        badguys = []
                        enemys = []
                        walls = []
                        boss = []
                        missiles = []
                        boss_missiles = []
                        break
                    mapcounter += 1
                    pygame.display.update() #화면 업데이트

    pygame.display.update() #화면 업데이트