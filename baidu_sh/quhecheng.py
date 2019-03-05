#!/usr/bin/python
#coding=utf-8
import os
import json 
import math 
import sys
import random
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')

def hand(list,line):
    #短句直接不切割
    hang_num = 18
    biaodian = [",","!","?","：","，","。","！","、","？","\"","“"]
    splitdian = [",","!","?","：","，","。","！","？",":"]
    def join_tit_and_adj(half):
        half = half + 1
        b_t = "".join(list[0:half])
        e_t = "".join(list[half:])
        l = len(b_t)
        l2 = len(e_t)
        if (l< hang_num and l2 < hang_num ):
           #print l,l2,b_t.encode('gbk'),"ttt",e_t.encode('gbk')
           return l
        return None
    if len(line) < 15:
        return 100
    #标点切词
    def biaodian_fn(list):
        biaodian_index = []
        for index,i in enumerate(list):
            if i in splitdian:
                temp = join_tit_and_adj(index)
                if temp != None:
                    biaodian_index.append(temp)
        if len(biaodian_index)>0:
            #print biaodian_index,biaodian_index[len(biaodian_index)/2]
            if len(biaodian_index) > 1 and list[-1] in biaodian:
                return biaodian_index[len(biaodian_index)/2-1]
            return biaodian_index[len(biaodian_index)/2]
            #else:    
                #return biaodian_index[len(biaodian_index)/2]
        else:
            return None
    biao_res = biaodian_fn(list)
    if biao_res !=None:
        return biao_res
    #尝试切词中间切词
    def weitiao(list,num):
        half = len(list)/2+num
        if len(list)>half+1 and len(list)>1:
        #    print len(list),half
            if list[half+1] in biaodian or list[half] in biaodian:
                return None
        b_t = "".join(list[0:half])
        e_t = "".join(list[half:])
        l = len(b_t)
        l2 = len(e_t)
        if (l<hang_num and l2 <hang_num ):
           return l
    try_list = [0,-1,1,2,-2,3,-3]
    for x in try_list:
        res = weitiao(list,x)
        if res != None:
            return res 
    return hang_num 

def map_t(line):
    #line = line.decode("gbk")
    cut = jieba.cut(line)
    title_list = []
    for x in cut:
        title_list.append(x)
    area = hand(title_list,line)
    if area != 100:
        #print area,"area",len(line)
        str_ = str(line[0:area] + "\\\\n" + line[area:])
    else:
        str_ = str(line[0:area])
    return str_
    

def doing(f):
    d = {}
    with open(f) as fp:
        for line in fp:
            try:
                js = json.loads(line)
                if js['key'] not in d:
                    d[js['key']] = 1 
            except Exception as e:
                next
    return d

def filters(line,doing):
    line = line.decode("gbk")
    try:
        js = json.loads(line);
    except Exception as e:
        return None
    ideaid = js["key"]
    if ideaid in doing:
        return
    trade = js['yin']['tradeid']
    #if trade == "64"or trade == "66" or trade == "84" or trade == "59" or trade == "67" or trade == "77" or trade == "54" :    
     #   return 
    temp = js['wen']['title']
    title = js['wen']['title'].encode('utf-8')
    index = title.find("#")
    reg ={"#{地域}":"本地","#{日期}":"今天","#{年龄}":"年轻人","#{性别}":"本地人","#{星期}":"本周","#{收入水平}":"工薪族","#{所在行业}":"各行业","#{手机系统}":"手机用户","#{教育水平}":"年轻人","#{学校名}":"高校","#{学生阶段}":"学生","#{星座}":"这星座","#{商圈}":"本区","#{行政区}":"本区","#{反向性别}":"朋友","#{工作地}":"单位","#{热门游戏}":"5v5","#{亲密人群}":"朋友","#{用钱场景}":"买买买","#{地铁站}":"本地","#{社交圈}":"朋友圈","#{商场}":"商场","#{手机操作系统}":"手机","#{}":"",}
    if index != -1:
        for i in reg:
            title = title.replace(i,reg[i],10)
        js["wen"]["title"] = title.encode('utf-8').decode('utf-8')
    #print len(js["wen"]["title"])
    js["wen"]["title"] = map_t(js["wen"]["title"]).encode('utf-8').decode('utf-8')
    #print ideaid
    temp = str(temp[0:15] + "\\\\n" + temp[15:])
    #print ideaid,"\t",js["wen"]["title"].encode('gbk'),"\t",temp.encode('gbk')
    print json.dumps(js,ensure_ascii=False)
    #print js["key"]
if __name__ =="__main__":
    do_file="./data/doing_he_cheng"
    doing = doing(do_file) 
    for line in sys.stdin:
        filters(line,doing)



