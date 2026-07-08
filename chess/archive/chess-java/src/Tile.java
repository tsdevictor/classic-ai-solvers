import javax.swing.*;

public class Tile extends JButton {
    private final int myCol, myRow;
    private boolean isActive;

    public Tile(int row, int col) {
        myRow = row;
        myCol = col;
    }

    public int getCol() {
        return myCol;
    }

    public int getRow() {
        return myRow;
    }

    public void makeActive() {
        isActive = true;
    }

    public void makeInactive() {
        isActive = false;
    }

    public boolean isActive() {
        return isActive;
    }

    public String toString() {
        return "(" + myRow + ", " + myCol + ")";
    }
}
