#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import time
import random

class Base(object):
    """基类"""

    def __init__(self, x, y, screen, image_name):
        self._x = x
        self._y = y
        self.screen = screen
        self.image = pygame.image.load(image_name)


class BasePlane(Base):
    """创建飞机基类"""

    def __init__(self, x, y, screen, image_name):
        super(BasePlane, self).__init__(x, y, screen, image_name)
        self.bullet_list = []

    def display(self):
        self.screen.blit(self.image, (self._x,self._y))

        bullets_remove = []
        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()
            #判断子弹越界后添加到删除子弹列表，不能直接使用remove删除，否则会出现漏删引起BUG
            #不能在for循环中删除元素，删除元素后，后面的元素就会挤到刚才删除的元素上
            #指针指到新的元素下，下次循环后就会跳过这个最先挤上来的元素导致漏删。
            if bullet.jugde():
                bullets_remove.append(bullet)

        #虽然不可以删除遍历的列表，但是可以删除别的列表，不会导致漏删
        for bullet in bullets_remove:
            self.bullet_list.remove(bullet)


class HeroPlane(BasePlane):
    """
    创建飞机类
    """

    def __init__(self, screen_temp):
        super(HeroPlane, self).__init__(190, 600, screen_temp, "./feiji/hero1.png")

    def move_left(self):
        self._x -= 15

    def move_right(self):
        self._x += 15

    def move_up(self):
        self._y -= 15

    def move_down(self):
        self._y += 15

    def fire(self):
        bullet = Bullet(self._x, self._y, self.screen)
        self.bullet_list.append(bullet)


class EnemyPlane(BasePlane):
    """
    创建敌军类
    """

    def __init__(self, screen_temp):
        super(EnemyPlane, self).__init__(0, 0, screen_temp,
                "./feiji/enemy0.png")
        self.direction = "RIGHT"

    def move(self):
        if self.direction == "RIGHT":
            self._x += 10
        elif self.direction == "LEFT":
            self._x -= 10

        if self._x > 430:
            self.direction = "LEFT"
        elif self._x < 0:
            self.direction = "RIGHT"


    def fire(self):
        random_num = random.randint(1, 60)
        if random_num == 30 or random_num == 50:
            bullet = EnemyBullet(self._x, self._y, self.screen)
            self.bullet_list.append(bullet)


class BaseBullet(Base):
    """子弹基类"""

    def display(self):
        self.screen.blit(self.image, (self._x, self._y))

    def jugde(self):
        if self._y < 0 or self._y > 752:
            return True
        else:
            return False


class Bullet(BaseBullet):
    """
    创建子弹类
    """

    def __init__(self, x, y, screen):
        super(Bullet, self).__init__(x+40, y-10, screen, "./feiji/bullet.png")

    def move(self):
        self._y -= 50


class EnemyBullet(BaseBullet):
    """
    创建敌军子弹类
    """

    def __init__(self, x, y, screen):
        super(EnemyBullet, self).__init__(x+25, y+40, screen, "./feiji/bullet1.png")

    def move(self):
        self._y += 15


def Key_Input(hero):
    """接受键盘的输入"""

    for event in pygame.event.get():
        if event.type == QUIT:
            print("exit:")
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_a or event.key == K_LEFT:
                hero.move_left()
                print("left")
            elif event.key == K_d or event.key == K_RIGHT:
                print("right")
                hero.move_right()
            elif event.key == K_w or event.key == K_UP:
                print("up")
                hero.move_up()
            elif event.key == K_s or event.key == K_DOWN:
                print("down")
                hero.move_down()
            elif event.key == K_SPACE:
                print("space")
                hero.fire()


def main():
    """
    创建飞机主要运行逻辑
    """

    screen = pygame.display.set_mode((480,724), 0, 32)
    background = pygame.image.load("./feiji/background.png")
    #创建一个飞机对象
    hero = HeroPlane(screen)
    #创建一个敌军对象
    enemy = EnemyPlane(screen)

    while True:
        screen.blit(background, (0,0))
        hero.display()

        enemy.display()
        enemy.move()
        enemy.fire()

        #获取键盘输入事件
        Key_Input(hero)
        pygame.display.update()
        time.sleep(0.05)

if __name__ == "__main__":
    main()
