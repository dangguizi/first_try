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
