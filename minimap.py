#-*-coding: cp1251 -*-
from pygame import *
import work01
import menu
def quit(mymap):
	
	work01.TakeBackground2(mymap)
	mymap.Back.blit(mymap.Background,(0,0))
	mymap.Back.blit(menu.menu.MainSurf,(menu.menu.position))

	mymap.BackWasSaved=False
	mymap.NeedUpdate=True
	mymap.FormFlag=False
	mymap.FlagMinimap=not mymap.FlagMinimap
	return mymap

def control(mymap,e):
	if mymap.MinimapLoad:
		mymap.FlagMinimapOperator=False
		mymap.Back.blit(menu.menu.MainSurf,(menu.menu.position))
		mymap.sc.blit(mymap.Back,(0,0))
		mymap.MinimapLoad=False
	mymap.Back.blit(menu.menu.MainSurf,(menu.menu.position))
	mymap.sc.blit(mymap.Back,(0,0))
	if e.type==MOUSEBUTTONDOWN:
		if e.dict['button']==1:
			id=menu.Control(mymap,e)
			if id==5:
				mymap=quit(mymap)
			mymap.FlagMinimapOperator=True
	if e.type==MOUSEBUTTONUP:
		if e.dict['button']==1:
			mymap.FlagMinimapOperator=False
	if e.type==MOUSEMOTION:
		if mymap.FlagMinimapOperator:
			x=e.dict['pos'][0]
			y=e.dict['pos'][1]
			x1=x
			y1=y-(768-200)
			if x1>-1 and x1<401 and y1>-1 and y1<201:
				kx=mymap.KoefMinimap[0]
				ky=mymap.KoefMinimap[1]
				min_x=mymap.MinXY[0]-5
				min_y=mymap.MinXY[1]
				new_x=int(kx*x1/64-min_x)
				new_y=int(ky*y1/64-min_y)
				mymap.Rel_x=new_x*64
				mymap.Rel_y=new_y*64
				work01.Redraw(mymap)
				mymap.Back.blit(mymap.Minimap,(0,768-200))
				mymap.NeedUpdate=True
	if e.type==KEYDOWN:
		if e.key==K_ESCAPE:
			mymap=quit(mymap)
	return mymap