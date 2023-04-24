from flask import Flask,render_template

# 创建flask应用
app = Flask(__name__)


# 创建路由
@app.route('/camera')
def get_lottery_image():   # 将摄像头拍照数据通过post方法传递给后端，后端执行解析，返回
    img = ''
    return img


@app.route('/result')
def check_lottery():   # 将识别后的数据传递给前段
    info = {
        'redball': '02,03,04,05,06,07',
        'blueball': '08'
    }
    return render_template('info.html', info=info)


if __name__ == '__main__':
    app.run(debug=True)

