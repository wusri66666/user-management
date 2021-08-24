## 环境依赖
- django==2.1
- djangorestframework==3.9.4
- django-cors-headers==3.0.2
- pymysql==0.9.3
- gunicorn==19.9.0

## 目录介绍
```
 ├── aiot_server_system                            //项目文件夹
 │    |--__init__.py
 |    |--urls.py
 |    |--wsgi.py
 |    |--settings.py
 |    |--base.py
 |    |--dev.py
 |    |--production.py
 │
 ├── code.json                      //错误码
 │
 ├── Dockerfile                     //Dockerfile
 │
 ├── enterypoint.sh                 //项目启动脚本
 │  
 ├── gunicorn.conf                  //gunicorn配置文件
 │                  
 ├── manage.py                      //manage.py
 │                  
 ├── README.md                      //README.md
 │                 
 ├── requirements.txt               //三方库   
 │ 
 └── secrets.json                   //数据库配置
```

## 项目运行
- 首先在secrets.json文件中配置数据库连接信息
- 本地运行,首先迁移数据库生成表,然后运行,迁移和运行时可以指定环境为local,test_server,production
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver --settings=settings.local
```
- 打包运行,首先构建docker镜像，运行镜像的时候指定好运行环境,环境为local,test_server,production其中一种,命令如下
```
sudo docker build -t test:v1 .
sudo docker run -it -e ENV=local -p 8000:80 test:v1
```
        