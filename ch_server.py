#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket,pymysql
import threading,json,hashlib


# UDP打洞
# 定长包头(15B) + 变长聊天消息(昵称:聊天内容)

def client_chat(sock_conn, client_addr):
    try:
        while True:
                msg_len_data = sock_conn.recv(15)
                if not msg_len_data:
                    break

                msg_len = int(msg_len_data.decode().rstrip())
                recv_size = 0
                msg_content_data = b""
                while recv_size < msg_len:
                    tmp_data = sock_conn.recv(msg_len - recv_size)
                    if not tmp_data:
                        break
                    msg_content_data += tmp_data
                    recv_size += len(tmp_data)
                
                else:
                    msg_content_data = json.loads(msg_content_data.decode())
                    print(msg_content_data)
                    if msg_content_data["op"] == 0:
                        db = pymysql.connect("localhost","root","1478963520.ai","mydage")
                        cur = db.cursor()
                        hashlib_pwd = hashlib.md5(msg_content_data["args"]["password"].encode())
                        print("我是校验的密码",hashlib_pwd)
                        cur.execute("select * from user where username='%s' and  password='%s' "%(msg_content_data["args"]["name"],hashlib_pwd.hexdigest()))
                        mysql_data = cur.fetchall()
                        cur.close()
                        db.close()
                        if len(mysql_data) == 0:
                            sock_conn.send("我你大爷".encode())
                    # 发送给其他所有在线的客户端
                        else:
                            
                            news = msg_content_data["args"]["name"]+":"+msg_content_data["news"]
                            print(news)
                            msg_send_data = {"op":0,"args":{"name":msg_content_data["args"]["name"]},"news":news}
                            msg_send_data = json.dumps(msg_send_data)
                            print(msg_send_data)
                            msg_send_len = str(len(msg_send_data.encode())).encode()+b' '*(15-len(str(len(msg_send_data.encode())).encode()))
                            for sock_tmp, tmp_addr in client_socks: 
                                if sock_tmp is not sock_conn:
                                    try:
                                        sock_tmp.send(msg_send_len)
                                        sock_tmp.send(msg_send_data.encode())
                                    except:
                                        client_socks.remove((sock_tmp, tmp_addr))
                                        sock_tmp.close()
                    continue
                break
    finally:
            client_socks.remove((sock_conn, client_addr))
            sock_conn.close()


sock_listen = socket.socket()
sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_listen.bind(("0.0.0.0", 9998))
sock_listen.listen(5)

client_socks = []

while True:
    sock_conn, client_addr = sock_listen.accept()
    client_socks.append((sock_conn, client_addr))
    threading.Thread(target=client_chat, args=(sock_conn, client_addr)).start()



