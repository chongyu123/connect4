from random import randint
import copy

# board size
WIDTH = 7
HEIGHT = 6

# number of consecutive chips to win
WINNING_LENGTH = 4

# depth of board evaluation search
LOOKUP_LEVEL = 4


class Game(object):

    def __init__(self):
        self.reset()


    def reset(self):
        self.board = [[0 for x in range(HEIGHT)] for x in range(WIDTH)] 


    # print the board
    def show(self, board=None):
        if (board == None):
            board = self.board
        
        for x in range(WIDTH):
            print x,
        print
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if board[x][y] == 0:
                    print '.',
                else:
                    print board[x][y],
            print
    
    
    # no more space left
    def is_full(self):
        for x in range(0, WIDTH):
            if self.board[x][0] == 0:
                return False
        return True

        
    # returns True if the chip is a winner
    def drop_chip(self, x, chip):
        y_position = self.insert_chip_board(self.board, x, chip)
        self.show()
        if (y_position != False):
            if self.is_board_winner(self.board, chip):
                #print "##### WINNER!! %s #######" % chip
                return True
               
        return False


    def insert_chip_board(self, board, x, chip):
        for y in range(HEIGHT):
            if board[x][y] != 0:
                if y != 0:
                    board[x][y-1] = chip
                    return y-1
                else:
                    return False
        board[x][y] = chip
        return y


    # returns True if the move is a winner
    def computer_move(self):
        print "\nThinking...\n"
        position = self.get_suggestion('O')
        if self.drop_chip(position, 'O'):
            return True
        
        return False


    # evaluate each index and return the best scored index for the next move
    def get_suggestion(self, chip):
        scores = []
        for x in range(0, WIDTH):
            if self.board[x][0] == 0:
                new_board = copy.deepcopy(self.board)
                self.insert_chip_board(new_board, x, chip)
                scores.append(self.eval_board(new_board, chip))
            else:
                scores.append(None)
            
        # give a higher weight to center of the board
        for i in range(0, WIDTH):
            if scores[i] != None:
                scores[i] = scores[i] + ((WIDTH/2) - abs((WIDTH/2) - i))

        # find default index
        index = None;
        for i in range(0, WIDTH):
            if scores[i] != None:
                index = i
                break;

        # board is full
        if index == None:
            return None

        for i in range(0, WIDTH):
            if scores[i] != None:
                if scores[index] < scores[i]:
                    index = i

        print "my evaluation of the board. Higher score the better."
        print scores
        print "I choose %d" % index
        print

        return index


    # evaluate the board and return a score
    # the evaluation looks ahead LOOKUP_LEVEL deep into the moves
    # The deeper we go, the longer it takes, but possibly better moves
    def eval_board(self, board, chip, level=0):
        if level >= LOOKUP_LEVEL:
            return 0

        score = 0
        # determine positive or negative of the score
        score_sign = 1
        if (level % 2) == 1:
            score_sign = -1

        if self.is_board_winner(board, chip):
            score = pow(10,LOOKUP_LEVEL-level) * score_sign
        else:
            level = level + 1
            # switch chip
            if (chip == 'O'):
                chip = 'X'
            else:
                chip = 'O'
            
            for x in range(0, WIDTH):
                new_board = copy.deepcopy(board)
                self.insert_chip_board(new_board, x, chip)
                score = score + self.eval_board(new_board, chip, level)

        return score


    # check if the chip type is a winner on the board
    def is_board_winner(self, board, chip):
        for x in range(0, WIDTH):
            for y in range(0, HEIGHT):
                if board[x][y] == chip:
                    if self.is_chip_winner(board, x, y):
                        return True
                    break
        return False

    # determine if the selected chip is a winner by counting the surounding chips
    def is_chip_winner(self, board, x, y):
        #print "checking for winner at (%d, %d)" % (x,y)
        chip = board[x][y]
        if (self.count_consecutive(board, x, y, 0, 1) + self.count_consecutive(board, x, y, 0, -1) + 1) >= WINNING_LENGTH:
            return True
        if (self.count_consecutive(board, x, y, 1, 0) + self.count_consecutive(board, x, y, -1, 0) + 1) >= WINNING_LENGTH:
            return True
        if (self.count_consecutive(board, x, y, 1, 1) + self.count_consecutive(board, x, y, -1, -1) + 1) >= WINNING_LENGTH:
            return True
        if (self.count_consecutive(board, x, y, -1, 1) + self.count_consecutive(board, x, y, 1, -1) + 1) >= WINNING_LENGTH:
            return True
        
        return False

    # count the consecutive same chips into one direction
    def count_consecutive(self, board, x, y, change_x, change_y):
        chip = board[x][y]
        count = 0
        while (x >= 0) and (x < WIDTH) and (y >= 0) and (y < HEIGHT) and (board[x][y] == chip):
            x = x + change_x
            y = y + change_y
            count = count + 1
            
        return count - 1

    
if __name__ == "__main__":
    game = Game()
    game.show()
    while True:
        if game.is_full():
            print "##### It's a tie #####"
            break
        position = raw_input('> ')
        if position == '':
            continue
        if game.drop_chip(int(position), 'X'):
            print "##### You WIN! #####"
            break
        elif game.computer_move():
            print "##### I WIN! #####"
            break

