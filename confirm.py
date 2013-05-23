#-*-coding: cp1251 -*-
from pygame import *
import os
from pygui import *
form=Form()
form.Elements=[]
form.width=290
form.height=50
form.background=(210,210,210)
x_form=1024/2-form.width/2
y_form=768/2-form.height/2
form.position=(x_form,y_form)

SAVE_BUT=0
DONT_SAVE=1
CANCEL=2


button01=Button()
a=button01
a.text="Сохранить"
text=unicode(a.text,encoding='cp1251')
text_surf=Font3.render(text,1,bl,wh)
w_text=text_surf.get_width()
a.position=(15,20)
a.width=w_text+8
a.height=20
x=a.position[0]
y=a.position[1]
w=a.width
h=a.height
a.background=Rect((x-3, y-3, w+3, h+3))
a.border=Rect((x-3, y-3, w+3, h+3))
a.shadow=Rect((x-2, y-2, w+2, h+2))
form.Elements.append(a)

button02=Button()
a=button02
a.text="Не сохранять"
text=unicode(a.text,encoding='cp1251')
text_surf=Font3.render(text,1,bl,wh)
w_text=text_surf.get_width()
a.position=(105,20)
a.width=w_text+8
a.height=20
x=a.position[0]
y=a.position[1]
w=a.width
h=a.height
a.background=Rect((x-3, y-3, w+3, h+3))
a.border=Rect((x-3, y-3, w+3, h+3))
a.shadow=Rect((x-2, y-2, w+2, h+2))
form.Elements.append(a)

button03=Button()
a=button03
a.text="Отмена"
text=unicode(a.text,encoding='cp1251')
text_surf=Font3.render(text,1,bl,wh)
w_text=text_surf.get_width()
a.position=(215,20)
a.width=w_text+8
a.height=20
x=a.position[0]
y=a.position[1]
w=a.width
h=a.height
a.background=Rect((x-3, y-3, w+3, h+3))
a.border=Rect((x-3, y-3, w+3, h+3))
a.shadow=Rect((x-2, y-2, w+2, h+2))
form.Elements.append(a)

form.Focus=(-1,0)

sc=display.set_mode((1024,768))
sc.fill(wh)
going=True

form.Render()

def quit(mymap):
	mymap.sc.blit(mymap.Background,(0,0))
	display.update()
	mymap.BackWasSaved=False
	mymap.NeedUpdate=True
	mymap.FormFlag=False

def dispatcher(mymap,e):
	mymap.sc.blit(form.MainSurf,(form.position))# Делать это только когда флаг необходимости установлен
	display.flip()# каждый раз???
	if e.type==MOUSEBUTTONDOWN:
		form.Focus=form.getObj(e)
		# print "form.Focus[0]",form.Focus[0]
		if form.Focus[0]==SAVE_BUT:# Сохранить кнопка
			mymap.SaveAndExit=True
			quit(mymap)
		elif form.Focus[0]==CANCEL:# отмена кнопка
			quit(mymap)
		elif form.Focus[0]==DONT_SAVE:
			mymap.Exit=True
			quit(mymap)
		else:
			form.Control(e)
	if e.type==MOUSEBUTTONUP:
		pass
	if e.type==KEYDOWN:
		if e.key==K_ESCAPE:
			# going=False
			quit(mymap)
		form.Control(e)
	if e.type==MOUSEMOTION:
		pass
	return mymap