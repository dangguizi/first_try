from socket import *
import time
import os
client=socket()
client.connect(('ZHOUSHUN',8080))
xieyi='''
    +----------------------+
        1.想服务器端上传文件
        2.从服务器端下载文件
    +----------------------+
    '''

login='''
    +----------------------+
    +        身份验证        + 
    +    请输入用户名和密码：  +   
    +----------------------+
    '''
def handle_data():
    is_quit = False
    while True:
        if is_quit:
            break
        send_mas = input(xieyi).strip()
        if send_mas in ['1','2']:
            if send_mas=="1":
                client.send(send_mas.encode('utf-8'))
                if client.recv(1024).decode('utf-8')=='OK':
                    while True:
                        filename=input("请输入文件名：").strip()
                        root_path ='D:\FTP//'
                        print(root_path+filename)
                        if isfile(root_path+filename):
                            print("文件存在")
                            client.send(readfile(root_path+filename))
                            print("文件发送成功，共 {} 字节".format(len(readfile(root_path+filename))))
                            is_quit = True
                            exit()
                            break
                        else:
                            print("文件不存在")
                            continue
                else:
                    break
            else:
                client.send(send_mas.encode('utf-8'))
                data=client.recv(1024)
                if data=='未找到您的上传记录':
                    print("未找到上传记录")
                    client.close()
                else:
                    print("一共有以下文件可以下载")
                    print(data.decode('utf-8'))
                    data=input("请输入您选择的文件>>").strip()
                    client.send(data.encode('utf-8'))
                    data=client.recv(1000000)
                    if data:
                        save_file(data)
                        break
                    else:
                        print("文件被删除")
        else:
            print("输入错误，请重新输入")
def isfile(filename):
    result=os.path.exists(filename)
    return result
def readfile(filename):
    with open(filename,'rb') as f:
        data=f.read()
    return data
def main():
    print(login)
    send_mas = input(">>").strip()
    client.send(send_mas.encode('utf-8'))
    recv_data = client.recv(1024)
    if recv_data.decode('utf-8') == '登陆成功':
        print("服务端允许获得连接")
        handle_data()
    else:
        print("服务器端不允许获得连接")
def save_file(data):
    today_now = time.strftime('%Y%m%d%H%M%S')
    filename =today_now + '.jpg'
    root_path = 'D:\FTP//'
    # os.makedirs(root_path)
    with open(root_path + filename, 'wb') as f:
        f.write(data)
    print("文件保存成功!共 {} 字节".format(len(data)))

if __name__=='__main__':
    main()
