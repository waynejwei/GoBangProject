"""
工厂类
"""
import abc


class Chess(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    @abc.abstractmethod  # 下面是抽象的对象方法
    def getType(self):
        pass

    @abc.abstractmethod
    def win(self, chess_type):
        pass