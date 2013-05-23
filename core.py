#-*-coding: cp1251 -*-
import os
def GetFilteredDirList(path,filter):
	list=[]
	temp_list=[]
	list=os.listdir(path)
	for i in list:
		FullName=path+"/"+i
		if os.path.isdir(FullName):
			temp_list.append(i)
	for i in list:
		FullName=path+"/"+i
		if not os.path.isdir(FullName):
			NameExt=os.path.splitext(i)[1]
			# if NameExt==filter:
			if NameExt==".map":# временно для тестов скролбара
				temp_list.append(i)
	return temp_list