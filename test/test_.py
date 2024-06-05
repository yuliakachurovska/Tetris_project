import pytest
from tetris import Tetris, Piece
import tkinter as tk

"""
Кожен тест починається з фіктивної області MockCanvas, яка створюється для того, 
щоб імітувати клас Canvas з бібліотеки Tkinter. Потім визначаються фіктивні фікстури canvas і tetris,
які використовуються для передачі MockCanvas та об'єкта Tetris в кожен тест відповідно.
"""

class MockCanvas:
    def create_rectangle(self, *args, **kwargs):
        pass

    def create_line(self, *args, **kwargs):
        pass

    def delete(self, *args):
        pass

@pytest.fixture
def canvas():
    return MockCanvas()

@pytest.fixture
def tetris(canvas):
    return Tetris(canvas)

def test_tetris_initialization(tetris, canvas):
    assert tetris.score == 0
    assert tetris.canvas == canvas
    assert len(tetris.game_board) == 20
    assert all(len(row) == 10 for row in tetris.game_board)
    assert tetris.current_piece is not None
    assert not tetris.game_over
    assert tetris.game_running

def test_spawn_new_piece(tetris):
    tetris.spawn_new_piece()
    assert tetris.current_piece is not None

def test_move_piece_down(tetris):
    initial_y = tetris.current_piece.y
    tetris.move_piece_down()
    assert tetris.current_piece.y == initial_y + 1

def test_check_collision_with_bottom(tetris):
    tetris.current_piece.y = 19
    assert tetris.check_collision() == True

def test_lock_piece(tetris):
    tetris.current_piece.x = 0
    tetris.current_piece.y = 0
    tetris.lock_piece()
    assert tetris.game_board[0][0] == tetris.current_piece.color

def test_clear_lines(tetris):
    tetris.game_board[19] = [1] * 10  # Заповнюємо останню лінію
    tetris.clear_lines()
    assert tetris.score == 30
    assert all(cell == 0 for cell in tetris.game_board[19])

def test_rotate_piece():
    piece = Piece()
    original_shape = piece.shape
    rotated_shape = piece.rotate()
    assert len(original_shape) == len(rotated_shape[0])
    assert len(original_shape[0]) == len(rotated_shape)

def test_stop_game(tetris):
    tetris.stop_game()
    assert tetris.game_over
    assert not tetris.game_running

if __name__ == "__main__":
    pytest.main()
