from tkinter import *
from PIL import ImageTk, Image

class TakenPiecesPanel(Frame):
    WIDTH = 60
    HEIGHT = 430

    def __init__(self, master=None, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)

        self.north_panel = Frame(self)
        self.south_panel = Frame(self)

        self.north_pieces = []
        self.south_pieces = []
        for k in range(16):
            self.north_pieces.append(Frame(self.north_panel, width=self.WIDTH/2, height=26))
            self.north_pieces[k].pack()
            self.south_pieces.append(Frame(self.south_panel, width=self.WIDTH/2, height=26))
            self.south_pieces[k].pack()

        self.north_panel.pack(side=LEFT)
        self.south_panel.pack(side=RIGHT)

    def redo(self, move_log):
        import gui.table as gt
        for k in range(16):
            for widget in self.north_pieces[k].winfo_children():
                widget.destroy()
            for widget in self.south_pieces[k].winfo_children():
                widget.destroy()

        white_taken_pieces = []
        black_taken_pieces = []

        for move in move_log.moves:
            if move.is_attack():
                taken_piece = move.get_attacked_piece()
                if taken_piece.is_white:
                    white_taken_pieces.append(taken_piece)
                else:
                    black_taken_pieces.append(taken_piece)

        # import engine.extra.sort
        # engine.extra.sort.sort(white_taken_pieces)
        # engine.extra.sort.sort(black_taken_pieces)

        for piece in white_taken_pieces:
            last = 0
            image_path = gt.Table.TilePanel.PIECE_ICON_PATH + ('W' if piece.is_white else 'B') + str(piece) + '.png'
            photo = ImageTk.PhotoImage(Image.open(image_path).resize((16, 16), Image.Resampling.LANCZOS))

            label = Label(self.south_pieces[last], image=photo, bg=self.cget('bg'),
                          borderwidth=0, highlightthickness=0, width=self.WIDTH/2, height=26)
            label.image = photo
            label.pack()
            last += 1

        for piece in black_taken_pieces:
            last = 0
            image_path = gt.Table.TilePanel.PIECE_ICON_PATH + ('W' if piece.is_white else 'B') + str(piece) + '.png'
            photo = ImageTk.PhotoImage(Image.open(image_path).resize((16, 16), Image.Resampling.LANCZOS))

            label = Label(self.north_pieces[last], image=photo, bg=self.cget('bg'),
                          borderwidth=0, highlightthickness=0, width=self.WIDTH/2, height=26)
            label.image = photo
            label.pack()
            last += 1
