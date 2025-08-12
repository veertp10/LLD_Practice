from collections import deque
from enum import Enum

class PieceType(Enum):
    X = 1
    O = 2

class PlayingPiece:
    def __init__(self, piece_type):
        self.piece_type = piece_type

class PlayingPieceX(PlayingPiece):
    def __init__(self):
        super().__init__(PieceType.X)

class PlayingPieceO(PlayingPiece):
    def __init__(self):
        super().__init__(PieceType.O)

class Player:
    def __init__(self, name, playing_piece):
        self.name = name
        self.playing_piece = playing_piece

class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]

    def add_piece(self, row, column, playing_piece):
        if self.board[row][column] is not None:
            return False
        self.board[row][column] = playing_piece
        return True

    def get_free_cells(self):
        free_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is None:
                    free_cells.append((i, j))
        return free_cells

    def print_board(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is not None:
                    print(self.board[i][j].piece_type.name, end="   ")
                else:
                    print("    ", end="")
                print(" | ", end="")
            print()

class TicTacToeGame:
    def __init__(self):
        self.players = deque()
        self.game_board = None
    
    def initialize_game(self):
        player1 = Player("Player1", PlayingPieceX())
        player2 = Player("Player2", PlayingPieceO())
        
        self.players.append(player1)
        self.players.append(player2)
        
        self.game_board = Board(3)

    def start_game(self):
        while True:
            player_turn = self.players.popleft()
            
            self.game_board.print_board()
            
            free_spaces = self.game_board.get_free_cells()
            if not free_spaces:
                return "tie"
            
            print(f"Player: {player_turn.name} Enter row,column: ", end="")
            try:
                user_input = input()
                if not user_input:
                    print("Invalid input, please try again.")
                    self.players.appendleft(player_turn)
                    continue
                values = user_input.split(',')
                if len(values) != 2:
                    print("Invalid input format, please enter 'row,column'.")
                    self.players.appendleft(player_turn)
                    continue
                input_row = int(values[0].strip())
                input_column = int(values[1].strip())
            except (ValueError, IndexError):
                print("Incorrect input, please enter valid integers for row and column.")
                self.players.appendleft(player_turn)
                continue
            
            if not (0 <= input_row < self.game_board.size and 0 <= input_column < self.game_board.size):
                print("Incorrect position chosen, try again. Row and column must be within the board size.")
                self.players.appendleft(player_turn)
                continue

            piece_added_successfully = self.game_board.add_piece(input_row, input_column, player_turn.playing_piece)
            
            if not piece_added_successfully:
                print("Incorrect position chosen, try again. The cell is already occupied.")
                self.players.appendleft(player_turn)
                continue
            
            self.players.append(player_turn)
            
            if self.is_there_winner(input_row, input_column, player_turn.playing_piece.piece_type):
                return player_turn.name

    def is_there_winner(self, row, column, piece_type):
        row_match = all(self.game_board.board[row][i] and self.game_board.board[row][i].piece_type == piece_type for i in range(self.game_board.size))
        
        column_match = all(self.game_board.board[i][column] and self.game_board.board[i][column].piece_type == piece_type for i in range(self.game_board.size))
        
        diagonal_match = all(self.game_board.board[i][i] and self.game_board.board[i][i].piece_type == piece_type for i in range(self.game_board.size))
        
        anti_diagonal_match = all(self.game_board.board[i][self.game_board.size - 1 - i] and self.game_board.board[i][self.game_board.size - 1 - i].piece_type == piece_type for i in range(self.game_board.size))

        return row_match or column_match or diagonal_match or anti_diagonal_match

if __name__ == "__main__":
    game = TicTacToeGame()
    game.initialize_game()
    print("game winner is:", game.start_game())