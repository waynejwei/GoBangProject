"""
黑棋
"""
from abc import ABC

from Chess import Chess


class BlackChess(Chess, ABC):

    def __init__(self, x, y, subject):
        self.x = x
        self.y = y
        self.type = 1
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
            print('黑棋：黑棋获胜！')
        else:
            print('黑棋：白棋获胜！')
