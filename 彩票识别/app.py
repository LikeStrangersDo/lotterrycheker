from flask import Flask

# 创建flask应用
app = Flask(__name__)


# 创建路由
@app.route('/')
def get_lottery_image():
    pass


@app.route('/')
def check_lottery():
    pass


@app.route('/1')
def res_lottery():
    pass

