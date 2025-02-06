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
   
### Concert_Ticket
大麦网演唱会抢票程序
* Python3.6
* Selenium
## 准备工作
* 下载anaconda，对应python3.6
* 下载火狐浏览器（推荐）以及对应的geckodriver.exe，并将此exe转移到python.exe旁边。谷歌浏览器的操作类似。
* 打开命令提示窗口，输入pip install selenium
* 如果提示其他包未安装，请用相同的方式下载
* 在user_info.txt中输入提示的信息
* 在主函数中按要求输入演唱会信息
* 运行代码，在这个过程中注意观察串口输出