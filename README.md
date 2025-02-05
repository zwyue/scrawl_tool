## 资料网站

### 田间小站 https://www.tjxz.cc
### 扇贝 https://web.shanbay.com

### 菜单 html
 - 运行 [菜单](scratch_menu.py) 生成 doc/menu.txt
 - 使用 nginx 部署静态资源
    ```
      1.docker pull nginx  
      2.docker docker run --restart always --name nginx -d -p 7788:80 nginx
      3.挂载目录
        docker container cp nginx:/var/log/nginx D:\projects\env\nginx\logs
        docker container cp nginx:/etc/nginx/nginx.conf D:\projects\env\nginx\conf
        docker container cp nginx:/etc/nginx/conf.d/default.conf D:\projects\env\nginx\conf.d
        docker container cp nginx:/usr/share/nginx/html/index.html D:\projects\env\nginx\html 
      4.docker stop nginx  
      5.docker rm nginx
      6.修改 default.conf ,添加 [ charset utf-8; ]分号不能丢
      7.运行如下命令
    docker run --restart always --name nginx -d -p 7788:80 -v D:\projects\env\nginx\logs:/var/log/nginx -v D:\projects\backup\practice\scrawl_tool:/usr/share/nginx/html -v D:\projects\env\nginx\conf\nginx.conf:/etc/nginx/nginx.conf -v D:\projects\env\nginx\conf.d:/etc/nginx/conf.d -d nginx:latest
   ```