# -*- coding: utf-8 -*-
# 强制修复Windows系统默认编码问题，防止读取文件乱码
import _locale
_locale._getdefaultlocale = (lambda *args: ('zh_CN', 'utf-8'))

# 导入Flask框架核心模块，用于创建Web应用
from flask import Flask, render_template, request, jsonify, redirect, url_for
# 导入SQLAlchemy，用于操作SQLite数据库
from flask_sqlalchemy import SQLAlchemy
# 导入Flask-Login，用于处理用户登录会话管理
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# 导入Werkzeug密码工具，用于安全存储和验证密码（不存明文）
from werkzeug.security import generate_password_hash, check_password_hash
# 导入datetime，用于记录测试的时间戳
from datetime import datetime
# 导入系统模块，用于进一步修复Windows控制台输出乱码
import sys
import io

# ==================== Windows控制台编码二次修复 ====================
# 仅在Windows系统下执行，强制标准输出和错误输出为UTF-8
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ==================== Flask应用初始化 ====================
# 创建Flask应用实例，显式指定模板文件夹路径
app = Flask(__name__, template_folder='templates')
# 设置应用密钥，用于加密session和cookie（生产环境请替换为复杂随机字符串）
app.config['SECRET_KEY'] = 'your_secure_random_secret_key_here_change_in_production'
# 配置SQLite数据库URI，数据库文件名为typing.db，存放在项目根目录
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///typing.db'
# 关闭SQLAlchemy的对象修改追踪功能，减少内存占用
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ==================== 数据库对象初始化 ====================
# 创建SQLAlchemy数据库操作对象，绑定到Flask应用
db = SQLAlchemy(app)
# 创建Flask-Login登录管理器对象
login_manager = LoginManager()
# 将登录管理器绑定到Flask应用
login_manager.init_app(app)
# 设置未登录用户访问受保护页面时的跳转路由
login_manager.login_view = 'login'

# ==================== 数据库模型定义 ====================
# 用户模型：继承UserMixin（提供默认的用户认证方法）和db.Model（数据库基类）
class User(UserMixin, db.Model):
    # 定义主键id：整数类型，自增
    id = db.Column(db.Integer, primary_key=True)
    # 定义用户名字段：字符串类型，最大长度80，唯一，不能为空
    username = db.Column(db.String(80), unique=True, nullable=False)
    # 定义密码哈希字段：字符串类型，最大长度128，不能为空（不存明文密码）
    password_hash = db.Column(db.String(128), nullable=False)
    # 定义与测试记录的一对多关系：一个用户可以有多条测试记录
    records = db.relationship('Record', backref='user', lazy=True)

    # 定义设置密码的方法：将明文密码转换为哈希值存储
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 定义验证密码的方法：比较输入的明文密码和存储的哈希值
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 测试记录模型：继承db.Model
class Record(db.Model):
    # 定义主键id：整数类型，自增
    id = db.Column(db.Integer, primary_key=True)
    # 定义WPM字段：整数类型，每分钟击键数，不能为空
    wpm = db.Column(db.Integer, nullable=False)
    # 定义准确率字段：浮点数类型，0-100之间，不能为空
    accuracy = db.Column(db.Float, nullable=False)
    # 定义测试时长字段：整数类型，单位秒，不能为空
    duration = db.Column(db.Integer, nullable=False)
    # 定义测试时间戳字段：日期时间类型，默认值为当前UTC时间
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # 定义用户ID外键字段：关联到用户表的id，不能为空
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# ==================== Flask-Login用户加载回调 ====================
# 定义用户加载函数：Flask-Login会用这个函数从数据库加载用户对象
@login_manager.user_loader
def load_user(user_id):
    # 根据用户ID（转换为整数）查询并返回用户对象
    return User.query.get(int(user_id))

# ==================== 创建数据库表 ====================
# 使用Flask应用上下文创建所有定义的模型对应的数据库表
with app.app_context():
    db.create_all()

# ==================== 路由定义 ====================
# 定义首页路由：仅允许GET请求，需要登录才能访问
@app.route('/')
@login_required
def index():
    # 渲染index.html模板并返回给浏览器
    return render_template('index.html')

# 定义登录路由：允许GET和POST请求
@app.route('/login', methods=['GET', 'POST'])
def login():
    # 如果是POST请求（用户提交了登录表单）
    if request.method == 'POST':
        # 从表单数据中获取用户名
        username = request.form['username']
        # 从表单数据中获取密码
        password = request.form['password']
        # 根据用户名查询数据库中的用户对象
        user = User.query.filter_by(username=username).first()
        
        # 如果用户存在且密码验证通过
        if user and user.check_password(password):
            # 登录用户，创建用户会话
            login_user(user)
            # 重定向到首页
            return redirect(url_for('index'))
        # 如果登录失败，重新渲染登录页并传递错误信息
        return render_template('login.html', error='Invalid username or password')
    
    # 如果是GET请求，直接渲染登录页
    return render_template('login.html')

# 定义注册路由：允许GET和POST请求
@app.route('/register', methods=['GET', 'POST'])
def register():
    # 如果是POST请求（用户提交了注册表单）
    if request.method == 'POST':
        # 从表单数据中获取用户名
        username = request.form['username']
        # 从表单数据中获取密码
        password = request.form['password']
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            # 如果用户名已存在，重新渲染注册页并传递错误信息
            return render_template('register.html', error='Username already exists')
        
        # 创建新的用户对象
        user = User(username=username)
        # 设置用户密码（自动转换为哈希值）
        user.set_password(password)
        # 将新用户添加到数据库会话
        db.session.add(user)
        # 提交数据库会话，将数据保存到数据库
        db.session.commit()
        
        # 注册成功，重定向到登录页
        return redirect(url_for('login'))
    
    # 如果是GET请求，直接渲染注册页
    return render_template('register.html')

# 定义登出路由：仅允许GET请求，需要登录才能访问
@app.route('/logout')
@login_required
def logout():
    # 登出用户，清除用户会话
    logout_user()
    # 重定向到登录页
    return redirect(url_for('login'))

# 定义保存测试记录的API路由：仅允许POST请求，需要登录才能访问
@app.route('/api/save-record', methods=['POST'])
@login_required
def save_record():
    # 从请求中获取JSON格式的数据
    data = request.get_json()
    # 创建新的测试记录对象
    record = Record(
        wpm=data['wpm'],              # 从JSON数据中获取WPM
        accuracy=data['accuracy'],    # 从JSON数据中获取准确率
        duration=data['duration'],    # 从JSON数据中获取测试时长
        user_id=current_user.id       # 获取当前登录用户的ID
    )
    # 将测试记录添加到数据库会话
    db.session.add(record)
    # 提交数据库会话，将数据保存到数据库
    db.session.commit()
    # 返回JSON格式的成功响应
    return jsonify({'success': True})

# 定义获取历史记录的API路由：仅允许GET请求，需要登录才能访问
@app.route('/api/get-history')
@login_required
def get_history():
    # 查询当前用户的最近10条测试记录，按时间戳倒序排列
    records = Record.query.filter_by(user_id=current_user.id).order_by(Record.timestamp.desc()).limit(10).all()
    # 将记录列表转换为JSON格式并返回
    return jsonify([{
        'wpm': r.wpm,                                    # WPM
        'accuracy': round(r.accuracy, 2),               # 准确率（保留2位小数）
        'duration': r.duration,                          # 测试时长
        'timestamp': r.timestamp.strftime('%Y-%m-%d %H:%M')  # 格式化时间戳为可读字符串
    } for r in records])

# ==================== 应用启动 ====================
# 如果是直接运行这个脚本（而不是被其他脚本导入）
if __name__ == '__main__':
    # 启动Flask开发服务器，开启调试模式（生产环境请关闭debug）
    app.run(debug=True)