# -*- coding: utf-8 -*-
"""

"""

import cv2  
import numpy as np    
# import heatmap
import os
from PIL import Image
import csv
import math

"""
预设参数
"""
pic_height=436
pic_width=422
vessel_Dir = os.listdir(os.path.dirname(os.getcwd())+'/vesselsegmentation/output/')
remove_illu_Dir = os.listdir(os.path.dirname(os.getcwd())+'/vesselsegmentation/input/')
focus_Dir = os.listdir(os.path.dirname(os.getcwd())+'/find od/input/focus/')
focus_threshold=10
macula_radius_para=1.5

class Node:
    center=[]
    father=[]
    son=[]
#    def __init__(self,center,father,son):
#        self.son=[]
#        self.center=center
#        self.father=father
#        self.son.append(son)
    def __init__(self,center,father):
        self.center=center
        self.father=father
        for i in range(len(self.son)):
            self.son.pop()


"""
打开图片
"""
def OpenPic(src,Dir_str):
    src_found=""
    Dir = os.listdir(Dir_str)
    for i in range(len(Dir)):
        if Dir[i].find(src)>=0:# and Dir[i].find(".png")>0:
#            print src[:len(src)-8],"*",focus_Dir[i]
            src_found=Dir[i]
            break
        else:
            if i is range(len(Dir)-1):
                print (src,"PICTURE NOT FOUND!")
    print (src_found)
    return cv2.imread(Dir_str+src_found)
    

"""
导入OD数据
"""
datas = []
with open(os.path.dirname(os.getcwd())+'/find od/output/OD_result.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        datas.append(row)
    for i in range(1, len(datas)):
        datas[i - 1] = datas[i]
        datas[i] = []
    del datas[len(datas)-1]
#    print datas
csvfile.close()

"""
高斯滤波核
"""
kernel=np.uint8(np.zeros((5,5)))
for x in range(5):
    kernel[x,2]=1;
    kernel[2,x]=1;
    
"""
计算两点之间的距离
"""
def distance(x1,y1,x2,y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5

"""
直线方程
"""
def equation_y(x,x1,y1,x2,y2):
    if not x1-x2== 0:
        # return (x * (y2 - y1) + x1 * y1 - x1 * y2 - x1 * y1 + x2 * y1) / (float)(x2 - x1)
        return (x*(y1-y2)-x2*y1+x2*y2-x2*y2+x1*y2)/float(x1-x2)
    else:
        return 0

"""
指定长度画线
"""
def DrawLength(l,x1,y1,x2,y2,colour="r",pic="vsl"):
    a=x2-x1
    b=y2-y1
    c=(a**2+b**2)**0.5
    sin=b/c
    cos=a/c
    j=int(l*cos)
    i=int(l*sin)
    if colour=="r" and pic=="vsl":
        cv2.line(vsl, (OD_x, OD_y), (OD_x+j, OD_y+i), (255, 200, 0), 2)
    elif colour=="g"and pic=="vsl":
        cv2.line(vsl, (OD_x, OD_y), (OD_x+j, OD_y+i), (0, 255, 0), 1)
    elif colour=="r" and pic=="ori":
        cv2.line(ori, (OD_x, OD_y), (OD_x+j, OD_y+i), (255, 200, 0), 2)
    elif colour=="g"and pic=="ori":
        cv2.line(ori, (OD_x, OD_y), (OD_x+j, OD_y+i), (0, 255, 0), 1)
    return j,i

"""
连接方向
"""
def MakeArrows(arrows):
#    cv2.imshow("",vsl)
#    cv2.waitKey(0)
    for i in range(0,len(vsl),12):
        for j in range(0,len(vsl[0]),12):
            if vsl[i][j][0]==255:
                # cv2.line(vsl, (OD_x,OD_y), (j, i), (0, 255, 0), 1)
#                jj,ii=DrawLength(100,OD_x,OD_y,j,i,colour="g",pic="vsl")
                jj,ii=DrawLength(100,OD_x,OD_y,j,i,colour="g",pic="vsl")
                # print "----------",(jj**2+ii**2)**0.5
                arrows.append((jj,ii))
    return arrows

"""
寻找最暗点为黄斑
"""

def FindMacula(AverPointX,AverPointY,AverPointR):
    def AroundDark(i, j):
        return ori[i, j, 1]  # +ori[i,j-1,1]+ori[i,j+1,1]+ori[i-1,j,1]+ori[i-1,j+1,1]+ori[i-1,j-1,1]+ori[i+1,j,1]+ori[i+1,j+1,1]+ori[i+1,j-1,1]
#    ori=origin.copy()

    ori=remove_illu
#    cv2.imshow("",ori)
#    cv2.waitKey(0)    
    
    DarkestX=0
    DarkestY=0
    Darkest=255

    vsl=vessel.copy()
    vsl=vsl[:,:,0]
#    vsl = cv2.dilate(vsl, kernel)
#    vsl = cv2.dilate(vsl, kernel)
    _, vsl = cv2.threshold(vsl, 10, 255, cv2.THRESH_BINARY)
#    cv2.imshow(src,vsl)
#    cv2.waitKey(0)   

    for i in range(len(ori)):
        for j in range(len(ori[0])):
            '''
            找出除了血管、病灶以外最暗的地方
            '''
            if distance(AverPointY,AverPointX,i,j)<AverPointR and vsl[i,j]== 0 and focus[i,j]<focus_threshold:

                # ori[i, j, 1] = 200
                if AroundDark(i,j)<Darkest:
                    DarkestX = i
                    DarkestY = j
                    Darkest = AroundDark(i,j)
    temp=DarkestY
    DarkestY=DarkestX
    DarkestX=temp
    
#    vsl = vsl[:, :, np.newaxis]
#    vsl = np.concatenate((vsl, vsl, vsl), axis=2)
    # cv2.imshow("",ori)
    # cv2.waitKey(0)
    return DarkestX,DarkestY,vsl

"""
重新调整阈值
"""
def reset_threshold(real,vsl):
    default_theshold=10
    while real<40000:
        print ("########",real,default_theshold)
        default_theshold=default_theshold-1
        _, vsl = cv2.threshold(vessel, default_theshold, 255, cv2.THRESH_BINARY)
        real=0
        for i in range(len(vsl)):
            for j in range(len(vsl[0])):
                if vsl[i][j][0]>0:
                    real=real+1
    return vsl

"""
主函数
"""
write_lines=[]
with open('./output/Macula_result.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        write_lines.append(row)
        break
    print (write_lines)
csvfile.close()
count=0
for src in vessel_Dir:
    count=count+1
    src=src[:src.find(".")]
#    src="20051020_62014_0100_PP"
    
    print (src,count)
    OD_x=0
    OD_y=0
    OD_r=0
    arrows = []
    # print datas
    for i in datas:
        if i[0].find(src)>=0:
            print ("datas:",i[1], i[2], i[3])
            OD_x = int(i[1])
            OD_y = int(i[2])
            OD_r = int(i[3])
            break
        

    if OD_r==0:
        continue 

    '''
    查找对应的去光照图片
    '''
#    print remove_illu_Dir

    for i in range(len(remove_illu_Dir)):
        if remove_illu_Dir[i].find(src[:len(src)-4])>=0:
#            print src[:len(src)-8],"*",remove_illu_Dir[i]
            remove_illu_src=remove_illu_Dir[i]
            break
        else:
            if i is range(len(remove_illu_Dir)-1):
                print (src,"REM_ILLU NOT FOUND!")
    remove_illu = cv2.imread(os.path.dirname(os.getcwd())+'/vesselsegmentation/input/'+remove_illu_src)
    
    '''
    查找血管图片
    '''
#    vessel = cv2.imread("./input/vessel/"+src+".tif.png")
    vessel = OpenPic(src,os.path.dirname(os.getcwd())+'/vesselsegmentation/output/')
    # _, vessel = cv2.threshold(vessel, 10, 255, cv2.THRESH_BINARY)
    

    vsl=vessel.copy()
#    vsl=cv2.resize(vsl,(pic_height,pic_width))
    default_theshold=10
    _, vsl = cv2.threshold(vsl, default_theshold, 255, cv2.THRESH_BINARY)
    remove_illu=cv2.resize(remove_illu,(len(vessel[0]),len(vessel)))  



    '''
    血管去除病灶
    '''
    focus_src=''
    for i in range(len(focus_Dir)):
        if focus_Dir[i].find(src[:len(src)-8])>=0 and focus_Dir[i].find(".png")>=0:
#            print src[:len(src)-8],"*",focus_Dir[i]
            focus_src=focus_Dir[i]
            break
        else:
            if i is range(len(focus_Dir)-1):
                print (src,"FOCUS NOT FOUND!")
    focus = cv2.imread(os.path.dirname(os.getcwd())+'/find od/input/focus/'+focus_src)[:,:,0]
    focus=cv2.resize(focus,(len(vsl[0]),len(vsl)))
    
    white_count=0
    for i in range(len(vsl)):
        for j in range(len(vsl[0])):
            
            if vsl[i][j][0]>0:
                white_count=white_count+1
            
            if focus[i][j]>focus_threshold and vsl[i][j][0]>0:
                vsl[i][j][0]=0
                vsl[i][j][1]=0
                vsl[i][j][2]=0
            
    if white_count<30000:
        vsl = reset_threshold(white_count,vsl)
#    cv2.imshow(src,vsl)
#    cv2.waitKey(0)
    _, vsl = cv2.threshold(vsl, 10, 255, cv2.THRESH_BINARY)#40#140
    vsl=cv2.resize(vsl,(len(remove_illu[0]),len(remove_illu)))
    vessel=vsl.copy()

    '''
    进行向量方法检测
    '''
    arrows=MakeArrows(arrows)

    # print arrows
    # print len(arrows)
    aver_arrow_x=0
    aver_arrow_y=0
    for i in range(len(arrows)):
        aver_arrow_x = aver_arrow_x + arrows[i][0]
        aver_arrow_y = aver_arrow_y + arrows[i][1]
    aver_arrow_x=aver_arrow_x/len(arrows)
    aver_arrow_y=aver_arrow_y/len(arrows)
    # print aver_arrow_x,aver_arrow_y
    # cv2.line(vsl, (OD_x, OD_y), (OD_x+aver_arrow_x, OD_y+aver_arrow_y), (0, 0, 255), 2)
    # cv2.line(vsl, (0,int(equation_y(0,aver_arrow_x+OD_x,aver_arrow_y+OD_y,OD_x,OD_y))), (len(vsl),int(equation_y(len(vsl),aver_arrow_x+OD_x,aver_arrow_y+OD_y,OD_x,OD_y))), (0, 0, 255), 2)

    '''
    在origin上画图
    '''
    macula_radius=macula_radius_para*OD_r
#    origin=cv2.imread("./input/origin/"+src+".tif")
    ori=remove_illu.copy()#origin.copy() 
#    ori=cv2.resize(ori,(len(vessel[0]),len(vessel)))        
    length=35*math.log(OD_r,2)
    jj, ii = DrawLength(length, OD_x, OD_y, aver_arrow_x + OD_x, aver_arrow_y + OD_y, colour="r", pic="ori")
    cv2.circle(ori, (OD_x, OD_y), OD_r, (0, 128, 255), 2, lineType=4)  # 视盘区域 黄色
    cv2.circle(ori, (OD_x + jj, OD_y + ii), int(macula_radius), (255, 100, 100), 2, lineType=4)  # 黄斑区域 蓝色
    MaculaX, MaculaY,conter_vsl = FindMacula(OD_x + jj, OD_y + ii, macula_radius)
    cv2.circle(ori, (MaculaX, MaculaY), 10, (20, 120, 80), -1, lineType=4)  # 预测的黄斑位置
    
    
    
    '''
    在vessel上画图
    '''
    for i in range(len(vsl)):
        for j in range(len(vsl[0])):
#            if conter_vsl[i][j]>0 and vsl[i][j][0]==0:
#                vsl[i][j][1]=100
            if focus[i][j]>focus_threshold:
                vsl[i][j][2]=focus[i][j]
#    cv2.circle(vsl, (OD_x, OD_y), OD_r, (255, 128, 0), 2, lineType=4)  # 视盘区域 黄色  
    # print length,"!!!!!!!!!!"
    jj,ii = DrawLength(length,OD_x,OD_y,aver_arrow_x+OD_x,aver_arrow_y+OD_y,colour="r",pic="vsl")
    cv2.circle(vsl, (OD_x, OD_y), OD_r, (0, 128, 255), 2, lineType=4)  # 视盘区域 黄色
    cv2.circle(vsl, (OD_x+jj, OD_y+ii),int(macula_radius), (255, 100, 100), 2, lineType=4)  # 黄斑区域 蓝色
    # print "OD",200/float(OD_r)
    
    '''
    在result上标记黄斑
    '''
    origin=remove_illu.copy()
    result=origin.copy()
    cv2.circle(result, (MaculaX, MaculaY), 10, (20, 120, 80), -1, lineType=4)  # 预测的黄斑位置
    
    '''
    显示demo
    '''
    mix = np.hstack([ori, vsl])
    cv2.destroyAllWindows()
    # cv2.imshow(src,mix)
    # cv2.waitKey(200)
    cv2.imwrite("./output/demo/"+src+".jpg",mix)
    cv2.imwrite("./output/demo/result/" + src+".jpg", result)
    
    row = []
    row.append(src)
    row.append(MaculaX)
    row.append(MaculaY)
    write_lines.append(row)

with open('./output/Macula_result.csv', 'wb') as csvfile:
    print ("SAVING DATAS...")
    spamwriter = csv.writer(csvfile, dialect='excel')
    for i in range(len(write_lines)):
        spamwriter.writerow(write_lines[i])
        print (write_lines[i])
csvfile.close()
print ("FINISHED!")
cv2.destroyAllWindows()
# cv2.imwrite("./demo/lines.jpg",lines)
# cv2.imwrite("./demo/dots.jpg",dots)