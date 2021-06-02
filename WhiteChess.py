"""
白棋
"""
from abc import ABC

from Chess import Chess


class WhiteChess(Chess, ABC):

    def __init__(self, x, y, subject):
        self.x = x
        self.y = y
        self.type = 2
        self.subject = subject
        self.subject.attach(self)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getType(self):
        return self.type

    def win(self, chess_type):
        if chess_type == self.getType():
            print('白棋：白棋获胜！')
        else:
            print('白棋：黑棋获胜！')
