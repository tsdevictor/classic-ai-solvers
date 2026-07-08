import javax.swing.*;
import java.util.ArrayList;

public class Piece {
    private final int myType;
    private boolean isWhite, firstMove, justAdvancedTwo;

    public Piece() {
        myType = 0;
    }

    public Piece(int t, boolean w) {
        myType = t;
        isWhite = w;
        firstMove = true;
        justAdvancedTwo = false;
    }

    public void move() {
        firstMove = false;
    }

    public void setJustAdvancedTwo(boolean j) {
        justAdvancedTwo = j;
    }

    public boolean getJustAdvancedTwo() {
        return justAdvancedTwo;
    }

    public ArrayList<Tile> validMoves(Piece[][] pieceLayout, Tile position) {
        int row = position.getRow();
        int col = position.getCol();
        Piece piece = pieceLayout[row][col];
        ArrayList<Tile> possibleMoves = new ArrayList<>();

        if (piece.isPawn()) {
            int one = isWhite ? -1 : 1;
            int two = isWhite ? -2 : 2;
            boolean pawnFirstMove = isWhite ? row == 6 : row == 1;
            if (pawnFirstMove && pieceLayout[row + two][col].isEmpty() && pieceLayout[row + one][col].isEmpty())
                possibleMoves.add(new Tile(row + two, col));
            if (row != 0 && row != 7) {
                if (pieceLayout[row + one][col].isEmpty())
                    possibleMoves.add(new Tile(row + one, col));
                if (col != 0) {
                    Piece diagonal = pieceLayout[row + one][col - 1];
                    if (diagonal.isWhite() != this.isWhite && !diagonal.isEmpty())
                        possibleMoves.add(new Tile(row + one, col - 1));
                }
                if (col != 7) {
                    Piece diagonal = pieceLayout[row + one][col + 1];
                    if (diagonal.isWhite() != this.isWhite && !diagonal.isEmpty())
                        possibleMoves.add(new Tile(row + one, col + 1));
                }
            }
            if ((this.isWhite && row == 3) || (!this.isWhite && row == 4))
                for (int k = -1; k <= 1; k += 2)
                        if (col + k >= 0 && col + k <= 7) {
                            Piece pawn = pieceLayout[3][col + k];
                            if (pieceLayout[2][col + k].isEmpty() && pawn.isPawn() && pawn.getJustAdvancedTwo() && !pawn.isWhite())
                                possibleMoves.add(new Tile(2, col + k));
                            pawn = pieceLayout[4][col + k];
                            if (pieceLayout[5][col + k].isEmpty() && pawn.isPawn() && pawn.getJustAdvancedTwo() && pawn.isWhite())
                                possibleMoves.add(new Tile(5, col + k));
                        }
        }

        else if (piece.isKnight()) {
            possibleMoves.add(new Tile(row + 2, col + 1));
            possibleMoves.add(new Tile(row + 2, col - 1));
            possibleMoves.add(new Tile(row - 2, col + 1));
            possibleMoves.add(new Tile(row - 2, col - 1));
            possibleMoves.add(new Tile(row + 1, col + 2));
            possibleMoves.add(new Tile(row + 1, col - 2));
            possibleMoves.add(new Tile(row - 1, col + 2));
            possibleMoves.add(new Tile(row - 1, col - 2));
        }

        else if (piece.isBishop()) {
            //diagonal down right
            int c = col + 1;
            for (int r = row + 1; r < 8 && c < 8; r++) {
                if (pieceLayout[r][c].isEmpty())
                    possibleMoves.add(new Tile(r, c));
                else {
                    if (!pieceLayout[r][c].isWhite() == this.isWhite)
                        possibleMoves.add(new Tile(r, c));
                    break;
                }
                c++;
            }

            //diagonal up left
            c = col - 1;
            for (int r = row - 1; r >= 0 && c >= 0; r--) {
                if (pieceLayout[r][c].isEmpty())
                    possibleMoves.add(new Tile(r, c));
                else {
                    if (!pieceLayout[r][c].isWhite() == this.isWhite)
                        possibleMoves.add(new Tile(r, c));
                    break;
                }
                c--;
            }

            //diagonal down
            // left
            c = col - 1;
            for (int r = row + 1; r < 8 && c >= 0; r++) {
                if (pieceLayout[r][c].isEmpty())
                    possibleMoves.add(new Tile(r, c));
                else {
                    if (!pieceLayout[r][c].isWhite() == this.isWhite)
                        possibleMoves.add(new Tile(r, c));
                    break;
                }
                c--;
            }

            //diagonal up right
            c = col + 1;
            for (int r = row - 1; r >= 0 && c < 8; r--) {
                if (pieceLayout[r][c].isEmpty())
                    possibleMoves.add(new Tile(r, c));
                else {
                    if (!pieceLayout[r][c].isWhite() == this.isWhite)
                        possibleMoves.add(new Tile(r, c));
                    break;
                }
                c++;
            }
        }

        else if (piece.isRook()) {
            //same column below
            for (int r = row + 1; r < 8; r++) {
                if (pieceLayout[r][col].isEmpty())
                    possibleMoves.add(new Tile(r, col));
                else {
                    if (!pieceLayout[r][col].isWhite() == isWhite)
                        possibleMoves.add(new Tile(r, col));
                    break;
                }
            }

            //same column above
            for (int r = row - 1; r >= 0; r--) {
                if (pieceLayout[r][col].isEmpty())
                    possibleMoves.add(new Tile(r, col));
                else {
                    if (!pieceLayout[r][col].isWhite() == isWhite)
                        possibleMoves.add(new Tile(r, col));
                    break;
                }
            }

            //same row to the right
            for (int c = col + 1; c < 8; c++) {
                if (pieceLayout[row][c].isEmpty())
                    possibleMoves.add(new Tile(row, c));
                else {
                    if (!pieceLayout[row][c].isWhite() == isWhite)
                        possibleMoves.add(new Tile(row, c));
                    break;
                }
            }

            //same row to the left
            for (int c = col - 1; c >= 0; c--) {
                if (pieceLayout[row][c].isEmpty())
                    possibleMoves.add(new Tile(row, c));
                else {
                    if (!pieceLayout[row][c].isWhite() == isWhite)
                        possibleMoves.add(new Tile(row, c));
                    break;
                }
            }
        }

        else if (piece.isQueen()) {
            //diagonal down right
            int c = col + 1;
            for (int r = row + 1; r < 8 && c < 8; r++) {
                if (pieceLayout[r][c].isEmpty())
                    possibleMoves.add(new Tile(r, c));
                else {
                    if (!pieceLayout[r][c].isWhite() == this.isWhite)
                        possibleMoves.add(new Tile(r, c));
                    break;
                }
                c++;
            }

            //diagonal up left
            c = col - 1;
            for (int r = row - 1; r >= 0 && c >= 0; r--) {
                if (pieceLayout[r][c].isEmpty())
                    possibleMoves.add(new Tile(r, c));
                else {
                    if (!pieceLayout[r][c].isWhite() == this.isWhite)
                        possibleMoves.add(new Tile(r, c));
                    break;
                }
                c--;
            }

            //diagonal down left
            c = col - 1;
            for (int r = row + 1; r < 8 && c >= 0; r++) {
                if (pieceLayout[r][c].isEmpty())
                    possibleMoves.add(new Tile(r, c));
                else {
                    if (!pieceLayout[r][c].isWhite() == this.isWhite)
                        possibleMoves.add(new Tile(r, c));
                    break;
                }
                c--;
            }

            //diagonal up right
            c = col + 1;
            for (int r = row - 1; r >= 0 && c < 8; r--) {
                if (pieceLayout[r][c].isEmpty())
                    possibleMoves.add(new Tile(r, c));
                else {
                    if (!pieceLayout[r][c].isWhite() == this.isWhite)
                        possibleMoves.add(new Tile(r, c));
                    break;
                }
                c++;
            }

            //same column below
            for (int r = row + 1; r < 8; r++) {
                if (pieceLayout[r][col].isEmpty())
                    possibleMoves.add(new Tile(r, col));
                else {
                    if (!pieceLayout[r][col].isWhite() == isWhite)
                        possibleMoves.add(new Tile(r, col));
                    break;
                }
            }

            //same column above
            for (int r = row - 1; r >= 0; r--) {
                if (pieceLayout[r][col].isEmpty())
                    possibleMoves.add(new Tile(r, col));
                else {
                    if (!pieceLayout[r][col].isWhite() == isWhite)
                        possibleMoves.add(new Tile(r, col));
                    break;
                }
            }

            //same row to the right
            for (int co = col + 1; co < 8; co++) {
                if (pieceLayout[row][co].isEmpty())
                    possibleMoves.add(new Tile(row, co));
                else {
                    if (!pieceLayout[row][co].isWhite() == isWhite)
                        possibleMoves.add(new Tile(row, co));
                    break;
                }
            }

            //same row to the left
            for (int co = col - 1; co >= 0; co--) {
                if (pieceLayout[row][co].isEmpty())
                    possibleMoves.add(new Tile(row, co));
                else {
                    if (!pieceLayout[row][co].isWhite() == isWhite)
                        possibleMoves.add(new Tile(row, co));
                    break;
                }
            }
        }

        else if (piece.isKing()) {
            possibleMoves.add(new Tile(row + 1, col + 1));
            possibleMoves.add(new Tile(row + 1, col - 1));
            possibleMoves.add(new Tile(row - 1, col + 1));
            possibleMoves.add(new Tile(row - 1, col - 1));
            possibleMoves.add(new Tile(row + 1, col));
            possibleMoves.add(new Tile(row - 1, col));
            possibleMoves.add(new Tile(row, col + 1));
            possibleMoves.add(new Tile(row, col - 1));
        }

        //remove invalid moves
        for (int k = 0; k < possibleMoves.size(); k++) {
            int r = possibleMoves.get(k).getRow();
            int c = possibleMoves.get(k).getCol();
            if (r > 7 || r < 0 || c > 7 || c < 0 || (!pieceLayout[r][c].isEmpty() && pieceLayout[r][c].isWhite() == this.isWhite)) {
                possibleMoves.remove(k);
                k--;
            }
        }

        return possibleMoves;
    }

    public boolean inCheck(Piece[][] pieceLayout, Tile kingPos) {
        int row = kingPos.getRow();
        int col = kingPos.getCol();
        for (int r = 0; r < 8; r++) {
            for (int c = 0; c < 8; c++) {
                Piece beingChecked = pieceLayout[r][c];
                if (!beingChecked.isEmpty() && (beingChecked.isWhite() != this.isWhite)) {
                    ArrayList<Tile> validMoves = beingChecked.validMoves(pieceLayout, new Tile(r, c));
                    for (Tile validMove : validMoves)
                        if (validMove.getCol() == col && validMove.getRow() == row)
                            return true;
                }
            }
        }
        return false;
    }

    public void removeInvalidMoves(ArrayList<Tile> possibilities, Piece[][] pieceLayout, Tile movingPiece, Tile kingPos) {
        int mr = movingPiece.getRow();
        int mc = movingPiece.getCol();

        boolean isKing = pieceLayout[mr][mc].isKing();

        boolean castle = false;
        if (isKing() && pieceLayout[mr][mc].isFirstMove()) {
            if (pieceLayout[mr][0].isRook() && pieceLayout[mr][0].isFirstMove()) {
                boolean blocking = false;
                if (!inCheck(pieceLayout, new Tile(mr, mc))) {
                    if (!(pieceLayout[mr][1].isEmpty()))
                        blocking = true;
                    for (int c = 2; c < 4; c++)
                        if (inCheck(pieceLayout, new Tile(mr, c)) || !(pieceLayout[mr][c].isEmpty()))
                            blocking = true;
                    if (!blocking) {
                        possibilities.add(new Tile(mr, 2));
                        castle = true;
                    }
                }
            }
        }
        if (pieceLayout[mr][7].isRook() && pieceLayout[mr][7].isFirstMove()) {
            boolean blocking = false;
            if (!inCheck(pieceLayout, new Tile(mr, mc))) {
                for (int c = 5; c < 7; c++)
                    if (inCheck(pieceLayout, new Tile(mr, c)) || !(pieceLayout[mr][c].isEmpty()))
                        blocking = true;
                if (!blocking) {
                    possibilities.add(new Tile(mr, 6));
                    castle = true;
                }
            }
        }


        for (int k = 0; k < possibilities.size(); k++) {
            int tr = possibilities.get(k).getRow();
            int tc = possibilities.get(k).getCol();
            boolean enPassant = pieceLayout[mr][mc].isPawn() && tc != mc && pieceLayout[tr][tc].isEmpty();
            Piece enP = null;
            if (enPassant) {
                enP = pieceLayout[mr][tc];
                pieceLayout[mr][tc] = new Piece();
            }

            if (!castle) {
                Piece atTarget = pieceLayout[tr][tc];
                pieceLayout[tr][tc] = pieceLayout[mr][mc];
                pieceLayout[mr][mc] = new Piece();

                if (isKing)
                    kingPos = new Tile(tr, tc);

                boolean inCheck = inCheck(pieceLayout, kingPos);
                if (inCheck) {
                    possibilities.remove(k);
                    k--;
                }

                pieceLayout[mr][mc] = pieceLayout[tr][tc];
                pieceLayout[tr][tc] = atTarget;
                if (enPassant)
                    pieceLayout[mr][tc] = enP;
            }
        }
    }

    public void checkmate(Piece[][] pieceLayout, Tile kingPos) {
        boolean onlyZeroes = true;
        for (int r = 0; r < pieceLayout.length; r++)
            for (int c = 0; c < pieceLayout.length; c++) {
                if (pieceLayout[r][c].isWhite() == pieceLayout[kingPos.getRow()][kingPos.getCol()].isWhite()) {
                    ArrayList<Tile> validMoves = pieceLayout[r][c].validMoves(pieceLayout, new Tile(r, c));
                    pieceLayout[r][c].removeInvalidMoves(validMoves, pieceLayout, new Tile(r, c), kingPos);
                    if (validMoves.size() != 0)
                        onlyZeroes = false;
                }
            }

        if (inCheck(pieceLayout, kingPos) && onlyZeroes) {
            JOptionPane.showMessageDialog(null, (isWhite ? "Black" : "White") + " wins!");
            System.exit(0);
        } else if (onlyZeroes) {
            JOptionPane.showMessageDialog(null, "Draw by stalemate");
            System.exit(0);
        }
    }

    public boolean isWhite() {
        return isWhite;
    }

    public boolean isFirstMove() {
        return firstMove;
    }

    public boolean isEmpty() {
        int EMPTY = 0;
        return myType == EMPTY;
    }

    public boolean isPawn() {
        int PAWN = 6;
        return myType == PAWN;
    }

    public boolean isKnight() {
        int KNIGHT = 5;
        return myType == KNIGHT;
    }

    public boolean isBishop() {
        int BISHOP = 4;
        return myType == BISHOP;
    }

    public boolean isRook() {
        int ROOK = 3;
        return myType == ROOK;
    }

    public boolean isQueen() {
        int QUEEN = 2;
        return myType == QUEEN;
    }

    public boolean isKing() {
        int KING = 1;
        return myType == KING;
    }

    public String toString() {
        if (isPawn())
            return "Pawn";
        if (isKnight())
            return "Knight";
        if (isBishop())
            return "Bishop";
        if (isRook())
            return "Rook";
        if (isQueen())
            return "Queen";
        else
            return "King";
    }
}
