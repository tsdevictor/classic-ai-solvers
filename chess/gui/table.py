from gui.game_history_panel import *
from gui.taken_pieces_panel import *
from gui.game_setup import *
# from engine.players.ai.minimax import *
from engine.players.ai.opener_minimax import *
from PIL import ImageTk, Image
import os

PATH = os.path.dirname(__file__)

class Table:
    WHITE = [255, 206, 158]
    BLACK = [209, 139, 71]
    GRAY = [105, 113, 125]
    FONT_BLACK = [0, 0, 0]

    highlight_legal_moves = False

    chess_board = None

    source_tile = None
    destination_tile = None
    moved_piece = None

    game_frame = None
    board_panel = None
    taken_pieces_panel = None
    game_history_panel = None
    move_log = None

    white_player_type = None
    black_player_type = None
    search_depth = 1

    popup = None

    computer_move = None

    def __init__(self):
        import engine.board.board
        Table.chess_board = engine.board.board.Board.create_standard_board()

        import time
        start_time = time.process_time()
        for i in range(100000):
            for piece in self.chess_board.white_pieces:
                piece.calculate_moves(self.chess_board)
        print(time.process_time() - start_time)

        Table.game_frame = Tk()
        Table.game_frame.title('Chess')
        Table.game_frame.geometry('610x430')  # width x height
        Table.game_frame.iconbitmap(os.path.join(PATH, 'icon.ico'))
        Table.game_frame.grid_propagate(False)

        menu_bar = Menu(Table.game_frame, bd=0)
        Table.game_frame.config(menu=self.create_menu_bar(menu_bar), padx=0, pady=0)

        Table.taken_pieces_panel = TakenPiecesPanel(master=Table.game_frame, bd=0, width=50)
        Table.taken_pieces_panel.pack(side=LEFT)
        Table.board_panel = Table.BoardPanel(master=Table.game_frame, bd=5)
        Table.board_panel.pack(side=LEFT)
        Table.game_history_panel = GameHistoryPanel(master=Table.game_frame, bd=0)
        Table.game_history_panel.pack(side=LEFT)

        Table.move_log = Table.MoveLog()

        Table.game_frame.mainloop()

    def create_menu_bar(self, menu_bar: Menu) -> Menu:
        file_menu = Menu(menu_bar, tearoff=False)
        file_menu.add_command(label='Load PGN File', command=self.open_pgn_file)
        file_menu.add_command(label='Exit', command=Table.game_frame.destroy)
        menu_bar.add_cascade(label='File', menu=file_menu)

        preferences_menu = Menu(menu_bar, tearoff=False)
        preferences_menu.add_command(label='Flip Board', command=self.flip_board)
        preferences_menu.add_checkbutton(label='Highlight Legal Moves', onvalue=1, offvalue=0,
                                         command=self.change_highlight_choice)
        menu_bar.add_cascade(label='Preferences', menu=preferences_menu)

        options_menu = Menu(menu_bar, tearoff=False)
        options_menu.add_command(label='Set up game', command=self.show_options_popup)
        menu_bar.add_cascade(label='Options', menu=options_menu)

        return menu_bar

    @staticmethod
    def ai_move():
        if Table.is_ai(Table.chess_board.current_player) and \
                not Table.chess_board.current_player.is_in_checkmate() and \
                not Table.chess_board.current_player.is_in_stalemate():
            # minimax = Minimax(Table.search_depth)
            minimax = OpenerMinimax(Table.search_depth)
            # Table.computer_move = minimax.execute(Table.chess_board)
            Table.computer_move = minimax.execute(Table.chess_board,
                                                  Table.move_log.moves[-1] if len(Table.move_log.moves) > 0 else None,
                                                  len(Table.move_log.moves))
            Table.update_board(Table.chess_board.current_player.make_move(Table.computer_move).get_transition_board(), Table.computer_move)

        if Table.chess_board.current_player.is_in_checkmate():
            popup = Toplevel(Table.game_frame)
            popup.geometry('240x40')
            popup.title('Game Over')
            popup.iconbitmap(os.path.join(PATH, 'icon.ico'))
            Label(popup, text=str(Table.chess_board.current_player) + ' is in checkmate!',
                  borderwidth=0, highlightthickness=0).pack()
        elif Table.chess_board.current_player.is_in_stalemate():
            popup = Toplevel(Table.game_frame)
            popup.geometry('240x40')
            popup.title('Game Over')
            popup.iconbitmap(os.path.join(PATH, 'icon.ico'))
            Label(popup, text=str(Table.chess_board.current_player) + ' is in stalemate!',
                  borderwidth=0, highlightthickness=0).pack()

    @staticmethod
    def update_board(new_board, move=None):
        Table.chess_board = new_board
        if move is not None:
            Table.move_log.add_move(move)
            Table.game_history_panel.redo(Table.chess_board, Table.move_log)
            Table.taken_pieces_panel.redo(Table.move_log)
            Table.move_made_update(Table.PlayerType.COMPUTER)
        Table.board_panel.draw_board()

        Table.game_frame.update()

        Table.ai_move()

    @staticmethod
    def move_made_update(player_type: int):
        pass

    @staticmethod
    def is_ai(player):
        if Table.white_player_type is None or Table.black_player_type is None:
            return False
        if player.is_white and Table.white_player_type.is_ai():
            return True
        if player.is_black and Table.black_player_type.is_ai():
            return True
        return False

    @staticmethod
    def show_options_popup():
        Table.popup = GameSetup()

    @staticmethod
    def flip_board():
        Table.board_panel.reverse()

    @staticmethod
    def open_pgn_file():
        print("open up that pgn file!")

    @staticmethod
    def change_highlight_choice():
        Table.highlight_legal_moves = not Table.highlight_legal_moves
        Table.board_panel.draw_board()

    class BoardPanel(Frame):
        DARK_COLOR = '#d18b47'
        LIGHT_COLOR = '#ffce9e'

        def __init__(self, master=None, cnf=None, **kw):
            if cnf is None:
                cnf = {}
            super().__init__(master, cnf, **kw)
            self.board_tiles = []
            for r in range(8):
                for c in range(8):
                    tile_panel = Table.TilePanel(r, c, self, width=50, height=50, bd=0,
                                                 bg=self.LIGHT_COLOR if r % 2 == c % 2 else self.DARK_COLOR)
                    self.board_tiles.append(tile_panel)
                    tile_panel.bind("<Button-1>", tile_panel.left_mouse_event)
                    tile_panel.bind("<Button-3>", tile_panel.right_mouse_event)
                    tile_panel.grid(row=r, column=c)

        def draw_board(self):
            for tile_panel in self.board_tiles:
                tile_panel.draw_tile(Table.chess_board)

        def reverse(self):
            self.board_tiles.reverse()
            for r in range(8):
                for c in range(8):
                    self.board_tiles[r * 8 + c].grid(row=r, column=c)

        def remove_highlight(self):
            for tile_panel in self.board_tiles:
                tile_panel.highlight_legal_moves(Table.chess_board, None)

    class TilePanel(Frame):
        PIECE_ICON_PATH = os.path.join(PATH, 'images/')
        GRAY = '#808080'

        def __init__(self, r, c, master=None, cnf=None, **kw):
            if cnf is None:
                cnf = {}
            super().__init__(master, cnf, **kw)
            self.row = r
            self.col = c
            self.color = self.cget('bg')
            self.label = None
            self.draw_tile(Table.chess_board)
            self.image_path = ''

        def draw_tile(self, board):
            r = self.row
            c = self.col
            for widget in self.winfo_children():
                widget.destroy()

            self.highlight_legal_moves(board, Table.moved_piece)

            if board[r][c].is_occupied():
                self.image_path = self.PIECE_ICON_PATH + ('W' if board[r][c].piece.is_white else 'B') + str(
                    board[r][c].piece) + '.png'
                photo = ImageTk.PhotoImage(Image.open(self.image_path).resize((50, 50), Image.Resampling.LANCZOS))

                self.label = Label(self, image=photo, bg=self.cget('bg'), borderwidth=0, highlightthickness=0)
                self.label.image = photo
                self.label.bind("<Button-1>", self.left_mouse_event)
                self.label.bind("<Button-3>", self.right_mouse_event)
                self.label.pack()

        def highlight_legal_moves(self, board, moved_piece):
            if Table.highlight_legal_moves:
                if moved_piece is not None:
                    if moved_piece.same_color(board.current_player):
                        legal_moves = moved_piece.calculate_moves(board)
                        for move in legal_moves:
                            if move.target.row == self.row and move.target.col == self.col:
                                self.config(bg='gray')
                    else:
                        self.config(bg=self.color)
                else:
                    self.config(bg=self.color)
            else:
                self.config(bg=self.color)

        @staticmethod
        def right_mouse_event(event):
            Table.source_tile = None
            Table.destination_tile = None
            Table.moved_piece = None

        def left_mouse_event(self, event):
            import engine.move.move

            if Table.source_tile is None:  # first click
                Table.source_tile = Table.chess_board[self.row][self.col]
                if Table.source_tile.is_empty():
                    Table.source_tile = None
                else:
                    Table.moved_piece = Table.source_tile.piece
            else:  # second click
                Table.destination_tile = Table.chess_board[self.row][self.col]
                move = engine.move.move.MoveFactory.create_move(Table.chess_board, Table.source_tile,
                                                                Table.destination_tile)
                transition = Table.chess_board.current_player.make_move(move)

                Table.source_tile = None
                Table.destination_tile = None
                Table.moved_piece = None

                was_legal_move = transition.get_move_status().is_done()
                if was_legal_move:
                    Table.update_board(transition.get_transition_board(), move)

                if not was_legal_move:
                    self.left_mouse_event(event)
                    self.master.remove_highlight()

    class MoveLog:
        def __init__(self):
            self.moves = []

        def add_move(self, move):
            self.moves.append(move)

        def size(self) -> int:
            return len(self.moves)

        def clear(self):
            self.moves.clear()

        def remove_move(self, move):
            return self.moves.remove(move)

    class PlayerType:
        HUMAN = 0
        COMPUTER = 1

        def __init__(self, player_type: str):
            if player_type == 'HUMAN':
                self.type = self.HUMAN
            elif player_type == 'COMPUTER':
                self.type = self.COMPUTER

        def __str__(self):
            if self.type == self.HUMAN:
                return 'HUMAN'
            return 'COMPUTER'

        def is_ai(self):
            return self.type == self.COMPUTER

        def is_human(self):
            return self.type == self.HUMAN
