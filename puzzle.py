
import argparse
import draw

# class of board
# every board is an object of the class Board 
class Board:
    def __init__(self, left, right, bottom, top):
        self.left, self.right, self.bottom, self.top = left, right, bottom, top
    
    # call this method to return four boundaries of the board 
    def get_boundary(self):
        return self.left, self.right, self.bottom, self.top

class Puzzle:
    def __init__(self, size, block):
        # size is the size of board. 
        # block is the position (x,y) of the block 
        
        # fill the initial block as black
        draw.draw_one_square(block, 'k')
        # draw the grid on the board 
        draw.grid(size)

        # create the board at full size 
        board = Board(1, size, 1, size) 
        # call solve to fill the Tromino recursively using divide and conquer 
        self.solve(block, board)
        
        # show and save the result in a picture 
        draw.save_and_show(size, block)


    def solve(self, block, board):
        # block is a position (row, column) and board is an object of Board class 
        # recursively call solve() on four small size boards with only one block on each board
        # stop the recursive call when reaching to the base case, which is board 2*2
        #  
        # call draw.draw_one_tromino(type, board) to draw one type of tromino at the center of the board. The type of the tromino is an integer 1 to 4 as explained in the instruction and the board is an object of Board class where you want to draw the tromino at its center. 
       
        left, right, bottom, top = board.get_boundary()

        # Finding the centers row and column
        row_center, col_center = (top + bottom) // 2, (right + left) // 2

        # Making four sub-boards into four quadrants
        top_left_board = Board(left, col_center, row_center + 1, top)
        top_right_board = Board(col_center + 1, right, row_center + 1, top)
        bottom_left_board = Board(left, col_center, bottom, row_center)
        bottom_right_board = Board(col_center + 1, right, bottom, row_center)

        # We get the type of tromino block needed
        type = self.get_tromino_type(block, board)

        # We draw a tromino at the center of the board so that each quadrant has at least one block
        draw.draw_one_tromino(type, board)

        if left == right - 1 and bottom == top - 1:
            draw.draw_one_tromino(type, board)
            return board
        else:

            # Figuring out which quadrant the initial block in on
            if block[0] > row_center and block[1] <= col_center:
                self.solve(block, top_left_board)
            else:
                self.solve((row_center+1, col_center), top_left_board)

            if block[0] > row_center and block[1] > col_center:
                self.solve(block, top_right_board)
            else:
                self.solve((row_center+1, col_center+1), top_right_board)

            if block[0] <= row_center and block[1] <= col_center:
                self.solve(block, bottom_left_board)
            else:
                self.solve((row_center, col_center), bottom_left_board)

            if block[0] <= row_center and block[1] > col_center:
                self.solve(block, bottom_right_board)
            else:
                self.solve((row_center, col_center+1), bottom_right_board)

    def get_tromino_type(self, block, board):
        # return the type of the tromino you should draw based on the position of the block and the board.
        left, right, bottom, top = board.get_boundary()

        row_center, col_center = (top + bottom) // 2, (right + left) // 2

        if block == (top, right) or (block[0] > row_center and block[1] > col_center):
            return 1
        elif block == (top, left) or (block[0] > row_center and block[1] <= col_center):
            return 2
        elif block == (bottom, left) or (block[0] <= row_center and block[1] <= col_center):
            return 3
        elif block == (bottom, right) or (block[0] <= row_center and block[1] > col_center):
            return 4


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='puzzle')

    parser.add_argument('-size', dest='size', required = True, type = int, help='size of the board: 2^n')
    parser.add_argument('-block', dest='block', required = True, nargs='+', type = int, help='position of the initial block')

    args = parser.parse_args()

    # size must be a positive integer 2^n
    # block must be two integers between 1 and size 
    game = Puzzle(args.size, tuple(args.block))

    # game = puzzle(8, (1,1))
    # python puzzle.py -size 8 -block 1 1