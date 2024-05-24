import numpy as np
import random
import sys
import math


## Default parameters for this lab

# size of gaming board
ROW_COUNT = 6
COLUMN_COUNT = 7

# denote which one to play
PLAYER = 0
AI = 1

# use for initialize the gaming board
EMPTY = 0

# specific piece number of  Player and AI
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4


class ConnectFour:
    def __init__(self):
        self.board = self.create_board()
        self.last_move = None  # Keeps track of the last move made

    #Initialize a 7x6 board with all empty slots.
    def create_board(self):
        board = np.zeros((ROW_COUNT,COLUMN_COUNT))
        return board

    # drop a piece into the specific (row, column)
    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    # check current position in the board is valid
    def is_valid_location(self, board, col):
        return board[0][col] == 0



    ## This method finds the next open row in a given column where a piece can be dropped. 
    # It iterates through each row in the specified column and returns the row number 
    # where the first empty space (0) is found.

    def get_next_open_row(self, board, col):
        for r in range(ROW_COUNT-1, -1, -1):
            if board[r][col] == 0:
                return r
        return None
            
    # print the board
    def print_board(self, board):
        print("\n".join(["\t".join([str(cell) for cell in row]) for row in board]))

    # check if the current player has won the game.
    def winning_move(self, board, piece):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True

    def evaluate_window(self, window, piece):
        
        # you've provided is designed to score a given window (a subset of the Connect-4 board) based on the presence of player pieces,
        # AI pieces, and empty spaces. 
        
        score = 0
        opp_piece = PLAYER_PIECE
        if piece == PLAYER_PIECE:
            opp_piece = AI_PIECE

        # If the window contains four of the piece (either player or AI), the score increases by 100, indicating a winning condition.
        if window.count(piece) == 4:
            score += 100
            
        # If there are three piece and one empty space, the score increases by 5, indicating a potential win in the next move.
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
            
        # If the window has two piece and two empty spaces, the score increases by 2, signifying a developing opportunity.
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2

        # If the opponent has three pieces and there's one empty space, the score decreases by 4. This reflects the need to block the opponent's potential win.
        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score

    # The score_position method you provided is designed to evaluate the entire Connect-4 board and assign a score based on the current position of the pieces.
    # This score helps the AI to make decisions. 
    def score_position(self, board, piece):
        score = 0

        ## Score center column
        ## This part focuses on the center column, often a strategic position in Connect-4. 
        # It counts the number of piece in the center column and multiplies this count by 3, 
        # adding this to the total score.
        center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        ## This loop scans each row of the board. For each row, it creates a 'window' of 4 spaces 
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(COLUMN_COUNT-3):
                window = row_array[c:c+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(ROW_COUNT-3):
                window = col_array[r:r+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)
       
        '''
        Score positive sloped diagonal
        Here, it evaluates diagonal lines sloping upwards. 
        It moves through the board, creating diagonal windows and scoring them.
        '''
        ## [TODO-1]
        

        '''
        This part evaluates diagonals sloping downwards, 
        again using evaluate_window to score these sections.
        '''
        ## [TODO-2]
        

        # return scor

        return score

    # check the gaming is over: win/lose/tie
    def is_terminal_node(self, board):
        return self.winning_move(board, PLAYER_PIECE) or self.winning_move(board, AI_PIECE) or len(self.get_valid_locations(board)) == 0

    # find the valid position for current board
    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if self.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    # find the best move of AI/Player according to the current board
    def pick_best_move(self, board, piece):

        valid_locations = self.get_valid_locations(board)
        best_score = -10000
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = self.get_next_open_row(board, col)
            temp_board = board.copy()
            self.drop_piece(temp_board, row, col, piece)
            score = self.score_position(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col


class ConnectFour_Minimax(ConnectFour): 
    
    def __init__(self):
        super().__init__()
    
    def minimax(self, board, depth, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            
            ### [TODO-1]
            '''
            If the depth is 0 or the node is terminal (indicating a win, lose, or tie state), 
            the function returns the heuristic value of the node. 
            Wins and losses have large positive or negative values, respectively.
            '''
           
            
        if maximizingPlayer:
            
            ### [TODO-2]
            '''
            When the function is evaluating the AI's move, it needs to maximize the score.
            It iterates through all valid locations, simulates dropping an AI piece there, 
            and calls minimax recursively with reduced depth. 
            The function keeps track of the highest score found to 
            skip evaluating branches that won't be chosen.
            
            Hint:
            1.  you can refer to the function of 'pick_best_move'
            '''
            
            

        else: # Minimizing player
            
            ### [TODO-3]
            
            '''
            For the human player, this part aims to minimize the score. 
            It similarly iterates through valid moves, simulates them, and calls minimax recursively, 
            this time trying to find and keep the minimum score.
            
            Hint:
            1.  you can refer to the function of 'pick_best_move'
            '''
            
            

class ConnectFour_Minimax_Pruning(ConnectFour): 
    
    def __init__(self):
        super().__init__()
        
    def minimax_pruning(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            
            ### [TODO-1]
            '''
            If the depth is 0 or the node is terminal (indicating a win, lose, or tie state), 
            the function returns the heuristic value of the node. 
            Wins and losses have large positive or negative values, respectively.
            '''
            
            
        if maximizingPlayer:
            
            ### [TODO-2]
            '''
            When the function is evaluating the AI's move, it needs to maximize the score.
            It iterates through all valid locations, simulates dropping an AI piece there, 
            and calls minimax recursively with reduced depth. 
            The function keeps track of the highest score found and uses alpha-beta pruning to 
            skip evaluating branches that won't be chosen.
            
            Hint:
            1.  you can refer to the function of 'pick_best_move'
            '''
            
           

        else: # Minimizing player
            
            ### [TODO-3]
            
            '''
            For the human player, this part aims to minimize the score. 
            It similarly iterates through valid moves, simulates them, and calls minimax recursively, 
            this time trying to find and keep the minimum score and apply alpha-beta prunning.
            
            Hint:
            1.  you can refer to the function of 'pick_best_move'
            '''
            
           


