#百度通用翻译API,不包含词典、tts语音合成等资源，如有相关需求请联系translate_api@baidu.com
# coding=utf-8
 
import http.client
import hashlib
import urllib
import random
import json
 
# 百度appid和密钥需要通过注册百度【翻译开放平台】账号后获得
appid = '20221220001502928'        # 填写你的appid
secretKey = 'c6V9Y22DD1y7VtgUsI0V'    # 填写你的密钥

def translate(toLang, q, fromLang = 'auto'):

    httpClient = None
    myurl = '/api/trans/vip/translate'  # 通用翻译API HTTP地址

    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + \
            '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    # 建立会话，返回结果
    try:
        httpClient = http.client.HTTPConnection('fanyi-api.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        
        dst = result['trans_result'][0]['dst']
        return dst
     
    except Exception as e:
        print (e)
    finally:
        if httpClient:
            httpClient.close()

# 使用方式：
# import baidu_tf
# dst = baidu_tf.translate(toLang=target_language,q=kv[1])