import sys
import re
import os
from pprint import pprint
import operator
import subprocess as sp
import base64
import multiprocessing as mp
import cv2
import util
import conf
import cvtools
import numpy as np
import random

import argparse
import datetime
import time
import random
import urlparse
import json
import util
import hashlib   


def bml_map(line, download_dir_name, merged_dir_name):
    #try:
        fs = line.strip().split('\t')
        pics = fs[0:3]
	title = fs[4]
	brand = fs[5]
	audio_url = fs[7]
	ideaid = fs[-1]
        m2 = hashlib.md5()   
        output_dir = download_dir_name
        url_names = []
        pic_file_names = []
        pic_local_paths = []
	q_all=[]	
        ready_pics = 0
        for index,p in enumerate(pics):
            m2.update(p + 'sunfuhao')
            file_name = m2.hexdigest() 
            fn_suf = file_name+'.jpg' 
            output_path = os.path.join(output_dir, fn_suf)
            url_names.append(p)
            pic_file_names.append(fn_suf)
            pic_local_paths.append(output_path)

            #download
            if os.path.exists(output_path):
                util.print_err("dupulicated image %s" % (file_name))
                ready_pics+= 1
                continue
            img_data = None
            use_proxy = False
            for i in range(50):     
	    #while True:
                try:
                    img_data = util.http_get(p, use_proxy)
                    util.print_err("%s downloaded succeed" % p)
                    break
                except Exception as e:
                    util.print_err("%s %s" % (e,p))
                    use_proxy = not use_proxy
                    util.print_err("use proxy")
                    time.sleep(1)
                    continue
            if img_data is not None and len(img_data) > 1000:
		q0 = None
            	for i in range(30):     
                    try:
		        q0 = cvtools.req_clarity_bvc(img_data)
			if q0<0.3 :
			    return None
	   		q_all.append(q0)
			break
                    except Exception as e:
                        util.print_err("fail_clarity")
                        time.sleep(2)
                        continue
                with open(output_path, 'w') as fn:
                    fn.write(img_data)
                img1 = cv2.imread(output_path)
                img1 = cvtools.img_resize(img1, (370, 245))
                cv2.imwrite(output_path, img1)
                ready_pics += 1
            else:
                util.print_err("%s download failed!!!" % p)

        if ready_pics != 3:
            util.print_err("has not enough images %s" % (len(pic_file_names)))
            return

        img_name1,img_name2,img_name3 = pic_file_names[0],pic_file_names[1],pic_file_names[2]
        fimg1, fimg2, fimg3 = pic_local_paths
        img1, img2, img3 = cv2.imread(fimg1), cv2.imread(fimg2), cv2.imread(fimg3)
        res_dir_chaofen = merged_dir_name
	#make mapper_quality
	#for index,files in enumerate(pic_local_paths):
	#    name = "q"+str(index)
	#    for i in range(1, 500):
	#    #while True:
	#	try:
	#	    name = cvtools.img_quality_ht(files)
	#	    q_all.append(name)
	#	    #if name < 0.55:
	#		#return None
	#	    break
	#	except Exception as e:
	#	    util.print_err("%s %s" % (e,files))
	#	    time.sleep(10)
 
	#q0 = cvtools.img_quality_ht(fimg1)
        #q1 = cvtools.img_quality_ht(fimg2)
        #q2 = cvtools.img_quality_ht(fimg3)
	#print q0,q1,q2
	#if (q0< 0.55 or q1<0.55 or q2<0.55) :
	#    return None;
        fn_path1 = os.path.join(res_dir_chaofen, img_name1)
        fn_path2 = os.path.join(res_dir_chaofen, img_name2)
        fn_path3 = os.path.join(res_dir_chaofen, img_name3)
        
        cv2.imwrite(fn_path1, img1)
        cv2.imwrite(fn_path2, img2)
        cv2.imwrite(fn_path3, img3)
        c0 = cvtools.super_resolution(fn_path1, svr_url, is_local=False)
	h, w, d = c0.shape[:3]
        target_sz = (h, int(867), d)
        c2_p = cvtools.img_padding(c0, target_sz, dir='h', method='gblur')
        cv2.imwrite(fn_path1, c2_p)
	
        with open(fn_path1) as f:
             base1 = base64.b64encode(f.read())
        c0 = cvtools.super_resolution(fn_path2, svr_url, is_local=False)
	h, w, d = c0.shape[:3]
        target_sz = (h, int(867), d)
        c2_p = cvtools.img_padding(c0, target_sz, dir='h', method='gblur')
        cv2.imwrite(fn_path2, c2_p)
	
        with open(fn_path2) as f:
             base2 = base64.b64encode(f.read())
        c0 = cvtools.super_resolution(fn_path3, svr_url, is_local=False)
	h, w, d = c0.shape[:3]
        target_sz = (h, int(867), d)
        c2_p = cvtools.img_padding(c0, target_sz, dir='h', method='gblur')
        cv2.imwrite(fn_path3, c2_p)
        with open(fn_path3) as f:
             base3 = base64.b64encode(f.read())
	#fn = open("./log_res", 'a')
	#templtelist = ['feedinspireing2','Digital Zoom-3','Color Swipe-3','ElegantSlideshow-3']
	templtelist = ['99','98','97','96']
	templte = random.choice(templtelist)
	templte = "99" 
	basestr = base1+"\t"+base2+"\t"+base3+"\t"+"end after three pics"+"\n"
	prjson = '{"video_key":"%s","company":"%s","audio":["%s"],"pic_and_desc":[{"pic_binary":"%s","desc":"%s"},{"pic_binary":"%s","desc":"%s"},{"pic_binary":"%s","desc":"%s"}],"trade":[{"trade_id_1st":"%s","trade_name_1st":"feed"}],"ad_info":{"userid":"%s","planid":"123","unitid":"123","winfoid":"123"},"other_info":{"lp_url":""}}' %(ideaid,title,audio_url,base1,title,base2,brand,base3,title,templte,ideaid)
	#with open("./data/log_res",'a') as fn:
	#    fn.write(prjson)
	#fn.close()
	#if len(q_all) == 3: 
	#    print (prjson+"\t"+str(q_all[0])+"\t"+str(q_all[1])+"\t"+str(q_all[2]))
	#else:
	#    print (prjson+"\t"+"not_3pic")
	print prjson
#    except Exception as e:
#        util.print_err("%s" % e)
#        util.print_err(line)
#        return

if __name__ == "__main__":
    download_dir_name = sys.argv[1]
    merged_dir_name = sys.argv[2]
    util.print_err("%s %s" % (download_dir_name, merged_dir_name))
    global svr_url
    svr_url = [cvtools.get_server_addr()]
    for line in sys.stdin:
        bml_map(line, download_dir_name, merged_dir_name)

