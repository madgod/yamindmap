#-*-coding: cp1251 -*-
from pygame import *
import os
import core
init()
bg=50,50,50
fc=155,155,155
wh=255,255,255
bl=0,0,0
FormSurf=Surface((100,100))
FormSurf.fill(wh)
# Font3=font.Font(None,24)#Courier New
# Font3=font.SysFont('couriernew', 14, bold=True, italic=False)
Font3=font.SysFont('arial', 14, bold=False, italic=False)
text_surf=Font3.render("text",1,fc,wh)
FormSurf.blit(text_surf,(20,20))
TEXTEDIT=6
OK_BUT=4
CANCEL_BUT=5
CONTENT=8
SCROLLBAR=9

class Form:
	def __init__(self):
		self.Dirlist=[]# список файлов у контента
		self.Sbarlist=[]# И список объектов у скролл бара
		self.Focus=None
		self.background=(0,0,0)
		self.type='form'
		self.Elements=[]# Список объектов
		self.width=0
		self.height=0
		self.position=0
		self.MainSurf=None
		self.FlagTakeScroll=False
		self.Delta=0
	def Render(self):
		color=self.background
		width=self.width
		height=self.height
		self.MainSurf=Surface((width,height))
		self.MainSurf.fill(color)
		for i in self.Elements:
			# ЛУЧШЕ ДЛЯ КАЖДОГО ЭЛЕМЕНТА ВЫЗЫВАТЬ СВОЮ ФУНКЦИЮ ОТРИСОВКИ
			if i.type=='label':
				backcolor=i.background
				# С чего вдруг перестало кодироватьсЯ?
				# print "i.text= ",i.text
				text=unicode(i.text,encoding='cp1251')
				# text=text
				text_surf=Font3.render(text,1,bl,backcolor)
				self.MainSurf.blit(text_surf,i.position)
				# А как же рамка на кнопках? Эта визуализация зависит от типа - например, метка простая
				i.width=text_surf.get_width()
				i.height=text_surf.get_height()
			elif i.type=='button':
				draw.rect(self.MainSurf,wh,(i.background),0)
				draw.rect(self.MainSurf,(127,127,127),(i.shadow),3)
				draw.rect(self.MainSurf,bl,(i.border),1)
				text=unicode(i.text,encoding='cp1251')
				text_surf=Font3.render(text,1,bl,wh)
				x=(i.width/2-text_surf.get_width()/2)+i.position[0]#ошибка?
				y=(i.height/2-text_surf.get_height()/2)+i.position[1]
				t_pos=(x,y)
				self.MainSurf.blit(text_surf,t_pos)
			elif i.type=='textedit':
				draw.rect(self.MainSurf,wh,(i.position[0]-1,i.position[1]-1,i.width,i.height),0)
				draw.rect(self.MainSurf,(127,127,127),(i.position[0]-1,i.position[1]-1,i.width,i.height),1)
				text=i.text[0]
				text_surf=Font3.render(text,1,bl,wh)
				self.MainSurf.blit(text_surf,(i.position[0],i.position[1]+4))
			elif i.type=='content':
				pass
				i.getList()
				self.Dirlist=i.drawList()
				draw.rect(self.MainSurf,wh,((i.position),(i.width,i.height)),0)
				self.MainSurf.blit(i.surf,(i.position[0]+2,i.position[1]))
			elif i.type=='scrollbar':
				self.MainSurf.blit(i.left,(i.position))
				self.MainSurf.blit(i.right,(i.position[0]+i.width-16,i.position[1]))
				i.barPosition=(i.position[0]+16+i.bar_width*self.Elements[CONTENT].CURPAGE,i.position[1])
				self.MainSurf.blit(i.bar,i.barPosition)
				self.Sbarlist=[]
				self.Sbarlist.append(Rect((i.position[0]+212,i.position[1]+184),(15,15)))
				self.Sbarlist.append(Rect((i.position[0]+i.width-16+212,i.position[1]+184),(15,15)))
				self.Sbarlist.append(Rect((i.barPosition[0]+212,i.barPosition[1]+184),(i.bar_width,15)))
	def Control(self,e):#obj=textedit01
		if e.type==MOUSEBUTTONDOWN:
			obj=self.Focus
			if self.Focus[0]==TEXTEDIT:
				obj=self.Elements[6]# Это не нужно, нужно перенаправить на обработчик 
			elif self.Focus[0]==CONTENT:#Имена файлов
				obj=self.Elements[CONTENT]
				if self.Focus[1]!=-1:
					text=obj.list[self.Focus[1]]
					obj2=self.Elements[TEXTEDIT]
					NameFile=obj.path+os.sep+text
					if not os.path.isdir(NameFile):
						NameExt=os.path.splitext(NameFile)[1]
						if NameExt==".map":
							text1=unicode(text,encoding='cp1251')
							obj2.text[0]=text1
					if text=="..":
						uppath=os.path.split(obj.path)[0]
						obj.path=uppath
						obj.path2=core.GetFilteredDirList(uppath,".map")[:]
						obj.path2.insert(0,"..")
						obj.LASTPAGE=len(obj.path2)/17
						obj.getList()
						self.Elements[CONTENT].CURPAGE=0
						self.Elements[CONTENT].LASTPAGE=len(self.Elements[CONTENT].path2)/17
						self.Elements[CONTENT].Dirlist=self.Elements[CONTENT].drawList()# ?
						self.Elements[SCROLLBAR].bar_width=(obj.width-32)/(self.Elements[CONTENT].LASTPAGE+1)
						self.Elements[SCROLLBAR].drawBar()
						self.Elements[10].text=self.Elements[CONTENT].path# ОШИБКА!
					else:
						old_path=obj.path
						new_path=os.path.split(obj.path)[0]
						if old_path==new_path:
							path_temp=obj.path+text# ERROR!
						else:
							path_temp=obj.path+os.sep+text# ERROR!
						if os.path.isdir(path_temp):# Если это каталог - заходим внутрь = получаем новый список
							obj.path=path_temp
							uppath=obj.path
							obj.path2=''
							obj.path2=core.GetFilteredDirList(uppath,".map")[:]
							obj.path2.insert(0,"..")
							obj.getList()
							self.Elements[CONTENT].LASTPAGE=len(self.Elements[CONTENT].path2)/17
							self.Elements[CONTENT].CURPAGE=0
							self.Elements[CONTENT].Dirlist=self.Elements[CONTENT].drawList()
							self.Elements[SCROLLBAR].bar_width=(obj.width-32)/(self.Elements[CONTENT].LASTPAGE+1)
							self.Elements[SCROLLBAR].drawBar()
							self.Elements[10].text=self.Elements[CONTENT].path
					# должны перерисовать форму (желательно только текстедит)
					self.Render()
			elif self.Focus[0]==SCROLLBAR:# Стрелки и бар
				if self.Focus[1]==0:
					if self.Elements[CONTENT].CURPAGE!=0:
						self.Elements[CONTENT].CURPAGE-=1
				elif self.Focus[1]==1:
					if self.Elements[CONTENT].LASTPAGE!=self.Elements[CONTENT].CURPAGE:
						self.Elements[CONTENT].CURPAGE+=1
				elif self.Focus[1]==2:
					self.FlagTakeScroll=True
					obj=self.Elements[SCROLLBAR]
				self.Elements[SCROLLBAR].drawBar()
				self.Render()
				draw.rect(self.MainSurf,(0,255,0),((obj.barPosition),(obj.bar_width,obj.height)),0)
		if e.type==MOUSEBUTTONUP:
			self.FlagTakeScroll=False
			self.Delta=0
		if e.type==KEYDOWN:
			if e.key==K_ESCAPE:
				going=False#?
			else:
				obj=self.Elements[TEXTEDIT]
				obj.redraw(e,self)#можно передать и sc
		if e.type==MOUSEMOTION:
			if self.FlagTakeScroll:
				dx=e.dict['rel'][0]
				dy=e.dict['rel'][1]
				self.Delta+=dx
				if abs(self.Delta)>self.Elements[SCROLLBAR].bar_width:
					obj=self.Elements[SCROLLBAR]
					if self.Delta<0:
						if self.Elements[CONTENT].CURPAGE!=0:
							self.Elements[CONTENT].CURPAGE-=1
					elif self.Delta>0:
						if self.Elements[CONTENT].LASTPAGE!=self.Elements[CONTENT].CURPAGE:
							self.Elements[CONTENT].CURPAGE+=1
					obj.barPosition=(obj.position[0]+16+obj.bar_width*self.Elements[CONTENT].CURPAGE,obj.position[1])
					self.Elements[SCROLLBAR].drawBar()
					self.Render()
					self.Delta=0

	def getObj(self,e):
		x=e.dict['pos'][0]
		y=e.dict['pos'][1]
		id,id1=-1,-1
		for i in self.Elements:
			delta_x=self.position[0]
			delta_y=self.position[1]
			r=Rect((i.position[0]+delta_x,i.position[1]+delta_y),(i.width,i.height))
			if (r.collidepoint(x, y)):
				id=self.Elements.index(i)
				if id==8:
					for j in self.Dirlist:
						if j.collidepoint(x,y):
							id1=self.Dirlist.index(j)
				elif id==9:
					for j in self.Sbarlist:
						if j.collidepoint(x,y):
							id1 = self.Sbarlist.index(j)
		return(id,id1)
class Label:
	text=''
	type='label'
	width=0
	height=0
	background=(0,0,0)
	def getSize(self):
		text=unicode(self.text,encoding='cp1251')
		text_surf=Font3.render(self.text,1,bl,fc)
		self.width=text_surf.get_width()
		self.height=text_surf.get_height()

class Button:
	text=''
	type='button'
	color=(0,0,0)
	width=0
	height=0
	position=()
	background=0
	border=0
	shadow=0
	def getSize(self):
		text=unicode(self.text,encoding='cp1251')
		text_surf=Font3.render(self.text,1,bl,fc)
		self.width=text_surf.get_width()+4
		self.height=text_surf.get_height()+4
class Textedit:
	def __init__(self):
		self.type='textedit'
		self.text=['']
		self.last_cur_x=0
		self.lasr_cur_y=0
		self.cur_x=0
		self.cur_y=0# Если многострочный
		self.max_w=0
		self.width=0
		self.height=0
		self.position=()
		self.begin=0
		self.end=0
		self.wrap=False
		self.clearSurf=0
	def redraw(self,e,form):
		k1=e.unicode
		text=self.text[0]
		cur=self.cur_x
		if e.key==K_BACKSPACE:
			if cur>0:
				txt1=text[:cur-1]
				txt2=text[cur:]
				txt=txt1+txt2
				self.text[0]=txt[:]
				cur-=1
				if cur<self.begin:
					self.begin-=1# НЕКРАСИВО ВЫГЛЯДИТ - ничего не меняется. Наверное и правда придется показывать больше символов
				self.ShowText(form)
		elif e.key==K_DELETE:
			if len(text)>cur:
				txt1=text[:cur]
				txt2=text[cur+1:]
				txt=txt1+txt2
				self.text[0]=txt[:]
				self.ShowText(form)
		elif e.key==K_RETURN:# относится к кнопке ОК
			pass
		elif e.key==K_UP:# игнор
			pass
		elif e.key==K_DOWN:# игнор
			pass
		elif e.key==K_RIGHT:# переместить курсор направо
			pass
			self.DrawCur(form,wh)
			if len(text)>cur:
				cur+=1
			if cur>self.end:
				self.begin+=1
			# print "Right",self.begin,cur
			self.ShowText(form)
		elif e.key==K_LEFT:# переместить курсор налево перерисовать строку ограничить видимостью
			pass
			self.DrawCur(form,wh)
			if cur>0:
				cur-=1
			if cur<self.begin:
				self.begin-=1
			self.ShowText(form)
		elif e.key==K_HOME:# переместиться на начало строки отобразить то что будет видимо
			pass
			cur=0
		elif e.key==K_END:# переместиться на конец строки
			pass
			cur=len(text)
		elif e.key in range(39,123) or (e.key in range(39,123) and e.mod==1) or e.key==32 or (e.key==32 and e.mod==1):
			txt1=text[:cur]#left side
			txt2=text[cur:]
			txt=txt1+k1+txt2
			self.text[0]=txt[:]
			cur+=1
			self.ShowText(form)
		self.cur_x=cur
		self.DrawCur(form,bl)
	def DrawCur(self,form,color):
		if self.cur_x<self.end:
			txt=self.text[0][self.begin:self.cur_x]
		else:
			txt=self.text[0][self.begin:self.end]
		w=Font3.render(txt,1,bl,wh).get_width()
		x=self.position[0]
		y=self.position[1]
		draw.line(form.MainSurf,color,(x+w,y+4),(x+w,y+17),1)
	def ShowText(self,form):
		txt=self.text[0][self.begin:self.cur_x]
		w=Font3.render(txt,1,bl,wh).get_width()
		while w>self.width:# если от начала то курсора больше ширины в символах чем поле то:
			txt=self.text[0][self.begin:self.cur_x]
			w=Font3.render(txt,1,bl,wh).get_width()
			if w>self.width:
				self.begin+=1# ищем такое начало, от которого ширина станет меньше
		txt=self.text[0][self.begin:]
		w=Font3.render(txt,1,bl,wh).get_width()
		end=len(self.text[0])
		if w>self.width-10:
			for i in range(17,end):
				txt=self.text[0][self.begin:self.begin+i]
				w=Font3.render(txt,1,bl,wh).get_width()
				if w>self.width-10:
					break
			self.end=self.begin+i-1
		else:
			self.end=len(self.text[0])
		text_surf=Font3.render(self.text[0][self.begin:self.end],1,bl,wh)
		form.MainSurf.blit(self.clearSurf,(self.position))#-стирание поля
		form.MainSurf.blit(text_surf,(self.position[0],self.position[1]+4))
		return 0

class Content:
	content=[]
	type='content'
	path2=''
	path=''
	width=0
	height=0
	position=()
	CURPAGE=0
	LASTPAGE=0
	list=[]
	surf=0
	def getList(self):
		Addr=self.CURPAGE*16
		self.list=[]
		if len(self.path2)>Addr+16:
			self.list=self.path2[Addr:Addr+16]
		else:
			self.list=self.path2[Addr:]
	def drawList(self):
		l=[]
		l1=[]
		max_w=0
		for i in self.list:
			# print i
			text=unicode(i,encoding='cp1251')
			# print text
			# print text.encode('cp1251')
			text_surf=Font3.render(text,1,bl,wh)
			l.append(text_surf)
			w=text_surf.get_width()
			if max_w<w:
				max_w=w
		y=0
		self.surf=Surface((max_w,len(self.list)*16))
		self.surf.fill(wh)
		for i in l:
			self.surf.blit(i,(0,y))
			y+=16
			r=i.get_rect()
			r[0]=self.position[0]+212+2
			r[1]=y-16+self.position[1]+184
			l1.append(r)
		return l1

class Scrollbar:
	width=0
	height=0
	left=0
	right=0
	bar=0
	position=()
	type='scrollbar'
	bar_width=0
	barPosition=(0,0)
	def drawBar(self):
		self.left=Surface((15,15))
		self.right=Surface((15,15))
		self.bar=Surface((self.bar_width,15))
		self.left.fill(wh)
		self.right.fill(wh)
		pointlist1=((1,8),(14,1),(14,14))
		pointlist2=((1,1),(14,8),(1,14))
		draw.polygon(self.left, bl, pointlist1, 0)
		draw.polygon(self.right, bl, pointlist2, 0)