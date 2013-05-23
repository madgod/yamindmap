#-*-coding: cp1251 -*-
import os
from pygame import *
import time
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

ramka=0
if ramka==1:
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
			# первая причина несуществования ячейки
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
		DrawObject(a,self)
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
	
	def deb_text(self):
		pass

def DrawMenu(mymap):#
	# print "DrawMenu"
	surf=Surface((sc.get_width(),50))
	color=(240,240,240)
	surf.fill(color)
	mymap.sc.blit(surf,(0,0))
	mymap.NeedUpdate=True

def DrawCursor(a,color,mymap):# Textedit перерисовать курсор
	# print "DrawCursor"
	if a.soft_y<=len(a.text)-1:
		text=a.text[a.soft_y][:a.soft_x]
		hard_x=Font2.render(text,1,fc,wh).get_width()
		hard_y=a.ry+2+a.soft_y*17-mymap.Rel_y
		draw.line(mymap.Back,color,(2+a.rx+hard_x-mymap.Rel_x,hard_y+4),(a.rx+2+hard_x-mymap.Rel_x,hard_y+13),1)
		mymap.NeedUpdate=True

def DrawTextLine(a,mymap):# Textedit  # рисуем текущую линию текста
	# print "DrawTextLine"
	text=a.text[a.soft_y]
	text_surf=Font2.render(text,1,fc,wh)
	x=a.rx+2-mymap.Rel_x
	y=a.ry+2+a.soft_y*17-mymap.Rel_y
	mymap.sc.blit(text_surf,(x,y))

def DrawChar(a,mymap):# Textedit # вывести символ на экран (нужна интерактивность а скорость набора разная)
	text=a.text[a.soft_y][:a.soft_x]
	text_surf=Font2.render(text,1,fc,wh)
	
	if a.w_clear!=0:
		text=a.text[a.soft_y]
		text_surf=Font2.render(text,1,fc,wh)
		# высота поверхности 17
		x=a.rx+2-mymap.Rel_x
		y=a.ry+2+a.soft_y*17-mymap.Rel_y
		CalcMaxW(a,mymap)
		s2=Surface((a.w_clear,17))
		s2.fill(wh)
		mymap.sc.blit(s2,(x,y))
		mymap.sc.blit(text_surf,(x,y))
		mymap.NeedUpdate=True
		DrawCursor(a,bl,mymap)
	else:
		x=a.rx+2-mymap.Rel_x
		y=a.ry+2+a.soft_y*17-mymap.Rel_y
		CalcMaxW(a,mymap)
		mymap.sc.blit(text_surf,(x,y))
		DrawCursor(a,bl,mymap)
		mymap.NeedUpdate=True

def GetTextWidth(text):# Вычисляемое - используется для поиска положения курсора в строке путем перебора от начала строки
	# print "GetTextWidth"
	w = Font2.render(text,1,fc,wh).get_width()
	return w

def CalcMaxW(a,mymap):
	# print "CalcMaxW"
	a.MaxW=0
	for i in range(0,len(a.text)):
		w=GetTextWidth(a.text[i])
		if w>a.MaxW:
			a.MaxW=w
	ChangeBorder(a,mymap)
	DrawBorder(a,bl,mymap)
	CorrectMap(a,mymap)

def ChangeBorder(a,mymap):# Textedit 
	# print "ChangeBorder"
	a.h=len(a.text)*17+4
	a.w=a.MaxW+4

def CorrectMap(a,mymap):# без рендера
	# print "CorrectMap"
	TempConsistList=[]
	mymap.GetCellList(a)
	TempConsistList=mymap.ConsistList
	TempDelList=[]
	TempAppendList=[]
	TempDelList=GetTempDelList(a.ConsistList,TempConsistList)
	TempAppendList=GetTempAppendList(a.ConsistList,TempConsistList)
	DelFromMap(TempDelList,a,mymap)
	AppendOnMap(TempAppendList,a,mymap)
	a.ConsistList=TempConsistList[:]

def DelFromMap(TempDelList,a,mymap):# без рендера
	# print "DelFromMap"
	
	obj=mymap.ObjectList.index(a)
	for i in TempDelList:# для всех кортежей с координатами ячеек
		y=i[0]
		x=i[1]
		list2=[]
		flag=False
		if obj in mymap.MapList[y][x]:
			flag=True
		if flag==True:mymap.MapList[y][x].remove(obj)

def AppendOnMap(TempAppendList,a,mymap):# без рендера
	# print "AppendOnMap"
	for i in TempAppendList:
		y=i[0]
		x=i[1]
		obj=mymap.ObjectList.index(a)
		if not mymap.IsCellExist(y,x):
			mymap.CreateCell(y,x)
		mymap.MapList[y][x].append(obj)

def GetTempDelList(list1,list2):# без рендера
	# print "GetTempDelList"
	TempDelList=[]
	for i in list1:
		if i not in list2:
			TempDelList.append(i)
	return TempDelList

def GetTempAppendList(list1,list2):# без рендера
	# print "GetTempAppendList"
	TempAppendList=[]
	for i in list2:
		if i not in list1:
			TempAppendList.append(i)
	return TempAppendList

def DrawLabel(text,mymap):# вывести надпись
	# print "DrawLabel"
	mymap.sc.fill(wh,(300,40,50,50))
	mymap.sc.blit(Font2.render(text,1,fc,wh),(300,40))
	mymap.NeedUpdate=True

def DrawLabelXY(text,x,y,mymap):
	# print "DrawLabelXY"
	text_surf=Font3.render(text,1,fc,wh)
	mymap.Back.blit(text_surf,(x,y))
	mymap.NeedUpdate=True

def RedrawObject(a,mymap):# Textedit
	Redraw2([a],mymap)
	DrawObject(a,mymap)
	DrawText([a],mymap)
	DrawCursor(a,bl,mymap)
	mymap.NeedUpdate=True

def key_disp(a,k1,e,mymap):# обработать события клавиш Это контроллер текстового поля
	print e.key,e.mod,K_c,KMOD_LCTRL,~(~KMOD_CAPS&~KMOD_LCTRL)
	if (e.key==K_s and e.mod==KMOD_LCTRL)  or (e.key==K_s and e.mod==~(~KMOD_CAPS&~KMOD_LCTRL)):
		mymap.QuickSave()
	if (e.key==K_c and e.mod==KMOD_LCTRL)  or (e.key==K_c and e.mod==~(~KMOD_CAPS&~KMOD_LCTRL)):
		# print scrap.get_types ()
		txt=scrap.get('text/plain;charset=utf-8')
		if txt:
			txt3=txt.decode('utf_16')
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
			CalcMaxW(a,mymap)
			Redraw2([a],mymap)
			Redraw(mymap)
		
	if (e.key==K_z and e.mod==KMOD_LCTRL)  or (e.key==K_z and e.mod==~(~KMOD_CAPS&~KMOD_LCTRL)):
		pass
	if e.key==K_BACKSPACE:#бекспейс должен поднимать строки если дошел до начала
		# должно проходить по спецсимволам и в конце попадать на простой текст через elif else if
		DrawCursor(a,wh,mymap)
		if a.soft_x!=0: # Если не первый символ в строке
			ClearWithBackground(a,mymap)
			text1=a.text[a.soft_y][:a.soft_x-1]
			text2=a.text[a.soft_y][a.soft_x:]
			text=text1+text2
			text_surf=Font2.render(a.text[a.soft_y],1,fc,wh)
			a.w_clear=text_surf.get_width()
			a.soft_x-=1
			a.text[a.soft_y]=text[:]# меньше на один символ
			CalcMaxW(a,mymap)
			a.etalon_w=0
			a.line_pos=(a.soft_x, a.soft_y)
			RedrawObject(a,mymap)
		else:#если в самом начале строки
			if a.soft_y!=0:# Не верхняя строчка
				ClearWithBackground(a,mymap)
				text1=a.text[a.soft_y-1]
				text2=a.text[a.soft_y][:]
				a.text.remove(a.text[a.soft_y])
				a.soft_x=len(a.text[a.soft_y-1])
				a.text[a.soft_y-1]=text1+text2
				a.soft_y-=1
				CalcMaxW(a,mymap)
				RedrawObject(a,mymap)
				DrawCursor(a,bl,mymap)
	elif e.key==K_RETURN:
		DrawCursor(a,wh,mymap)
		ClearWithBackground(a,mymap)
		if a.soft_x==len(a.text[a.soft_y]):# Если конец строки
			a.w_clear=0
			a.text.append('')
			a.soft_x=0
			a.soft_y+=1
			CalcMaxW(a,mymap)
			RedrawObject(a,mymap)
		else:
			text1=a.text[a.soft_y][:a.soft_x]
			text2=a.text[a.soft_y][a.soft_x:]
			a.text.insert(a.soft_y+1,'')
			a.text[a.soft_y]=text1[:]
			a.text[a.soft_y+1]=text2[:]
			a.soft_x=0
			a.soft_y+=1
			CalcMaxW(a,mymap)
			RedrawObject(a,mymap)
	elif e.key==K_UP:
		if a.soft_y!=0:
			if a.etalon_w==0:
				text=a.text[a.line_pos[1]][:a.line_pos[0]]#IndexError: list index out of range
				text_surf=Font2.render(text,1,fc,wh)
				a.etalon_w=text_surf.get_width()
			mymap.NeedUpdate=True
			a.soft_y-=1
			for i in range(0,len(a.text[a.soft_y])):
				text=a.text[a.soft_y][:i]
				w_line=GetTextWidth(text)
				if w_line>a.etalon_w:
					w1= w_line-a.etalon_w
					text=a.text[a.soft_y][:i-1]
					w_line2=GetTextWidth(text)
					w2=a.etalon_w-w_line2
					if w2>w1:
						a.soft_x=i
					elif w2<w1:
						a.soft_x=i-1
					break
				if w_line==a.etalon_w:
					a.soft_x=i
					break
			Redraw2([a],mymap)
			DrawText([a],mymap)
			DrawCursor(a,bl,mymap)
	elif e.key==K_DOWN:
		if a.soft_y!=len(a.text)-1:
			# если эталон ширины равен 0 то посчитать '
			if a.etalon_w==0:
				text=a.text[a.line_pos[1]][:a.line_pos[0]]
				text_surf=Font2.render(text,1,fc,wh)
				a.etalon_w=text_surf.get_width()
			# DrawCursor(a,wh,mymap)
			# DrawTextLine(a,mymap)
			a.soft_y+=1
			for i in range(0,len(a.text[a.soft_y])):
				text=a.text[a.soft_y][:i]
				w_line=GetTextWidth(text)
				if w_line>a.etalon_w:
					w1= w_line-a.etalon_w
					text=a.text[a.soft_y][:i-1]
					w_line2=GetTextWidth(text)
					w2=a.etalon_w-w_line2
					if w2>w1:
						a.soft_x=i
					elif w2<w1:
						a.soft_x=i-1
					break
				if w_line==a.etalon_w:
					a.soft_x=i
					break
			Redraw2([a],mymap)
			DrawText([a],mymap)
			DrawCursor(a,bl,mymap)
	elif e.key==K_RIGHT:
		if a.soft_x!=len(a.text[a.soft_y]):
			a.soft_x+=1
			DrawText([a],mymap)
			DrawCursor(a,bl,mymap)
		a.etalon_w=0
		a.line_pos=(a.soft_x, a.soft_y)
	elif e.key==K_LEFT:
		if a.soft_x!=0:
			DrawCursor(a,wh,mymap)
			a.soft_x-=1
			DrawText([a],mymap)
			DrawCursor(a,bl,mymap)
		a.etalon_w=0
		a.line_pos=(a.soft_x, a.soft_y)
	elif e.key==K_HOME:
		ClearWithBackground(a,mymap)
		a.soft_x=0
		RedrawObject(a,mymap)
		DrawCursor(a,bl,mymap)
	elif e.key==K_END:
		ClearWithBackground(a,mymap)
		a.soft_x=len(a.text[a.soft_y])
		RedrawObject(a,mymap)
		DrawCursor(a,bl,mymap)
	elif e.key==K_DELETE:
		if len(a.text[a.soft_y])==a.soft_x:#  В конце строки
			if a.soft_y<len(a.text)-1:# если внизу есть строки
				text1=a.text[a.soft_y]
				text2=a.text[a.soft_y+1]# по идее не должно вылезать за пределы
				text=text1+text2
				a.text[a.soft_y]=text[:]
				a.text.remove(a.text[a.soft_y+1])
				CalcMaxW(a,mymap)
				Redraw2([a],mymap)
				TakeBackground(a,mymap)
				ClearWithBackground(a,mymap)#СПОРНЫЙ ВОПРОС
				
				DrawObject(a,mymap)# Вообще-то может измениться рамка
				DrawText([a],mymap)
				Redraw(mymap)
				DrawCursor(a,bl,mymap)
		else:# Посреди строки
			text1=a.text[a.soft_y][:a.soft_x]
			text2=a.text[a.soft_y][a.soft_x+1:]
			text=text1+text2
			a.text[a.soft_y]=text[:]
			CalcMaxW(a,mymap)
			Redraw2([a],mymap)
			TakeBackground(a,mymap)
			ClearWithBackground(a,mymap)
			DrawObject(a,mymap)# Вообще-то может измениться рамка
			DrawText([a],mymap)
			Redraw(mymap)
			DrawCursor(a,bl,mymap)
	elif (e.key in range(39,123) and e.mod!=64) or (e.key in range(39,123) and e.mod==1) or e.key==32 or (e.key==32 and e.mod==1):# обычный текст (нужно сделать автоперенос чтобы не вылезало за экран)
		if a!=None:
			ClearWithBackground(a,mymap)
			text1=a.text[a.soft_y][:a.soft_x]#left side
			text2=a.text[a.soft_y][a.soft_x:]
			text=text1+k1+text2
			a.text[a.soft_y]=text[:]
			a.soft_x+=1
			CalcMaxW(a,mymap)
			RedrawObject(a,mymap)
	
	
def ClearWithBackground(a,mymap):
	# print "ClearWithBackground"
	mymap.EraseSurf=Surface((a.w+10,a.h+10))
	mymap.EraseSurf.fill(wh)
	mymap.EraseSurf.blit(mymap.Background,(-(a.rx-mymap.Rel_x-10),-(a.ry-mymap.Rel_y-10)))
	mymap.Back.blit(mymap.EraseSurf,(a.rx-mymap.Rel_x-10,a.ry-mymap.Rel_y-10))

def PrepareObject(x,y,mymap):# Textedit # создать основной объект
	# print "PrepareObject"
	a = text_box()# создаем объект
	a.text=['']
	a.rx=x+mymap.Rel_x# реальные координаты
	a.ry=y+mymap.Rel_y# реальные координаты
	return a

def DrawText(list,mymap):# Использовать после загрузки
	# print "DrawText"
	for i in list:
		EraseSurf=Surface(i.TextSurf.get_size())
		EraseSurf.fill(wh)
		mymap.Back.blit(EraseSurf,(i.x+1,i.y+1))
		mymap.Back.blit(i.TextSurf,(i.x+1,i.y+1))
	mymap.NeedUpdate=True


def DrawText2(list,mymap):# Использовать после загрузки
	# print "DrawText"
	for i in list:
		if (i.text!=['']):
			x=i.x
			y=i.y-17
			for j in range(len(i.text)):
				y+=17
				text=i.text[j]
				text_surf=Font2.render(text,1,fc,wh)
				mymap.sc.blit(text_surf,(x+2,y+2))
	mymap.NeedUpdate=True
	
def Redraw(mymap):
	# print "Redraw"
	rel_x=mymap.Rel_x
	rel_y=mymap.Rel_y
	xk1=-(rel_x % 64)
	yk1=-(rel_y % 64)
	x_list=[]
	y_list=[]
	if mymap.FlagRamka:
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
				DrawLabelXY(text1+" : "+text2,x1+3,y1+3,mymap)
	mymap.Back=mymap.CLEAR
	mymap.Back.fill(wh)
	if mymap.LinesList!=[]:
		for i in mymap.LinesList:
			ObjA=i[0]
			ObjB=i[1]
			x1=mymap.ObjectList[ObjA].rx-mymap.Rel_x
			y1=mymap.ObjectList[ObjA].ry-mymap.Rel_y
			x2=mymap.ObjectList[ObjB].rx-mymap.Rel_x
			y2=mymap.ObjectList[ObjB].ry-mymap.Rel_y
			draw.line(mymap.Back,bl,(x1,y1),(x2,y2),1)
	list=GetScreenList(mymap)
	for i1 in list:
		a=mymap.ObjectList[i1]
		a.x=a.rx-mymap.Rel_x
		a.y=a.ry-mymap.Rel_y
		draw.circle(mymap.Back,wh,(a.x,a.y),10,0)# рисуем окружность по локальным координатам
		draw.circle(mymap.Back,bl,(a.x,a.y),10,1)
		draw.rect(mymap.Back, wh, (a.x,a.y,a.w,a.h), 0)# прямоугольник перекрывает окружность, которая нужна для операций с объектом
		draw.rect(mymap.Back, bl, (a.x,a.y,a.w,a.h), 1)
		DrawText([a],mymap)
	for i in mymap.ListSelection:# оставляем выделение при навигации по карте
			a=mymap.ObjectList[i]
			DrawSelection(a,bl,mymap)
	mymap.Back.blit(menu.menu.MainSurf,(menu.menu.position))# это можно исключить, если копировать мимо меню
	mymap.NeedUpdate=True

def Redraw2(list,mymap):
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

def GetScreenList(mymap):#Без рендера
	# print "GetScreenList"
	rel_x=mymap.Rel_x
	rel_y=mymap.Rel_y
	rel_xk=rel_x/64
	rel_yk=rel_y/64
	list=[]
	for i in range(rel_yk, rel_yk+14):#14? O_o
		for j in range(rel_xk,rel_xk+18):#18? o_O
			if mymap.IsCellExist(i,j):
				if mymap.MapList[i][j]!=[]:
					for k in mymap.MapList[i][j]:
						if k not in list:# длительная операция может лучше словарь?
							list.append(k)
	return list

def TakeBackground(a,mymap):# берет без одного объекта
	# print "TakeBackground"
	Background=mymap.Background
	Background.fill(wh)
	rel_x=mymap.Rel_x
	rel_y=mymap.Rel_y
	xk1=(rel_x/64*64)-rel_x
	yk1=(rel_y/64*64)-rel_y
	x_list=[]
	y_list=[]
	if mymap.FlagRamka:
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
	list=GetScreenList(mymap)
	idx=mymap.ObjectList.index(a)
	for i1 in list:
		if i1!=idx:
			i=mymap.ObjectList[i1]
			i.x=i.rx-mymap.Rel_x
			i.y=i.ry-mymap.Rel_y
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
	mymap.Background=Background

def TakeBackground2(mymap):# берет без одного объекта
	# print "TakeBackground"
	Background=mymap.Background
	Background.fill(wh)
	rel_x=mymap.Rel_x
	rel_y=mymap.Rel_y
	xk1=(rel_x/64*64)-rel_x
	yk1=(rel_y/64*64)-rel_y
	x_list=[]
	y_list=[]
	if mymap.FlagRamka:
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
	list=GetScreenList(mymap)
	for i1 in list:
		i=mymap.ObjectList[i1]
		i.x=i.rx-mymap.Rel_x
		i.y=i.ry-mymap.Rel_y
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
	mymap.Background=Background

def DrawObject(a,mymap):# отрисовать основной объект
	# print "DrawObject"
	a.x=a.rx-mymap.Rel_x# Что за дела тут после ДЕЛа? 
	a.y=a.ry-mymap.Rel_y
	draw.circle(mymap.Back,wh,(a.x,a.y),10,0)# рисуем окружность по локальным координатам
	draw.circle(mymap.Back,bl,(a.x,a.y),10,1)
	draw.rect(mymap.Back, wh, (a.x,a.y,a.w,a.h), 0)# прямоугольник перекрывает окружность, которая нужна для операций с объектом
	draw.rect(mymap.Back, bl, (a.x,a.y,a.w,a.h), 1)

def DrawBorder(a,color,mymap):# Textedit 
	# print "DrawBorder"
	draw.rect(mymap.Back, color, (a.rx-mymap.Rel_x,a.ry-mymap.Rel_y,a.w,a.h), 1)
	mymap.NeedUpdate=True

def DrawSelection(a,color,mymap):# Textedit 
	# print "DrawBorder"
	# draw.rect(sc, color, (a.rx-mymap.Rel_x-2,a.ry-mymap.Rel_y-2,a.w+3,a.h+3), 3)
	draw.rect(mymap.Back, color, (a.rx-mymap.Rel_x-2,a.ry-mymap.Rel_y-2,a.w+3,a.h+3), 3)
	mymap.NeedUpdate=True

def GetObject(x,y,mymap):# без рендер
	# print "GetObject"
	x=x+mymap.Rel_x
	y=y+mymap.Rel_y
	yk=y/64
	xk=x/64
	mymap.FlagInsideHotPoint=False
	mymap.FlagInsideObj=False
	if mymap.IsCellExist(yk,xk):
		list=mymap.MapList[yk][xk]
		if list:
			for j in list:
				i=mymap.ObjectList[j]
				if x>i.rx-10 and x<i.rx+10 and y>i.ry-10 and y<i.ry+10:
					mymap.FlagInsideHotPoint=True
				if x>i.rx and x<i.rx+i.w and y>i.ry and y<i.ry+i.h:
					mymap.FlagInsideObj=True
				if mymap.FlagInsideHotPoint==True and mymap.FlagInsideObj==True:
					mymap.FlagInsideHotPoint=False
				if mymap.FlagInsideHotPoint==True or mymap.FlagInsideObj==True:
					break
		if mymap.FlagInsideHotPoint==True or mymap.FlagInsideObj==True:
			return mymap.ObjectList.index(i)
	return -1


def GetObject2(x,y,mymap):# без рендер
	# print "GetObject"
	x=x+mymap.Rel_x
	y=y+mymap.Rel_y
	yk=y/64
	xk=x/64
	mymap.FlagInsideHotPoint=False
	mymap.FlagInsideObj=False
	if mymap.IsCellExist(yk,xk):
		list=mymap.MapList[yk][xk]
		
		if list:
			for j in list:
				i=mymap.ObjectList[j]
				if x>i.rx and x<i.rx+i.w and y>i.ry and y<i.ry+i.h:
					mymap.FlagInsideObj=True
				if mymap.FlagInsideObj==True:
					break
		if mymap.FlagInsideObj==True:
			return mymap.ObjectList.index(i)
	return -1
	

def GetObjectUnder(x,y,mymap):
	x=x+mymap.Rel_x
	y=y+mymap.Rel_y
	yk=y/64
	xk=x/64
	# может и не быть таких ячеек, проверить!
	flag=False
	list1=[]
	list=[]
	curObj=mymap.Focus
	curObj1=mymap.ObjectList.index(curObj)
	x1=curObj.rx-10
	x2=curObj.rx+curObj.w
	y1=curObj.ry-10
	y2=curObj.ry+curObj.h
	R1=Rect((x1,y1,x2-x1,y2-y1))
	for k in range(len(curObj.ConsistList)):
		yk=curObj.ConsistList[k][0]
		xk=curObj.ConsistList[k][1]
		list=mymap.MapList[yk][xk][:]
		if curObj1 in list:
			list.remove(curObj1)
		if list:
			for j in list:
				i=mymap.ObjectList[j]
				x1=i.rx-10
				x2=i.rx+i.w
				y1=i.ry-10
				y2=i.ry+i.h
				R2=Rect((x1,y1,x2-x1,y2-y1))
				if R1.colliderect(R2):
					if i!=curObj1:
						result=mymap.ObjectList.index(i)
						if result not in list1:
							list1.append(result)
					
	if len(list1)>0:
		return list1
		
	else:
		return -1

def ConvertEvent(e):
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


def FindPlaceCursorPartA(x,y,a,mymap):
	left=x-(a.rx-mymap.Rel_x)-2
	top=y-(a.ry-mymap.Rel_y)-2
	return left,top

def FindPlaceCursorPartB(left,top,a,mymap):
	DrawCursor(a,wh,mymap)
	if a.text!=['']:
		a.soft_y=top/17 # с У все верно вроде
		global count3
		w3=0
		if len(a.text)-1>=a.soft_y:
			w=GetTextWidth(a.text[a.soft_y])# ошибка как может быть soft_y>0 ?
			if w>left:# если курсор стал в конце строки то ставим курсор после последнего символа
				avr=w/len(a.text[a.soft_y])
				guess=left/avr
				w2=GetTextWidth(a.text[a.soft_y][:guess])
				begin=True
				if w2<left:
					while begin:
						guess+=1
						min=w2
						w2=GetTextWidth(a.text[a.soft_y][:guess])# Сравняется ли min и w2 после этого вычисления?
						if w2>left:
							res=(guess-1,guess,min,w2)
							begin=False
				elif w2>left:
					if left>GetTextWidth(a.text[a.soft_y][:1]):
						while begin:
							guess+=-1# уменьшаем или увеличиваем
							max=w2
							w2=GetTextWidth(a.text[a.soft_y][:guess])
							if w2<left:
								res=(guess,guess+1,w2,max)
								begin=False
						else:
							pass
				else:#если равно и точно попали - сразу нашли нужное значение (случайно например)
					pass
				if left>GetTextWidth(a.text[a.soft_y][:1]):
					if w2!=left:
						dx1=left-res[0]
						dx2=res[1]-left
						if dx1>dx2:# ближе налево выбираем лево
							a.soft_x=res[0]
							mymap.CursorOffset=res[2]
						elif dx1<dx2:#ближе направо выбираем право
							a.soft_x=res[1]
							mymap.CursorOffset=res[3]
						else:#если одинаково - нужно выбрать либо влево либо вправо случайно либо одинаково всегда лучше вправо
							a.soft_x=res[1]
							mymap.CursorOffset=res[3]
					else:
						a.soft_x=guess
						mymap.CursorOffset=w2
						
				else:
					a.soft_x=0
					mymap.CursorOffset=0
				
			else:# Если ширина всей строки равна или меньше отступа то ставим курсор в конец этой строки
				a.soft_x=len(a.text[a.soft_y])
				mymap.CursorOffset=w
	else:# Если нет текста. А если нет текста в линии? 
		a.soft_x=0
		a.soft_y=0
	if a.soft_y<0:
		a.soft_y=0
	if a.soft_y>len(a.text):
		a.soft_y=len(a.text)


def FindPlaceCursorPartB2(left,top,a,mymap):
	DrawCursor(a,wh,mymap)
	if a.text!=['']:
		a.soft_y=top/17 # с У все верно вроде
		global count3
		w3=0
		if len(a.text)-1>=a.soft_y:
			w=GetTextWidth(a.text[a.soft_y])# ошибка как может быть soft_y>0 ?
			if w>left:
				for i in range(0,len(a.text[a.soft_y])):# Перебираем всю строку
					w4=GetTextWidth(a.text[a.soft_y][i-1:i])# ширина одного символа
					w3+=w4# сумма ширин символов от начала строки - замена w
					w1=w3-w4# Сумма от начала строки до прошлого символа
					w1=GetTextWidth(a.text[a.soft_y][:i-1])
					w5=w3-1
					if w5>left:
						dx1=w5-left
						dx2=left-w1
						if dx1>dx2:
							a.soft_x=i-1
							mymap.CursorOffset=w1
						elif dx1<dx2:
							a.soft_x=i
							mymap.CursorOffset=w5
						else:
							a.soft_x=i-1
							mymap.CursorOffset=w1
						break
					elif w5==left:
						a.soft_x=i
						mymap.CursorOffset=w5
						break
			else:# Если линия такая же или меньше
				a.soft_x=len(a.text[a.soft_y])
	else:# Если нет текста. А если нет текста в линии? 
		a.soft_x=0
		a.soft_y=0
def GetRect(x1,y1,x2,y2):
	w=max(x1,x2)-min(x1,x2)
	h=max(y1,y2)-min(y1,y2)
	r=Rect(min(x1,x2),min(y1,y2),w,h)
	return r

def DispatchEvent(mymap,e):
	if e.type==KEYDOWN:
		if e.key==K_ESCAPE:
			mymap.ID=5
			TakeBackground2(mymap)
			mymap.FormFlag=True
	if e.type==QUIT:
		mymap.ID=5
		TakeBackground2(mymap)
		mymap.FormFlag=True
	if mymap.FormFlag:
		return mymap
	EVENT,x,y,delta_x,delta_y,e=ConvertEvent(e)
	iwant3=True# СЕКЦИЯ ДЛЯ ВРЕМЕННОГО СКРЫТИЯ ТЕКСТА ПРОГРАММЫ
	if iwant3:# РЕАКЦИЯ НА МЕНЮ
		mymap.ID=menu.Control(mymap,e)
		id=mymap.ID# юудет -1 если не на меню
		if id==2:# SAVE AS лучше
			mymap.SaveFormLoad=True
			TakeBackground2(mymap)
			mymap.FormFlag=True
		elif id==1:# Open
			mymap.OpenFormLoad=True
			TakeBackground2(mymap)
			mymap.FormFlag=True
		elif id==0:
			mymap.MapList={}
			mymap.ObjectList=[]
			mymap.Rel_x=0
			mymap.Rel_y=0
			mymap.LinesList=[]
			mymap.Background.fill(wh)
			mymap.SAVEPATH=''
			Redraw(mymap)# как понять, после какого экран сам обновится, а после какого нужно флаг менять?
		elif id==5:
			mymap.FlagMinimap=not mymap.FlagMinimap
			if mymap.FlagMinimap:
				mymap.MinimapLoad=True
				mymap.FormFlag=True
				mymap.ID=6
				TakeBackground2(mymap)
				mymap.Back.blit(mymap.Minimap,(0,768-200))
				mymap.NeedUpdate=True
			else:
				sc.blit(mymap.Background,(0,0))
				mymap.NeedUpdate=True
	if mymap.Focus!=-1:
		a=mymap.Focus
	if EVENT==M_LEFT_DOWN or EVENT==M_RIGHT_DOWN:
		obj=GetObject(x,y,mymap)
		if obj!=-1:
			a=mymap.ObjectList[obj]
			TakeBackground(a,mymap)
		if EVENT==M_LEFT_DOWN:
			x=e.dict['pos'][0]
			y=e.dict['pos'][1]
			if obj!=-1:# если есть объект
				if mymap.Focus!=-1:
					if obj!=mymap.ObjectList.index(mymap.Focus):
						a=mymap.ObjectList[obj]
						a.soft_x=0
						a.soft_y=0
						DrawObject(mymap.Focus,mymap)
						DrawText([mymap.Focus],mymap)
						mymap.Focus=a# МЕСТО ИЗМЕНЕНИЯ ФОКУСА
				else:# ТУТ ФОКУС ТОТ ЖЕ САМЫЙ ЧТО И ОБЪЕКТ 
					a=mymap.ObjectList[obj]
					mymap.Focus=mymap.ObjectList[obj]
				if mymap.FlagInsideHotPoint:# Для рисования линий
					if len(mymap.LineList)==0:
						mymap.LineList.append(obj)
					else:
						if mymap.LineList[0]!=obj:# БЕШЕНЫЙ КОСТЫЛЬ ДЛЯ РИСОВАНИЯ ЛИНИЙ
							tmp1=(mymap.LineList[0],obj)
							tmp2=(obj,mymap.LineList[0])
							if tmp1 not in mymap.LinesList and tmp2 not in mymap.LinesList:
								mymap.LinesList.append(tmp1)
								Redraw(mymap)
								mymap.LineList=[]
							else:
								if tmp1 in mymap.LinesList:
									mymap.LinesList.remove(tmp1)
								if tmp2 in mymap.LinesList:
									mymap.LinesList.remove(tmp2)
								mymap.LineList=[]
								Redraw(mymap)
				else:# Если внутри объекта - начинаем искать место для курсора - вынести в функцию?
					left,top=FindPlaceCursorPartA(x,y,a,mymap)
					mymap.FocusSelection=mymap.ObjectList.index(a)#длительная наверное операция
					FindPlaceCursorPartB(left,top,a,mymap)
					mymap.FlagTextSelection=True
					mymap.BeginTextSelection=(a.soft_x,a.soft_y)
					DrawCursor(a,bl,mymap)
			else:# если пусто под курсором пытаемся создать
				if y>50:# если не на меню
					b=PrepareObject(x,y,mymap)#задаем параметры
					mymap.TryCreateObject(b)# пытаемся создать - записать на карту и нарисовать
		elif EVENT==M_RIGHT_DOWN:
			if obj!=-1:# если не пусто
				a=mymap.ObjectList[obj]
				if obj not in mymap.ListSelection:
					mymap.ListSelection=[obj]
					DrawSelection(a,bl,mymap)
				mymap.Focus=a
				mymap.FlagTakeObj=True
				mymap.ObjectForReturn=(a.rx,a.ry)
				TakeBackground(a,mymap)# затратная операция - нужно выполнять только в четко расписанных случаях
				mymap.EraseSurf=Surface((a.w+10,a.h+10))
			else:
				mymap.FlagTakeMap=True
	elif EVENT==M_MIDDLE_DOWN:
		x=e.dict['pos'][0]
		y=e.dict['pos'][1]
		mymap.Selection=(x,y)
		mymap.FlagDrawSelection=True
	elif EVENT==M_MIDDLE_UP:
		mymap.FlagDrawSelection=False
		x1=mymap.Selection[0]
		y1=mymap.Selection[1]
		x=e.dict['pos'][0]
		y=e.dict['pos'][1]
		x2=x
		y2=y
		x1=x1+mymap.Rel_x
		y1=y1+mymap.Rel_y
		yk1=y1/64
		xk1=x1/64
		x2=x2+mymap.Rel_x
		y2=y2+mymap.Rel_y
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
				if mymap.IsCellExist(i,j):
					for k in mymap.MapList[i][j]:
						if k not in list:
							list.append(k)
		list2=[]
		for i in list:
			a=mymap.ObjectList[i]
			x1=a.rx-10
			y1=a.ry-10
			x2=a.rx+a.w
			y2=a.ry+a.h
			r1=GetRect(x1,y1,x2,y2)
			if r.contains(r1):
				list2.append(i)
		mymap.ListSelection=list2[:]# думал что получаю список выделенных
		Redraw(mymap)
	elif EVENT==M_LEFT_UP or EVENT==M_RIGHT_UP:
		if EVENT==M_LEFT_UP:
			mymap.FlagTextSelection=False
		elif EVENT==M_RIGHT_UP:
			if mymap.FlagTakeObj:
				result=GetObjectUnder(x,y,mymap)
				if result!=-1:
					mymap.Focus.rx=mymap.ObjectForReturn[0]
					mymap.Focus.ry=mymap.ObjectForReturn[1]
					CorrectMap(mymap.Focus,mymap)
					a=mymap.Focus
					Redraw(mymap)
			mymap.FlagTakeMap=False
			mymap.FlagTakeObj=False
	elif EVENT==K_PRESS:
		k1=e.unicode
		if mymap.Focus!=-1:
			a=mymap.Focus
		else:
			a=None
		key_disp(a,k1,e,mymap)
		if e.key==K_ESCAPE:
			mymap.ID=5
			TakeBackground2(mymap)
			mymap.FormFlag=True # ЭТО МОЖЕТ БЫТЬ НЕВЕРНО
	elif EVENT==M_MOVE:
		if mymap.FlagTextSelection:
			DrawText([a],mymap)
			id=GetObject2(x,y,mymap)
			if id==mymap.FocusSelection:
				left,top=FindPlaceCursorPartA(x,y,a,mymap)
				FindPlaceCursorPartB(left,top,a,mymap)# выход за пределы
				mymap.EndTextSelection=(a.soft_x,a.soft_y)#
				p1=mymap.BeginTextSelection
				p2=mymap.EndTextSelection
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
				mymap.Scrap=txt[:]
				text=txt.encode('utf_16')
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
					mymap.Back.blit(text_surf,(x,y))# УМЕНЬШИТЬ В ЭТОМ МЕСТЕ
				DrawCursor(a,bl,mymap)
		if mymap.FlagDrawSelection:
			x1=mymap.Selection[0]
			y1=mymap.Selection[1]
			mymap.EndSelection=(x1,y1)
			Redraw(mymap)
			draw.polygon(mymap.Back,bl,((x1,y1),(x,y1),(x,y),(x1,y)),1)
			mymap.NeedUpdate=True
		if mymap.FlagTakeMap:
			mymap.Rel_x-=delta_x
			mymap.Rel_y-=delta_y
			Redraw(mymap)
		if mymap.FlagTakeObj:
			for i in mymap.ListSelection:
				a=mymap.ObjectList[i]
				a.rx+=delta_x
				a.ry+=delta_y
				CorrectMap(a,mymap)
			Redraw(mymap)
	return mymap

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

def LoadAs(mymap):
	# print "LOAD!"
	mymap=Load(mymap.PATH)
	mymap.FlagNeedLoad=False
	return mymap

def SaveAs(mymap):
	# print "SAVEAS!"
	mymap.SAVEPATH=mymap.PATH
	mymap.QuickSave()
	mymap.FlagNeedSaveAs=False

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
			CorrectMap(i,mymap)
		mymap.SAVEPATH=LoadPath
		txt=LoadPath.encode('utf_8')
		display.set_caption(txt)
		filename="config.cfg"
		f=open(filename,'w')
		f.write("askform:0\n")
		f.write("loaddefault:1\n")
		# f.write("loadpath:"+LoadPath.decode('utf_8')+"\n")
		f.write("loadpath:"+LoadPath.encode('utf_8')+"\n")
		f.close()
		list=mymap.ObjectList
		Redraw2(list,mymap)
		mymap.CLEAR=Surface((mymap.sc.get_size()))
		mymap.CLEAR.fill(wh)
		mymap.Background=Surface((sc.get_size()))
	else:
		mymap = MyMap()
		mymap.sc=sc
	return mymap

def main():
	Askform,LoadDefault,LoadPath=LoadConfig()
	print LoadPath
	mymap=Load(LoadPath)
	mymap.ListSelection=[]
	Redraw(mymap)
	minimap1=True
	if minimap1:
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
	going=True
	while going:
		if mymap.NeedUpdate:
			mymap.sc.blit(mymap.Back,(0,0))
			display.update()
			mymap.NeedUpdate=False
		if mymap.FlagNeedLoad==True:
			mymap=Load(mymap.PATH)
			Redraw(mymap)
			mymap.ID=-1
		if mymap.FlagNeedSaveAs:
			SaveAs(mymap)
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
				mymap=DispatchEvent(mymap,e)# это один объект а внутри другой и они не возвращаются?
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
