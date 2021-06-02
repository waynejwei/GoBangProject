"""
观察者类，当某一棋子获胜时，通知
"""


class Subject(object):
    _instance = None

    def __new__(cls, *args, **kw):   # 实现单例模式
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self.chess_list = []

    def attach(self, chess):   # 添加观察者
        self.chess_list.append(chess)

    def setWiner(self, chess):   # 设置获胜方
        self.winNotify(chess.getType())

    def winNotify(self, chess_type):    # 通知每一种棋子获胜方
        for chess in self.chess_list:
            chess.win(chess_type)
