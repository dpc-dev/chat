## 类似QQ的多人聊天组

经过慢慢改造,离QQ更近了一步,实现了炫酷GUI登录注册,多人聊天，文件共享,仍在慢慢改造中......

### DPC通信协议

1. 基于TCP通信
2. 定长包头
3. json数据格式发
4. 客户端主动发送请求，服务端回应请求
5. 采用三个服务端，处理用户请求
6. 验证注册服务端，聊天发送接收服务端，文件上传下载服务端

#### 验证注册服务端通信格式

- 用户登录

```
1. 客户端：
   0:用户登录校验

- 示例：{
  "op":0,

	"args":{

	"user_name":"18671289536"

	"user_pwd":"........"

}

1.  服务端发送:
   test:0表示校验成功，1表示校验失败
   op:0表示用户登录

- 示例{
  	"op":0,
  	"test":0
  }

```

- 用户发送验证码

```
1.用户端发送
示例：
{
    "op":1,
    "args":{
        "user_phone":"186******"
    }
}
1.服务端响应
test:0表示成功，3表示手机号已存在,1表示网络问题,2表示手机号有问题
示例：
{
    "op":1,
    "test":0
}
```

- 用户端注册

```
1. 客户端：
   0:用户登录校验

- 示例：{
  "op":2,

	"args":{

	"user_name":"18671289536",

	"user_pwd":"........",
	"user_phone":"......",
	"user_vcode": ".....",
	"user_email":"....."
}
1.服务端响应
test:0表示成功，1表示用户名已经存在,2表示输入手机号有误,3表示验证码错误.
示例：
{
    "op":1,
    "test":0
}
```

#### 聊天发送接收服务器通信格式

数据传输格式为json格式

1. 客户端向服务器发送消息,op请求类型，0发消息请求

```
{
	"op":0
    "args":{"name":"...,"password":*******},
    "news":"我是消息"
}
服务器还需要验证用户名和密码
防止他人知道通信协议绕过登录验证
```

1. 服务器转发消息

```
{
	"op":0,
    "args":{"name":"***"},
    "news":"我是消息"
}
```





#### 上传下载文件服务器通信格式

- 文件处理

```
客户端上传请求
op请求类型0上传,1下载，file_type文件类型0文件，1文件夹
示例
{
    "op":0,
    "args":{"name":"***","password":"****"},
    "file_name":"0000",
    "file_type":0,
    "file_size":"00000"
}
{
    "op":0,
    "args":{"name":"***","password":"****"},
    "file_name":"0000",
    "file_type":1,
    "file_size":"0000",
    "file_dirname":"0000"
}
过程完成便直接断开连接
客户端下载请求,客户端要发送两个请求一个查看可以下载文件一个要下载文件,look,0表示查看文件,1表示下载文件
{
    "op":1,
    "args":{
        "name":"****",
        "password":"***"
        
    },
    "look":0
}
服务器响应,当前没有可下载文件exist_file就为0
{
    "op":1
    "exist_file":0
}
客户端下载指定文件请求
{
    "op":1,
     "args":{
        "name":"****",
        "password":"***"
        
    },
    "look":1,
    "file_name":"***"
}

服务器响应
{
    "op":1,
    "file_name":"0000",
    "file_type":0,
    "file_size":"00000"
}

下载文件或文件夹不存在
服务器响应，400文件不存在
{"op":1,"file_name":400}
```

