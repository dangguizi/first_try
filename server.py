import pymysql
import socketserver
import time
import os
xieyi='''
    +----------------------+
        1.向服务器端上传文件
        2.从服务器端下载文件
    +----------------------+
    '''

login='''
    +----------------------+
    +        身份验证        + 
    +    请输入用户名和密码：  +   
    +----------------------+
    '''


#实例化
class MyTCPhandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='cl19970312',
                db='ftp',
                charset='utf8',
            )
        except pymysql.Error as e:
            print("数据库连接失败", e)
            exit()
        finally:
            root_path = 'D:\FTP//'
            print("数据库连接成功")
            self.cur = conn.cursor()
            while True:
                try:
                    self.login_yanzheng = False
                    self.data=self.request.recv(1024)
                    print('{}:{}wrote:'.format(self.client_address[0],self.client_address[1]))
                    print("data:",self.data.decode('utf-8'))
                    if check_connect(self.data,self.cur):
                        print("登陆成功")
                        id=check_connect(self.data,self.cur)
                        self.login_yanzheng=True
                        self.request.send("登陆成功".encode('utf-8'))
                        if self.request.recv(1024).decode('utf-8')=='1':
                            print("准备接收文件")
                            self.request.send("OK".encode('utf-8'))
                            data=self.request.recv(10000000)
                            save_data(data,id,self.cur)
                            self.request.close()
                            conn.commit()
                        else:
                            print("准备向客户端传送文件")
                            data=query(id,self.cur)
                            if  not data:
                                self.request.send("未找到您的上传记录".encode('utf-8'))
                                print("与 {} 断开连接".format(self.client_address[0]))
                                self.request.close()
                            else:
                                self.request.send(data.encode('utf-8'))
                                request=self.request.recv(1024).decode('utf-8')
                                if isfile(root_path+request+'.jpg'):
                                    data=readfile(root_path+request+'.jpg')
                                    self.request.send(data)
                                else:
                                    self.request.send('')
                    else:
                        print("登陆失败")
                        self.login_yanzheng=False
                        self.request.send("登陆失败，用户名不存在".encode('utf-8'))
                except ConnectionError as e:
                    print(e)
                    break
                except:
                    break
def check_connect(data,cur):
    data=data.decode('utf-8').split()
    id,password=data[0],data[1]
    sql='select * from user where id={};'.format(id)
    cur.execute(sql)
    results=cur.fetchall()
    if results[0][0]==id and results[0][1]==password:
        return id
    else:
        return None

def isfile(filename):
    result=os.path.exists(filename)
    return result
def readfile(filename):
    with open(filename,'rb') as f:
        data=f.read()
    return data
def save_data(data,id,cur):
    today_now = time.strftime('%Y%m%d%H%M%S')
    filename=id+today_now+'.jpeg'
    root_path='D:\FTP//'
    #os.makedirs(root_path)
    with open(root_path+filename,'wb') as f:
        f.write(data)
    sql='insert into file values("{}","{}");'.format(id,filename.split('.')[0])
    print(sql)
    cur.execute(sql)
    print("文件上传成功，共 {} 字节".format(len(data)))

def query(id,cur):
    try:
        sql='select filename from file where id="{}";'.format(id)
        cur.execute(sql)
        results=cur.fetchall()
        data=''
        for result in results:
            data+=str(result)+','
        return data
    except pymysql.Error as e:
        print(e)
        return None

if __name__=='__main__':
    HOST ='ZHOUSHUN'
    PORT = 8080
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPhandler)
    server.serve_forever()