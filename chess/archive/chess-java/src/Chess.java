import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;

public class Chess {
    public static void main(String[] args) {
        Tile[][] tiles = new Tile[8][8];
        Piece[][] pieceLayout = new Piece[8][8];
        for(int r = 0; r < 8; r++) {
            for (int c = 0; c < 8; c++) {
                if (r == 0 || r == 7) {
                    boolean isWhite = r == 7;
                    if (c == 1 || c == 6)
                        pieceLayout[r][c] = new Piece(5, isWhite);
                    else if (c == 2 || c == 5)
                        pieceLayout[r][c] = new Piece(4, isWhite);
                    else if (c == 0 || c == 7)
                        pieceLayout[r][c] = new Piece(3, isWhite);
                    else if (c == 3)
                        pieceLayout[r][c] = new Piece(2, isWhite);
                    else
                        pieceLayout[r][c] = new Piece(1, isWhite);
                } else if (r == 1 || r == 6)
                    pieceLayout[r][c] = new Piece(6, r == 6);
                else
                    pieceLayout[r][c] = new Piece();
                tiles[r][c] = new Tile(r, c);
            }
        }

        JFrame frame = new JFrame("Chess");
        frame.setSize(500, 500);
        frame.setLocation(390, 0);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setContentPane(new ChessPanel(pieceLayout, tiles));
        frame.setVisible(true);
    }

    public static class ChessPanel extends JPanel {
        private final Piece[][] pieceLayout;
        private final Tile[][] tiles;
        private int prevRow, prevCol;
        private boolean whiteTurn;
        public ChessPanel(Piece[][] pieceLayout, Tile[][] tiles) {
            setLayout(new GridLayout(8, 8));
            whiteTurn = true;
            this.pieceLayout = pieceLayout;
            this.tiles = tiles;
            for (int r = 0; r < 8; r++)
                for (int c = 0; c < 8; c++) {
                    tiles[r][c] = new Tile(r, c);
                    if (r % 2 == c % 2)
                        tiles[r][c].setBackground(new Color(255, 206, 158));
                    else
                        tiles[r][c].setBackground(new Color(209, 139, 71));
                    if (!(pieceLayout[r][c].isEmpty()))
                        tiles[r][c].setIcon(new ImageIcon("src/Images/" +
                                (pieceLayout[r][c].isWhite() ? "White" : "Black") + pieceLayout[r][c].toString() + ".png"));
                    tiles[r][c].addActionListener(new Listener());
                    add(tiles[r][c]);
                }
        }

        private class Listener implements ActionListener {
            public void actionPerformed(ActionEvent e) {
                Tile source = (Tile) e.getSource();
                int col = source.getCol();
                int row = source.getRow();

                if (tiles[row][col].isActive()) {
                    boolean wasEmpty = pieceLayout[row][col].isEmpty();

                    boolean castle = false;
                    if (pieceLayout[prevRow][prevCol].isKing()) {
                        if (prevCol + 2 == col || prevCol - 2 == col) {
                            castle = true;
                        }
                    }

                    pieceLayout[row][col] = pieceLayout[prevRow][prevCol];
                    pieceLayout[prevRow][prevCol] = new Piece();
                    if (castle) {
                        if (prevCol + 2 == col) {
                            pieceLayout[row][prevCol + 1] = pieceLayout[row][7];
                            pieceLayout[row][7] = new Piece();
                        } else {
                            pieceLayout[row][prevCol - 1] = pieceLayout[row][0];
                            pieceLayout[row][0] = new Piece();
                        }
                    }

                    whiteTurn = !whiteTurn;

                    if (pieceLayout[row][col].isKing() || pieceLayout[row][col].isRook())
                        pieceLayout[row][col].move();

                    for (Piece[] pieces : pieceLayout)
                        for (int c = 0; c < pieceLayout.length; c++)
                            if (pieces[c].isPawn() && pieces[c].isWhite() == pieceLayout[row][col].isWhite())
                                pieces[c].setJustAdvancedTwo(false);

                    if(pieceLayout[row][col].isPawn()) {
                        if (row == 0 || row == 7)
                            pieceLayout[row][col] = getPawnChoice(pieceLayout[row][col].isWhite());
                        pieceLayout[row][col].setJustAdvancedTwo(Math.abs(row - prevRow) == 2);
                        if (wasEmpty && (row + 1 == prevRow || row - 1 == prevRow) && (col + 1 == prevCol || col - 1 == prevCol))
                            pieceLayout[prevRow][col] = new Piece();
                    }
                }
                for (int r = 0; r < 8; r++)
                    for (int c = 0; c < 8; c++) {
                        if (r % 2 == c % 2)
                            tiles[r][c].setBackground(new Color(255, 206, 158));
                        else
                            tiles[r][c].setBackground(new Color(209, 139, 71));
                        tiles[r][c].makeInactive();
                        if (!(pieceLayout[r][c].isEmpty()))
                            tiles[r][c].setIcon(new ImageIcon("src/Images/" +
                                    (pieceLayout[r][c].isWhite() ? "White" : "Black") + pieceLayout[r][c].toString() + ".png"));
                        else
                            tiles[r][c].setIcon(null);
                    }

                if (pieceLayout[row][col].isWhite() == whiteTurn) {
                    ArrayList<Tile> possibilities = pieceLayout[row][col].validMoves(pieceLayout, new Tile(row, col));

                    for(int r = 0; r < pieceLayout.length; r++)
                        for(int c = 0; c < pieceLayout.length; c++)
                            if(pieceLayout[r][c].isKing() && pieceLayout[r][c].isWhite() == pieceLayout[row][col].isWhite()) {
                                pieceLayout[r][c].removeInvalidMoves(possibilities, pieceLayout, new Tile(row, col), new Tile(r, c));
                                pieceLayout[r][c].checkmate(pieceLayout, new Tile(r, c));
                                break;
                            }

                    for (Tile possibility : possibilities) {
                        int r = possibility.getRow();
                        int c = possibility.getCol();
                        tiles[r][c].setBackground(Color.GRAY);
                        tiles[r][c].makeActive();
                    }
                }

                prevCol = col;
                prevRow = row;
            }
        }
        public Piece getPawnChoice(boolean isWhite) {
            int choice = 0;
            while (!(choice == 1 || choice == 2 || choice == 3 || choice == 4)) {
                try {
                    choice = Integer.parseInt(JOptionPane.showInputDialog("""
                        Type a number:
                        1. Queen
                        2. Rook
                        3. Bishop
                        4. Knight"""));
                    if(!(choice == 1 || choice == 2 || choice == 3 || choice == 4))
                        throw new NumberFormatException();
                } catch (NumberFormatException f) {
                    JOptionPane.showMessageDialog(null,
                            "That's not a valid choice. Remember to enter a number 1-4.");
                }
            }
            return new Piece(choice+1, isWhite);
        }
    }
}
