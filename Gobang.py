"""
Id: Gobang.py
ver 1.3.2
2020/07/31 01:42:10 David Li <david_ri@163.com>
"""


class Gobang:
    """ 五子棋类 """

    __currentCS = None

    def __init__(self, map_x: int = 9, map_y: int = 9,
                 cp_player1: str = 'X', cp_player2: str = 'O', cheating: bool = True):
        """
        构造一盘五子棋

        :param map_x: 列 无限大
        :param map_y: 行 最大26 即'Z'
        :param cp_player1: 玩家1 棋子
        :param cp_player2: 玩家2 棋子
        :param cheating: 是否开启“一键获胜”功能（是否充值）
        """
        self.mapX = map_x
        self.mapY = map_y
        self.cpPlayer1 = cp_player1
        self.cpPlayer2 = cp_player2
        self.cheat_mode = cheating

        start = True  # 是否开始游戏

        if map_y > 26 or len(cp_player1) != 1 or len(cp_player2) != 1:
            print('游戏仿佛无法开始哦 Σ(っ °Д °;)っ\n请检查->自定义参数')
            start = False

        while start:
            self.pos = [['-'] * map_x for _ in range(map_y)]  # 初始化棋盘
            for i in range(map_x * map_y):
                self.change_shape(i)  # 更改棋子样式
                self.chess_map()  # 打印棋盘
                while True:
                    pos_x, pos_y = self.put_chess()  # 获取用户输入的坐标
                    if not self.if_overlap(pos_x, pos_y):  # 判断棋子是否重叠
                        break
                self.pos[pos_y][pos_x] = self.__currentCS  # 把棋子填到对应坐标
                if self.judge(pos_x, pos_y):  # 判断输赢
                    break
            start = self.if_start()  # 要不要再来一把

    def change_shape(self, rounds):
        """
        更改棋子样式

        :param rounds: 当前回合数
        :return: 当前回合的棋子样式
        """
        print('ROUND:', rounds + 1)
        if rounds % 2 == 0:
            self.__currentCS = self.cpPlayer1
        else:
            self.__currentCS = self.cpPlayer2

    def put_chess(self) -> (int, int):
        """
        获取用户输入的坐标

        :return: (X-coordinate, Y-coordinate)
        """
        go = input('输入坐标，格式例如F3\n%s Player>>' % self.__currentCS)
        # 判断用户是否充钱
        if go == 'sudo win' and self.cheat_mode:
            go = self.cheat()

        # 判断用户输入格式 必须行+列的形式 大小写随意
        while len(go) == 0 or \
                not go[0].isalpha() \
                or not go[1:].isdigit() \
                or not int(go[1:]) <= self.mapX \
                or not (65 <= ord(go[0]) <= 64 + self.mapY or 97 <= ord(go[0]) <= 96 + self.mapY):
            go = input('输入坐标，格式例如F3\n%s Player>>' % self.__currentCS)
        return int(go[1:]) - 1, ord(go[0].upper()) - 65

    def chess_map(self):
        """ print the chess map """
        print('<>\t', end='')
        for i in range(1, self.mapX + 1):  # 打印列坐标
            print(i, end='\t')
        print()
        for i in range(self.mapY):  # 打印行坐标
            print(chr(65 + i), end='\t')
            for j in range(self.mapX):  # 打印每行的棋子
                print(self.pos[i][j], '\t', end='')
            print('')  # 换行

    def judge(self, x, y) -> bool:
        """
        判断胜负 最愚蠢的方法

        :param x: X-coordinate of the current chess
        :param y: Y-coordinate of the current chess
        :return: True     if win,
                 False    if not win yet
        """
        x_list = [1, 2, 3, 4]
        ll = rr = uu = dd = lu = ru = ld = rd = 0
        for i in x_list:  # ←
            if x - i >= 0 and self.pos[y][x - i] == self.__currentCS:
                ll += 1
            else:
                break
        for i in x_list:  # →
            if x + i <= self.mapX - 1 and self.pos[y][x + i] == self.__currentCS:
                rr += 1
            else:
                break
        for i in x_list:  # ↑
            if y - i >= 0 and self.pos[y - i][x] == self.__currentCS:
                uu += 1
            else:
                break
        for i in x_list:  # ↓
            if y + i <= self.mapY - 1 and self.pos[y + i][x] == self.__currentCS:
                dd += 1
            else:
                break
        for i in x_list:  # ↖
            if x - i >= 0 and y - 1 >= 0 and self.pos[y - i][x - i] == self.__currentCS:
                lu += 1
            else:
                break
        for i in x_list:  # ↗
            if x + i <= self.mapX - 1 and y - 1 >= 0 and self.pos[y - i][x + i] == self.__currentCS:
                ru += 1
            else:
                break
        for i in x_list:  # ↙
            if x - i >= 0 and y + 1 <= self.mapY - 1 and self.pos[y + i][x - i] == self.__currentCS:
                ld += 1
            else:
                break
        for i in x_list:  # ↘
            if x + i <= self.mapX - 1 and y + 1 <= self.mapY - 1 and self.pos[y + i][x + i] == self.__currentCS:
                rd += 1
            else:
                break
        if ll + rr == 4 or uu + dd == 4 or lu + rd == 4 or ld + ru == 4:
            self.chess_map()
            print('GAME FINISH\nPlayer %c is win' % self.__currentCS)
            return True
        return False

    def if_overlap(self, x, y) -> bool:
        """
        If there already a chess.

        :param x: X-coordinate
        :param y: Y-coordinate
        """
        if self.pos[y][x] != '-':
            print('此坐标已有棋子，请仔细观察棋盘')
            return True
        return False

    @staticmethod
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

    def cheat(self):
        """ 一键获胜 """
        self.pos = [[self.__currentCS] * self.mapX for _ in range(self.mapY)]
        self.pos[0][0] = '-'
        return 'A1'


if __name__ == '__main__':
    Gobang()
