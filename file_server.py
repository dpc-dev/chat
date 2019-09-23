import socket,os,sys,time
import threading,pymysql,json,hashlib
os.chdir(os.path.dirname(sys.argv[0]))

def user_service_thread(sock_conn, client_addr):
    do = 0
    try:
        while True:
            data_len = sock_conn.recv(15)
            if not data_len:
                print("客户端断开连接")
                break
            data_len = data_len.decode().rstrip()
            data_len = int(data_len)
            recv_size = 0
            json_data = b""
            while recv_size < data_len:
                tmp = sock_conn.recv(data_len - recv_size)
                if tmp == 0:
                    break
                json_data += tmp
                recv_size += len(tmp)    
            json_data = json_data.decode()
            req = json.loads(json_data)
            print("我是客户端的请求",req)
            #此时req为字典，是用户发送过来的请求
            if req["op"] == 0:
            #上传请求
                db = pymysql.connect("localhost","root","1478963520.ai","mydage")
                cur = db.cursor()
                hashlib_pwd = hashlib.md5(req["args"]["password"].encode())
                print("我是校验的密码",hashlib_pwd)
                cur.execute("select * from user where username='%s' and  password='%s' "%(req["args"]["name"],hashlib_pwd.hexdigest()))
                mysql_data = cur.fetchall()
                cur.close()
                db.close()
                if len(mysql_data) == 0:
                    sock_conn.send("我你大爷".encode())
                else:
                    if req["file_type"] == 0:
                        #客户端上传文件
                        print("客户端要上传文件")
                        file_size_re = int(req["file_size"])
                        recv_size = 0
                        file_data = b""
                        while recv_size < file_size_re:
                            
                            tmp = sock_conn.recv(file_size_re - recv_size)
                            
                            if not tmp:
                                break
                            
                            file_data += tmp
                            recv_size += len(tmp)
                            print("我是每次收的大小",recv_size)
                        file_path = os.path.dirname(sys.argv[0]) + "/" + req["file_name"]
                        with open(file_path,'wb') as f:
                            f.write(file_data)
                        print("我收到文件了")
                        #记录录入数据库中
                        file_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                        db = pymysql.connect("localhost","root","1478963520.ai","mydage")
                        cur = db.cursor()
                        cur.execute("insert into file values ('%s','%s','%s','文件')"%(req["file_name"],req["args"]["name"],file_time))
                        db.commit()
                        cur.close()
                        db.close()
                    if req["file_type"] == 1:
                        print("客户端要上传文件夹")
                        #客户端上传文件夹
                        if do == 0:
                            try:  
                                file_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                                db = pymysql.connect("localhost","root","1478963520.ai","mydage")
                                cur = db.cursor()
                                cur.execute("insert into file values ('%s','%s','%s','文件夹')"%(req["file_dirname"],req["args"]["name"],file_time))
                                db.commit()
                                cur.close()
                                db.close()
                            except KeyError:
                                pass
                        do += 1
                        file_dir = os.path.dirname(req["file_name"])
                        try:
                            os.makedirs(file_dir)
                        except FileExistsError:
                            pass
                        
                        filename = req["file_name"]
                        filesize = int(req["file_size"])
                        data = b""
                        data_cont = b""
                        cont1=0
                        print("我要开始接收内容了")
                        while True:
                            print("我在接收")
                            data = sock_conn.recv(filesize-cont1)
                            data_cont+=data
                            cont1+=len(data)
                            print(cont1,filesize)
                            if cont1 == filesize:
                                print("我在接收123")
                                break
                        with open(filename,"wb") as f:
                            f.write(data_cont) 
                        print("没问题")

            if req["op"] == 1:
                print("客户要下载文件")
                #下载传文件夹请求
                db = pymysql.connect("localhost","root","1478963520.ai","mydage")
                
                cur = db.cursor()
                print("...............")
                hashlib_pwd = hashlib.md5(req["args"]["password"].encode())
                print("我是校验的密码",hashlib_pwd)
                cur.execute("select * from user where username='%s' and  password='%s' "%(req["args"]["name"],hashlib_pwd.hexdigest()))
                mysql_data = cur.fetchall()
                cur.close()
                db.close()
                
                if len(mysql_data) == 0:
                    print("我被执行了")
                    sock_conn.send("我你大爷".encode())
                else:
                    print("账号密码校验成功")
                    if req["look"] == 0:
                    #查看可下载文件请求
                        db = pymysql.connect("localhost","root","1478963520.ai","mydage")
                        cur = db.cursor()
                        cur.execute("select * from file")
                        mysql_data = cur.fetchall()
                        if len(mysql_data) == 0:
                            exist_file=0
                        else:
                            exist_file=mysql_data
                        send_data = {"op":0,"exist_file":exist_file}
                        send_data = json.dumps(send_data)
                        send_data_size = str(len(send_data.encode())).encode()+b' '*(15-len(str(len(send_data.encode())).encode()))
                        sock_conn.send(send_data_size)
                        sock_conn.send(send_data.encode())
                    if req["look"] == 1:
                        #下载文件请求
                        print("客户要下载文件........")
                        filename = os.path.dirname(sys.argv[0])+"/"+req["file_name"]
                        if os.path.isdir(filename):
                            #下载目标是文件夹
                            try:
                                file_type = 1
                                print("下载的文件夹")
                                for root,dirs,files in os.walk(req["file_name"]):
                                    #遍历文件夹
                                    if len(files) == 0:
                                        pass
                                    else:
                                        for j in files:
                                            #合成相对路径
                                            file_send_name = os.path.join(root,j)
                                            file_size = str(os.path.getsize(file_send_name))
                                            
                                            send_data = {"op":1,"file_name":file_send_name,"file_type":file_type,"file_size":file_size}
                                            print(send_data)
                                            send_data = json.dumps(send_data)
                                            #send_data变成了json字符串
                                            send_data_size =str(len(send_data.encode())).encode()+ b' '*(15-len(str(len(send_data.encode())).encode()))
                                            sock_conn.send(send_data_size)
                                            sock_conn.send(send_data.encode())
                                            with open(file_send_name, "rb") as f:
                                                while True:
                                                    data = f.read(1024)
                                                    if len(data) == 0:
                                                        break
                                                    sock_conn.send(data)
                                sock_conn.close()
                            except:
                                print("文件不存在")
                                send_data =  {"op":1,"file_name":400}
                                send_data = json.dumps(send_data)
                                #send_data变成了json字符串
                                send_data_size =str(len(send_data.encode())).encode()+ b' '*(15-len(str(len(send_data.encode())).encode()))
                                sock_conn.send(send_data_size)
                                sock_conn.send(send_data.encode())
                                sock_conn.close()
                        else:
                            #下载目标是文件,其中file_size变成了字符串
                            try:
                                file_size = str(os.path.getsize(filename))
                                file_type = 0
                                send_data =  {"op":1,"file_name":req["file_name"],"file_type":file_type,"file_size":file_size}
                                send_data = json.dumps(send_data)
                                #send_data变成了json字符串
                                send_data_size =str(len(send_data.encode())).encode()+ b' '*(15-len(str(len(send_data.encode())).encode()))
                                sock_conn.send(send_data_size)
                                sock_conn.send(send_data.encode())
                                with open(filename, "rb") as f:
                                    while True:
                                        data = f.read(1024)
                                        if len(data) == 0:
                                            break
                                        sock_conn.send(data)
                                print("我发完了")
                                sock_conn.close()
                                

                            except:
                                send_data =  {"op":1,"file_name":400}
                                send_data = json.dumps(send_data)
                                #send_data变成了json字符串
                                send_data_size =str(len(send_data.encode())).encode()+ b' '*(15-len(str(len(send_data.encode())).encode()))
                                sock_conn.send(send_data_size)
                                sock_conn.send(send_data.encode())
                                sock_conn.close()
                                

    except:        
        print("客户端(%s:%s)断开连接！" % client_addr)
        sock_conn.close()


sock_listen = socket.socket()
sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_listen.bind(("127.0.0.1",9988))
sock_listen.listen(5)
while True:
        sock_conn, client_addr = sock_listen.accept()
        print("客户端(%s:%s)已连接！" % client_addr)
        threading.Thread(target=user_service_thread, args=(sock_conn, client_addr)).start()
sock_listen.close()