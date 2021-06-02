from flask import Flask
from flask import render_template
from flask import request
import pymysql
from WhiteChess import WhiteChess
from BlackChess import BlackChess
from Subject import Subject
import AudioLocation

app = Flask(__name__)
chessData = [[0 for i in range(15)] for i in range(15)]

try:
    conn = pymysql.connect(host='127.0.0.1', user='root', password='waynejwei464231',
                           database='gobang')
except ConnectionError:
    print('数据库连接失败')


@app.route('/h')
def hello_world():
    return 'Hello World!'


@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    print(username)
    print(password)
    cursor = conn.cursor()
    sql = 'select password from User where username = %s;'
    row = cursor.execute(sql, [username])
    if row == 1:
        pwd = cursor.fetchone()[0]  # cursor.fetch获取的是一个元组
        print(pwd)
        if pwd == password:
            # 如果登录成功则跳转至主页面
            return "true"
        else:
            return "false"
    else:
        # 如果登录失败则跳转到注册页面
        return "false"


@app.route('/register1', methods=['POST', 'GET'])
def register():
    return render_template('register.html')


@app.route('/register2', methods=['POST', 'GET'])
def register_post():
    username = request.form['username'].strip()
    password = request.form['password'].strip()
    cursor = conn.cursor()
    sql = 'select * from User where username = %s;'
    row = cursor.execute(sql, [username])
    if row == 0:
        sql = 'insert into User (username, password) values (%s, %s);'
        row = cursor.execute(sql, [username, password])
        conn.commit()
        if row == 1:
            print('插入成功')
            return "true"
        else:
            print('插入失败')
            return "fail"
    else:
        print('该用户名已被使用')
        return "false"


@app.route('/gobang', methods=['POST', 'GET'])
def gobang():
    try:
        chess_type_str = request.form['chess_type']
        if chess_type_str == 'true':
            chess_type = True
        else:
            chess_type = False
        x = int(request.form['x'])
        y = int(request.form['y'])
    except TypeError:
        return 0
    subject = Subject()
    print(id(subject))
    if chess_type:
        chess = BlackChess(x, y, subject)
    else:
        chess = WhiteChess(x, y, subject)
    chessData[chess.getY()][chess.getX()] = chess.getType()
    result = judge(chess.getY(), chess.getX(), chess.getType())
    return str(result)


def judge(x, y, chess):  # 判断该局棋盘是否赢了
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0

    # 左右判断
    for i in range(x, -1, -1):
        if chessData[i][y] != chess:
            break
        count1 = count1 + 1
    for i in range(x + 1, 15):
        if chessData[i][y] != chess:
            break
        count1 = count1 + 1
    # 上下判断
    for i in range(y, -1, -1):
        if chessData[x][i] != chess:
            break
        count2 = count2 + 1
    for i in range(y + 1, 15):
        if chessData[x][i] != chess:
            break
        count2 = count2 + 1
    # 左上右下判断
    j = y
    for i, j in zip(range(x, -1, -1), range(y, -1, -1)):
        if chessData[i][j] != chess:
            break
        count3 = count3 + 1
    for i, j in zip(range(x + 1, 15), range(y + 1, 15)):
        if chessData[i][j] != chess:
            break
        count3 = count3 + 1
    # 右上左下判断
    for i, j in zip(range(x, -1, -1), range(y, 15)):
        if chessData[i][j] != chess:
            break
        count4 = count4 + 1
    for i, j in zip(range(x + 1, 15), range(y - 1, -1, -1)):
        if chessData[i][j] != chess:
            break
        count4 = count4 + 1

    if count1 >= 5 or count2 >= 5 or count3 >= 5 or count4 >= 5:
        subject = Subject()
        blackChess = BlackChess(0, 0, subject)
        whiteChess = WhiteChess(0, 0, subject)
        if chess == 1:
            subject.setWiner(blackChess)
            return 1  # 黑棋赢了
        else:
            subject.setWiner(whiteChess)
            return 2  # 白棋赢了
    return 0  # 都没有赢


@app.route('/reset', methods=['POST', 'GET'])
def reset():
    global chessData
    chessData = [[0 for i in range(15)] for i in range(15)]
    for i in chessData:
        print(i)
    return "true"


@app.route('/backChess', methods=['POST', 'GET'])
def backChess():
    try:
        chess_type_str = request.form['chess_type']
        if chess_type_str == 'true':
            chess_type = True
        else:
            chess_type = False
        x = int(request.form['x'])
        y = int(request.form['y'])
    except TypeError:
        return 0
    subject = Subject()
    if chess_type:
        chess = BlackChess(x, y, subject)
    else:
        chess = WhiteChess(x, y, subject)
    chessData[chess.getY()][chess.getX()] = 0  # 归还原来的状态
    return "true"


@app.route('/go', methods=['POST', 'GET'])
def go():
    return render_template('go.html')


@app.route('/my_gobang', methods=['POST', 'GET'])
def myGo():
    return render_template('my_gobang.html')


@app.route('/audio', methods=['POST', 'GET'])
def audio():
    location = AudioLocation.getLocation()
    print(location)
    lie = ''
    hang = location[0]
    for i in range(len(location) - 1):
        if i != 0:
            lie = lie + location[i]
    print(hang)
    print(lie)
    try:
        x = ord(hang) - 65
        y = int(lie)
        print(x)
        print(y)
    except ValueError or AttributeError or TypeError:
        return {
            "x": 0,
            "y": 0,
            "msg": False
        }
    if 0 <= x <= 14 and 1 <= y <= 15:
        return {
            "x": x,
            "y": y - 1,  # 从0开始
            "msg": True
        }
    else:
        return {
            "x": 0,
            "y": 0,
            "msg": False
        }


if __name__ == '__main__':
    app.run()
