import socket,json,requests,time,hashlib
import threading,pymysql,random
def test_user(ss,addr):
    #全局变量进行声明,注意全局变量
    global vcode,phone
    try:
        while True:
            harvest_size = 15
            harvest_size1 = 0
            harvest_size2 = 15
            harvest_data = b''
            while True:
                harvest_data1 = ss.recv(harvest_size2)
                if not harvest_data1:
                    break
                harvest_data += harvest_data1
                harvest_size1 += len(harvest_data1)
                harvest_size2 = harvest_size - harvest_size1
                print(harvest_data)
                if harvest_size2 == 0:
                    break
            if not harvest_data1:
                break
            data_json_size = int(harvest_data.rstrip().decode())
            print(data_json_size)
            data_json_size1 = 0
            data_json_size2 = 1000
            data_json = b''
            if data_json_size < data_json_size2:
                data_json_size2 = data_json_size
            while True:
                data_json1 = ss.recv(data_json_size2)
                data_json += data_json1
                data_json_size1 += len(data_json1)
                data_json_size2 = data_json_size - data_json_size1
                if data_json_size2 == 0:
                    break
            data_json = json.loads((data_json.decode()))
            print("我是客户端发过来的字典",data_json)
            #此时请求消息变成了字典
            #请求消息类型是数字
            #服务器响应数据也是数字
            if data_json["op"] == 0:
                #用户发起了登录请求
                print("我是登录请求...")
                db = pymysql.connect("localhost","root","1478963520.ai","mydage")
                cur = db.cursor()
                hashlib_pwd = hashlib.md5(data_json["args"]["user_pwd"].encode())
                print("我是校验的密码",hashlib_pwd)
                cur.execute("select * from user where username='%s' and  password='%s' "%(data_json["args"]["user_name"],hashlib_pwd.hexdigest()))
                mysql_data = cur.fetchall()
                cur.close()
                db.close()
                if len(mysql_data) == 0:
                    print("我登录失败了")
                    send_data = {"op":0,"test":1}
                    send_data = json.dumps(send_data)
                else:
                    
                    send_data = {"op":0,"test":0}
                    send_data = json.dumps(send_data)
            if data_json["op"] == 1:
                print("..........................")
                #用户发起了获取验证码请求
                db = pymysql.connect("localhost","root","1478963520.ai","mydage")
                cur = db.cursor()
                cur.execute("select * from user where phone='%s' "%data_json["args"]["user_phone"])
                mysql_data = cur.fetchall()
                cur.close()
                db.close()
                if len(mysql_data) == 0:
                    appkey = '7ab939170065932ed9c334046ced4e69'
                    appsecret = 'cc268c9ee59a'
                    nonce = random.randint(10000, 100000000)
                    ctime = str(time.time())
                    curtime = ctime
                    s = appsecret + str(nonce) + curtime
                    checksum = hashlib.sha1(s.encode('utf-8')).hexdigest()
                    Content_Type = "application/x-www-form-urlencoded;charset=utf-8"
                    header = {'Content-Type': Content_Type, 'AppKey': appkey, 'Nonce': str(nonce), 'CurTime': curtime,'CheckSum': checksum}
                    post_data = {"mobile":data_json["args"]["user_phone"]}
                    url = 'https://api.netease.im/sms/sendcode.action'
                    wangyi_data = requests.post(url,data=post_data,headers =header)
                    wangyi_vcode=wangyi_data.json()
                    print(wangyi_vcode)

                    if wangyi_vcode["code"] == 200:
                        phone = data_json["args"]["user_phone"]
                        vcode = wangyi_vcode["obj"]
                        send_data = {"op":1,"test":0}
                        send_data = json.dumps(send_data)
                    else:
                        if wangyi_vcode["code"] == 315 or wangyi_vcode["code"] == 500:
                            send_data = {"op":1,"test":1}
                            send_data = json.dumps(send_data)
                        else:
                            send_data = {"op":1,"test":2}
                            send_data = json.dumps(send_data)
                else:
                    send_data = {"op":1,"test":3}
                    send_data = json.dumps(send_data)

            if data_json["op"] == 2:
                #用户发起了注册请求
        
                #,服务器只验证用户名是否存在，手机号是否与发送验证码的手机号一致，验证码是否正确
                
                db = pymysql.connect("localhost","root","1478963520.ai","mydage")
                cur = db.cursor()
                cur.execute("select * from user where username='%s' "%data_json["args"]["user_name"])
                mysql_data = cur.fetchall()
                cur.close()
                db.close()
                if len(mysql_data) == 0:
                    if phone == data_json["args"]["user_phone"]:
                        if vcode == data_json["args"]["user_vcode"]:
                            send_data = {"op":2,"test":0}
                            send_data = json.dumps(send_data)
                            db = pymysql.connect("localhost","root","1478963520.ai","mydage")
                            cur = db.cursor()
                            hashlib_pwd = hashlib.md5(data_json["args"]["user_pwd"].encode())

                            cur.execute("insert into user (username,password,phone,email) values ('%s','%s','%s','%s')"%(data_json["args"]["user_name"],hashlib_pwd.hexdigest(),data_json["args"]["user_phone"],data_json["args"]["user_email"]))
                            db.commit()
                            cur.close()
                            db.close()

                        else:
                            send_data = {"op":2,"test":3}
                            send_data = json.dumps(send_data)
                    else:
                        send_data = {"op":2,"test":2}
                        send_data = json.dumps(send_data)
                else:
                    send_data = {"op":2,"test":1}
                    send_data = json.dumps(send_data)
            send_data_size = str(len(send_data.encode())).encode() + b' '*(15-len(str(len(send_data.encode()))))
            try:
                ss.send(send_data_size)
                print("我发送了个什么东西....",send_data,type(send_data))
                ss.send(send_data.encode())
            except:
                ss.close()            
    finally:
        ss.close()
            
        

if __name__ == "__main__":
               
    # 验证码是字符串
    vcode = 0
    # 手机号也是字符串,放在用户在验证手机后提交，又修改手机号
    phone = 0        
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", 9999))
    sock.listen(5)
    while True:
        try:
            ss,addr = sock.accept()
            print("用户连接上",addr)
            threading.Thread(target=test_user,args=(ss,addr)).start()
        except:
            pass