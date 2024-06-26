import math
from GameRepresentation import GameBoard
from Player import Player
from Move import Move
class Computer(Player):
    def __init__(self, color):
        super().__init__(color)
        self.played = None

    # Alpha-Beta Pruning 
    def alpha_beta(self, board, depth, alpha, beta, maximizing):
        # if the depth is 0 or the game is over, return the utility of the board
        if depth == 0 or board.is_game_over():
            return board.get_utility(self.color) 

        if maximizing:
            maxVal = -math.inf 
            # get all available moves for the current player
            available_moves = Move(board.board).get_available_moves(self) 
            # if there are no available moves, pass the turn to the other player
            if not available_moves:
                return self.alpha_beta(board, depth-1, alpha, beta, False)
            played_moves = {}
            # for each available move, create a new board and call the alpha_beta function recursively
            for move in available_moves:
                tmpBoard = GameBoard()
                # copy the ND array by value
                tmpBoard.board = board.board.copy()
                tmpBoard.player1 = board.player1
                tmpBoard.player2 = board.player2
                # make the move on the new board
                Move(tmpBoard.board).move(move[0], move[1], self)
                # get the value after making the move 
                val = self.alpha_beta(tmpBoard, depth - 1, alpha, beta, False)
                # store the move and its value
                played_moves[val] = move
                # update the max value
                maxVal = max(maxVal, val)
                # update alpha
                alpha = max(alpha, val)
                # prune the tree condition
                if beta <= alpha:
                    break

            if maxVal != -math.inf: 
                # get the move that corresponds to the max value 
                self.played = played_moves.get(maxVal, None)
            return maxVal
    
        else: 
            # get the other player
            otherPlayer = board.player1 if self.color == board.player2.color else board.player2
            minVal = math.inf
            available_moves = Move(board.board).get_available_moves(otherPlayer)
            if not available_moves:
                return self.alpha_beta(board, depth-1, alpha, beta, True)
            
            for move in available_moves:
                tmpBoard = GameBoard()
                tmpBoard.board = board.board.copy()
                tmpBoard.player1 = board.player1
                tmpBoard.player2 = board.player2
                Move(tmpBoard.board).move(move[0], move[1], otherPlayer)
                val = self.alpha_beta(tmpBoard, depth - 1, alpha, beta ,True)
                minVal = min(minVal, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break
                
            return minVal
        
    def set_depth(self, depth):
        self.depth = depth
        
    def play(self, board):
        # reset the played move
        self.played = None
        # create a temporary board
        tmpBoard = GameBoard()
        tmpBoard.board = board.board.copy()
        tmpBoard.player1 = board.player1
        tmpBoard.player2 = board.player2
        # call the alpha_beta function
        self.alpha_beta(tmpBoard, self.depth, -math.inf, math.inf, True)
        print("Computer played: ", self.played)
        return self.played