#-*-coding: cp1251 -*-
from pygame import *
import os
import core
from pygui import *
form=Form()
form.Elements=[]
form.width=600
form.height=400
form.background=(210,210,210)
form.position=(212,184)

label01=Label()#Сохранить
a=label01
a.text="Сохранить"
a.position=(5,10)
a.background=(210,210,210)
form.Elements.append(a)

label02=Label()# Рабочая папка (Чье содержимое мы видим)
a=label02
a.text="Каталог:"
a.background=(210,210,210)
a.position=(85,36)
form.Elements.append(a)

label03=Label()# Имя файла
a=label03
a.text="Имя файла:"
a.position=(145,335)
a.background=(210,210,210)
form.Elements.append(a)

label04=Label()# Расширение
a=label04
a.text="Тип файла:"
a.position=(145,365)
a.background=(210,210,210)
form.Elements.append(a)

button01=Button()# Сохранить
a=button01
a.text="Сохранить"

a.width=76
a.height=19
a.background=Rect((509, 335, 82, 24))
a.border=Rect((510, 336, 80, 22))
a.shadow=Rect((509, 335, 82, 24))
a.position=(512, 338)
form.Elements.append(a)

button02=Button()# Отмена
a=button02
a.text="Отмена"
a.width=button01.width
a.height=button01.height
a.background=Rect((509, 360, 82, 24))
a.border=Rect((510, 361, 80, 22))
a.shadow=Rect((509, 360, 82, 24))
a.position=(512, 363)
form.Elements.append(a)


textedit01=Textedit()# имя файла
a=textedit01

a.text=['']
a.position=(145+130,335)
a.width=200
a.height=22
a.Wrap=False
a.clearSurf=Surface((a.width,a.height))
a.clearSurf.fill(wh)
form.Elements.append(a)

textedit02=Textedit()# Расширение
a=textedit02
a.position=(145+130,335+28)
a.width=200
a.height=22
a.Wrap=False
a.clearSurf=Surface((a.width,a.height))
a.clearSurf.fill(wh)
form.Elements.append(a)

content01=Content()# Содержимое
a=content01
a.width=445
a.height=259
a.position=(145,56)
path=os.getcwd()
path2=core.GetFilteredDirList(path,".map")
path2.insert(0,"..")
a.path2=path2
a.path=path

a.getList()
form.Dirlist=a.drawList()
a.LASTPAGE=len(path2)/17
form.Elements.append(a)
scrollbar01=Scrollbar()
a=scrollbar01
a.position=(145,314)
a.width=445
a.height=16

a.bar_width=(a.width-32)/(content01.LASTPAGE+1)
scrollbar01.drawBar()
form.Elements.append(a)

label05=Label()# Расширение
a=label05

a.text=form.Elements[CONTENT].path
a.position=(145,36)
a.background=(210,210,210)
form.Elements.append(a)

form.Focus=(6,-1)

form.Render()

def quit(mymap):
	mymap.sc.blit(mymap.Background,(0,0))
	display.update()
	mymap.BackWasSaved=False
	mymap.NeedUpdate=True
	mymap.FormFlag=False
	return mymap


def CheckPermission(form,mymap):
	pass
	if (form.Elements[TEXTEDIT].text)!=['']:
		path=form.Elements[TEXTEDIT].text[0]
		Access=False
		if  len(path)>4 and path[-4:]==".map":
			# print "os.isdir(path)", os.path.isdir(path)
			# СНАЧАЛА - существует или нет, а то не сможем проверить каталог или файл, если файла нет
			if os.path.exists(path):
				if not os.path.isdir(path):
					pass
					# print "NO IT IS FILE"
					# Access=True
				else:
					pass
					# print "IT IS DIR"
			else:
				pass
				# print "NOT EXIST"
			Access=True
		if Access:
			mymap.FlagNeedSaveAs=True
			txt1=form.Elements[CONTENT].path
			txt2=form.Elements[TEXTEDIT].text[0]
			# txt2=txt2.encode('utf-8')
			mymap.PATH=txt1+os.sep+txt2
			# и имя и путь в другую переменную
			mymap=quit(mymap)
	return mymap
	


def dispatcher(mymap,e):
	if mymap.SaveFormLoad:
		form.Elements[TEXTEDIT].text=['']
		content01.path=os.getcwd()
		path2=core.GetFilteredDirList(path,".map")
		path2.insert(0,"..")
		content01.path2=path2
		
		form.Render()
		form.Focus=(-1,0)
		mymap.SaveFormLoad=False
	
	mymap.sc.blit(form.MainSurf,(form.position))# Делать это только когда флаг необходимости установлен
	display.update()# каждый раз???
	if form.Focus[0]==OK_BUT:# Сохранить кнопка
		mymap=CheckPermission(form,mymap)
	if e.type==MOUSEBUTTONDOWN:
		form.Focus=form.getObj(e)
		if form.Focus[0]==OK_BUT:# Сохранить кнопка
			mymap=CheckPermission(form,mymap)
		elif form.Focus[0]==CANCEL_BUT:# отмена кнопка
			mymap=quit(mymap)
			going=False
		else:
			form.Control(e)
	if e.type==MOUSEBUTTONUP:
		pass
		form.Control(e)
	if e.type==KEYDOWN:
		if e.key==K_ESCAPE:
			going=False
			mymap=quit(mymap)
		elif e.key==K_RETURN:
			form.Focus=(OK_BUT,0)
		else:
			form.Control(e)
	if e.type==MOUSEMOTION:
		form.Control(e)
	return mymap