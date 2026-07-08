class GameSetup:
    def __init__(self):
        import gui.table as gt
        num_elements = 0

        import os
        PATH = os.path.dirname(__file__)

        self.popup = gt.Toplevel(gt.Table.game_frame)
        self.popup.geometry('150x270')
        self.popup.title('Options')
        self.popup.iconbitmap(os.path.join(PATH, 'TRANSPARENT.ico'))

        white_label = gt.Label(self.popup, text='White:', borderwidth=0, highlightthickness=0)
        white_label.grid(row=num_elements, column=0, sticky='W')
        self.white_player_type = gt.StringVar()
        white_option1 = gt.ttk.Radiobutton(self.popup, text='Human', value='HUMAN', variable=self.white_player_type)
        white_option2 = gt.ttk.Radiobutton(self.popup, text='Computer', value='COMPUTER',
                                           variable=self.white_player_type)
        num_elements += 1
        white_option1.grid(row=num_elements, column=0, sticky='W')
        white_option1.invoke()
        num_elements += 1
        white_option2.grid(row=num_elements, column=0, sticky='W')
        num_elements += 1

        spacer1 = gt.Label(self.popup, text="")
        spacer1.grid(row=num_elements, column=0)
        num_elements += 1

        black_label = gt.Label(self.popup, text='Black:', borderwidth=0, highlightthickness=0)
        black_label.grid(row=num_elements, column=0, sticky='W')
        self.black_player_type = gt.StringVar()
        black_option1 = gt.ttk.Radiobutton(self.popup, text='Human', value='HUMAN', variable=self.black_player_type)
        black_option2 = gt.ttk.Radiobutton(self.popup, text='Computer', value='COMPUTER',
                                           variable=self.black_player_type)
        num_elements += 1
        black_option1.grid(row=num_elements, column=0, sticky='W')
        black_option1.invoke()
        num_elements += 1
        black_option2.grid(row=num_elements, column=0, sticky='W')
        num_elements += 1

        spacer2 = gt.Label(self.popup, text="")
        spacer2.grid(row=num_elements, column=0)
        num_elements += 1

        depth_label = gt.Label(self.popup, text='AI Search Depth: ', borderwidth=0, highlightthickness=0)
        depth_label.grid(row=num_elements, column=0, sticky='W')
        self.search_depth = gt.StringVar(value=3)
        spin_box = gt.ttk.Spinbox(self.popup,
                                  from_=1,
                                  to=5,
                                  textvariable=self.search_depth,
                                  wrap=True)
        num_elements += 1
        spin_box.grid(row=num_elements, column=0, sticky='W')
        num_elements += 1

        spacer3 = gt.Label(self.popup, text="")
        spacer3.grid(row=num_elements, column=0)
        num_elements += 1

        ok_button = gt.ttk.Button(self.popup, text='OK', command=self.ok)
        ok_button.grid(row=num_elements, column=0, sticky='W')
        num_elements += 1
        cancel_button = gt.ttk.Button(self.popup, text='Cancel', command=self.cancel)
        cancel_button.grid(row=num_elements, column=0, sticky='W')

    def cancel(self):
        self.popup.destroy()

    def ok(self):
        import gui.table as gt
        gt.Table.white_player_type = gt.Table.PlayerType(self.white_player_type.get())
        gt.Table.black_player_type = gt.Table.PlayerType(self.black_player_type.get())
        gt.Table.search_depth = int(self.search_depth.get())
        self.cancel()
        gt.Table.update_board(gt.Table.chess_board)
