#!/usr/bin/env python
# coding: utf-8

# In[215]:


import random 
import cairo

cells = {}
cell_width = 100 # total cells in a row
cell_length = 100 # total cells in a column
def init_cells():
    """init the cells to zeros."""
    for r in range(cell_width):
        for c in range(cell_length):
            cells[(r,c)] = 0 # 0 reperesent wall, 1 will represent rooms and hallways in the dungeon

class Room:
    """class for rooms in dungeon generation."""
    def __init__(self,r,c,width,length):
        """init attribute for room class."""
        self.r = r
        self.c = c
        self.width = width
        self.length = length
        
    def overlap(room, rooms):
        """check if there is any overlapping between rooms.
        return True if there is overlapping"""
        for _room in rooms:
            r_min_1,r_max_1 = room.r,room.r + room.width
            r_min_2,r_max_2 = _room.r, _room.r + _room.width
            c_min_1, c_max_1 = room.c, room.c + room.length
            c_min_2, c_max_2 = _room.c, _room.c + _room.length
            # check the overlapping conditions
            if (r_min_1 <= r_max_2 and r_max_1 >= r_min_2) and (c_min_1 <= c_max_2 and c_max_1 >= c_min_2):
                return True
        return False
    
    def generate_rooms():
        """generate rooms in the dungeon."""
        total_rooms_cnt = random.randrange(min_rooms_cnt,max_rooms_cnt) # generate max number of rooms randomly
        for i in range(total_rooms_cnt):
            r,c = random.randrange(0,cell_width), random.randrange(0,cell_length)
            width, length = random.randrange(min_room_length,max_room_length), random.randrange(min_room_length,max_room_length)
            room = Room(r,c,width,length)
            # check overlapping between rooms
            if Room.overlap(room, rooms) == False:
                rooms.append(room)
        for room in rooms:
            for r in range(room.r, room.r+room.width):
                for c in range(room.c, room.c+room.length):
                    cells[(r,c)] = 1     
    
    def hallways():
        """draws hallways to connect rooms."""
        for i in range(len(rooms)-1):
            roomA = rooms[i]
            roomB = rooms[i+1]
            for r in range(roomA.r,roomB.r):
                cells[(r,roomA.c)] = 1
            for c in range(roomA.c, roomB.c):
                cells[(roomA.r,c)] = 1
            for r in range(roomB.r,roomA.r):
                cells[(r,roomA.c)] = 1
            for c in range(roomB.c, roomA.c):
                cells[(roomA.r,c)] = 1
                
    def generate_dungeon():
        """highlight the dungeon with cario rectangles."""
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24,1000,1000)
        context = cairo.Context(surface)
        for r in range(cell_width):
            for c in range(cell_length):
                if cells[(r,c)] == 0:
                    context.set_source_rgb(0.0,0.0,0.2) # [0,1]
                else:
                    context.set_source_rgb(1.0,0.0,0.0) # red
                context.rectangle(r*10, c*10, 5, 5) 
                context.fill()
        surface.write_to_png("random_dungeon.png") # generate image

        
# define parameters for this dungeon (room size + number of rooms range)
min_room_length = 5
max_room_length = 10
min_rooms_cnt = 10
max_rooms_cnt = 20
rooms = []

# generate the 2D dungeon by functions sequencially
init_cells()
Room.generate_rooms()
Room.hallways()
Room.generate_dungeon()
    

