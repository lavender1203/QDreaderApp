# QDreaderApp
起点读书app登录协议
服务器：以ubuntu系统为例
# 下载源代码
xjg@xjg-pc:~/work$git clone https://github.com/lavender1203/QDreaderApp.git
# 安装python3
# 安装python库 scrapy jpype1 selenium
xjg@xjg-pc:~/work/QDreaderApp$sudo apt install python3-pip  
xjg@xjg-pc:~/work/QDreaderApp$pip3 install scrapy   
# 安装jdk
xjg@xjg-pc:~/work/QDreaderApp$sudo apt install openjdk-8-jdk
# 配置jvm路径---ubuntu系统不用配置
xjg@xjg-pc:~/work/QDreaderApp$sudo find / -name 'libjvm.so'
 
/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server/libjvm.so
# 安装chromedriver
xjg@xjg-pc:~/work/QDreaderApp$sudo apt install chromium   #版本78.0.3904.108  
去http://npm.taobao.org/mirrors/chromedriver/下载对应的chromedriver
http://chromedriver.storage.googleapis.com/78.0.3904.105/chromedriver_linux64.zip
解压后复制到/usr/bin目录下
xjg@xjg-pc:~/work/QDreaderApp$sudo cp chromedriver /usr/bin/

# 运行
xjg@xjg-pc:~/work/QDreaderApp$ python3 MainTest.py
