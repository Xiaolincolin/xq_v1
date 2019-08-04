"""
author: Colin
@time: 2019-04-30 10:14
explain:

"""
import http.client as hc
from urllib import parse
import json
#服务地址
sms_host = "sms.yunpian.com"
voice_host = "voice.yunpian.com"
#端口号
port = 443
#版本号
version = "v2"
#查账户信息的URI
user_get_uri = "/" + version + "/user/get.json"
#智能匹配模板短信接口的URI
sms_send_uri = "/" + version + "/sms/single_send.json"
#模板短信接口的URI
sms_tpl_send_uri = "/" + version + "/sms/tpl_single_send.json"
#语音短信接口的URI
sms_voice_send_uri = "/" + version + "/voice/send.json"
#语音验证码
voiceCode = 1234
def get_user_info(apikey):
    """
    取账户信息
    """
    conn = hc.HTTPSConnection(sms_host , port=port)
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    conn.request('POST',user_get_uri,parse.urlencode( {'apikey' : apikey}))
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

def send_sms(apikey, text, mobile):
    """
    通用接口发短信
    """
    params = parse.urlencode({'apikey': apikey, 'text': text, 'mobile':mobile})
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    conn = hc.HTTPSConnection(sms_host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

def tpl_send_sms(tpl_value, mobile):
    # 修改为您的apikey.可在官网（http://www.yunpian.com)登录后获取
    apikey = "7c5676d70eda4cd3e92ec13f24b172fe"
    # 修改为您要发送的短信内容
    # 调用模板接口发短信
    tpl_id = 2854526  # 对应的模板内容为：您的验证码是#code#【#company#】

    """
    模板接口发短信
    """
    params = parse.urlencode({
        'apikey': apikey,
        'tpl_id': tpl_id,
        'tpl_value': parse.urlencode(tpl_value),
        'mobile': mobile
    })
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    conn = hc.HTTPSConnection(sms_host, port=port, timeout=30)
    conn.request("POST", sms_tpl_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str.decode('utf8')

def send_voice_sms(apikey, code, mobile):
    """
    通用接口发短信
    """
    params = parse.urlencode({'apikey': apikey, 'code': code, 'mobile':mobile})
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    conn = hc.HTTPSConnection(voice_host, port=port, timeout=30)
    conn.request("POST", sms_voice_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

if __name__ == '__main__':
    str = {"code":0,"msg":"发送成功","count":1,"fee":0.05,"unit":"RMB","mobile":"15729588225","sid":39992428074}
    print(str['code'])