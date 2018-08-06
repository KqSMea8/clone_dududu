import cv2
from InnerToken import InnerToken
import util
import conf
import numpy as np
import base64
import general_classify_client_pb2 as general_classify_client
import urllib
import urllib2
import random
import json
import time


def gblur(img_data, kernel_size=(155, 155), sigma=10):
    #img = cv2.GaussianBlur(img_data, kernel_size, sigma)
    #img = cv2.bilateralFilter(img_data , 9 , 75 ,75)  
    img = cv2.blur(img_data , kernel_size)  
    return img


def prepare_request(img_data):

    return req_json


def super_resolution(img_file_path, url, is_local=True, option='super_resolution'):
    if is_local:
        return super_resolution_local(img_file_path, option)
    else:
        return super_resolution_bvc(img_file_path, url, option)

def get_server_addr():
    proxy_url = conf.api['bvc_proxy']
    for i in range(10):
        try:
            res_proxy = json.loads(util.http_get(proxy_url))
            server_json = random.choice(res_proxy['result']['ServerInfo'])
            addr = server_json['Server']['service_addr'][0]
            break
        except Exception as e:
            util.print_err(e)
            util.print_err("getting proxy url...")
            time.sleep(1)
    ip = addr.split(':')[0]
    port = 40077
    url =  "http://%s:%s/1" % (ip, port)
    return url


def super_resolution_bvc(img_file_path, url, option='super_resolution'):
    with open(img_file_path) as f:
        logid = random.randint(1000000, 100000000)
        requestinfo = {
                'image': base64.b64encode(f.read()),
                'type_name': 'image_restoration',
                'option': option,
                }
        data = json.dumps(requestinfo)

        req_array = {
                'jsonrpc':'2.0',
                'method':'classify',
                'id':'123',
                'params':[{
                        'appid': '123456',
                        'logid': logid,
                        'format': 'json',
                        'from': 'test-python',
                        'cmdid': '123',
                        'clientip': '0.0.0.0',
                        'data': base64.b64encode(data),
                    }]
                    }
        req_json = json.dumps(req_array)
        res = None
        res_json = None

        for i in range(1, 50):
            try:
                req = urllib2.Request(url[0]) 
                req.add_header('Content-Type', 'application/json')
                response = urllib2.urlopen(req, req_json, 10000)
                res = json.loads(response.read()) 
                res_json = json.loads(base64.b64decode(res['result']['_ret']['result']))
                img_str = base64.b64decode(res_json['image'])
                nparr = np.fromstring(img_str, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                break
            except Exception as e:
                util.print_err(e)
                util.print_err("bvc req failed. change server")
                util.print_err(res)
                util.print_err(res_json)
                time.sleep(5)
                url[0] = get_server_addr()
                util.print_err(url)
        return img

def super_resolution_local(img_file_path, option='super_resolution'):
    with open(img_file_path) as f:
        logid = random.randint(1000000, 100000000)
        requestinfo = {
                'image': base64.b64encode(f.read()),
                'type_name': 'image_restoration',
                'option': option,
                }
        data = json.dumps(requestinfo)

        req_array = {
                        'appid': '123456',
                        'logid': logid,
                        'format': 'json',
                        'from': 'test-python',
                        'cmdid': '123',
                        'clientip': '0.0.0.0',
                        'data': base64.b64encode(data),
                    }
        req_json = json.dumps(req_array)

        url = conf.api['super_resolution_local']
        print url
        req = urllib2.Request(url) 
        req.add_header('Content-Type', 'application/json')
        for i in range(1, 50):
            #try:
                response = urllib2.urlopen(req, req_json, 10000)
                res = json.loads(response.read()) 
                print res
                res_json = json.loads(base64.b64decode(res['result']))
                img_str = base64.b64decode(res_json['image'])
                nparr = np.fromstring(img_str, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                break
            #except Exception as e:
            #    util.print_err(e)
            #    util.print_err(res_json)
            #    time.sleep(1)
        return img


def super_resolution_ht(img_file_path, option='super_resolution'):
    with open(img_file_path) as f:
        it = InnerToken()
        token = it.generateToken(**conf.apiInfo)
        req_json = {
                'image': base64.b64encode(f.read()),
                'option': option,
                'access_token': token,
                }
        url = conf.api['super_resolution_ht']
        for i in range(1, 50):
            try:
                res_json = util.http_post(url, req_json)
                img_str = base64.b64decode(res_json['result']['image'])
                nparr = np.fromstring(img_str, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                break
            except Exception as e:
                util.print_err(e)
                util.print_err(res_json)
                time.sleep(1)

    return img


def img_quality_ht(img_file_path):
    with open(img_file_path) as f:
        it = InnerToken()
        token = it.generateToken(**conf.apiInfo_2)
        req_json = {
                'image': base64.b64encode(f.read()),
                'access_token': token,
                }
        url = conf.api['img_quality_ht']
        for i in range(1, 50):
            try:
                res_json = util.http_post(url, req_json)
		quality = res_json['result'];
		log_id =  res_json['log_id']
                #img_str = base64.b64decode(res_json['result']['image'])
                #nparr = np.fromstring(img_str, np.uint8)
                #img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                break
            except Exception as e:
                util.print_err(e)
                util.print_err(res_json)
                time.sleep(1)
    return quality 


def img_padding(img, target_sz, dir='h', method='gblur'):
    th, tw, d = target_sz
    h, w, d = img.shape[:3]

    if dir == 'h':
        assert tw >= w
        cen = int(w/2)
        p = int((tw - w) / 2)
        gb_d1 = img[:, :p, :]
        gb_d2 = img[:, -p:, :]
        #gb_d1 = img[:, :cen, :]
        #gb_d2 = img[:, cen:, :]

        gb_d1 = img_resize( gb_d1, (p, th) )
        gb_d2 = img_resize( gb_d2, (p, th) )
    elif dir == 'v':
        assert th >= h
        p = int((th - h) / 2)
        cen = int(h/2)
        #gb_d1 = img[cen-p:cen, :,:]
        #gb_d2 = img[cen:cen+p, :,:]
        #gb_d1 = img[:p, :,:]
        #gb_d2 = img[-p:, :,:]
        gb_d1 = img[:cen, :,:]
        gb_d2 = img[-cen:, :,:]


        gb_d1 = img_resize( gb_d1, (tw, p) )
        gb_d2 = img_resize( gb_d2, (tw, p) )
    else:
        assert False

    if method == 'gblur' :
        g1 = gblur(gb_d1)
        g2 = gblur(gb_d2)
    elif method == 'black':
        g1 = gb_d1.copy()
        g2 = gb_d2.copy()
        g1[:,:,:] = 0
        g2[:,:,:] = 0

    img = img_concat_list((g1, img, g2), dir)
    return img


def img_concat_list(img_list, dir='h'):
    assert len(img_list) > 1

    img_con = img_list[0]
    for img in img_list[1:]:
        img_con = img_concat(img_con, img, dir)

    return img_con


def img_concat(img1, img2, dir='h'):
    h1, w1, d1 = img1.shape[:3]
    h2, w2, d2 = img2.shape[:3]

    assert d1 == d2

    if dir == 'h':
        vis = np.zeros((max(h1, h2), w1 + w2, d1), np.uint8)
        vis[:h1, :w1] = img1
        vis[:h2, w1:w1 + w2] = img2
    elif dir == 'v':
        vis = np.zeros((h1 + h2, max(w1, w2), d1), np.uint8)
        vis[:h1, :w1] = img1
        vis[h1:h1 + h2, :w2] = img2

    return vis


def img_resize(img1, target_sz, alg=cv2.INTER_CUBIC):
    '''target sz (width, height, depth)'''
    return cv2.resize(img1, target_sz, interpolation=alg)   


def req_clarity_bvc(img_data):
    #with open(img_file_path) as f:
	request_pb = general_classify_client.GeneralClassifyRequest()
    	request_pb.image = img_data
   	classify_type = request_pb.classify_type.add()
    	classify_type.type_name = 'clarity'
    	classify_type.topnum = 1
    	request_str = request_pb.SerializePartialToString()

        logid = random.randint(1000000, 100000000)
        #requestinfo = {
        #        'image': base64.b64encode(f.read()),
        #        }
        #data = json.dumps(requestinfo)

        req_array = {
                        'appid': '123456',
                        'logid': logid,
                        'format': 'json',
                        'from': 'test-python',
                        'cmdid': '123',
                        'clientip': '0.0.0.0',
                        'data': base64.b64encode(request_str),
                    }
        req_json = json.dumps(req_array)

        url = conf.api['req_clarity_bvc']
        req = urllib2.Request(url) 
        req.add_header('Content-Type', 'application/json')
    	response = None
        for i in range(1, 50):
            try:
                response = urllib2.urlopen(req, req_json, 1)
		res_str_tmp = response.read()
    		json_res = json.loads(res_str_tmp)
    		if "err_no" not in json_res:
       			return "no err_no"

    		if json_res["err_no"] != 0:
        		return "err_no is not 0\t" + res_str_tmp
                res_pb = general_classify_client.GeneralClassifyResponse()

    		res_pb.ParseFromString(base64.b64decode(json_res['result']))
		for result in res_pb.result:
		        if result.type_name == "clarity":
				res = (result.probability[0]+6)/12
		break
            except Exception as e:
                util.print_err(e)
                time.sleep(1)
        return res 
