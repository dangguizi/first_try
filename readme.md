FTP文件传输： 

    【1】 分为服务端和客户端，要求可以有多个客户端同时操作。
    【2】 客户端要求身份验证。
    【3】 客户端可以查看服务器文件库中有什么文件。
    【4】 客户端可以从文件库中下载文件到本地。
    【5】 客户端可以上传一个本地文件到文件库。
    【6】 使用print在客户端打印命令输入提示，引导操作
    【7】 文件夹D：/FTP为文件库
    
ftp:

身份验证:

    成功:

        上传文件

            保存文件（server）

        下载文件

            保存文件（client）

    失败:
        退出

mysql:

    打开命令行输入
        mysql -u root -p→
        →password→
        show databases;
        create database ftp;
        use ftp;
        create table user(id varchar(40) primary key,
                          password varchar(40));
        insert into user value('000001','123456'),('000002','123456'),('000003','654321');
