#-*-coding: cp1251 -*-
import os
from pygame import *
import time
# такие пакеты уже могут быть. Нужно создать уникальное имя пакета
import openform
import saveform
import confirm
import menu
import minimap

M_LEFT_DOWN=1
M_LEFT_UP=2
M_RIGHT_DOWN=3
M_RIGHT_UP=4
M_MOVE=5
K_PRESS=6
M_MIDDLE_DOWN=7
M_MIDDLE_UP=8
bg=50,50,50
fc=155,155,155
wh=255,255,255
bl=0,0,0
init()
count3=0
key.set_repeat(250, 40)
#sc=display.set_mode((1024,768),FULLSCREEN,32)
sc=display.set_mode((1024,768))
scrap.init()
sc.fill(wh)
Font2=font.Font(None,24)#Courier New
Font3=font.Font(None,14)#Courier New
# Font2=font.SysFont('couriernew', 14, bold=True, italic=False)
display.flip()

"""
Задача: откоментировать
Сформировать архитектуру приложения

Используется два вида объектов:
объект карта - в единственном числе как тип содержащий необходимые переменные
для работы
Этот объект пересылается в функции, которые могут получить доступ ко всем переменным объекта

второй объект - текстовое поле с рамкой, который производится во множественном числе.

Основная задумка - разделить карту на ячейки по 64 пикселя, распределять объекты соответственно 
занимаемым ими ячейкам

Используются несколько форм: основная,сохранения, загрузки, подтверждения выхода, миникарта.
Для перехода основного потока на обработку нужной формы используются флаги.
Устаналивается ИД формы, в зависимости от установленого ИД выполняется нужный обработчик.
После обработки формы устанавливается флаг обозначающий результат формы:
нужно загрузить, нужно сохранить, нужно выйти, показать, спрятать миникарту

Затем выполняется нужная функция и флаги сбрасываются в первоначальное состояние.


Надеюсь, объекты передаются по ссылке, большого потребления памяти замечено не было.

Нарисовать хорошую карту и возможно, анимационную презентацию туториал.


-Кнопка перехода в полноэкранный режим и обратно
(правда какие-то глюки при сворачивании и переключении окон)

функции делятся на вычисление значений и установку значений
для того и другого необходимо чтение значений
но функция не имеет доступа к переменным верхнего уровня кроме переданных ей аргументов и глобальных переменных
поэтому я передаю ей объект, который содержит нужные переменные

Можно ли разделить функции так, чтобы они обрабатывали небольшую часть информации, которую можно передать в аргументах?
Нужно будет помнить все функции и какие аргументы они используют. Это чертовски много информации.


Итак, все функции, в которых есть а и мумап нужно переделать на методы класса мумап и использовать не А а фокус-объект
возможно, приравнять а и фокус объект для краткости

при вызове функции не надо писать self в аргументах
при вызове функции метода надо писать перед именем функции self
метод не может вызвать функцию верхнего уровня


можно ли делать методы у текстбокса? или использовать универсальный текстбокс из пакета пигуи?
у меня не просто текстбокс а с окружностью
зачем мне окружность?
можно соединять с центром или краем объекта
перетаскивать за объект.
Окружность не так и нужна. Назначение окружности неясно
в окружности текст не смотрится
можно использовать прямоугольник с закругленными углами

какие методы должны быть у текстбокса?
контроллер клавиатуры
функции рисования
изменения рамки, текста

расположение текстбокса зависит от списка координат на карте
а это уже задача карты как контейнера
карта - это контейнер для элементов

пользуясь информацией из контейнера можно программировать модель
которая должна быть отделена и от текстбоксов и от их контейнера
мы храним все текстбоксы в контейнерах



"""

""" Ошибки
-при скрытии миникарты не рисуются линии
какая функция там используется?
"""

""" Задачи
Перевести все аргументы в функциях типа (а)
в self.Focus или типа того
Сделать одну форму вместо сохранить и загрузить
разные надписи и разные проверки на разрешение выйти из формы

Первая открытая карта должна быть лучше.

Нужны стрелки от А к В

Убрать окружности?
Пока они мне нравятся. Как шарниры. Можно будет присоединять
просто к шарнирам


Форма-билдер форм
вывести компоненты
фокус - -1 или прошлый нажатый компонент

порождать на экране нужный компонент
удалять при выборе переключателя "удалить"
передвигать, изменять размер
назначать внутреннее имя, записывать в список ректов и ИД

сохранять в файл в формате CSS

Писать контроллер отдельно, загрузив компоненты из файла
(попытка объединить CSS и JS, или скорее Python)

Зная имя компонента, которое мы задали мы прописываем желаемое поведение, и связываем с этим поведением дальнейшие действия.

Всегда ли такое поведение будет одинаковое?
Можно заменять функции из некоторого набора возможных функций

При одних условиях-флагах компоненты могут вести себя так, при других - иначе.

Анимация, изменения текста, появление исчезание, смена цвета, блокировка на измнение.








"""
ramka=0
if ramka:
	for i in range(0,1024,64):
		draw.line(sc,bl,(i,0),(i,768),1)
	for i in range(0,768,64):
		draw.line(sc,bl,(0,i),(1024,i),1)
	display.update()

class text_box:
	def __init__(self):
		self.x=0
		self.y=0
		self.rx=0
		self.ry=0
		self.w=60
		self.h=20
		self.cur_line=[]
		self.w_clear=0 # ширина стираемой области
		self.soft_x=0
		self.soft_y=0
		self.max_w=60
		self.etalon_w=0
		self.line_pos=(0,0)
		self.MaxW=0 # максимальная ширина
		self.WList=[] # список значений ширины каждой строки

class MyMap:
	def __init__(self):
		self.FlagMinimapOperator=False
		self.MinimapLoad=False
		self.OpenFormLoad=False
		self.SaveFormLoad=False
		self.CursorOffset=0
		self.SelBuf=None
		self.CLEAR=Surface((0,0))
		self.Back=Surface((0,0))
		self.LinesList=[]
		self.MinXY=(0,0)
		self.KoefMinimap=(0,0)
		self.Minimap=None
		self.FlagMinimap=False
		self.Scrap=""
		self.OldRect=-1
		self.FocusSelection=None
		self.EndTextSelection=(0,0)
		self.BeginSelection=(0,0)
		self.FlagTextSelection=False
		self.SaveAndExit=False
		self.Exit=False
		self.FlagRamka=False
		self.ListSelection=[]
		self.Selection=(0,0)
		self.EndSelection=(0,0)
		self.FlagDrawSelection=False
		self.PATH=''
		self.LOADPATH="1.map"
		self.SAVEPATH="1.map"
		self.FlagNeedSaveAs=False
		self.FlagNeedLoad=False
		self.ID=-1
		self.ObjectForReturn=-1
		self.NeedUpdate=True
		self.Focus=-1
		self.sc=None
		self.EraseSurf=Surface((0,0))
		self.Going=True
		self.ObjectList=[]
		self.Background=Surface((0,0))
		self.BackWasSaved=False
		self.MapList={}
		self.LineList=[]
		self.Rel_x=0
		self.Rel_y=0
		self.ConsistList=[]
		self.CheckList=[]
		self.Pointer=0
		self.FormFlag=False
		self.FlagInsideObj=False
		self.FlagInsideHotPoint=False
		self.FlagTakeMap=False
		self.FlagTakeObj=False
	def TryCreateObject(self,a):
		# print "TryCreateObject"
		self.ConsistList=[]
		self.GetCellList(a)# создали список ячеек из которых состоит объект
		self.CheckList=[]
		list=[]
		for self.Pointer in range(0,len(self.ConsistList)):
			yk=self.ConsistList[self.Pointer][0]
			xk=self.ConsistList[self.Pointer][1]
			cellexist=self.IsCellExist(yk,xk)
			pointer=self.Pointer
			if cellexist:
				# превратим адреса в индексы объектов!
				yk=self.ConsistList[pointer][0]
				xk=self.ConsistList[pointer][1]
				if len(self.MapList[yk][xk])==1:
					list.append(self.MapList[yk][xk][0])
				else:
					for i in range(0,len(self.MapList[yk][xk])):
						if self.MapList[yk][xk][i] not in list:
							list.append(self.MapList[yk][xk][i])
		if len(list)!=0:# если нет ни одной ячейки - нечего проверять на пересечение
			for i in range(0,len(list)):
				b=self.ObjectList[list[i]]
				flag=self.GetIntersectList(a,b)
				if flag==True:break
			if flag==False:
				self.PutObject(a)
		else:
			self.PutObject(a)# 
	def GetCellList(self,a):# без рендера
		self.ConsistList=[]
		i1=(a.rx-10)/64# объект начинается с круга
		i2=(a.ry-10)/64# объект начинается с круга
		i3=(a.rx+a.w)/64
		i4=(a.ry+a.h)/64
		for i in range(i2,i4+1):
			for j in range(i1,i3+1):
				self.ConsistList.append((i,j))
	def GetIntersectList(self,a,b):# без рендера
		# возвращает, есть ли ячейки в которых А пересекается с Б
		# print "GetIntersectList"
		flag=False
		x1=a.rx-10
		x2=a.rx+a.w
		y1=a.ry-10
		y2=a.ry+a.h
		x3=b.rx-10
		x4=b.rx+b.w
		y3=b.ry-10
		y4=b.ry+b.h
		list1=[(x1,y1),(x1,y2),(x2,y1),(x2,y2)]
		list2=[(x3,y3),(x3,y4),(x4,y3),(x4,y4)]
		for i in range(0,len(list1)):
			x1=list1[i][0]
			y1=list1[i][1]
			if x1>x3 and x1<x4 and y1>y3 and y1<y4:
				flag=True
				break
		if flag==True:return flag
		x3=a.rx-10
		x4=a.rx+a.w
		y3=a.ry-10
		y4=a.ry+a.h
		for i in range(0,len(list2)):
			x1=list1[i][0]
			y1=list1[i][1]
			if x1>x3 and x1<x4 and y1>y3 and y1<y4:
				flag=True
				break
		return flag
	def IsCellExist(self,yk,xk):# без рендера
		# проверяет, есть ли такая ячейка а Л1
		# print "IsCellExist"
		flag=False
		if self.MapList.has_key(yk):
			if self.MapList[yk].has_key(xk):
				flag=True
				# если есть и У и Х тогда пишем в список
				# пишем в список ссылку на А
			else:# нет такого столбца в этой строке
				pass
				
				# вторая причина несуществования ячейки
		else:# нет такой строки
			pass
		return flag
	def CreateCell(self,yk,xk):# без рендера
		# создает ячейку в Л1 (или список ячеек с координатами Х У)
		# print "CreateCell"
		if self.MapList.has_key(yk):
			if self.MapList[yk].has_key(xk):
				pass
				# Запись ссылки
			else:# нет такого столбца в этой строке
				self.MapList[yk][xk]=[]
				
				# создание столбца, запись ссылки
		else:# нет такой строки
			self.MapList[yk]={}
			self.MapList[yk][xk]=[]
	def PutObject(self,a):# без рендера
		# помещает объект по списку ячеек
		# print "PutObject"
		self.ObjectList.append(a)
		if len(self.ConsistList)!=0:
			a.ConsistList=self.ConsistList
			for self.Pointer in range(0,len(self.ConsistList)):
				yk=self.ConsistList[self.Pointer][0]
				xk=self.ConsistList[self.Pointer][1]
				flag=self.IsCellExist(yk,xk)
				if not flag:
					self.CreateCell(yk,xk)
				a.text=['']
				self.MapList[yk][xk].append(self.ObjectList.index(a))
				self.Focus=a
		self.DrawObject(a)
		self.NeedUpdate=True
	def Save(self):
		# print "Save"
		if self.SAVEPATH=='':
			pass
			self.FormFlag=True
			self.ID=2
		else:
			fname=self.SAVEPATH
			f1=open(fname,"w")
			f1.write(str(self.Rel_x)+"\n")
			f1.write(str(self.Rel_y)+"\n")
			f1.write(str(len(self.ObjectList))+"\n")
			for i in self.ObjectList:
				f1.write(str(i.x)+"\n")
				f1.write(str(i.y)+"\n")
				f1.write(str(i.rx)+"\n")
				f1.write(str(i.ry)+"\n")
				f1.write(str(i.w)+"\n")
				f1.write(str(i.h)+"\n")
				f1.write(str(0)+"\n")
				f1.write(str(0)+"\n")
				f1.write(str(0)+"\n")
				f1.write(str(i.MaxW)+"\n")
				f1.write(str(len(i.text))+"\n")
				for j in i.text:
					txt=j.encode('utf-8')
					f1.write(txt+"\n")
			for i in self.LinesList:
				txt=''
				for j in i:
					txt+=str(j)+","
				txt=txt[:-1]+"\n"
				f1.write(txt)
			f1.close()
			f1.close()
			print "saved"
	def QuickSave(self):
		# print "QuickSave"
		if self.SAVEPATH=='':
			self.FormFlag=True
			self.ID=2
		else:
			fname=self.SAVEPATH
			f1=open(fname,"w")
			f1.write(str(self.Rel_x)+"\n")
			f1.write(str(self.Rel_y)+"\n")
			f1.write(str(len(self.ObjectList))+"\n")
			for i in self.ObjectList:
				f1.write(str(i.x)+"\n")
				f1.write(str(i.y)+"\n")
				f1.write(str(i.rx)+"\n")
				f1.write(str(i.ry)+"\n")
				f1.write(str(i.w)+"\n")
				f1.write(str(i.h)+"\n")
				f1.write(str(0)+"\n")
				f1.write(str(0)+"\n")
				f1.write(str(0)+"\n")
				f1.write(str(i.MaxW)+"\n")
				f1.write(str(len(i.text))+"\n")
				for j in i.text:
					txt=j.encode('utf-8')
					f1.write(txt+"\n")
			for i in self.LinesList:
				txt=''
				for j in i:
					txt+=str(j)+","
				txt=txt[:-1]+"\n"
				f1.write(txt)
			f1.close()
			print "saved"
	def DrawCursor(self,a,color):# Textedit перерисовать курсор
		# print "DrawCursor"
		if a.soft_y<=len(a.text)-1:
			text=a.text[a.soft_y][:a.soft_x]
			hard_x=Font2.render(text,1,fc,wh).get_width()
			hard_y=a.ry+2+a.soft_y*17-self.Rel_y
			draw.line(self.Back,color,(2+a.rx+hard_x-self.Rel_x,hard_y+4),(a.rx+2+hard_x-self.Rel_x,hard_y+13),1)
			self.NeedUpdate=True
	def DrawTextLine(self,a):# Textedit  # рисуем текущую линию текста
		# print "DrawTextLine"
		text=a.text[a.soft_y]
		text_surf=Font2.render(text,1,fc,wh)
		x=a.rx+2-self.Rel_x
		y=a.ry+2+a.soft_y*17-self.Rel_y
		self.sc.blit(text_surf,(x,y))
	def DrawChar(self,a):# Textedit # вывести символ на экран (нужна интерактивность а скорость набора разная)
		text=a.text[a.soft_y][:a.soft_x]
		text_surf=Font2.render(text,1,fc,wh)
		
		if a.w_clear!=0:
			text=a.text[a.soft_y]
			text_surf=Font2.render(text,1,fc,wh)
			# высота поверхности 17
			x=a.rx+2-self.Rel_x
			y=a.ry+2+a.soft_y*17-self.Rel_y
			CalcMaxW(a,self)
			s2=Surface((a.w_clear,17))
			s2.fill(wh)
			self.sc.blit(s2,(x,y))
			self.sc.blit(text_surf,(x,y))
			self.NeedUpdate=True
			DrawCursor(a,bl,self)
		else:
			x=a.rx+2-self.Rel_x
			y=a.ry+2+a.soft_y*17-self.Rel_y
			CalcMaxW(a,self)
			self.sc.blit(text_surf,(x,y))
			DrawCursor(a,bl,self)
			self.NeedUpdate=True
	def CalcMaxW(self,a):
		# print "CalcMaxW"
		a.MaxW=0
		for i in range(0,len(a.text)):
			w=self.GetTextWidth(a.text[i])
			if w>a.MaxW:
				a.MaxW=w
		self.ChangeBorder(a)
		self.DrawBorder(a,bl)
		self.CorrectMap(a)
	def CorrectMap(self,a):# без рендера
		# print "CorrectMap"
		TempConsistList=[]
		self.GetCellList(a)
		TempConsistList=self.ConsistList
		TempDelList=[]
		TempAppendList=[]
		TempDelList=self.GetTempDelList(a.ConsistList,TempConsistList)
		TempAppendList=self.GetTempAppendList(a.ConsistList,TempConsistList)
		self.DelFromMap(TempDelList,a)
		self.AppendOnMap(TempAppendList,a)
		a.ConsistList=TempConsistList[:]
	def DelFromMap(self,TempDelList,a):# без рендера
		# print "DelFromMap"
		
		obj=self.ObjectList.index(a)
		for i in TempDelList:# для всех кортежей с координатами ячеек
			y=i[0]
			x=i[1]
			list2=[]
			flag=False
			if obj in self.MapList[y][x]:
				flag=True
			if flag==True:self.MapList[y][x].remove(obj)
	def AppendOnMap(self,TempAppendList,a):# без рендера
		# print "AppendOnMap"
		for i in TempAppendList:
			y=i[0]
			x=i[1]
			obj=self.ObjectList.index(a)
			if not self.IsCellExist(y,x):
				self.CreateCell(y,x)
			self.MapList[y][x].append(obj)
	def GetTempDelList(self,list1,list2):# без рендера
		# print "GetTempDelList"
		TempDelList=[]
		for i in list1:
			if i not in list2:
				TempDelList.append(i)
		return TempDelList
	def GetTempAppendList(self,list1,list2):# без рендера
		# print "GetTempAppendList"
		TempAppendList=[]
		for i in list2:
			if i not in list1:
				TempAppendList.append(i)
		return TempAppendList
	def DrawLabel(self,text):# вывести надпись
		# print "DrawLabel"
		self.sc.fill(wh,(300,40,50,50))
		self.sc.blit(Font2.render(text,1,fc,wh),(300,40))
		self.NeedUpdate=True
	def DrawLabelXY(self,text,x,y):
		# print "DrawLabelXY"
		text_surf=Font3.render(text,1,fc,wh)
		self.Back.blit(text_surf,(x,y))
		self.NeedUpdate=True
	def RedrawObject(self,a):# Textedit
		self.Redraw2([a])
		self.DrawObject(a)
		self.DrawText([a])
		self.DrawCursor(a,bl)
		self.NeedUpdate=True
	def key_disp(self,a,k1,e):# обработать события клавиш Это контроллер текстового поля
		# print e.key,e.mod,K_c,KMOD_LCTRL,~(~KMOD_CAPS&~KMOD_LCTRL)
		if (e.key==K_s and e.mod==KMOD_LCTRL)  or (e.key==K_s and e.mod==~(~KMOD_CAPS&~KMOD_LCTRL)):
			mymap.QuickSave()
		if (e.key==K_c and e.mod==KMOD_LCTRL)  or (e.key==K_c and e.mod==~(~KMOD_CAPS&~KMOD_LCTRL)):
			# print scrap.get_types ()
			txt=scrap.get('text/plain;charset=utf-8')
			if txt:
				# txt3=txt.decode('utf_8')
				pass
				# print "txt3",txt3
				
			else:
				print "There does not seem to be text in the clipboard."
			
		if (e.key==K_v and e.mod==KMOD_LCTRL)  or (e.key==K_v and e.mod==~(~KMOD_CAPS&~KMOD_LCTRL)):
			txt=scrap.get('text/plain;charset=utf-8')
			if txt:
				txt3=txt.decode("utf-16")
				list=[]
				list=txt3[:-1].split("\n")
				if list==[]:list.append(txt3)
				if list[-1]=="\n":list=list[:-1]
				up=a.text[:a.soft_y+1]
				first_half=a.text[a.soft_y][:a.soft_x]
				second_half=a.text[a.soft_y][a.soft_x:]
				up[-1]=first_half[:]+list[0]
				up.extend(list[1:])
				if up[-1]=="":
					up=up[:-1]
				up[-1]+=second_half
				up.extend(a.text[a.soft_y+1:])
				a.text=up[:]
				self.CalcMaxW(a)
				self.Redraw2([a])
				self.Redraw()
			
		if (e.key==K_z and e.mod==KMOD_LCTRL)  or (e.key==K_z and e.mod==~(~KMOD_CAPS&~KMOD_LCTRL)):
			pass
		if e.key==K_BACKSPACE:#бекспейс должен поднимать строки если дошел до начала
			# должно проходить по спецсимволам и в конце попадать на простой текст через elif else if
			self.DrawCursor(a,wh)
			if a.soft_x!=0: # Если не первый символ в строке
				self.ClearWithBackground(a)
				text1=a.text[a.soft_y][:a.soft_x-1]
				text2=a.text[a.soft_y][a.soft_x:]
				text=text1+text2
				text_surf=Font2.render(a.text[a.soft_y],1,fc,wh)
				a.w_clear=text_surf.get_width()
				a.soft_x-=1
				a.text[a.soft_y]=text[:]# меньше на один символ
				self.CalcMaxW(a)
				a.etalon_w=0
				a.line_pos=(a.soft_x, a.soft_y)
				self.RedrawObject(a)
			else:#если в самом начале строки
				if a.soft_y!=0:# Не верхняя строчка
					self.ClearWithBackground(a)
					text1=a.text[a.soft_y-1]
					text2=a.text[a.soft_y][:]
					a.text.remove(a.text[a.soft_y])
					a.soft_x=len(a.text[a.soft_y-1])
					a.text[a.soft_y-1]=text1+text2
					a.soft_y-=1
					self.CalcMaxW(a)
					self.RedrawObject(a)
					self.DrawCursor(a,bl)
		elif e.key==K_RETURN:
			self.DrawCursor(a,wh)
			self.ClearWithBackground(a)
			if a.soft_x==len(a.text[a.soft_y]):# Если конец строки
				a.w_clear=0
				a.text.append('')
				a.soft_x=0
				a.soft_y+=1
				self.CalcMaxW(a)
				self.RedrawObject(a)
			else:
				text1=a.text[a.soft_y][:a.soft_x]
				text2=a.text[a.soft_y][a.soft_x:]
				a.text.insert(a.soft_y+1,'')
				a.text[a.soft_y]=text1[:]
				a.text[a.soft_y+1]=text2[:]
				a.soft_x=0
				a.soft_y+=1
				self.CalcMaxW(a)
				self.RedrawObject(a)
		elif e.key==K_UP:
			if a.soft_y!=0:
				if a.etalon_w==0:
					text=a.text[a.line_pos[1]][:a.line_pos[0]]#IndexError: list index out of range
					text_surf=Font2.render(text,1,fc,wh)
					a.etalon_w=text_surf.get_width()
				self.NeedUpdate=True
				a.soft_y-=1
				for i in range(0,len(a.text[a.soft_y])):
					text=a.text[a.soft_y][:i]
					w_line=self.GetTextWidth(text)
					if w_line>a.etalon_w:
						w1= w_line-a.etalon_w
						text=a.text[a.soft_y][:i-1]
						w_line2=self.GetTextWidth(text)
						w2=a.etalon_w-w_line2
						if w2>w1:
							a.soft_x=i
						elif w2<w1:
							a.soft_x=i-1
						break
					if w_line==a.etalon_w:
						a.soft_x=i
						break
				self.Redraw2([a])
				self.DrawText([a])
				self.DrawCursor(a,bl)
		elif e.key==K_DOWN:
			if a.soft_y!=len(a.text)-1:
				# если эталон ширины равен 0 то посчитать '
				if a.etalon_w==0:
					text=a.text[a.line_pos[1]][:a.line_pos[0]]
					text_surf=Font2.render(text,1,fc,wh)
					a.etalon_w=text_surf.get_width()
				a.soft_y+=1
				for i in range(0,len(a.text[a.soft_y])):
					text=a.text[a.soft_y][:i]
					w_line=self.GetTextWidth(text)
					if w_line>a.etalon_w:
						w1= w_line-a.etalon_w
						text=a.text[a.soft_y][:i-1]
						w_line2=self.GetTextWidth(text)
						w2=a.etalon_w-w_line2
						if w2>w1:
							a.soft_x=i
						elif w2<w1:
							a.soft_x=i-1
						break
					if w_line==a.etalon_w:
						a.soft_x=i
						break
				self.Redraw2([a])
				self.DrawText([a])
				self.DrawCursor(a,bl)
		elif e.key==K_RIGHT:
			if a.soft_x!=len(a.text[a.soft_y]):
				a.soft_x+=1
				self.DrawText([a])
				self.DrawCursor(a,bl)
			a.etalon_w=0
			a.line_pos=(a.soft_x, a.soft_y)
		elif e.key==K_LEFT:
			if a.soft_x!=0:
				self.DrawCursor(a,wh)
				a.soft_x-=1
				self.DrawText([a])
				self.DrawCursor(a,bl)
			a.etalon_w=0
			a.line_pos=(a.soft_x, a.soft_y)
		elif e.key==K_HOME:
			self.ClearWithBackground(a)
			a.soft_x=0
			self.RedrawObject(a)
			self.DrawCursor(a,bl)
		elif e.key==K_END:
			self.ClearWithBackground(a)
			a.soft_x=len(a.text[a.soft_y])
			self.RedrawObject(a)
			self.DrawCursor(a,bl)
		elif e.key==K_DELETE:
			if len(a.text[a.soft_y])==a.soft_x:#  В конце строки
				if a.soft_y<len(a.text)-1:# если внизу есть строки
					text1=a.text[a.soft_y]
					text2=a.text[a.soft_y+1]# по идее не должно вылезать за пределы
					text=text1+text2
					a.text[a.soft_y]=text[:]
					a.text.remove(a.text[a.soft_y+1])
					self.CalcMaxW(a)
					self.Redraw2([a])
					self.TakeBackground(a)
					self.ClearWithBackground(a)#СПОРНЫЙ ВОПРОС
					
					self.DrawObject(a)# Вообще-то может измениться рамка
					self.DrawText([a])
					self.Redraw()
					self.DrawCursor(a,bl)
			else:# Посреди строки
				text1=a.text[a.soft_y][:a.soft_x]
				text2=a.text[a.soft_y][a.soft_x+1:]
				text=text1+text2
				a.text[a.soft_y]=text[:]
				self.CalcMaxW(a)
				self.Redraw2([a])
				self.TakeBackground(a)
				self.ClearWithBackground(a)
				self.DrawObject(a)# Вообще-то может измениться рамка
				self.DrawText([a])
				self.Redraw()
				self.DrawCursor(a,bl)
		elif (e.key in range(39,123) and e.mod!=64) or (e.key in range(39,123) and e.mod==1) or e.key==32 or (e.key==32 and e.mod==1):# обычный текст (нужно сделать автоперенос чтобы не вылезало за экран)
			if a!=None:
				self.ClearWithBackground(a)
				text1=a.text[a.soft_y][:a.soft_x]#left side
				text2=a.text[a.soft_y][a.soft_x:]
				text=text1+k1+text2
				a.text[a.soft_y]=text[:]
				a.soft_x+=1
				self.CalcMaxW(a)
				self.RedrawObject(a)
	def ClearWithBackground(self,a):
		# print "ClearWithBackground"
		self.EraseSurf=Surface((a.w+10,a.h+10))
		self.EraseSurf.fill(wh)
		self.EraseSurf.blit(self.Background,(-(a.rx-self.Rel_x-10),-(a.ry-self.Rel_y-10)))
		self.Back.blit(self.EraseSurf,(a.rx-self.Rel_x-10,a.ry-self.Rel_y-10))
	def PrepareObject(self,x,y):# Textedit # создать основной объект
		# print "PrepareObject"
		a = text_box()# создаем объект
		a.text=['']
		a.rx=x+self.Rel_x# реальные координаты
		a.ry=y+self.Rel_y# реальные координаты
		return a
	def DrawText(self,list):# Использовать после загрузки
		# print "DrawText"
		for i in list:
			if i.text==['']:
				i.TextSurf=Surface((i.w-2,i.h-2))
				i.TextSurf.fill(wh)
			EraseSurf=Surface(i.TextSurf.get_size())
			EraseSurf.fill(wh)
			self.Back.blit(EraseSurf,(i.x+1,i.y+1))
			self.Back.blit(i.TextSurf,(i.x+1,i.y+1))
		self.NeedUpdate=True
	def DrawText2(self,list):# Использовать после загрузки
		# print "DrawText"
		for i in list:
			if (i.text!=['']):
				x=i.x
				y=i.y-17
				for j in range(len(i.text)):
					y+=17
					text=i.text[j]
					text_surf=Font2.render(text,1,fc,wh)
					self.sc.blit(text_surf,(x+2,y+2))
		self.NeedUpdate=True
	def Redraw(self):
		# print "Redraw"
		rel_x=self.Rel_x
		rel_y=self.Rel_y
		xk1=-(rel_x % 64)
		yk1=-(rel_y % 64)
		x_list=[]
		y_list=[]
		if self.FlagRamka:
			for i in range(xk1,xk1+1088,64):
				draw.line(sc,bl,(i,0),(i,768),1)
				x_list.append(i)
			for i in range(yk1,yk1+768+64,64):
				draw.line(sc,bl,(0,i),(1024,i),1)
				y_list.append(i)
			for i in range(0,len(x_list)):
				for j in range(0,len(y_list)):
					x1=x_list[i]
					y1=y_list[j]
					text1=str((x1+rel_x)/64)
					text2=str((y1+rel_y)/64)
					# text1=str((x1+rel_x)>>6)
					# text2=str((y1+rel_y)>>6)
					self.DrawLabelXY(text1+" : "+text2,x1+3,y1+3)
		self.Back=self.CLEAR
		self.Back.fill(wh)
		if self.LinesList!=[]:
			for i in self.LinesList:
				ObjA=i[0]
				ObjB=i[1]
				x1=self.ObjectList[ObjA].rx-self.Rel_x
				y1=self.ObjectList[ObjA].ry-self.Rel_y
				x2=self.ObjectList[ObjB].rx-self.Rel_x
				y2=self.ObjectList[ObjB].ry-self.Rel_y
				draw.line(self.Back,bl,(x1,y1),(x2,y2),1)
		list=self.GetScreenList()
		for i1 in list:
			a=self.ObjectList[i1]
			a.x=a.rx-self.Rel_x
			a.y=a.ry-self.Rel_y
			draw.circle(self.Back,wh,(a.x,a.y),10,0)# рисуем окружность по локальным координатам
			draw.circle(self.Back,bl,(a.x,a.y),10,1)
			draw.rect(self.Back, wh, (a.x,a.y,a.w,a.h), 0)# прямоугольник перекрывает окружность, которая нужна для операций с объектом
			draw.rect(self.Back, bl, (a.x,a.y,a.w,a.h), 1)
			self.DrawText([a])
		for i in self.ListSelection:# оставляем выделение при навигации по карте
				a=self.ObjectList[i]
				self.DrawSelection(a,bl)
		self.Back.blit(menu.menu.MainSurf,(menu.menu.position))# это можно исключить, если копировать мимо меню
		self.NeedUpdate=True
	def Redraw2(self,list):
		for i in list:
			i.TextSurf=Surface((i.MaxW,2+len(i.text)*17))
			i.TextSurf.fill(wh)
			if (i.text!=['']):
				for j in range(len(i.text)):
					x=0
					y=j*17
					text=i.text[j]
					text_surf=Font2.render(text,1,fc,wh)
					i.TextSurf.blit(text_surf,(x,y))
	def GetScreenList(self):#Без рендера
		# print "GetScreenList"
		rel_x=self.Rel_x
		rel_y=self.Rel_y
		rel_xk=rel_x/64
		rel_yk=rel_y/64
		list=[]
		for i in range(rel_yk, rel_yk+14):#14? O_o
			for j in range(rel_xk,rel_xk+18):#18? o_O
				if self.IsCellExist(i,j):
					if self.MapList[i][j]!=[]:
						for k in self.MapList[i][j]:
							if k not in list:# длительная операция может лучше словарь?
								list.append(k)
		return list
	def TakeBackground(self,a):# берет без одного объекта
		# print "TakeBackground"
		Background=self.Background
		Background.fill(wh)
		rel_x=self.Rel_x
		rel_y=self.Rel_y
		xk1=(rel_x/64*64)-rel_x
		yk1=(rel_y/64*64)-rel_y
		x_list=[]
		y_list=[]
		if self.FlagRamka:
			for i in range(xk1,xk1+1024+64,64):
				draw.line(Background,bl,(i,0),(i,768),1)
				x_list.append(i)
			for i in range(yk1,yk1+768+64,64):
				y_list.append(i)
				draw.line(Background,bl,(0,i),(1024,i),1)
			# Проставляем адреса ячеек
			for i in range(0,len(x_list)):
				for j in range(0,len(y_list)):
					x1=x_list[i]
					y1=y_list[j]
					text1=str((x1+rel_x)/64)
					text2=str((y1+rel_y)/64)
					text=text1+" : "+text2
					text_surf=Font3.render(text,1,fc,wh)
					Background.blit(text_surf,(x1+3,y1+3))
		rel_xk=-rel_x/64
		rel_yk=-rel_y/64
		list=[]
		list=self.GetScreenList()
		idx=self.ObjectList.index(a)
		for i1 in list:
			if i1!=idx:
				i=self.ObjectList[i1]
				i.x=i.rx-self.Rel_x
				i.y=i.ry-self.Rel_y
				draw.circle(Background,wh,(i.x,i.y),10,0)# рисуем окружность по локальным координатам
				draw.circle(Background,bl,(i.x,i.y),10,1)
				draw.rect(Background, wh, (i.x,i.y,i.w,i.h), 0)# прямоугольник перекрывает окружность, которая нужна для операций с объектом
				draw.rect(Background, bl, (i.x,i.y,i.w,i.h), 1)
				if (i.text!=['']):
					for j in range(0,len(i.text)):
						x=2+i.x
						y=j*17+2+i.y
						text=i.text[j]
						text_surf=Font2.render(text,1,fc,wh)
						Background.blit(text_surf,(x,y))
		self.Background=Background
	def TakeBackground2(self):# берет без одного объекта
		# print "TakeBackground"
		Background=self.Background
		Background.fill(wh)
		rel_x=self.Rel_x
		rel_y=self.Rel_y
		xk1=(rel_x/64*64)-rel_x
		yk1=(rel_y/64*64)-rel_y
		x_list=[]
		y_list=[]
		if self.FlagRamka:
			# рисуем рамку
			for i in range(xk1,xk1+1024+64,64):
				draw.line(Background,bl,(i,0),(i,768),1)
				x_list.append(i)
			for i in range(yk1,yk1+768+64,64):
				y_list.append(i)
				draw.line(Background,bl,(0,i),(1024,i),1)
			# Проставляем адреса ячеек
			for i in range(0,len(x_list)):
				for j in range(0,len(y_list)):
					x1=x_list[i]
					y1=y_list[j]
					text1=str((x1+rel_x)/64)
					text2=str((y1+rel_y)/64)
					text=text1+" : "+text2
					text_surf=Font3.render(text,1,fc,wh)
					Background.blit(text_surf,(x1+3,y1+3))
		rel_xk=-rel_x/64
		rel_yk=-rel_y/64
		list=[]
		list=self.GetScreenList()
		for i1 in list:
			i=self.ObjectList[i1]
			i.x=i.rx-self.Rel_x
			i.y=i.ry-self.Rel_y
			draw.circle(Background,wh,(i.x,i.y),10,0)# рисуем окружность по локальным координатам
			draw.circle(Background,bl,(i.x,i.y),10,1)
			draw.rect(Background, wh, (i.x,i.y,i.w,i.h), 0)# прямоугольник перекрывает окружность, которая нужна для операций с объектом
			draw.rect(Background, bl, (i.x,i.y,i.w,i.h), 1)
			if (i.text!=['']):
				for j in range(0,len(i.text)):
					x=2+i.x
					y=j*17+2+i.y
					text=i.text[j]
					text_surf=Font2.render(text,1,fc,wh)
					Background.blit(text_surf,(x,y))
		self.Background=Background
	def DrawObject(self,a):# отрисовать основной объект
		# print "DrawObject"
		a.x=a.rx-self.Rel_x# Что за дела тут после ДЕЛа? 
		a.y=a.ry-self.Rel_y
		draw.circle(self.Back,wh,(a.x,a.y),10,0)# рисуем окружность по локальным координатам
		draw.circle(self.Back,bl,(a.x,a.y),10,1)
		draw.rect(self.Back, wh, (a.x,a.y,a.w,a.h), 0)# прямоугольник перекрывает окружность, которая нужна для операций с объектом
		draw.rect(self.Back, bl, (a.x,a.y,a.w,a.h), 1)
	def DrawBorder(self,a,color):# Textedit 
		# print "DrawBorder"
		draw.rect(self.Back, color, (a.rx-self.Rel_x,a.ry-self.Rel_y,a.w,a.h), 1)
		self.NeedUpdate=True
	def DrawSelection(self,a,color):# Textedit 
		# print "DrawBorder"
		# draw.rect(sc, color, (a.rx-mymap.Rel_x-2,a.ry-mymap.Rel_y-2,a.w+3,a.h+3), 3)
		draw.rect(self.Back, color, (a.rx-self.Rel_x-2,a.ry-self.Rel_y-2,a.w+3,a.h+3), 3)
		self.NeedUpdate=True
	def GetObject(self,x,y):# без рендер
		# print "GetObject"
		x=x+self.Rel_x
		y=y+self.Rel_y
		yk=y/64
		xk=x/64
		self.FlagInsideHotPoint=False
		self.FlagInsideObj=False
		if self.IsCellExist(yk,xk):
			list=self.MapList[yk][xk]
			if list:
				for j in list:
					i=self.ObjectList[j]
					if x>i.rx-10 and x<i.rx+10 and y>i.ry-10 and y<i.ry+10:
						self.FlagInsideHotPoint=True
					if x>i.rx and x<i.rx+i.w and y>i.ry and y<i.ry+i.h:
						self.FlagInsideObj=True
					if self.FlagInsideHotPoint==True and self.FlagInsideObj==True:
						self.FlagInsideHotPoint=False
					if self.FlagInsideHotPoint==True or self.FlagInsideObj==True:
						break
			if self.FlagInsideHotPoint==True or self.FlagInsideObj==True:
				return self.ObjectList.index(i)
		return -1
	def GetObject2(self,x,y):# без рендер
		# print "GetObject"
		x=x+self.Rel_x
		y=y+self.Rel_y
		yk=y/64
		xk=x/64
		self.FlagInsideHotPoint=False
		self.FlagInsideObj=False
		if self.IsCellExist(yk,xk):
			list=self.MapList[yk][xk]
			
			if list:
				for j in list:
					i=self.ObjectList[j]
					if x>i.rx and x<i.rx+i.w and y>i.ry and y<i.ry+i.h:
						self.FlagInsideObj=True
					if self.FlagInsideObj==True:
						break
			if self.FlagInsideObj==True:
				return self.ObjectList.index(i)
		return -1
	def GetObjectUnder(self,x,y):
		x=x+self.Rel_x
		y=y+self.Rel_y
		yk=y/64
		xk=x/64
		# может и не быть таких ячеек, проверить!
		flag=False
		list1=[]
		list=[]
		curObj=self.Focus
		curObj1=self.ObjectList.index(curObj)
		x1=curObj.rx-10
		x2=curObj.rx+curObj.w
		y1=curObj.ry-10
		y2=curObj.ry+curObj.h
		R1=Rect((x1,y1,x2-x1,y2-y1))
		for k in range(len(curObj.ConsistList)):
			yk=curObj.ConsistList[k][0]
			xk=curObj.ConsistList[k][1]
			list=self.MapList[yk][xk][:]
			if curObj1 in list:
				list.remove(curObj1)
			if list:
				for j in list:
					i=self.ObjectList[j]
					x1=i.rx-10
					x2=i.rx+i.w
					y1=i.ry-10
					y2=i.ry+i.h
					R2=Rect((x1,y1,x2-x1,y2-y1))
					if R1.colliderect(R2):
						if i!=curObj1:
							result=self.ObjectList.index(i)
							if result not in list1:
								list1.append(result)
						
		if len(list1)>0:
			return list1
			
		else:
			return -1
	def FindPlaceCursorPartA(self,x,y,a):
		left=x-(a.rx-self.Rel_x)-2
		top=y-(a.ry-self.Rel_y)-2
		return left,top
	def FindPlaceCursorPartB(self,left,top,a):
		self.DrawCursor(a,wh)
		if a.text!=['']:
			a.soft_y=top/17 # с У все верно вроде
			global count3
			w3=0
			if len(a.text)-1>=a.soft_y:
				w=self.GetTextWidth(a.text[a.soft_y])# ошибка как может быть soft_y>0 ?
				if w>left:# если курсор стал в конце строки то ставим курсор после последнего символа
					avr=w/len(a.text[a.soft_y])
					guess=left/avr
					w2=self.GetTextWidth(a.text[a.soft_y][:guess])
					begin=True
					if w2<left:
						while begin:
							guess+=1
							min=w2
							w2=self.GetTextWidth(a.text[a.soft_y][:guess])# Сравняется ли min и w2 после этого вычисления?
							if w2>left:
								res=(guess-1,guess,min,w2)
								begin=False
					elif w2>left:
						if left>self.GetTextWidth(a.text[a.soft_y][:1]):
							while begin:
								guess+=-1# уменьшаем или увеличиваем
								max=w2
								w2=self.GetTextWidth(a.text[a.soft_y][:guess])
								if w2<left:
									res=(guess,guess+1,w2,max)
									begin=False
							else:
								pass
					else:#если равно и точно попали - сразу нашли нужное значение (случайно например)
						pass
					if left>self.GetTextWidth(a.text[a.soft_y][:1]):
						if w2!=left:
							dx1=left-res[0]
							dx2=res[1]-left
							if dx1>dx2:# ближе налево выбираем лево
								a.soft_x=res[0]
								self.CursorOffset=res[2]
							elif dx1<dx2:#ближе направо выбираем право
								a.soft_x=res[1]
								self.CursorOffset=res[3]
							else:#если одинаково - нужно выбрать либо влево либо вправо случайно либо одинаково всегда лучше вправо
								a.soft_x=res[1]
								self.CursorOffset=res[3]
						else:
							a.soft_x=guess
							self.CursorOffset=w2
							
					else:
						a.soft_x=0
						self.CursorOffset=0
					
				else:# Если ширина всей строки равна или меньше отступа то ставим курсор в конец этой строки
					a.soft_x=len(a.text[a.soft_y])
					self.CursorOffset=w
		else:# Если нет текста. А если нет текста в линии? 
			a.soft_x=0
			a.soft_y=0
		if a.soft_y<0:
			a.soft_y=0
		if a.soft_y>len(a.text):
			a.soft_y=len(a.text)
	def GetRect(self,x1,y1,x2,y2):
		w=max(x1,x2)-min(x1,x2)
		h=max(y1,y2)-min(y1,y2)
		r=Rect(min(x1,x2),min(y1,y2),w,h)
		return r
	def DispatchEvent(self,e):
		if e.type==KEYDOWN:
			if e.key==K_ESCAPE:
				self.ID=5
				self.TakeBackground2()
				self.FormFlag=True
		if e.type==QUIT:
			self.ID=5
			self.TakeBackground2()
			self.FormFlag=True
		if self.FormFlag:
			return 
		EVENT,x,y,delta_x,delta_y,e=self.ConvertEvent(e)
		iwant3=True# СЕКЦИЯ ДЛЯ ВРЕМЕННОГО СКРЫТИЯ ТЕКСТА ПРОГРАММЫ
		if iwant3:# РЕАКЦИЯ НА МЕНЮ
			self.ID=menu.Control(self,e)
			id=self.ID# юудет -1 если не на меню
			if id==2:# SAVE AS лучше
				self.SaveFormLoad=True
				self.TakeBackground2()
				self.FormFlag=True
			elif id==1:# Open
				self.OpenFormLoad=True
				self.TakeBackground2()
				self.FormFlag=True
			elif id==0:
				self.MapList={}
				self.ObjectList=[]
				self.Rel_x=0
				self.Rel_y=0
				self.LinesList=[]
				self.Background.fill(wh)
				self.SAVEPATH=''
				self.Redraw()# как понять, после какого экран сам обновится, а после какого нужно флаг менять?
			elif id==5:
				self.FlagMinimap=not self.FlagMinimap
				if self.FlagMinimap:
					self.MinimapLoad=True
					self.FormFlag=True
					self.ID=6
					self.TakeBackground2()
					self.Back.blit(self.Minimap,(0,768-200))
					self.NeedUpdate=True
				else:
					sc.blit(self.Background,(0,0))
					self.NeedUpdate=True
		if self.Focus!=-1:
			a=self.Focus
		if EVENT==M_LEFT_DOWN or EVENT==M_RIGHT_DOWN:
			obj=self.GetObject(x,y)
			if obj!=-1:
				a=self.ObjectList[obj]
				self.TakeBackground(a)
			if EVENT==M_LEFT_DOWN:
				x=e.dict['pos'][0]
				y=e.dict['pos'][1]
				if obj!=-1:# если есть объект
					if self.Focus!=-1:
						if obj!=self.ObjectList.index(self.Focus):
							a=self.ObjectList[obj]
							a.soft_x=0
							a.soft_y=0
							self.DrawObject(self.Focus)
							self.DrawText([self.Focus])
							self.Focus=a# МЕСТО ИЗМЕНЕНИЯ ФОКУСА
					else:# ТУТ ФОКУС ТОТ ЖЕ САМЫЙ ЧТО И ОБЪЕКТ 
						a=self.ObjectList[obj]
						self.Focus=self.ObjectList[obj]
					if self.FlagInsideHotPoint:# Для рисования линий
						if len(self.LineList)==0:
							self.LineList.append(obj)
						else:
							if self.LineList[0]!=obj:# БЕШЕНЫЙ КОСТЫЛЬ ДЛЯ РИСОВАНИЯ ЛИНИЙ
								tmp1=(self.LineList[0],obj)
								tmp2=(obj,self.LineList[0])
								if tmp1 not in self.LinesList and tmp2 not in self.LinesList:
									self.LinesList.append(tmp1)
									self.Redraw()
									self.LineList=[]
								else:
									if tmp1 in self.LinesList:
										self.LinesList.remove(tmp1)
									if tmp2 in self.LinesList:
										self.LinesList.remove(tmp2)
									self.LineList=[]
									self.Redraw()
					else:# Если внутри объекта - начинаем искать место для курсора - вынести в функцию?
						left,top=self.FindPlaceCursorPartA(x,y,a)
						self.FocusSelection=self.ObjectList.index(a)#длительная наверное операция
						self.FindPlaceCursorPartB(left,top,a)
						self.FlagTextSelection=True
						self.BeginTextSelection=(a.soft_x,a.soft_y)
						self.DrawCursor(a,bl)
				else:# если пусто под курсором пытаемся создать
					if y>50:# если не на меню
						b=self.PrepareObject(x,y)#задаем параметры
						self.TryCreateObject(b)# пытаемся создать - записать на карту и нарисовать
			elif EVENT==M_RIGHT_DOWN:
				if obj!=-1:# если не пусто
					a=self.ObjectList[obj]
					if obj not in self.ListSelection:
						self.ListSelection=[obj]
						self.DrawSelection(a,bl)
					self.Focus=a
					self.FlagTakeObj=True
					self.ObjectForReturn=(a.rx,a.ry)
					self.TakeBackground(a)# затратная операция - нужно выполнять только в четко расписанных случаях
					self.EraseSurf=Surface((a.w+10,a.h+10))
				else:
					self.FlagTakeMap=True
		elif EVENT==M_MIDDLE_DOWN:
			x=e.dict['pos'][0]
			y=e.dict['pos'][1]
			self.Selection=(x,y)
			self.FlagDrawSelection=True
		elif EVENT==M_MIDDLE_UP:
			self.FlagDrawSelection=False
			x1=self.Selection[0]
			y1=self.Selection[1]
			x=e.dict['pos'][0]
			y=e.dict['pos'][1]
			x2=x
			y2=y
			x1=x1+self.Rel_x
			y1=y1+self.Rel_y
			yk1=y1/64
			xk1=x1/64
			x2=x2+self.Rel_x
			y2=y2+self.Rel_y
			yk2=y2/64
			xk2=x2/64
			r=GetRect(x1,y1,x2,y2)
			BeginX=min(xk1,xk2)
			EndX=max(xk1,xk2)
			BeginY=min(yk1,yk2)
			EndY=max(yk1,yk2)
			list=[]
			for i in range(BeginY,EndY):
				for j in range(BeginX,EndX):
					if self.IsCellExist(i,j):
						for k in self.MapList[i][j]:
							if k not in list:
								list.append(k)
			list2=[]
			for i in list:
				a=self.ObjectList[i]
				x1=a.rx-10
				y1=a.ry-10
				x2=a.rx+a.w
				y2=a.ry+a.h
				r1=GetRect(x1,y1,x2,y2)#?
				if r.contains(r1):
					list2.append(i)
			self.ListSelection=list2[:]# думал что получаю список выделенных
			self.Redraw()
		elif EVENT==M_LEFT_UP or EVENT==M_RIGHT_UP:
			if EVENT==M_LEFT_UP:
				self.FlagTextSelection=False
			elif EVENT==M_RIGHT_UP:
				if self.FlagTakeObj:
					result=self.GetObjectUnder(x,y)
					if result!=-1:
						self.Focus.rx=self.ObjectForReturn[0]
						self.Focus.ry=self.ObjectForReturn[1]
						self.CorrectMap(self.Focus)
						a=self.Focus
						self.Redraw()
				self.FlagTakeMap=False
				self.FlagTakeObj=False
		elif EVENT==K_PRESS:
			k1=e.unicode
			if self.Focus!=-1:
				a=self.Focus
			else:
				a=None
			self.key_disp(a,k1,e)
			if e.key==K_ESCAPE:
				self.ID=5
				self.TakeBackground2()
				self.FormFlag=True # ЭТО МОЖЕТ БЫТЬ НЕВЕРНО
		elif EVENT==M_MOVE:
			if self.FlagTextSelection:
				self.DrawText([a])
				id=self.GetObject2(x,y)
				if id==self.FocusSelection:
					left,top=self.FindPlaceCursorPartA(x,y,a)
					self.FindPlaceCursorPartB(left,top,a)# выход за пределы
					self.EndTextSelection=(a.soft_x,a.soft_y)#
					p1=self.BeginTextSelection
					p2=self.EndTextSelection
					if p1[1]>p2[1]:
						p3=p2
						p4=p1
					elif p1[1]<p2[1]:
						p3=p1
						p4=p2
					elif p1[1]==p2[1]:
						if p1[0]>p2[0]:
							p3=p2
							p4=p1
						elif p1[0]<p2[0]:
							p3=p1
							p4=p2
						elif p1[0]==p2[0]:
							p3=p1
							p4=p2
					p1=p3
					p2=p4
					list=[]
					for i in range(p1[1],p2[1]+1):
						if i<len(a.text):
							end=len(a.text[i])
							if p1[1]==p2[1]:# Если всё на одной линии то от минимума до максимума
								list.append((p1[1],p1[0],p2[0]))
								break
							if i!=p2[1]:# есть линии ниже
								if i==p1[1]:# если первая линия - до конца
									list.append((i,p1[0],end))
								else:
									list.append((i,0,end))
							else:
								list.append((i,0,p2[0]))
								break
					txt=""
					for i in list:
						txt+=a.text[i[0]][i[1]:i[2]]+"\n"# ЧТО ЗА ОШИБКА? Это сборки строки для буфера обмена, что с ней?
					self.Scrap=txt[:]
					text=txt.encode('utf_16')
					# text=txt
					scrap.put ('text/plain;charset=utf-8', text)
					for j in range(0,len(list)):# Выделение текста цветом
						i=list[j]
						text=a.text[i[0]][i[1]:i[2]]
						if i[1]==0:
							w=0
						else:
							txt=a.text[i[0]][:i[1]]
							surf=Font2.render(txt,1,fc,wh)
							w = surf.get_width()
							surf=None
						text_surf=None
						text_surf=Font2.render(text,1,fc,(12,255,255))
						x=1+a.x+w
						y=i[0]*17+1+a.y
						self.Back.blit(text_surf,(x,y))# УМЕНЬШИТЬ В ЭТОМ МЕСТЕ
					self.DrawCursor(a,bl)
			if self.FlagDrawSelection:
				x1=self.Selection[0]
				y1=self.Selection[1]
				self.EndSelection=(x1,y1)
				self.Redraw()
				draw.polygon(self.Back,bl,((x1,y1),(x,y1),(x,y),(x1,y)),1)
				self.NeedUpdate=True
			if self.FlagTakeMap:
				self.Rel_x-=delta_x
				self.Rel_y-=delta_y
				self.Redraw()
			if self.FlagTakeObj:
				for i in self.ListSelection:
					a=self.ObjectList[i]
					a.rx+=delta_x
					a.ry+=delta_y
					self.CorrectMap(a)
				self.Redraw()
	def SaveAs(self):
		# print "SAVEAS!"
		self.SAVEPATH=self.PATH
		self.QuickSave()
		self.FlagNeedSaveAs=False
	def ChangeBorder(self,a):# Textedit 
		# print "ChangeBorder"
		a.h=len(a.text)*17+4
		a.w=a.MaxW+4
	def ConvertEvent(self,e):
		EVENT=-1
		x,y,delta_x,delta_y=0,0,0,0
		if e.type==MOUSEBUTTONDOWN:
			if e.dict['button']==3:
				EVENT=M_RIGHT_DOWN
			elif e.dict['button']==1:
				EVENT=M_LEFT_DOWN
			elif e.dict['button']==2:
				EVENT=M_MIDDLE_DOWN
		elif e.type==MOUSEBUTTONUP:
			if e.dict['button']==3:
				EVENT=M_RIGHT_UP
			elif e.dict['button']==2:
				EVENT=M_MIDDLE_UP
			elif e.dict['button']==1:
				EVENT=M_LEFT_UP
		elif e.type==MOUSEMOTION:
			EVENT=M_MOVE
		elif e.type==KEYDOWN:
			EVENT=K_PRESS
		elif e.type==QUIT:
			EVENT=QUIT
		if EVENT==M_MOVE:
			delta_x=e.dict['rel'][0]
			delta_y=e.dict['rel'][1]
		if EVENT in range(1,6):
			
			x=e.dict['pos'][0]
			y=e.dict['pos'][1]
			
		
		return EVENT,x,y,delta_x,delta_y,e
	def GetTextWidth(self,text):# Вычисляемое - используется для поиска положения курсора в строке путем перебора от начала строки
		# print "GetTextWidth"
		w = Font2.render(text,1,fc,wh).get_width()
		return w

def LoadConfig():
	filename="config.cfg"
	f=open(filename,'r')
	for i in f:
		p=string.find(i,":")
		key=i[:p]
		value=i[p+1:]
		if key=="askform":Askform=value[:-1]
		if key=="loaddefault":LoadDefault=value[:-1]
		if key=="loadpath":LoadPath=value[:-1].decode("utf_8")
	f.close()
	return Askform,LoadDefault,LoadPath
def Load(LoadPath):
	# print LoadPath
	if os.path.exists(LoadPath):
		# ЕСЛИ ОШИБКА НУЖНО ЗАГРУЗИТЬ КАКОЙ_ТО ДРУГОЙ ИЛИ ПО СПИСКУ ИЛИ ПЕРВЫЙ СУЩЕСТВУЮЩИЙ, ТОЖЕ ПОПЫТАТЬСЯ
		f1=open(LoadPath,"r")
		# отслеживаем переменные
		data=f1.readlines()
		data2=[]
		f1.close()
		for i in data:
			if i[-1:]=="\n":
				txt=unicode(i[:-1],encoding='utf-8')
				data2.append(txt)
			else:
				txt=unicode(i,encoding='utf-8')
				data2.append(txt)
		mymap = MyMap()
		mymap.Rel_x=int(data2[0])
		mymap.Rel_y=int(data2[1])
		count=int(data2[2])
		addr=2
		for i in range(count):
			a = text_box()
			a.x=int(data2[addr+1])
			a.y=int(data2[addr+2])
			a.rx=int(data2[addr+3])
			a.ry=int(data2[addr+4])
			a.w=int(data2[addr+5])
			a.h=int(data2[addr+6])
			a.soft_x=int(data2[addr+7])
			a.soft_y=int(data2[addr+8])
			a.etalon_w=int(data2[addr+9])
			a.MaxW=int(data2[addr+10])
			count2=int(data2[addr+11])
			a.text=[]
			for j in range(1,count2+1):
				if data2[addr+11+j][-1:]=="\n":
					
					a.text.append(data2[addr+11+j][:-1])
				else:
					a.text.append(data2[addr+11+j])
			mymap.ObjectList.append(a)
			addr=addr+11+j
		tmp4=[]
		for i in range(addr+1,len(data2)):
			tmp=data2[i].split(",")
			tmp3=(int(tmp[0]),int(tmp[1]))
			tmp4.append(tmp3)
		mymap.LinesList=tmp4[:]
		mymap.sc=sc
		for i in mymap.ObjectList:
			i.ConsistList=[]
			mymap.CorrectMap(i)
			if i.text==['']:
				i.TextSurf=Surface((i.w-2,i.h-2))
				i.TextSurf.fill(wh)
		mymap.SAVEPATH=LoadPath
		txt=LoadPath.encode('utf_8')
		display.set_caption(txt)
		filename="config.cfg"
		f=open(filename,'w')
		f.write("askform:0\n")
		f.write("loaddefault:1\n")
		# f.write("loadpath:"+LoadPath.decode('utf_8')+"\n")
		# В этом месте нужно сравнить текущий путь (глянуть в опенформ)
		# и часть пути без имени файла
		#
		#
		#
		# print "os.getcwd()",os.getcwd()
		# print "LoadPath",LoadPath
		# print "os.path.splitext(LoadPath)[0]",os.path.splitext(LoadPath)
		# print "os.path.relpath(LoadPath)",os.path.relpath(LoadPath) 
		LoadPath=os.path.relpath(LoadPath)
		f.write("loadpath:"+LoadPath.encode('utf_8')+"\n")
		f.close()
		list=mymap.ObjectList
		mymap.Redraw2(list)
		mymap.CLEAR=Surface((mymap.sc.get_size()))
		mymap.CLEAR.fill(wh)
		mymap.Background=Surface((sc.get_size()))
		minimap1=True
		if minimap1:# Вынести в функцию и вызывать при загрузке файла
			x_min,y_min,x_max,y_max=0,0,0,0
			x_min=mymap.ObjectList[0].ConsistList[0][1]
			y_min=mymap.ObjectList[0].ConsistList[0][0]
			for i in mymap.ObjectList:
				for j in i.ConsistList:
					if j[0]>y_max:
						y_max=j[0]
					if j[0]<y_min:
						y_min=j[0]
					if j[1]>x_max:
						x_max=j[1]
					if j[1]<x_min:
						x_min=j[1]
			mymap.MinXY=(x_min,y_min)
			x_max+=5
			y_max+=5
			if x_min>0:
				x_real=(x_max-x_min)*64
			else:
				x_real=(abs(x_min)+abs(x_max))*64
			if y_min>0:
				y_real=(y_max-y_min)*64
			else:
				y_real=(abs(y_min)+abs(y_max))*64
			x_koef=x_real/400.
			y_koef=y_real/200.
			Minimap=Surface((400,200))
			Minimap.fill((240,240,240))
			for i in mymap.ObjectList:
				x1=int((i.rx-10)/x_koef)
				x2=int((i.w+10)/x_koef)
				y1=int((i.ry-10)/y_koef)
				y2=int((i.h+10)/y_koef)
				R=Rect(x1,y1,x2,y2)
				draw.rect(Minimap, bl, R, 0)
			mymap.Minimap=Minimap
			mymap.KoefMinimap=(x_koef,y_koef)
	else:
		mymap = MyMap()
		mymap.sc=sc
	return mymap



def main():
	Askform,LoadDefault,LoadPath=LoadConfig()
	# print LoadPath
	mymap=Load(LoadPath)
	mymap.ListSelection=[]
	mymap.Redraw()
	going=True
	t1=time.clock()
	t3=0
	t4=0
	while going:
		"""
		отсчет времени,
		накапливать время
		первый замер
		второй показывает время между двумя замерами
		если времени прошло мало, меньше чем задумано,
		то прибавляем ещё несколько раз, циклов
		обнуляем если сравнялось
		считаем заново
		
		
		"""
		anim=True
		if anim:
			t2=time.clock()
			t3+=t2
			# print t3
			if t3>400 and t4<30:
				animobj=mymap.ObjectList[-2]
				animobj.rx+=2
				animobj.ry+=2
				t1=time.clock()
				mymap.Redraw()
				t3=0
				t4+=1
			
		if mymap.NeedUpdate:
			mymap.sc.blit(mymap.Back,(0,0))
			display.flip()
			mymap.NeedUpdate=False
		if mymap.FlagNeedLoad==True:
			mymap=Load(mymap.PATH)
			mymap.Redraw()
			mymap.ID=-1
		if mymap.FlagNeedSaveAs:
			mymap.SaveAs()
			mymap.ID=-1
		mymap.FlagNeedSaveAs=False
		mymap.FlagNeedLoad=False
		if mymap.Exit:
			quit()
			going=False
		if mymap.SaveAndExit:
			mymap.Save()
			if mymap.SAVEPATH!="":
				quit()
				going=False
			else:
				mymap.SaveAndExit=False
		if going:
			e=event.poll()
			if mymap.FormFlag==False:
				mymap.DispatchEvent(e)# это один объект а внутри другой и они не возвращаются?
			else:
				if mymap.ID==1:
					mymap=openform.dispatcher(mymap,e)
				elif mymap.ID==2:
					mymap=saveform.dispatcher(mymap,e)
				elif mymap.ID==5:
					mymap=confirm.dispatcher(mymap,e)
				elif mymap.ID==6:
					fn=minimap.control
					mymap=fn(mymap,e)
if __name__=='__main__':
	main()
