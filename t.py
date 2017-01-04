#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Quarto
"""
from random import choice

EMPTY = -1

def to_str(i):
    if i == EMPTY:
        return '    '
    assert 0 <= i < 16
    return '{:04b}'.format(i)


HORIZONTAL_LINE = '\n' + '-' * (4 * 4 + 3) + '\n'
def print_board(board):
    print HORIZONTAL_LINE.join(
        '|'.join(to_str(x) for x in line)
        for line in board)


def piece_or_pos_id(board, x, y):
    v = board[y][x]
    if v != EMPTY:
        # piece exists
        return to_str(v)
    return '<{:2d}>'.format(y * 10 + x + 11)


def print_board_with_pos_id(board):
    print HORIZONTAL_LINE.join(
        '|'.join(
            piece_or_pos_id(board, x, y) for x in range(4)
        ) for y in range(4)
    )


class Player(object):
    def choose_piece(self, available):
        raise NotImplemented


    def choose_position(self, board):
        raise NotImplemented



class RandomPlayer(Player):
    def choose_piece(self, available):
        "given available pieces, choose one"
        #ret = choice(available)
        ret = available[0]
        available.remove(ret)
        print 'com choose> {}'.format(to_str(ret))
        return ret


    def choose_position(self, board):
        available_pos = [
            (x, y)
            for x in range(4) for y in range(4)
            if board[y][x] == EMPTY]
        ret = choice(available_pos)
        return ret



class HumanPlayer(Player):
    def choose_position(self, board):
        print_board_with_pos_id(board)
        pos = input("where to place?> ")
        x = (pos - 11) % 10
        y = (pos - 11) / 10
        return (x, y)


    def choose_piece(self, available):
        readable = map(to_str, available)
        print ', '.join(readable)
        while True:
            p = raw_input('which?> ')
            if p in readable: break
        i = readable.index(p)
        ret = available[i]
        available.remove(ret)
        return ret


def all_same(xs):
    return all(x == xs[0] for x in xs[1:])


def line_check(line):
    "return non-zero if the line is completed"
    if any(v == EMPTY for v in line): return None
    assert len(line) == 4
    buf = map(to_str, line)
    samebits = [all_same([buf[j][i] for j in range(4)]) for i in range(4)]
    if any(samebits):
        return ''.join(to_str(line[0])[i] if samebits[i] else '-' for i in range(4))


def status_check(board):
    for i in range(4):
        a = line_check(board[i])
        if a:
            print 'complete row {}: {}'.format(i + 1, a)
            return a
        a = line_check([board[j][i]for j in range(4)])
        if a:
            print 'complete col {}: {}'.format(i + 1, a)
            return a

    a = line_check([board[j][j]for j in range(4)])
    if a:
        print 'complete right-down: {}'.format(a)
        return a
    a = line_check([board[3 - j][j]for j in range(4)])
    if a:
        print 'complete right-up: {}'.format(a)
        return a


available = range(16)
board = [[EMPTY] * 4 for i in range(4)]
#players = [HumanPlayer(), RandomPlayer()]
players = [RandomPlayer(), RandomPlayer()]
turn = 0
while True:
    player = players[turn % 2]
    p = player.choose_piece(available)

    player = players[(turn + 1) % 2]
    x, y = player.choose_position(board)
    board[y][x] = p
    print_board(board)
    if status_check(board):
        print "WIN"
        break
    if not available:
        print "DRAW"
        break

    turn += 1
