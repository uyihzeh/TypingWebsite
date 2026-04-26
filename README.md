# TypingWebsite
A simple website for improving typing speed.

功能特性
- ✅ 纯 26 个小写英文字母随机生成，没有大写，不用切换输入法
- ✅ 实时显示 WPM（每分钟击键数）、准确率、剩余时间
- ✅ 支持 1/2/3/5 分钟四种测试时长
- ✅ 完整的用户注册 / 登录系统
- ✅ 历史测试记录保存
- ✅ 响应式设计，手机电脑都能用
- ✅ 免费 HTTPS 证书自动续期
- ✅ 部署在阿里云香港服务器，无需备案
技术栈
- 后端：Python Flask
- 数据库：SQLite（轻量，不用安装额外数据库）
- 前端：HTML + CSS + 原生 JavaScript（不用框架，简单易懂）
- Web 服务器：Nginx
- WSGI 服务器：Gunicorn
- SSL 证书：Let's Encrypt 免费证书
- 服务器：阿里云香港轻量应用服务器
本地开发环境搭建
1. 准备工作
你需要先在电脑上安装 Python 3.8 或更高版本，去 Python 官网下载就行：https://www.python.org/downloads/
安装的时候记得勾选 "Add Python to PATH"，不然在终端里用不了。
2. 下载项目代码
如果你已经把代码放到 GitHub 了，直接 clone 下来：
git clone https://github.com/你的用户名/typing-master.git
cd typing-master
或者直接下载 ZIP 压缩包，解压后进入文件夹。
3. 创建 Python 虚拟环境（推荐，避免依赖冲突）
Windows 系统：
python -m venv venv
venv\Scripts\activate
Mac/Linux 系统：
python3 -m venv venv
source venv/bin/activate
激活虚拟环境后，你的终端提示符前面会出现(venv)字样。
4. 安装项目依赖
pip install flask flask-sqlalchemy flask-login werkzeug
5. 运行项目
python app.py
然后打开浏览器，访问 http://localhost:5000
6. 本地测试
- 点击 "Register here" 注册一个账号
- 登录后测试打字功能
- 测试历史记录功能是否正常
部署到阿里云香港服务器（最详细的部分）
第一步：购买阿里云香港轻量应用服务器
1. 打开阿里云官网，搜索 "轻量应用服务器"
2. 点击 "立即购买"
3. 配置选择（严格按照这个选，不要选错）：
  - 地域：中国香港（不需要备案）
  - 实例规格：通用型
  - 套餐：1 核 2G 30G SSD 3M 带宽（完全够用，月费约 25 元）
  - 镜像：系统镜像 → Ubuntu 22.04 LTS 64 位（最稳定）
  - 购买时长：先买 1 个月试试
4. 完成支付，等待 2-3 分钟服务器创建完成
第二步：获取服务器信息
1. 进入阿里云轻量应用服务器控制台
2. 找到你刚买的服务器，记录下公网 IP 地址（比如：[47.242.xxx.xxx](47.242.xxx.xxx)）
3. 点击 "远程连接" → "设置密码"，设置一个 root 用户的密码
第三步：连接服务器
我推荐用 FinalShell，免费又好用：http://www.hostbuf.com/
1. 打开 FinalShell，点击左上角的 "新建连接"
2. 填写以下信息：
  - 名称：随便填
  - 主机：你的服务器公网 IP 地址
  - 端口：22
  - 用户名：root
  - 密码：刚才设置的 root 密码
3. 点击 "确定"，然后双击连接
4. 第一次连接会弹出 "主机密钥确认"，点击 "接受并保存"
如果连接成功，你会看到类似这样的界面：
Welcome to Ubuntu 22.04.4 LTS (GNU/Linux 5.15.0-107-generic x86_64)

root@iZwz9xxxxxxxxx:~#
第四步：服务器环境配置
在 FinalShell 的终端中，逐行执行以下命令，每执行完一行等待它完成再执行下一行。
1. 更新系统软件包
apt update && apt upgrade -y
2. 安装必要的软件
# 安装Python3、pip和虚拟环境
apt install python3 python3-pip python3-venv -y

# 安装Nginx（用于反向代理）
apt install nginx -y

# 安装Certbot（用于申请免费HTTPS证书）
apt install certbot python3-certbot-nginx -y
3. 验证安装是否成功
# 验证Python版本（应该显示3.10.x）
python3 --version

# 验证Nginx是否运行（应该显示active running）
systemctl status nginx
第五步：上传代码到服务器
1. 在 FinalShell 左侧，点击 "文件管理" 标签
2. 进入/var/www/目录（点击左侧的 var，再点击 www）
3. 把你本地电脑上的整个typing-master文件夹，直接拖拽到 FinalShell 的文件管理窗口中
4. 等待上传完成
上传完成后文件结构应该是：
/var/www/typing-master/
├── app.py
├── static/
│   └── style.css
└── templates/
    ├── index.html
    ├── login.html
    └── register.html
5. 设置文件夹权限（重要，不然后面会报错）
chmod -R 777 /var/www/typing-master
第六步：配置 Python 虚拟环境和依赖
# 进入项目文件夹
cd /var/www/typing-master

# 创建Python虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装项目依赖
pip install flask flask-sqlalchemy flask-login werkzeug gunicorn
安装完成后，你的终端提示符前面会出现(venv)字样。
第七步：配置 Gunicorn 系统服务（让网站后台运行）
Gunicorn 是一个生产级的 Python WSGI 服务器，比 Flask 自带的开发服务器稳定得多。
1. 创建服务文件
nano /etc/systemd/system/typing-master.service
2. 复制以下内容，粘贴进去（右键粘贴）
[Unit]
Description=Gunicorn instance to serve typing-master
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/typing-master
Environment="PATH=/var/www/typing-master/venv/bin"
ExecStart=/var/www/typing-master/venv/bin/gunicorn -w 1 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
3. 保存并退出
按Ctrl+O（字母 O），然后按Enter确认保存，最后按Ctrl+X退出 nano 编辑器。
4. 启动服务并设置开机自启
# 重新加载systemd配置
systemctl daemon-reload

# 启动服务
systemctl start typing-master

# 设置开机自启（服务器重启后网站自动启动）
systemctl enable typing-master

# 验证服务状态（应该显示active running）
systemctl status typing-master
如果显示active (running)，说明服务启动成功！
第八步：配置 Nginx 反向代理
Nginx 负责接收用户的 HTTP 请求，然后转发给 Gunicorn 处理，同时提供静态文件服务和 HTTPS 支持。
1. 删除 Nginx 默认配置
rm /etc/nginx/sites-enabled/default
2. 创建新的 Nginx 配置文件
nano /etc/nginx/sites-available/typing-master
3. 复制以下内容，粘贴进去（把 [shturl.cc/FxOHI](shturl.cc/FxOHI) 换成你自己的域名）
# HTTP自动重定向到HTTPS
server {
    listen 80;
    server_name shturl.cc/FxOHI www.shturl.cc/FxOHI;
    return 301 https://$host$request_uri;
}

# HTTPS主配置
server {
    listen 443 ssl;
    server_name shturl.cc/FxOHI www.shturl.cc/FxOHI;

    # SSL证书路径（Certbot自动生成的，不要改）
    ssl_certificate /etc/letsencrypt/live/shturl.cc/FxOHI/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/shturl.cc/FxOHI/privkey.pem;

    # SSL安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    # 反向代理到Gunicorn
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
4. 保存并退出
按Ctrl+O，Enter，Ctrl+X。
5. 创建软链接并测试配置
# 创建软链接到sites-enabled目录
ln -s /etc/nginx/sites-available/typing-master /etc/nginx/sites-enabled/

# 测试Nginx配置是否正确（应该显示test is successful）
nginx -t

# 重启Nginx
systemctl restart nginx
第九步：域名解析
1. 进入阿里云云解析 DNS 控制台
2. 找到你的域名，点击 "解析设置"
3. 点击 "添加记录"，添加以下两条记录：
记录类型
主机记录
记录值
TTL
A
@
你的服务器公网 IP 地址
10 分钟
A
www
你的服务器公网 IP 地址
10 分钟
- @记录：让用户直接输入shturl.cc/FxOHI就能访问
- www记录：让用户输入www.shturl.cc/FxOHI也能访问
解析通常需要 5-10 分钟生效，最长不超过 1 小时。
第十步：配置阿里云控制台防火墙（重要，别忘了这一步）
1. 进入阿里云轻量应用服务器控制台
2. 点击你的服务器 → 左侧 "防火墙"
3. 点击 "添加规则"，一次性添加以下 3 条规则：
协议
端口
策略
TCP
80
允许
TCP
443
允许
ICMP
全部
允许
4. 保存后，等待 1 分钟让规则生效
第十一步：申请并配置 HTTPS 证书（必做！现在浏览器都要求 HTTPS）
我们使用 Let's Encrypt 提供的免费 SSL 证书，有效期 90 天，自动续期。
1. 先停止 Nginx 服务（避免端口占用）
systemctl stop nginx
2. 使用 Certbot 独立模式申请证书（最稳定，不依赖 Nginx）
certbot certonly --standalone -d shturl.cc/FxOHI -d www.shturl.cc/FxOHI
3. 按照提示操作
1. 输入你的邮箱地址（用于证书到期提醒）
2. 输入Y同意服务条款
3. 输入N不接收广告邮件
4. 等待验证完成
成功后会显示：
Congratulations! Your certificate and chain have been saved at:
/etc/letsencrypt/live/shturl.cc/FxOHI/fullchain.pem
Your key file has been saved at:
/etc/letsencrypt/live/shturl.cc/FxOHI/privkey.pem
4. 启动 Nginx
systemctl start nginx
5. 验证自动续期
certbot renew --dry-run
如果显示 "Congratulations, all renewals succeeded"，说明自动续期配置成功，以后不用管了。
第十二步：验证部署成功
1. 打开浏览器，清除缓存（或者用无痕模式）
2. 输入你的域名：https://shturl.cc/FxOHI
3. 你应该能看到打字网站的登录页面
4. 检查浏览器地址栏左侧是否有小锁图标，说明 HTTPS 配置成功
🎉 恭喜，你的网站已经成功部署到服务器，可以访问了。

常见问题：
#1. 防火墙的问题
有两个防火墙层级，很多人只开了一个：
1. 阿里云控制台防火墙（必须开 80、443、ICMP）
2. 服务器内部的 ufw 防火墙（Ubuntu 默认开启，建议直接关闭）
关闭 ufw 防火墙的命令：
ufw disable
#2. 编码问题
Windows 系统下 Python 读取文件会有编码问题，我在 [app.py](app.py) 顶部加了这几行代码解决：
# -*- coding: utf-8 -*-
import _locale
_locale._getdefaultlocale = (lambda *args: ('zh_CN', 'utf-8'))
而且所有 HTML 文件都要确保是 UTF-8 编码保存的，不要用 GBK。
常见问题排查
网站打不开
1. 检查防火墙是否开放了 80 和 443 端口
2. 检查 Nginx 是否运行：systemctl status nginx
3. 检查 Gunicorn 是否运行：systemctl status typing-master
4. 检查域名解析是否正确：ping shturl.cc/FxOHI
502 Bad Gateway 错误
这是 Gunicorn 服务没有运行导致的，执行：
systemctl restart typing-master
无法注册或登录
这是数据库文件权限问题，执行：
chmod 777 /var/www/typing-master/typing.db
查看错误日志
# 查看Nginx错误日志
tail -f /var/log/nginx/error.log

# 查看Gunicorn错误日志
journalctl -u typing-master -f
后续可以添加的功能
- 排行榜系统
- 多种难度模式（加入数字、符号）
- 打字音效
- 打字成就系统
- 多人在线对战
- 打字数据分析和图表展示
写在最后
这是我第一个完整部署上线的全栈项目，从最开始的代码编写到最后的服务器部署，踩了无数的坑，但也学到了很多东西。希望这个详细的 README 能帮到你，让你少走一些弯路。
如果你觉得这个项目对你有帮助，欢迎给个 Star！有问题也可以提 Issue，我会尽量回复。
祝你用这个小网站练出超快的打字击键速度！
