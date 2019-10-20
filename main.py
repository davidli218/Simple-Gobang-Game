"""
Id: simple gobang game.py
ver 1.3.0
2019/09/15 21:56:18 David Li
"""


# 更改棋子样式
def ChangeShape(rounds):  # 返回值：(str)棋子样式
    print('ROUND:', rounds + 1)
    if rounds % 2 == 0:
        return cp_Player1
    else:
        return cp_Player2


# 获取用户输入的坐标
def PutGo():  # 返回值：横坐标x，纵坐标y
    go = input('输入坐标，格式例如F3\n%s Player>>' % chessShape)
    # 判断用户是否充钱
    if go == 'sudo win' and cheat:
        go = Cheat()
    # 判断用户输入格式 必须行+列的形式 大小写随意
    while len(go) == 0 or \
            not go[0].isalpha() \
            or not go[1:].isdigit() \
            or not int(go[1:]) <= mapX \
            or not (65 <= ord(go[0]) <= 64 + mapY or 97 <= ord(go[0]) <= 96 + mapY):
        go = input('输入坐标，格式例如F3\n%s Player>>' % chessShape)
    return int(go[1:]) - 1, ord(go[0].upper()) - 65


# 检测棋子是否重叠
def IfOverlap(x, y):  # 返回值：重叠 True/ 不重叠 False
    if pos[y][x] != '-':
        print('此坐标已有棋子，请仔细观察棋盘')
        return True
    return False


# 打印棋盘
def ChessMap():
    print('<>\t', end='')
    for i in range(1, mapX + 1):  # 打印列坐标
        print(i, end='\t')
    print()
    for i in range(mapY):  # 打印行坐标
        print(chr(65 + i), end='\t')
        for j in range(mapX):  # 打印每行的棋子
            print(pos[i][j], '\t', end='')
        print('')  # 换行


# 判断胜负 最愚蠢的方法
def Judge(shape, x, y):  # 返回值：赢 True/ 未结束 False
    xlist = [1, 2, 3, 4]
    LL = RR = UU = DD = LU = RU = LD = RD = 0
    for i in xlist:  # ←
        if x - i >= 0 and pos[y][x - i] == shape:
            LL += 1
        else:
            break
    for i in xlist:  # →
        if x + i <= mapX - 1 and pos[y][x + i] == shape:
            RR += 1
        else:
            break
    for i in xlist:  # ↑
        if y - i >= 0 and pos[y - i][x] == shape:
            UU += 1
        else:
            break
    for i in xlist:  # ↓
        if y + i <= mapY - 1 and pos[y + i][x] == shape:
            DD += 1
        else:
            break
    for i in xlist:  # ↖
        if x - i >= 0 and y - 1 >= 0 and pos[y - i][x - i] == shape:
            LU += 1
        else:
            break
    for i in xlist:  # ↗
        if x + i <= mapX - 1 and y - 1 >= 0 and pos[y - i][x + i] == shape:
            RU += 1
        else:
            break
    for i in xlist:  # ↙
        if x - i >= 0 and y + 1 <= mapY - 1 and pos[y + i][x - i] == shape:
            LD += 1
        else:
            break
    for i in xlist:  # ↘
        if x + i <= mapX - 1 and y + 1 <= mapY - 1 and pos[y + i][x + i] == shape:
            RD += 1
        else:
            break
    if LL + RR == 4 or UU + DD == 4 or LU + RD == 4 or LD + RU == 4:
        ChessMap()
        print('GAME FINISH\nPlayer %c is win' % shape)
        return True
    return False


# 要不要再来一把
def IfStart():  # 返回值：来 True/ 不来了 False
    choice_dic = {'N': False, 'Y': True}
    while True:
        choice = choice_dic.get(input('Do you want to play again:').capitalize(), 'Invalid Input')
        if type(choice) == bool:
            return choice
        print(choice)


# 一键获胜
def Cheat():
    global pos
    pos = [[chessShape] * mapX for i in range(mapY)]
    pos[0][0] = '-'
    return 'A1'


'''main初始化'''
mapX = 26  # 列 自定义 无限大
mapY = 26  # 行 自定义 最大26 即'Z'
cp_Player1 = 'X'  # 自定义
cp_Player2 = 'O'  # 自定义
cheat = True  # 是否开启“一键获胜”功能（是否充值）
start = True  # 是否开始游戏
'''main验证'''
if mapY > 26 or len(cp_Player1) != 1 or len(cp_Player2) != 1:
    print('游戏仿佛无法开始哦 Σ(っ °Д °;)っ\n请检查->自定义参数')
    start = False
'''main开始'''
while start:
    pos = [['-'] * mapX for i in range(mapY)]  # 初始化棋盘
    for i in range(mapX * mapY):
        chessShape = ChangeShape(i)  # 更改棋子样式
        ChessMap()  # 打印棋盘
        while True:
            pos_x, pos_y = PutGo()  # 获取用户输入的坐标
            if not IfOverlap(pos_x, pos_y):  # 判断棋子是否重叠
                break
        pos[pos_y][pos_x] = chessShape  # 把棋子填到对应坐标
        if Judge(chessShape, pos_x, pos_y):  # 判断输赢
            break
    start = IfStart()  # 要不要再来一把
