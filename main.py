
import copy

""" Simple TICTACTOE Game Class """

class TicTacToe(object):
    
    def start(self):
        elapsed_turns = 0

        board = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']]

        turn_player = 'x'

        while elapsed_turns <= 9:

            #TODO: ADD MINIMAX
            print(turn_player + " turn!")

            self.print_board(board)

            if(turn_player == 'x'):

                coord_x = int(input("Coordinate 1: "))
                coord_y = int(input("Coordinate 2: "))

                #TODO: VALIDATE INPUTS

                
            
            else:
                #AI - Minimax application

                move = best_move(board)
                coord_x, coord_y = move[0], move[1]



            board[coord_x][coord_y] = turn_player

            win_result = self.checkwin(board)

            if(win_result == 1):
                print("Player x won")
                self.print_board(board)
                return elapsed_turns
            elif(win_result == 2):
                print("Player o won")
                self.print_board(board)
                return elapsed_turns

            if(turn_player == 'x'):
                turn_player = 'o'
            else:
                turn_player = 'x'

            elapsed_turns+=1
            
        return elapsed_turns

    def print_board(self, board): #TODO: REMOVE THIS
        for row in board:
            for elem in row:
                print(elem, end=" ")
            print("")
        
    def checkwin(self, board):
        #1 - player 1; 2 - player 2; 0 - not yet
        for row in board:
            if(row == ['x','x','x']):
                return 1
            elif(row == ['o', 'o', 'o']):
                return 2
        
        for i in range(len(board)):
            column = [row[i] for row in board]
            if(column == ['x','x','x']):
                return 1
            elif(column == ['o', 'o', 'o']):
                return 2

        diag_1 = []
        diag_2 = []
        idx = 0

        for row in board:
            diag_1.append(row[idx])
            diag_2.append(row[(len(row) - 1 - idx)])
            idx+=1
        
        if ['x', 'x', 'x'] in [diag_1, diag_2]:
            return 1
        
        if ['o', 'o', 'o'] in [diag_1, diag_2]:
            return 2

        return 0
        


class BoardNode(object):

    def __init__(self, board):
        self.board = board
        self.eval = None
        self.children = [] #Array of boards
        self.move = []
        self.player = None


    """" Fills the children to be used as base for calculating the best """
    def compute_possible_moves(self, current_player = 'o'):

        
        for i, row in enumerate(self.board):
            for j, elem in enumerate(row):
                if elem == ' ':

                    #print(i, j, elem)
                    childboard = copy.deepcopy(self.board)
                    childboard[i][j] = current_player

                    childnode = BoardNode(childboard)
                    childnode.move = [i, j]

                    self.children.append(childnode)


        


    def compute_all_possible_moves(self, current_player = 'o'):

        if self.is_terminal(): # Unnecessary to compute possible moves if its a terminal board
            return

        self.compute_possible_moves(current_player)

        if(current_player == 'o'):
            current_player = 'x'
        else:
            current_player = 'o'

        for child_node in self.children:
            child_node.compute_all_possible_moves(current_player)


    def is_terminal(self):
        #TODO: MERGE WITH CHECKWIN
        #1 - player 1; 2 - player 2; 0 - not yet
        for row in self.board:
            if(row == ['x','x','x']):
                return True
            elif(row == ['o', 'o', 'o']):
                return True
        
        for i in range(len(self.board)):
            column = [row[i] for row in self.board]
            if(column == ['x','x','x']):
                return True
            elif(column == ['o', 'o', 'o']):
                return True

        diag_1 = []
        diag_2 = []
        idx = 0

        for row in self.board:
            diag_1.append(row[idx])
            diag_2.append(row[(len(row) - 1 - idx)])
            idx+=1
        
        if ['x', 'x', 'x'] in [diag_1, diag_2]:
            return True
        
        if ['o', 'o', 'o'] in [diag_1, diag_2]:
            return True

        return False

    def print_board(self):
        for row in self.board:
            for elem in row:
                print(elem, end=" ")
            print("")

    def print_tree(self):
        
        self.print_board()

        print(" ")
        #print(utility(self.board, 'o'))

        for child_node in self.children:
            child_node.print_tree()
    
class BoardTree(object):

    def __init__(self):
        self.root = BoardNode([
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']])



""" Receives a board and evaluates it. Returns the normalized result """

def utility(board, current_player = 'o'):
    #Heuristics go here
    score = 0

    for row in board:
        if row == [current_player, current_player, current_player]:
            score = 1
            return score # Special case: doesnt need to proceed
        if (row.count(current_player) == 2 and row.count(' ') == 1):
            score += 0.2
        if (row.count(current_player) == 1 and row.count(' ') == 2):
            score += 0.1

    for i in range(len(board)):
        column = [row[i] for row in board]
        #print(column)

        if column == [current_player, current_player, current_player]:
            score = 1
            return score # Special case: doesnt need to proceed
        if (column.count(current_player) == 2 and column.count(' ') == 1):
            score += 0.2
        if (column.count(current_player) == 1 and column.count(' ') == 2):
            score += 0.1

    diag_1 = []
    diag_2 = []
    idx = 0

    for row in board:
        diag_1.append(row[idx])
        diag_2.append(row[(len(row) - 1 - idx)])
        idx+=1

    #print(diag_1)
    #print(diag_2)

    if [current_player, current_player, current_player] in [diag_1, diag_2]:
        score = 1
        return score # Special case: doesnt need to proceed

    if (diag_1.count(current_player) == 2 and diag_1.count(' ') == 1):
        score += 0.2
    if (diag_2.count(current_player) == 2 and diag_2.count(' ') == 1):
        score += 0.2

    #TODO: add more strategic rules, maybe?
    #TODO: DEFENSIVE STRATEGY?

    #Naive normalization

    if score >= 1:
        score = 0.9

    return score

def min(board_node):

    if(board_node.children == [] or board_node.is_terminal()): #TODO: ADD DEPTH LIMIT
        board_node.eval = utility(board_node.board)
        return board_node
    
    board_node.eval = 100

    for child_node in board_node.children:
        max(child_node)

        #Storing at the tree itself
        if child_node.eval < board_node.eval:
            board_node.eval = child_node.eval
            
    return board_node

def max(board_node):
    
    if(board_node.children == [] or board_node.is_terminal()): #TODO: ADD DEPTH LIMIT
        board_node.eval = utility(board_node.board)
        return board_node
    
    board_node.eval = -100
    #current_best_move = []

    for child_node in board_node.children:
        min(child_node)

        if child_node.eval > board_node.eval:
            board_node.eval = child_node.eval
            
    return board_node



def minimax(board_node):

    board_node.compute_all_possible_moves()
    #board_node.print_tree() #ATTENTION, ONLY EXECUTE FOR FEW RESULTS

    #print(board_node.is_terminal())

    #Calls max at start because minimax  will always be used for the "computer player"
    #print(max(board_node).eval)
    maxed_node = max(board_node)

    return maxed_node

    '''for child in board_node.children:
        print(child.move, child.eval)'''

""" Wrapper for the minimax computation """
def best_move(board):

    board_node = BoardNode(board)

    maxed_node = minimax(board_node)

    #Using child node eval values from maxed to find the 'best path' computed

    current_best_move = []
    current_best_score = -100

    for child_node in maxed_node.children:
        if(current_best_score < child_node.eval):
            current_best_score = child_node.eval
            current_best_move = child_node.move

    return current_best_move


sample_board1 = [
    ['o','o', ' '],
    [' ', 'x', 'o'],
    ['x', 'x', 'o']]

sample_board2 = [
    ['1','2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9']]

#print(utility(sample_board2))

'''boardnode1 = BoardNode(sample_board1)
boardnode1.compute_possible_moves()

boardnode1.print_board()

print("CHILDREN: \n")

for node in boardnode1.children:
    node.print_board()'''

#boardnode1 = BoardNode(sample_board1)

'''boardnode1.compute_all_possible_moves()
boardnode1.print_tree()'''

#minimax(boardnode1)

#print(best_move(sample_board1))

game = TicTacToe()
game.start()