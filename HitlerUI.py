# -*- coding: utf-8 -*-


import pygame as p
import pandas as pd
import numpy as np
import time
import math
from HitlerModels import *

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)
grey = (200, 200, 200)


(width, height) = (720, 720)
fps = 30


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


p.init()
p.display.set_caption('SecretHitler')
screen = p.display.set_mode((width, height))
p.display.flip()


MainMenu = True
Flash = False
Page2 = False
Zero_order = False
First_order = False
Second_order = False

val = 5
clock = p.time.Clock()


def take_input():
    global val

    events = p.event.get()
    for event in events:
        if event.type == p.KEYDOWN:
            keys = p.key.get_pressed()

            if keys[p.K_5]:
                val = 5
            if keys[p.K_6]:
                val = 6
            if keys[p.K_7]:
                val = 7
            if keys[p.K_8]:
                val = 8
            if keys[p.K_9]:
                val = 9


class Player_unit():
    def __init__(self, pos, unit_number):
        self.pos = pos
        self.unit_number = unit_number

    def draw(self, name):
        if name == 'fascist':

            p.draw.circle(screen, red, self.pos, 20)
        if name == 'liberal':
            p.draw.circle(screen, blue, self.pos, 20)
        if name == 'president':
            p.draw.circle(screen, yellow, self.pos, 20)
            largeText = p.font.Font('freesansbold.ttf', 10)
            TextSurf, TextRect = text_objects("P", largeText, black)
            TextRect.center = self.pos
            screen.blit(TextSurf, TextRect)
        if name == 'chancellor':
            p.draw.circle(screen, white, self.pos, 20)
            largeText = p.font.Font('freesansbold.ttf', 10)
            TextSurf, TextRect = text_objects("C", largeText, black)
            TextRect.center = self.pos
            screen.blit(TextSurf, TextRect)


class Game_Manager():
    def __init__(self, n_players, game_object):
        self.game_object = game_object
        self.n_players = n_players
        center = (720//2, 720//2)
        radius = 200
        self.spots = []
        self.players = []
        for i in range(self.n_players):

            self.spots.append((int(radius*math.cos(i*((2*math.pi)/self.n_players))+center[0]),
                               int(radius*math.sin(i*((2*math.pi)/self.n_players))+center[1])))

            self.players.append(Player_unit(self.spots[-1], i))

    def draw(self):
        for i in range(self.n_players):
            if self.game_object.president == i:

                self.players[i].draw('president')
                continue
            if self.game_object.chancellor == i:
                self.players[i].draw('chancellor')
                continue
            if self.game_object.is_liberal(i):
                self.players[i].draw('liberal')
            if self.game_object.is_fascist(i):
                self.players[i].draw('fascist')
        self.draw_state()
        self.draw_score()

    def draw_state(self):
        largeText = p.font.Font('freesansbold.ttf', 30)
        TextSurf, TextRect = text_objects(
            self.game_object.game_state, largeText, red)
        TextRect.center = (360, 100)
        screen.blit(TextSurf, TextRect)

    def draw_score(self):
        largeText = p.font.Font('freesansbold.ttf', 20)

        TextSurf, TextRect = text_objects(
            str(self.game_object.liberal_wins), largeText, blue)
        TextRect.center = (275, 678)
        screen.blit(TextSurf, TextRect)

        TextSurf, TextRect = text_objects(
            str(self.game_object.fascist_wins), largeText, red)
        TextRect.center = (575, 678)
        screen.blit(TextSurf, TextRect)


class Menu_Button():
    def __init__(self, name, pos, img_name):
        self.name = name
        self.pos = pos
        self.img = img_name

    def draw(self, mouse):

        button = p.image.load(self.img)
        button = p.transform.scale(button, (150, 50))
        screen.blit(button, self.pos)
        if (mouse[0] > self.pos[0]) and mouse[0] < self.pos[0]+100 and mouse[1] > self.pos[1] and mouse[1] < self.pos[1]+50:
            p.draw.rect(
                screen, blue, (self.pos[0]+3, self.pos[1]+3, 144, 44), 2)
            a = p.mouse.get_pressed()
            if a[0] == 1:
                print(self.name)
                self.click()

    def click(self):
        global MainMenu, Page2, Zero_order, First_order, Second_order
        if self.name == "Start":
            # time.sleep(0.5)
            MainMenu = False
            Page2 = True
            time.sleep(0.5)
            return
        if self.name == "Exit":
            time.sleep(0.5)
            MainMenu = False
            Page2 = False
            return

        if self.name == 'zero_order':
            time.sleep(0.5)
            MainMenu = False
            Page2 = False
            Zero_order = True
            return
        if self.name == 'first_order':
            time.sleep(0.5)
            MainMenu = False
            Page2 = False
            First_order = True
            return
        if self.name == 'second_order':
            time.sleep(0.5)
            MainMenu = False
            Page2 = False
            Second_order = True
            return


def run_ui():
    global Flash, clock, MainMenu, Page2, Zero_order, First_order, Second_order
    flash_count = 0
    Start = Menu_Button("Start", (275, 300), 'sh_start_b.png')
    Exit = Menu_Button("Exit", (275, 400), 'sh_exit_b.png')
    z_o = Menu_Button("zero_order", (275, 400), 'z_o.png')
    f_o = Menu_Button("first_order", (275, 500), 'f_o.png')
    s_o = Menu_Button("second_order", (275, 600), 's_o.png')
    l_score = Menu_Button("l_score", (125, 650), 'l_score.png')
    f_score = Menu_Button("f_score", (425, 650), 'f_score.png')
    while MainMenu:
        mouse = p.mouse.get_pos()
        clock.tick(fps)
        screen.fill(black)
        title = p.image.load('sh_title.png')
        screen.blit(title, (130, 100))

        Start.draw(mouse)
        Exit.draw(mouse)
        p.display.flip()
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
                p.display.quit()
                p.quit()

    while Page2:
        #print("Inside Page 2")

        mouse = p.mouse.get_pos()
        clock.tick(fps)
        screen.fill(black)
        title = p.image.load('sh_np.png')
        screen.blit(title, (110, 100))
        p.draw.rect(screen, grey, (330, 300, 44, 44))
        p.draw.rect(screen, green, (330, 300, 44, 44), 2)
        take_input()
        largeText = p.font.Font('freesansbold.ttf', 20)
        TextSurf, TextRect = text_objects(str(val), largeText, black)
        TextRect.center = (330+22, 300+22)
        screen.blit(TextSurf, TextRect)
        z_o.draw(mouse)
        f_o.draw(mouse)
        s_o.draw(mouse)

        p.display.flip()
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
                p.display.quit()
                p.quit()

    if Zero_order:

        game_obj = Zero_Order(val)
        manager = Game_Manager(val, game_obj)
    while Zero_order:

        mouse = p.mouse.get_pos()
        clock.tick(fps)
        screen.fill(black)
        manager.draw()
        l_score.draw(mouse)
        f_score.draw(mouse)
        p.display.flip()
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
                p.display.quit()
                p.quit()

    while First_order:
        mouse = p.mouse.get_pos()
        clock.tick(fps)
        screen.fill(black)

        print("Enter First")
        p.display.flip()
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
                p.display.quit()
                p.quit()
    while Second_order:
        mouse = p.mouse.get_pos()
        clock.tick(fps)
        screen.fill(black)

        print("Enter Second")
        p.display.flip()
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
                p.display.quit()
                p.quit()

    p.display.quit()
    p.quit()


run_ui()
