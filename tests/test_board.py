from game.board import Board


def test_board_init():
    b = Board(6, 7)
    assert b.rows == 6
    assert b.cols == 7
    assert all(cell == 0 for row in b.grid for cell in row)
    assert b.last_move is None


def test_drop():
    b = Board(4, 4)
    assert b.drop(1, 1) == 3
    assert b.grid[3][1] == 1
    assert b.drop(1, 2) == 2
    assert b.grid[2][1] == 2
    assert b.drop(1, 1) == 1
    assert b.grid[1][1] == 1
    assert b.drop(1, 2) == 0
    assert b.grid[0][1] == 2
    assert b.drop(1, 1) is None  # Column full
    assert b.drop(5, 1) is None  # Out of range


def test_win():
    ...
