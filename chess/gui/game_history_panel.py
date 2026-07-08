from tkinter import *
from tkinter import ttk

class GameHistoryPanel(Frame):
    def __init__(self, master=None, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)

        # scrollbar
        self.scroll = Scrollbar(self)
        self.scroll.pack(side=RIGHT, fill=Y)

        self.table = ttk.Treeview(self, yscrollcommand=self.scroll.set, height=19)
        self.table.pack()

        self.scroll.config(command=self.table.yview)
        self.table['columns'] = ('white_moves', 'black_moves')    # define column
        self.table.column('#0', width=0, stretch=NO)              # format column
        self.table.column('white_moves', anchor=CENTER, width=60)
        self.table.column('black_moves', anchor=CENTER, width=60)

        self.table.heading("#0", text="", anchor=CENTER)          # add headings
        self.table.heading("white_moves", text="White", anchor=CENTER)
        self.table.heading("black_moves", text="Black", anchor=CENTER)

        self.last_index = -1

        self.table.pack()

    def get_row_count(self):
        return len(self.table.get_children())

    def clear(self):
        for item in self.table.get_children():
            self.table.delete(item)
        self.last_index = -1

    def get_value_at(self, r, c):
        return self.table.item(r, 'values')[c]

    def set_value_at(self, value, r: int, c):
        self.table.set(str(r), 'white_moves' if c == 0 else 'black_moves', value=value)

    def insert_data(self, white_col, move_text: str):
        if white_col:
            self.table.insert(parent='', index='end', iid=self.last_index, text='',
                              values=(move_text, ''))
            self.last_index += 1
        else:
            self.set_value_at(move_text, self.last_index-1, 1)

    @staticmethod
    def calculate_check_and_checkmate_hash(board):
        if board.current_player.is_in_checkmate():
            return '#'
        elif board.current_player.is_in_check():
            return '+'
        return ''

    def redo(self, board, move_history):
        self.clear()
        for move in move_history.moves:
            self.insert_data(move.piece.is_white, str(move))

        if move_history.size() > 0:
            last_move = move_history.moves[-1]
            move_text = str(last_move)
            self.set_value_at(move_text + self.calculate_check_and_checkmate_hash(board),
                              self.last_index-1, 0 if last_move.piece.is_white else 1)

        self.table.yview_moveto(1)  # scroll to bottom
