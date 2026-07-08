class Tile:
    def __init__(self, r, c):
        self.my_row = r
        self.my_col = c
        self.active = False

    def get_col(self):
        return self.my_col

    def get_row(self):
        return self.my_row

    def make_active(self):
        self.active = True

    def make_inactive(self):
        self.active = False

    def is_active(self):
        return self.active

    def to_string(self):
        return str(self.my_row) + ", " + str(self.my_col)
