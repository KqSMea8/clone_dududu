import sys
import re
import os
import json 

def get_dict(f):
    d = {}
    with open(f) as fp:
        for line in fp:
            line=line.strip('\n')
            fs = line.strip().split('\t')
            md5key = str(fs[0])
            md5key=md5key.strip()
            d[md5key] = fs[1]
    return d

def to_final_dict(img_dict, fi,fi_sql, oldmt, newmt):
    pic_dict = {} 
    with open(fi) as f:
        for line in f:
            line=line.strip('\n')
            fs = line.split('\t')
            if len(fs)<5:
                continue
            ideaid = fs[4]
            md5key = str(fs[3])
            if md5key not in img_dict:
                continue
            pic_url =img_dict[md5key]
            pic_dict[ideaid] = pic_url;
    with open(fi_sql) as f_sql:
        for line in f_sql:
            line=line.strip('\n')
            fs = line.split('\t')
            ideaid = fs[0]
            if ideaid not in pic_dict:
                continue
            str_ma = fs[7];
            str_ma = str_ma.replace(r'\\"', '')
            str_ma = str_ma.replace(r' ', '')
            js = json.loads(str_ma, encoding="gbk")
            pic_url = pic_dict[ideaid]
            json_str = r'{"pictures":[{"image":"%s"}]}' % (pic_url)

            final_fs = [ideaid, oldmt, newmt, json_str, 1, 0, 0, 1, 0, 0]

            try:
                print '\t'.join(map(str, final_fs))
            except Exception as e:
               next 
def to_unit(fi_sql):
    pic_dict = {} 
    with open(fi_sql) as f_sql:
        for line in f_sql:
            line=line.strip('\n')
            fs = line.split('\t')
	    if len(fs)<7:
		continue
            ideaid = fs[0]
            str_ma = fs[7];
            str_ma = str_ma.replace(r'\\"', '')
            str_ma = str_ma.replace(r' ', '')
            js = json.loads(str_ma, encoding="gbk")
            pic_url = pic_dict[ideaid]

            final_fs = [ideaid, oldmt, newmt, json_str, 1, 0, 0, 1, 0, 0]

            try:
                print '\t'.join(map(str, final_fs))
            except Exception as e:
               next 
if __name__ == "__main__":
    result_file = sys.argv[1]
    to_unit(result_file)
#    img_dict = get_dict(result_file)
    #to_final_dict(img_dict, idea_img_file,form_sql_file)


