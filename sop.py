#/usr/bin/python3 
# -*- coding : utf-8 -*-
import re
import tkinter as tk
import tkinter.messagebox,json,socket
import threading,time,os,sys,random
from PIL import  ImageTk
import PIL
import multiprocessing,sys
from user_test import *
from tkinter import *
from tkinter.filedialog import askdirectory
import tkinter.filedialog
dpc = multiprocessing.Queue()
user_list = []
#全局控制变量
mmm = 0
ddd = 0
def shangchuan():
        global ddd
        if ddd==0:
                if mmm>=1:
                        dpc.put({"op":2})
                        dpc.put(user_list[0])
                        tttttt = multiprocessing.Process(target=shangchuan1,args=(dpc,))
                        tttttt.start()
                else:
                        dpc.put(user_list[0])
                        tttttt = multiprocessing.Process(target=shangchuan1,args=(dpc,))
                        tttttt.start()
        else:
                dpc.put({"op":1})
                dpc.put(user_list[0])
                tttttt = multiprocessing.Process(target=shangchuan1,args=(dpc,))
                tttttt.start()
        ddd+=1
def shangchuan1(dpc):
        
        jjj = dpc.get()
        list1 = []
        list1.append(dpc.get())
        top = tkinter.Tk()
        top.title('上传文件')
        top.geometry('800x480')
        path_file = ""
        click = 0
        def choose_fiel():
                nonlocal path_file
                path_file = tkinter.filedialog.askopenfilename(title='选择文件')  # 选择文件
                e.set(path_file)
        def selectPath():
                nonlocal path_file
                path_file = askdirectory()
                e.set(path_file)
        def am():
                t = threading.Thread(target=dwonload,daemon=True)
                t.start()
                print("我被执行")
        def dwonload():
                nonlocal click
                if click==0:
                        pass
                else:
                        tkinter.messagebox.showwarning("来自大帅比的提示","客观别闹，上传的文件还没有传完")
                        return
                click = 1
                #控制变量
                print(os.path.dirname(path_file))
                try:
                        os.chdir(os.path.dirname(path_file))
                except:
                        click = 0
                        tkinter.messagebox.showwarning("来自大帅比的提示","请选择路径")
                        return
                send_filename = os.path.basename(path_file)
                try:
                        sock = socket.socket()
                        sock.connect(("127.0.0.1",9988))
                        time1 = time.time()
                        py = 0
                        jind = "<-"+"->"
                        if os.path.isdir(path_file):
                                print("发送的是文件夹")
                                file_type = 1
                                for root,dirs,files in os.walk(send_filename):
                                        #遍历文件夹
                                        if len(files) == 0:
                                                pass
                                        else:
                                                print(files)
                                                for j in files:
                                                        print("我是可发送的文件",j)
                                                        #合成相对路径
                                                        py+=1
                                                        file_send_name = os.path.join(root,j)
                                                        file_size = str(os.path.getsize(file_send_name))
                                                        
                                                        send_data = {"op":0,"args":{"name":list1[0]["name"],"password":list1[0]["password"]},"file_name":file_send_name,"file_type":file_type,"file_size":file_size,"file_dirname":send_filename}
                                                        send_data = json.dumps(send_data)
                                                        #send_data变成了json字符串
                                                        send_data_size =str(len(send_data.encode())).encode()+ b' '*(15-len(str(len(send_data.encode())).encode()))
                                                        sock.send(send_data_size)
                                                        sock.send(send_data.encode())
                                                        size_data_count = 0
                                                        cont1 = 0
                                                        f = open(file_send_name, "rb")
                                                        while True:
                                                                data = f.read(1024)
                                                                if len(data) == 0:
                                                                        break
                                                                sock.send(data)
                                                                size_data_count += len(data)
                                                                print(file_send_name)
                                                                cont = int((size_data_count/int(file_size))*100)
                                                                
                                                                
                                                                if cont == cont1:
                                                                
                                                                        pass
                                                                else:
                                                                        bai = "%"+str(cont)
                                                                        if cont%10==0:
                                                                                print("我被执行了")
                                                                                jind = "<- "+ "="*int(cont/10)+" ->"
                                                                                abb.set("我不是进度条:  "+jind+"  "+'已上传  %s'%bai)
                                                                        else:
                                                                                abb.set("我不是进度条:  "+jind+"  "+'已上传  %s'%bai)
                                                                        cont1 = cont
                                                        f.close()
                                
                                sock.close()
                                click = 0
                                print("我发送完了")                


                        else:                   
                                print("发送的是文件")
                                py+=1
                                file_type = 0
                                file_size = str(os.path.getsize(send_filename))
                                print(file_size)
                                send_data =  {"op":0,"args":{"name":list1[0]["name"],"password":list1[0]["password"]},"file_name":send_filename,"file_type":file_type,"file_size":file_size}
                                send_data = json.dumps(send_data)
                                #send_data变成了json字符串
                                send_data_size =str(len(send_data.encode())).encode()+ b' '*(15-len(str(len(send_data.encode())).encode()))
                                sock.send(send_data_size)
                                sock.send(send_data.encode())
                                print("头部消息发过去了")
                                size_data_count = 0
                                cont1 = 0
                                f = open(send_filename, "rb")
                                print("文件打开正常")
                                while True:
                                        data = f.read(2048)
                                        if len(data) == 0:
                                                break
                                        sock.send(data)
                                        size_data_count += len(data)
                                        cont = int((size_data_count/int(file_size))*100)
                                        
                                        
                                        if cont == cont1:
                                                
                                                pass
                                        else:
                                                bai = "%"+str(cont)
                                                if cont%10==0:
                                                        print("我被执行了")
                                                        jind = "<- "+ "="*int(cont/10)+" ->"
                                                        abb.set("我不是进度条:  "+jind+"  "+'已上传  %s'%bai)
                                                else:
                                                        abb.set("我不是进度条:  "+jind+"  "+'已上传  %s'%bai)
                                                cont1 = cont
                                
                                f.close()
                                
                        sock.close()
                        click = 0
                        time_conut = time.time()-time1
                        tk.messagebox.showinfo("来自大帅比的提示提示","上传完成!本次上传文件%s个,耗时%s秒"%(py,int(time_conut)))
                        print("我发送完了")
                except:
                        sock.close()
                        tkinter.messagebox.showerror("来自大帅比的提示","出错了！")
                        click = 0


        abb = tk.StringVar()
        tk.Label(top,textvariable =abb,font=("宋体", 15)).place(x=200, y=240)
        tk.Label(top,text = "目标文件:",font= ('宋体', 13)).place(x=80, y=345)
        e = tkinter.StringVar()
        e_entry = tkinter.Entry(top, width=50, textvariable=e,font= ('宋体', 13),borderwidth = 3)
        e_entry.place(x=160,y=345)
        tk.Button(top, text = "选择文件夹", command = selectPath).place(x=690,y=342)
        b1 = tk.Button(top, text='上传', width=17, height=1, command=am)
        b1.place(x=360,y=400)
        submit_button = tkinter.Button(top, text ="选择文件", command = choose_fiel)
        submit_button.place(x=620,y=342)
        
        top.mainloop()

def xiazai():
        global mmm
        if mmm == 0:
                if ddd >=1:
                        dpc.put({"op":2})
                        dpc.put(user_list[0])
                        ttttt = multiprocessing.Process(target=xiazai1,args=(dpc,))
                        ttttt.start()
                else:
                        dpc.put(user_list[0])
                        ttttt = multiprocessing.Process(target=xiazai1,args=(dpc,))
                        ttttt.start() 
        else:
                dpc.put({"op":2})
                dpc.put(user_list[0])
                ttttt = multiprocessing.Process(target=xiazai1,args=(dpc,))
                ttttt.start() 
        mmm+=1
def xiazai1(dpc):
        dpc_list = []
        lol = dpc.get()

        dpc_list.append(dpc.get())
        
        path_file = ""
        click = 0
        def selectPath():
                nonlocal path_file
                path_file = askdirectory()
                path.set(path_file)
        def print_selection():
                nonlocal click
                if click==0:
                        
                        t = threading.Thread(target=print_selection1,daemon=True)
                        t.start()
                else:
                        tk.messagebox.showerror("来自大帅比的提示","按钮好玩，但是不要多点哦~就是不理你")
                 
        def print_selection1():
                nonlocal click
                #设置控制变量，当按钮点击一次，任务没有结束，不会触发函数
                if click==0:
                        pass
                else:
                        tk.messagebox.showerror("来自大帅比的提示","按钮好玩，但是不要多点哦~")
                        return
                click = 1
                try:
                        value = lb.get(lb.curselection())
                except:
                        tk.messagebox.showerror("来自大帅比的提示","请选择要下载的文件或文件夹！")
                        click = 0
                        return
                print(value)   # 获取当前选中的文本
                filename = value[0]
                try:
                        sock = socket.socket()
                        sock.connect(("127.0.0.1",9988))
                        send_data = {"op":1,"args":{"name":dpc_list[0]["name"],"password":dpc_list[0]["password"]},"look":1,"file_name":filename}
                        send_data = json.dumps(send_data)
                        send_data_size = str(len(send_data.encode())).encode()+b' '*(15-len(str(len(send_data.encode())).encode()))
                        sock.send(send_data_size)
                        sock.send(send_data.encode())
                        py=0
                        time1 = time.time()
                        while True:
                                
                                jind = "<-"+"->"
                                data_size = sock.recv(15).decode().rstrip()
                                if not data_size:
                                        print("服务器传完了...")
                                        break
                                py+=1
                                print(data_size)
                                data_size = int(data_size)
                                data = sock.recv(data_size)
                                data = json.loads(data.decode())
                                if data["file_name"]==400:
                                        tk.messagebox.showerror("来自大帅比的提示","该文件或文件夹不存在！")
                                        
                                        return
                                else:
                                        if data["file_type"] == 0:
                                                #客户端下载文件
                                                file_size_re = int(data["file_size"])
                                                recv_size = 0
                                                file_data = b""
                                                size_data_count = 0
                                                cont1 = 0
                                                while recv_size < file_size_re:
                                                        tmp = sock.recv(file_size_re - recv_size)
                                                        if not tmp:
                                                                break
                                                        file_data += tmp
                                                        recv_size += len(tmp)
                                                
                                                        cont = int((recv_size/file_size_re)*100)

                                                        
                                                        
                                                        if cont == cont1:
                                                        
                                                                pass
                                                        else:
                                                                bai = "%"+str(cont)
                                                                if cont%10==0:
                                                                        print("我被执行了")
                                                                        jind = "<- "+ "="*int(cont/10)+" ->"
                                                                        abb.set("我不是进度条:  "+jind+"  "+'已下载  %s'%bai)
                                                                else:
                                                                        abb.set("我不是进度条:  "+jind+"  "+'已下载  %s'%bai)
                                                                cont1 = cont
                                                try:
                                                        if path_file=="":
                                                                tk.messagebox.showerror("来自大帅比的提示","请输入正确的文件路径！")
                                                                return
                                                        os.chdir(path_file)
                                                        file_path =  data["file_name"]
                                                        
                                                        
                                                        with open(file_path,'wb') as f:
                                                                f.write(file_data)
                                                        print(".............",path_file)
                                                        
                                                except:
                                                        tk.messagebox.showerror("来自大帅比的提示","请输入正确的文件路径！")
                                                        return
                                        if data["file_type"] == 1:
                                                if path_file=="":
                                                        tk.messagebox.showerror("来自大帅比的提示","请输入正确的文件路径！")
                                                        return
                                                os.chdir(path_file)
                                                file_dir = os.path.dirname(path_file + "/"+data["file_name"])
                                                print("我是文件路径",file_dir)
                                                try:
                                                        os.makedirs(file_dir)
                                                except FileExistsError:
                                                        pass
                                                filename = data["file_name"]
                                                filesize = int(data["file_size"])
                                                data = b""
                                                data_cont = b""
                                                cont1=0
                                                cont2=0
                                                print("我要开始接收内容了")
                                                while True:
                                                        
                                                        data = sock.recv(filesize-cont1)
                                                        data_cont+=data
                                                        cont1+=len(data)
                                                        
                                                        if cont1 == filesize:
                                                                print("我在接收123")
                                                                break
                        
                                                        cont = int((cont1/filesize)*100)
                                                        
                                                        
                                                        if cont == cont2:
                                                        
                                                                pass
                                                        else:
                                                                bai = "%"+str(cont)
                                                                if cont%10==0:
                                                                        print("我被执行了")
                                                                        jind = "<- "+ "="*int(cont/10)+" ->"
                                                                        abb.set("我不是进度条:  "+jind+"  "+'已下载  %s'%bai)
                                                                else:
                                                                        abb.set("我不是进度条:  "+jind+"  "+'已下载  %s'%bai)
                                                                cont2 = cont
                                                with open(filename,"wb") as op:
                                                        op.write(data_cont) 


                                                        # ooo = int(100/(int(filesize)/aoe))
                                                        # if ooo==bv:
                                                        #         pass
                                                        # else:     
                                                        #         oo = '%' + str(ooo)
                                                        #         if ooo%10==0:
                                                        #                 jind = "<-"+ "="*int(10-ooo/10)+"->"
                                                        #                 abb.set("我不是进度条:  "+jind+"  "+'还剩下  %s'%oo)
                                                        #         else:
                                                        #                 abb.set("我不是进度条:  "+jind+"  "+'还剩下  %s'%oo)
                                                        #         bv = ooo
                        time_conut = time.time()-time1
                        tk.messagebox.showinfo("来自大帅比的提示提示","下载完成!本次下载文件%s个,耗时%s秒"%(py,int(time_conut)))
                finally:
                        sock.close()
                        click = 0


        sock = socket.socket()
        try:
                sock.connect(("127.0.0.1",9988))


                send_data = {"op":1,"args":{"name":dpc_list[0]["name"],"password":dpc_list[0]["password"]},"look":0}
                send_data = json.dumps(send_data)
                send_data_size = str(len(send_data.encode())).encode()+b' '*(15-len(str(len(send_data.encode())).encode()))
                sock.send(send_data_size)
                sock.send(send_data.encode())
                data_size = sock.recv(15).decode().rstrip()
                data_size = int(data_size)
                data = sock.recv(data_size)
                data = json.loads(data.decode())
                sock.close()

                window = tk.Tk()
                
                window.title('文件下载')
                window.minsize(800,400)


                sb = Scrollbar(window)   
                sb.pack(side=RIGHT,fill=Y)
                
                var2 = tk.StringVar()
                

                var2.set(data["exist_file"]) 
                lb = tk.Listbox(window, listvariable=var2,yscrollcommand=sb.set)
                lb["font"] = ('微软雅黑', 12)
                lb["highlightcolor"] = "yellow"
                lb["selectbackground"] = "#DB7093"
                lb.pack(fill=BOTH)
                path = StringVar()
                Label(window,text = "目标路径:",font= ('宋体', 13)).place(x=140, y=345)
                Entry(window, textvariable = path,font= ('宋体', 13),borderwidth = 3,width = 40).place(x=220,y=345)
                Button(window, text = "路径选择", command = selectPath).place(x=590,y=342)
                # 第5步，创建一个按钮并放置，点击按钮调用print_selection函数
                abb = tk.StringVar()
                tk.Label(window,textvariable =abb,font=("宋体", 14)).place(x=200, y=240)
                b1 = tk.Button(window, text='下载', width=17, height=1, command=print_selection)
                b1.place(x=320,y=280)
                # 第8步，主窗口循环显示
                window.mainloop()
        except:
                tk.messagebox.showerror("来自大帅比的提示","网络开了小差...")
def denglu(dpc):
        def th2():
                nonlocal mai,but
                cc = ["#FFB6C1",'#FFC0CB', '#DC143C', '#FFF0F5', '#DB7093', '#FF69B4', '#FF1493', '#C71585', '#DA70D6', '#D8BFD8', '#DDA0DD', '#EE82EE', '#FF00FF', '#FF00FF', '#8B008B', '#800080', '#BA55D3', '#9400D3', '#9932CC', '#4B0082', '#8A2BE2', '#9370DB', '#7B68EE', '#6A5ACD', '#483D8B', '#E6E6FA', '#F8F8FF', '#0000FF', '#0000CD', '#191970', '#00008B', '#000080', '#4169E1', '#6495ED', '#B0C4DE', '#778899', '#708090', '#1E90FF', '#F0F8FF', '#4682B4', '#87CEFA', '#87CEEB', '#00BFFF', '#ADD8E6', '#B0E0E6', '#5F9EA0', '#F0FFFF', '#E0FFFF', '#AFEEEE', '#00FFFF', '#00FFFF', '#00CED1', '#2F4F4F', '#008B8B', '#008080', '#48D1CC', '#20B2AA', '#40E0D0', '#7FFFD4', '#66CDAA', '#00FA9A', '#F5FFFA', '#00FF7F', '#3CB371', '#2E8B57', '#F0FFF0', '#90EE90', '#98FB98', '#8FBC8F', '#32CD32',
        '#00FF00', '#228B22', '#008000', '#006400', '#7FFF00', '#7CFC00', '#ADFF2F', '#556B2F', '#9ACD32', '#6B8E23', '#F5F5DC', '#FAFAD2', '#FFFFF0', '#FFFFE0', '#FFFF00', '#808000', '#BDB76B', '#FFFACD', '#EEE8AA', '#F0E68C', '#FFD700', '#FFF8DC', '#DAA520', '#B8860B', '#FFFAF0', '#FDF5E6', '#F5DEB3', '#FFE4B5', '#FFA500', '#FFEFD5', '#FFEBCD', '#FFDEAD', '#FAEBD7', '#D2B48C', '#DEB887', '#FFE4C4', '#FF8C00', '#FAF0E6', '#CD853F', '#FFDAB9', '#F4A460', '#D2691E', '#8B4513', '#FFF5EE', '#A0522D', '#FFA07A', '#FF7F50', '#FF4500', '#E9967A', '#FF6347', '#FFE4E1', '#FA8072', '#FFFAFA', '#F08080', '#BC8F8F', '#CD5C5C', '#FF0000', '#A52A2A', '#B22222', '#8B0000', '#800000', '#FFFFFF', '#F5F5F5', '#DCDCDC', '#D3D3D3', '#C0C0C0', '#A9A9A9', '#808080', '#696969', '#000000']
                while True:

                        a = random.randint(0,len(cc)-1)
                        time.sleep(0.3)
                        but["bg"]=cc[a]

        def th3():
                nonlocal mai,but1
                cc = ["#FFB6C1",'#FFC0CB', '#DC143C', '#FFF0F5', '#DB7093', '#FF69B4', '#FF1493', '#C71585', '#DA70D6', '#D8BFD8', '#DDA0DD', '#EE82EE', '#FF00FF', '#FF00FF', '#8B008B', '#800080', '#BA55D3', '#9400D3', '#9932CC', '#4B0082', '#8A2BE2', '#9370DB', '#7B68EE', '#6A5ACD', '#483D8B', '#E6E6FA', '#F8F8FF', '#0000FF', '#0000CD', '#191970', '#00008B', '#000080', '#4169E1', '#6495ED', '#B0C4DE', '#778899', '#708090', '#1E90FF', '#F0F8FF', '#4682B4', '#87CEFA', '#87CEEB', '#00BFFF', '#ADD8E6', '#B0E0E6', '#5F9EA0', '#F0FFFF', '#E0FFFF', '#AFEEEE', '#00FFFF', '#00FFFF', '#00CED1', '#2F4F4F', '#008B8B', '#008080', '#48D1CC', '#20B2AA', '#40E0D0', '#7FFFD4', '#66CDAA', '#00FA9A', '#F5FFFA', '#00FF7F', '#3CB371', '#2E8B57', '#F0FFF0', '#90EE90', '#98FB98', '#8FBC8F', '#32CD32',
        '#00FF00', '#228B22', '#008000', '#006400', '#7FFF00', '#7CFC00', '#ADFF2F', '#556B2F', '#9ACD32', '#6B8E23', '#F5F5DC', '#FAFAD2', '#FFFFF0', '#FFFFE0', '#FFFF00', '#808000', '#BDB76B', '#FFFACD', '#EEE8AA', '#F0E68C', '#FFD700', '#FFF8DC', '#DAA520', '#B8860B', '#FFFAF0', '#FDF5E6', '#F5DEB3', '#FFE4B5', '#FFA500', '#FFEFD5', '#FFEBCD', '#FFDEAD', '#FAEBD7', '#D2B48C', '#DEB887', '#FFE4C4', '#FF8C00', '#FAF0E6', '#CD853F', '#FFDAB9', '#F4A460', '#D2691E', '#8B4513', '#FFF5EE', '#A0522D', '#FFA07A', '#FF7F50', '#FF4500', '#E9967A', '#FF6347', '#FFE4E1', '#FA8072', '#FFFAFA', '#F08080', '#BC8F8F', '#CD5C5C', '#FF0000', '#A52A2A', '#B22222', '#8B0000', '#800000', '#FFFFFF', '#F5F5F5', '#DCDCDC', '#D3D3D3', '#C0C0C0', '#A9A9A9', '#808080', '#696969', '#000000']
                while True:

                        a = random.randint(0,len(cc)-1)
                        time.sleep(0.3)
                        but1["bg"]=cc[a]


        def update(idx):
                frame = frames[idx]
                idx += 1
                label.configure(image=frame)
                mai.after(100, update, idx%numIdx)
        def th1():
                nonlocal mai
                cc = ["#FFB6C1",'#FFC0CB', '#DC143C', '#FFF0F5', '#DB7093', '#FF69B4', '#FF1493', '#C71585', '#DA70D6', '#D8BFD8', '#DDA0DD', '#EE82EE', '#FF00FF', '#FF00FF', '#8B008B', '#800080', '#BA55D3', '#9400D3', '#9932CC', '#4B0082', '#8A2BE2', '#9370DB', '#7B68EE', '#6A5ACD', '#483D8B', '#E6E6FA', '#F8F8FF', '#0000FF', '#0000CD', '#191970', '#00008B', '#000080', '#4169E1', '#6495ED', '#B0C4DE', '#778899', '#708090', '#1E90FF', '#F0F8FF', '#4682B4', '#87CEFA', '#87CEEB', '#00BFFF', '#ADD8E6', '#B0E0E6', '#5F9EA0', '#F0FFFF', '#E0FFFF', '#AFEEEE', '#00FFFF', '#00FFFF', '#00CED1', '#2F4F4F', '#008B8B', '#008080', '#48D1CC', '#20B2AA', '#40E0D0', '#7FFFD4', '#66CDAA', '#00FA9A', '#F5FFFA', '#00FF7F', '#3CB371', '#2E8B57', '#F0FFF0', '#90EE90', '#98FB98', '#8FBC8F', '#32CD32',
        '#00FF00', '#228B22', '#008000', '#006400', '#7FFF00', '#7CFC00', '#ADFF2F', '#556B2F', '#9ACD32', '#6B8E23', '#F5F5DC', '#FAFAD2', '#FFFFF0', '#FFFFE0', '#FFFF00', '#808000', '#BDB76B', '#FFFACD', '#EEE8AA', '#F0E68C', '#FFD700', '#FFF8DC', '#DAA520', '#B8860B', '#FFFAF0', '#FDF5E6', '#F5DEB3', '#FFE4B5', '#FFA500', '#FFEFD5', '#FFEBCD', '#FFDEAD', '#FAEBD7', '#D2B48C', '#DEB887', '#FFE4C4', '#FF8C00', '#FAF0E6', '#CD853F', '#FFDAB9', '#F4A460', '#D2691E', '#8B4513', '#FFF5EE', '#A0522D', '#FFA07A', '#FF7F50', '#FF4500', '#E9967A', '#FF6347', '#FFE4E1', '#FA8072', '#FFFAFA', '#F08080', '#BC8F8F', '#CD5C5C', '#FF0000', '#A52A2A', '#B22222', '#8B0000', '#800000', '#FFFFFF', '#F5F5F5', '#DCDCDC', '#D3D3D3', '#C0C0C0', '#A9A9A9', '#808080', '#696969', '#000000']
                while True:

                        for i in cc:
                                time.sleep(0.3)
                                tk.Label(mai,text="欢迎来到pp多人聊天组",bg = i,font=("宋体", 14)).place(x=115, y=190)
        def login(dpc):
                '''
                专门用户登录
                '''
                nonlocal mai,user_name,user_pwd
                sock = socket.socket()
                try:
                        sock.connect(("127.0.0.1", 9999))
                except:
                        tk.messagebox.showerror("来自大帅比的提示提示","网络错误!")
                        sys.exit(1)

                if len(user_name.get())==0 or len(user_pwd.get())==0:
                        tk.messagebox.showerror("来自大帅比的提示提示","客官，用户名或者密码不能为空!")
                else:
                        send_data = {"op":0,"args":{"user_name":user_name.get(),"user_pwd":user_pwd.get()}}
                        send_data = json.dumps(send_data)


                        send_size = str(len(send_data.encode())).encode()+b' '*(15-len(str(len(send_data.encode()))))
                        print(send_size,len(send_size))
                        sock.send(send_size)
                        print(send_size)
                        sock.send(send_data.encode())
                        try:
                                harvest_size = 15
                                harvest_size1 = 0
                                harvest_size2 = 15
                                harvest_data = b''
                                while True:
                                        harvest_data1 = sock.recv(harvest_size2)
                                        if not harvest_data1:
                                                break
                                        harvest_data += harvest_data1
                                        harvest_size1 += len(harvest_data1)
                                        harvest_size2 = harvest_size - harvest_size1
                                        if harvest_size2 == 0:
                                                break
                                data_json_size = int(harvest_data.decode().rstrip())
                                data_json_size1 = 0
                                data_json_size2 = 1000
                                data_json = b''
                                if data_json_size < data_json_size2:
                                        data_json_size2 = data_json_size
                                while True:
                                        data_json1 = sock.recv(data_json_size2)
                                        data_json += data_json1
                                        data_json_size1 += len(data_json1)
                                        data_json_size2 = data_json_size - data_json_size1
                                        if data_json_size2 == 0:
                                                break
                                data_json = json.loads((data_json.decode()))
                                print("我是字典",data_json)
                                #此时请求消息变成了字典
                                #请求消息类型是数字
                                #服务器响应数据也是数
                                if data_json["test"] == 0:
                                        tk.messagebox.showinfo("来自大帅比的提示提示","登录成功!")
                                        dpc.put({"op":1})
                                        dpc.put({"name":user_name.get(),"password":user_pwd.get()})
                                        mai.quit()
                                        
                                        
                                if data_json["test"] == 1:
                                        tk.messagebox.showerror("来自大帅比的提示提示","客官，用户名或者密码错误!")

                        finally:
                                sock.close()





        mai = tk.Tk() #创建一个Tk类的实例（即主窗口对象）
        mai.title("pp登录") 
        tk.Frame(master=None,bg = "black").pack(expand=tk.YES,fill=tk.BOTH)
        mai.minsize(400,400)
        numIdx = 30 # gif的帧数
        filename = os.path.dirname(sys.argv[0]) + "/" + 'ali.gif'
        frames = [tk.PhotoImage(file=filename, format='gif -index %i' %(i)) for i in range(numIdx)]
        label = tk.Label(mai)
        label.pack()
        mai.after(0, update, 0)

        threading.Thread(target=th1,daemon=True).start()


        tk.Label(mai, text='用户名：', font=("微雅软黑", 11),).place(x=50, y=240)
        user_name=tk.StringVar()
        tk.Entry(mai, textvariable=user_name,show=None, font=('仿宋', 14)).place(x=125, y=240)
        tk.Label(mai, text='密码：', font=("微雅软黑", 11)).place(x=50, y=280)
        user_pwd = tk.StringVar()
        tk.Entry(mai, textvariable=user_pwd,show='*', font=('仿宋', 14)).place(x=110, y=280)

        but = tk.Button(mai,text="登 录",command=lambda:login(dpc),width=14,height=0)
        but.place(x=150,y=320)
        threading.Thread(target=th2,daemon=True).start()
        mai.resizable(0,0)
        but1 = tk.Button(mai,text="注 册",command=regester1,width=6)
        threading.Thread(target=th3,daemon=True).start()
        but1.place(x=90,y=320)
        mai.mainloop()
        dpc.put({"op":0})
        
def on_send_msg():
        send_msg_btn["bg"] = "#FAEBD7"
        
        chat_msg = chat_msg_box.get(1.0, "end")
        if chat_msg == "\n":
                return

        chat_data = {"op":0,"args":{"name":user_list[0]["name"],"password":user_list[0]["password"]},"news":chat_msg}
        chat_data = json.dumps(chat_data)
        chat_data = chat_data.encode()
        data_len = "{:<15}".format(len(chat_data)).encode()
        
        try:
                sock.send(data_len)
                sock.send(chat_data)
        except:
        # sock.close()
                tk.messagebox.showerror("温馨提示", "发送消息失败，请检查网络连接！")
        else:
                chat_da = user_list[0]["name"] + " :"+chat_msg
                chat_msg_box.delete(1.0, "end")
                chat_record_box.configure(state=tk.NORMAL)
                chat_record_box.insert("end", chat_da + "\n")
                chat_record_box.configure(state=tk.DISABLED)
                send_msg_btn["bg"] = "#FFFFFF"

def recv_chat_msg():
        global sock

        while True:
                try:
                        while True:
                                msg_len_data = sock.recv(15)
                                if not msg_len_data:
                                        break

                                msg_len = int(msg_len_data.decode().rstrip())
                                recv_size = 0
                                msg_content_data = b""
                                while recv_size < msg_len:
                                        tmp_data = sock.recv(msg_len - recv_size)
                                        if not tmp_data:
                                                break
                                        msg_content_data += tmp_data
                                        recv_size += len(tmp_data)
                                else:
                                # 显示   
                                        print("我要显示了")
                                        msg_content_data = json.loads(msg_content_data.decode())
                                        print(msg_content_data)
                                        chat_record_box.configure(state=tk.NORMAL)
                                        chat_record_box.insert("end", msg_content_data["news"] + "\n")
                                        chat_record_box.configure(state=tk.DISABLED)
                                        continue
                                break
                finally:
                        sock.close()
                        sock = socket.socket()
                        sock.connect(("127.0.0.1", 9998))






def regester1():
        ttt = multiprocessing.Process(target=regester)
        ttt.start()

def regester():
        oo = 0
        ph = 0
        def phone_yanzheng():
                nonlocal oo,ph
                sock = socket.socket()
                try:
                        sock.connect(("127.0.0.1", 9999))
                except:
                        tk.messagebox.showerror("来自大帅比的提示提示","网络开小差了...请重新尝试!")
                        return
                if test_phone(user_phone.get()):
                        
                        send_phone = user_phone.get()
                        send_data = {"op":1,"args":{"user_phone":send_phone}}
                        send_data = json.dumps(send_data)
                        send_data_size = str(len(send_data.encode())).encode()+b' '*(15-len(str(len(send_data.encode()))))
                        sock.send(send_data_size)
                        sock.send(send_data.encode())
                        try:
                                harvest_size = 15
                                harvest_size1 = 0
                                harvest_size2 = 15
                                harvest_data = b''
                                while True:
                                        harvest_data1 = sock.recv(harvest_size2)
                                        if not harvest_data1:
                                                break
                                        harvest_data += harvest_data1
                                        harvest_size1 += len(harvest_data1)
                                        harvest_size2 = harvest_size - harvest_size1
                                        if harvest_size2 == 0:
                                                break
                                data_json_size = int(harvest_data.decode().rstrip())
                                data_json_size1 = 0
                                data_json_size2 = 1000
                                data_json = b''
                                if data_json_size < data_json_size2:
                                        data_json_size2 = data_json_size
                                while True:
                                        data_json1 = sock.recv(data_json_size2)
                                        data_json += data_json1
                                        data_json_size1 += len(data_json1)
                                        data_json_size2 = data_json_size - data_json_size1
                                        if data_json_size2 == 0:
                                                break
                                data_json = json.loads((data_json.decode()))
                                #此时请求消息变成了字典
                                #请求消息类型是数字
                                #服务器响应数据也是数字
                                if data_json["test"] == 0:
                                        oo = 1
                                        ph = user_phone.get()
                                        tk.messagebox.showinfo("来自大帅比的提示","验证码发送成功")
                                        return
                                if data_json["test"] == 1:
                                        tk.messagebox.showerror("来自大帅比的提示","网络开了小差...请点击重新发送")
                                        return
                                if data_json["test"] == 2:
                                        tk.messagebox.showerror("来自大帅比的提示","该手机号不存在！")
                                        return
                                if data_json["test"] == 3:
                                        tk.messagebox.showerror("来自大帅比的提示","手机号已注册！")
                                        return
                        finally:
                                sock.close()

                else:
                        tk.messagebox.showerror("来自大帅比的提示","客官，请输入正确的手机号!")

        def user_zhuche():
                nonlocal oo,ph
                sock = socket.socket()
                try:
                        sock.connect(("127.0.0.1", 9999))
                except:
                        tk.messagebox.showerror("来自大帅比的提示提示","网络开小差了...请重新尝试!")
                        return
                if oo ==0:
                        tk.messagebox.showerror("来自大帅比的提示","客官，请验证手机号!")
                else:
                        if test_name(user_name_re.get()):
                                if test_pwd(user_pwd_re.get()):
                                        if user_pwd_re.get()==user_pwd_re1.get():
                                                if user_phone.get()==ph :
                                                        if len(user_vcode.get())!=0:
                                                                if test_email(user_email.get()):
                                                                        send_data = {"op":2,"args":{"user_name":user_name_re.get(),"user_pwd":user_pwd_re.get(),"user_phone":user_phone.get(),"user_vcode":user_vcode.get(),"user_email":user_email.get()}}
                                                                        send_data = json.dumps(send_data)
                                                                        send_size = str(len(send_data.encode())).encode()+b' '*(15-len(str(len(send_data.encode()))))
                                                                        sock.send(send_size)
                                                                        sock.send(send_data.encode())
                                                                        try:
                                                                                harvest_size = 15
                                                                                harvest_size1 = 0
                                                                                harvest_size2 = 15
                                                                                harvest_data = b''
                                                                                while True:
                                                                                        harvest_data1 = sock.recv(harvest_size2)
                                                                                        if not harvest_data1:
                                                                                                break
                                                                                        harvest_data += harvest_data1
                                                                                        harvest_size1 += len(harvest_data1)
                                                                                        harvest_size2 = harvest_size - harvest_size1
                                                                                        if harvest_size2 == 0:
                                                                                                break
                                                                                data_json_size = int(harvest_data.decode().rstrip())
                                                                                data_json_size1 = 0
                                                                                data_json_size2 = 1000
                                                                                data_json = b''
                                                                                if data_json_size < data_json_size2:
                                                                                        data_json_size2 = data_json_size
                                                                                while True:
                                                                                        data_json1 = sock.recv(data_json_size2)
                                                                                        data_json += data_json1
                                                                                        data_json_size1 += len(data_json1)
                                                                                        data_json_size2 = data_json_size - data_json_size1
                                                                                        if data_json_size2 == 0:
                                                                                                break
                                                                                data_json = json.loads((data_json.decode()))
                                                                                #此时请求消息变成了字典
                                                                                #请求消息类型是数字
                                                                                #服务器响应数据也是数字
                                                                                if data_json["test"] == 0:
                                                                                        tk.messagebox.showinfo("来自大帅比的提示提示","注册成功!")
                                                                                        wind.quit()
                                                                                if data_json["test"] == 1:
                                                                                        tk.messagebox.showerror("来自大帅比的提示提示","用户名已存在!")
                                                                                if data_json["test"] == 2:
                                                                                        tk.messagebox.showerror("来自大帅比的提示提示","输入手机号有误!")
                                                                                if data_json["test"] == 3:
                                                                                        tk.messagebox.showerror("来自大帅比的提示提示","验证码错误!")

                                                                        finally:
                                                                                
                                                                                sock.close()
                                                                          
                                                                else:
                                                                        tk.messagebox.showerror("来自大帅比的提示提示","请输入正确邮箱!")
                                                                        return
                                                        else:
                                                                tk.messagebox.showerror("来自大帅比的提示提示","请输入验证码!")
                                                                return
                                                else:
                                                        tk.messagebox.showerror("来自大帅比的提示提示","请输入正确的手机号!")
                                                        return
                                        else:
                                                tk.messagebox.showerror("来自大帅比的提示提示","两次输入密码不一致!")
                                                return
                                else:
                                        tk.messagebox.showerror("来自大帅比的提示提示","用户密码强度太弱，或者不合法!")
                                        return
                                
                        else:
                                tk.messagebox.showerror("来自大帅比的提示提示","非法用户名!")
                                return


                                

         
        wind = tk.Tk()
        wind.minsize(400,400)
        wind.title("注册")
        filename1 = os.path.dirname(sys.argv[0]) + "/" + "ye.jpg"
        mg = PIL.Image.open(filename1)  
        imgg = ImageTk.PhotoImage(mg)
        lab=tk.Label(wind,image=imgg)
        lab.pack()
        tk.Label(wind, text='用户名:',font=("微雅软黑", 11)).place(x=23, y=25)
        user_name_re = tk.StringVar()
        tk.Entry(wind, textvariable=user_name_re,show=None, font=('仿宋', 14)).place(x=85, y=25)
        tk.Label(wind, text='(任意非空字符，最短为1，最长为6)',font=("微雅软黑", 9)).place(x=300, y=25)
        tk.Label(wind, text='用户密码:',font=("微雅软黑", 11)).place(x=23, y=60)
        user_pwd_re = tk.StringVar()
        tk.Entry(wind, textvariable=user_pwd_re,show="*", font=('仿宋', 14)).place(x=100, y=60)
        tk.Label(wind, text='(密码至少由数字和字母组合，最低6位，最高16位)',font=("微雅软黑", 9)).place(x=310, y=60)
        tk.Label(wind, text='确认密码:',font=("微雅软黑", 11)).place(x=23, y=95)
        user_pwd_re1 = tk.StringVar()
        tk.Entry(wind, textvariable=user_pwd_re1,show="*", font=('仿宋', 14)).place(x=100, y=95)
        tk.Label(wind, text='请输入手机号:',font=("微雅软黑", 11)).place(x=23, y=130)
        user_phone = tk.StringVar()
        tk.Entry(wind, textvariable=user_phone,show=None, font=('仿宋', 14)).place(x=130, y=130)
        tk.Button(wind,text="发送验证码",command=phone_yanzheng,width=8,height=-2).place(x=340, y=130)
        tk.Label(wind, text='请输入验证码:',font=("微雅软黑", 11)).place(x=23, y=165)
        user_vcode= tk.StringVar()
        tk.Entry(wind, textvariable=user_vcode,show=None, font=('仿宋', 14)).place(x=130, y=165)
        tk.Label(wind, text='请输入邮箱:',font=("微雅软黑", 11)).place(x=23, y=200)
        user_email = tk.StringVar()
        tk.Entry(wind, textvariable=user_email,show=None, font=('仿宋', 14)).place(x=120, y=200)
        tk.Button(wind,text="注册",command=user_zhuche,width=12,height=0).place(x=145, y=245)
        wind.resizable(0,0)
        wind.mainloop()



                

if __name__ == "__main__":

        tttt = multiprocessing.Process(target=denglu,args=(dpc,))
        tttt.start()
        tttt.join()
        oppp = dpc.get()
        if oppp["op"]==1:
                user_list.append(dpc.get())
                print("我是用户的名字和密码",user_list[0])
                      
                sock = socket.socket()
                sock.connect(("127.0.0.1", 9998))

                mainWnd = tk.Tk()
                mainWnd.title("当代青年在线激聊室")
                mainWnd.minsize(1000,500)
                menubar = tk.Menu(mainWnd)
                filemenu = tk.Menu(menubar, tearoff=0)
                menubar.add_cascade(label='文 件', menu=filemenu)
                filemenu.add_command(label='上 传',command=shangchuan)
                filemenu.add_command(label='下 载',command=xiazai)
                mainWnd.config(menu=menubar)

                editmenu = tk.Menu(menubar, tearoff=0)
                menubar.add_cascade(label='设 置', menu=editmenu)
                mainWnd.config(menu=menubar)


                chat_record_box = tk.Text(mainWnd)
                chat_record_box.configure(width=81, height=25,state=tk.DISABLED)
                chat_record_box.place(x=215,y=20)

                chat_msg_box = tk.Text(mainWnd)
                chat_msg_box.configure(width=81, height=5)
                chat_msg_box.place(x=215,y=370)

                send_msg_btn = tk.Button(mainWnd, width=16,height=1,text="发 送", command=on_send_msg)
                send_msg_btn.place(x=440,y=450)

                ml = threading.Thread(target=recv_chat_msg,daemon=True)
                ml.setDaemon(True)
                ml.start()

                mainWnd.mainloop()

                sock.close()

                # chek_liao()
                #threading.Thread(target=chek_liao).start().join()
                ##chek_1()

