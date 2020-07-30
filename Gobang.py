"""
Id: Gobang.py
ver 1.3.1
2020/07/30 23:05:27 David Li <david_ri@163.com>
"""


def change_shape(rounds) -> str:  # 返回值：(str)
    """
    更改棋子样式

    :param rounds: 当前回合数
    :return: 当前回合的棋子样式
    """
    print('ROUND:', rounds + 1)
    if rounds % 2 == 0:
        return cp_Player1
    else:
        return cp_Player2


def put_chess() -> (int, int):
    """
    获取用户输入的坐标

    :return: (X-coordinate, Y-coordinate)
    """
    go = input('输入坐标，格式例如F3\n%s Player>>' % chessShape)
    # 判断用户是否充钱
    if go == 'sudo win' and cheating:
        go = cheat()
    # 判断用户输入格式 必须行+列的形式 大小写随意
    while len(go) == 0 or \
            not go[0].isalpha() \
            or not go[1:].isdigit() \
            or not int(go[1:]) <= mapX \
            or not (65 <= ord(go[0]) <= 64 + mapY or 97 <= ord(go[0]) <= 96 + mapY):
        go = input('输入坐标，格式例如F3\n%s Player>>' % chessShape)
    return int(go[1:]) - 1, ord(go[0].upper()) - 65


def if_overlap(x, y) -> bool:  # 返回值：重叠 True/ 不重叠 False
    """
    If there already a chess.

    :param x: X-coordinate
    :param y: Y-coordinate
    """
    if pos[y][x] != '-':
        print('此坐标已有棋子，请仔细观察棋盘')
        return True
    return False


def chess_map():
    """ print the chess map """
    print('<>\t', end='')
    for i in range(1, mapX + 1):  # 打印列坐标
        print(i, end='\t')
    print()
    for i in range(mapY):  # 打印行坐标
        print(chr(65 + i), end='\t')
        for j in range(mapX):  # 打印每行的棋子
            print(pos[i][j], '\t', end='')
        print('')  # 换行


def judge(shape, x, y) -> bool:
    """
    判断胜负 最愚蠢的方法

    :param shape: Shape of the current chess
    :param x: X-coordinate of the current chess
    :param y: Y-coordinate of the current chess
    :return: True     if win,
             False    if not win yet
    """
    x_list = [1, 2, 3, 4]
    ll = rr = uu = dd = lu = ru = ld = rd = 0
    for i in x_list:  # ←
        if x - i >= 0 and pos[y][x - i] == shape:
            ll += 1
        else:
            break
    for i in x_list:  # →
        if x + i <= mapX - 1 and pos[y][x + i] == shape:
            rr += 1
        else:
            break
    for i in x_list:  # ↑
        if y - i >= 0 and pos[y - i][x] == shape:
            uu += 1
        else:
            break
    for i in x_list:  # ↓
        if y + i <= mapY - 1 and pos[y + i][x] == shape:
            dd += 1
        else:
            break
    for i in x_list:  # ↖
        if x - i >= 0 and y - 1 >= 0 and pos[y - i][x - i] == shape:
            lu += 1
        else:
            break
    for i in x_list:  # ↗
        if x + i <= mapX - 1 and y - 1 >= 0 and pos[y - i][x + i] == shape:
            ru += 1
        else:
            break
    for i in x_list:  # ↙
        if x - i >= 0 and y + 1 <= mapY - 1 and pos[y + i][x - i] == shape:
            ld += 1
        else:
            break
    for i in x_list:  # ↘
        if x + i <= mapX - 1 and y + 1 <= mapY - 1 and pos[y + i][x + i] == shape:
            rd += 1
        else:
            break
    if ll + rr == 4 or uu + dd == 4 or lu + rd == 4 or ld + ru == 4:
        chess_map()
        print('GAME FINISH\nPlayer %c is win' % shape)
        return True
    return False


def if_start() -> bool:
    """
    要不要再来一把

    :return: True     for continue,
             False    for finish
    """
    choice_dic = {'N': False, 'Y': True}
    while True:
        choice = choice_dic.get(input('Do you want to play again:').capitalize(), 'Invalid Input')
        if type(choice) == bool:
            return choice
        print(choice)


def cheat():
    """ 一键获胜 """
    global pos
    pos = [[chessShape] * mapX for _ in range(mapY)]
    pos[0][0] = '-'
    return 'A1'


if __name__ == '__main__':
    ''' 自定义 参数 '''
    mapX = 26  # 列 无限大
    mapY = 26  # 行 最大26 即'Z'
    cp_Player1 = 'X'  # 玩家1 棋子
    cp_Player2 = 'O'  # 玩家2 棋子
    cheating = True  # 是否开启“一键获胜”功能（是否充值）

    start = True  # 是否开始游戏

    if mapY > 26 or len(cp_Player1) != 1 or len(cp_Player2) != 1:
        print('游戏仿佛无法开始哦 Σ(っ °Д °;)っ\n请检查->自定义参数')
        start = False

    while start:
        pos = [['-'] * mapX for i in range(mapY)]  # 初始化棋盘
        for i in range(mapX * mapY):
            chessShape = change_shape(i)  # 更改棋子样式
            chess_map()  # 打印棋盘
            while True:
                pos_x, pos_y = put_chess()  # 获取用户输入的坐标
                if not if_overlap(pos_x, pos_y):  # 判断棋子是否重叠
                    break
            pos[pos_y][pos_x] = chessShape  # 把棋子填到对应坐标
            if judge(chessShape, pos_x, pos_y):  # 判断输赢
                break
        start = if_start()  # 要不要再来一把
