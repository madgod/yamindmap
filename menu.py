#-*-coding: cp1251 -*-
from pygame import *
import os
from pygui import *
menu=Form()
menu.Elements=[]

menu.width=1024
menu.height=30
menu.background=(100,100,250)
menu.position=(0,0)

menu.button01=Button()
a=menu.button01
a.text="New"
a.width=40# Экспериментально полученные значения
a.height=21
a.position=(10, 6)
x=a.position[0]
y=a.position[1]
w=a.width
h=a.height
a.background=Rect((x-3, y-3, w+3, h+3))
a.border=Rect((x-3, y-3, w+3, h+3))
a.shadow=Rect((x-2, y-2, w+2, h+2))
menu.Elements.append(a)

menu.button02=Button()
a=menu.button02
a.text="Open"
a.width=40# Экспериментально полученные значения
a.height=21
a.position=(60, 6)
x=a.position[0]
y=a.position[1]
w=a.width
h=a.height
a.background=Rect((x-3, y-3, w+3, h+3))
a.border=Rect((x-3, y-3, w+3, h+3))
a.shadow=Rect((x-2, y-2, w+2, h+2))
menu.Elements.append(a)

menu.button03=Button()
a=menu.button03
a.text="Save"
a.width=40# Экспериментально полученные значения
a.height=21
a.position=(110, 6)
x=a.position[0]
y=a.position[1]
w=a.width
h=a.height
a.background=Rect((x-3, y-3, w+3, h+3))
a.border=Rect((x-3, y-3, w+3, h+3))
a.shadow=Rect((x-2, y-2, w+2, h+2))
menu.Elements.append(a)

menu.button04=Button()
a=menu.button04
a.text="Help"
a.width=40# Экспериментально полученные значения
a.height=21
a.position=(160, 6)
x=a.position[0]
y=a.position[1]
w=a.width
h=a.height
a.background=Rect((x-3, y-3, w+3, h+3))
a.border=Rect((x-3, y-3, w+3, h+3))
a.shadow=Rect((x-2, y-2, w+2, h+2))
menu.Elements.append(a)

menu.button05=Button()
a=menu.button05
a.text="Prop"
a.width=40# Экспериментально полученные значения
a.height=21
a.position=(210, 6)
x=a.position[0]
y=a.position[1]
w=a.width
h=a.height
a.background=Rect((x-3, y-3, w+3, h+3))
a.border=Rect((x-3, y-3, w+3, h+3))
a.shadow=Rect((x-2, y-2, w+2, h+2))
menu.Elements.append(a)

menu.button06=Button()
a=menu.button06
a.text="Map"
a.width=40# Экспериментально полученные значения
a.height=21
a.position=(260, 6)
x=a.position[0]
y=a.position[1]
w=a.width
h=a.height
a.background=Rect((x-3, y-3, w+3, h+3))
a.border=Rect((x-3, y-3, w+3, h+3))
a.shadow=Rect((x-2, y-2, w+2, h+2))
menu.Elements.append(a)

menu.Render()

def quit(mymap):
	mymap.sc.blit(mymap.Background,(0,0))
	display.update()
	mymap.BackWasSaved=False
	mymap.FormFlag=not mymap.FormFlag
	
def Control(mymap,e):
	id=-1
	if e.type==MOUSEBUTTONDOWN:
		x=e.dict['pos'][0]# получаем Х 
		y=e.dict['pos'][1]# получаем У
		for i in menu.Elements:# можно ректы и заранее сохранить
			r=Rect((i.position),(i.width,i.height))
			if (r.collidepoint(x, y)):
				id=menu.Elements.index(i) 
	return id