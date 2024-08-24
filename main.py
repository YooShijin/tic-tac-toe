import sys
import copy
import pygame

from constants import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')

def get_empty_sqrs(board):
        empty_squares = []
        
        # Iterate over the rows
        for row in range(len(board)):
            # Iterate over the columns
            for col in range(len(board[row])):
                # Check if the square is empty (assuming 0 represents an empty square)
                if board[row][col] == 0:
                    # Add the (row, col) tuple to the empty_squares list
                    empty_squares.append((row, col))
        return empty_squares
def is_board_full(board):
        for row in range(3):
            for col in range(3):
                if board[row][col] == 0:
                    return False
        return True
class AI():
    def __init__(self, game):
        self.game = game 
    def minMax(self, board, player, m):
        if is_board_full(board) and not self.game.check_win(board,player%2 +1):
            return 0
        if self.game.check_win(board,player%2 +1):
            return m
        
        
        if(m == 1):
            eval = -100
            for row, col in get_empty_sqrs(board):
                temp_board = copy.deepcopy(board)
                temp_board[row][col] = player
                score = self.minMax(temp_board, player%2 + 1, m*(-1))
                eval = max(eval, score)
                return eval
        else:
            eval = 100
            for row, col in get_empty_sqrs(board):
                temp_board = copy.deepcopy(board)
                temp_board[row][col] = player
                score = self.minMax(temp_board, player%2 + 1, m*(-1))
                eval = min(eval, score)
                return eval
    def bestValue(self, board, player):
        best_score =  100
        best_move = (-1, -1)
        empty_board = get_empty_sqrs(board)
        for row, col in empty_board:
            temp_board = copy.deepcopy(board)
            temp_board[row][col] = player
            m = -1 if player == 2 else 1
            score = self.minMax(board, player%2 +1 , m * (-1))
            if(player == 2):
                if score < best_score:
                    best_score = score
                    best_move = (row, col)
            else:
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
        return best_move

class Game:
    def __init__(self):
        self.ai = AI(self)
        self.board = [[0] * 3 for _ in range(3)]  # 3x3 grid initialized with 0
        self.player = 1  # Player 1 is X, Player 2 is O
        self.game_over = False
        self.draw_lines()

    def draw_lines(self):
        screen.fill(BG_COLOR)
        pygame.draw.line(screen, LINE_COLOR, [WIDTH/3, 0], [WIDTH/3,HEIGHT ], 9)
        pygame.draw.line(screen, LINE_COLOR, [(WIDTH/3)*2, 0], [(WIDTH/3*2),HEIGHT ], 9)
        pygame.draw.line(screen, LINE_COLOR, [0, HEIGHT/3], [WIDTH, HEIGHT/3], 9)
        pygame.draw.line(screen, LINE_COLOR, [0, (HEIGHT/3)*2], [WIDTH, (HEIGHT/3)*2], 9)
    



    def mark_square(self, row, col, player):
            self.board[row][col] = player

    def available_square(self, row, col):
        return self.board[row][col] == 0
    
    

    def draw_square(self,x,y,player):
        if(player == 2):
            pygame.draw.circle(screen, CIRC_COLOR, [x*(WIDTH//3) + WIDTH/6 , y*(HEIGHT//3) + HEIGHT/6 ], 35, 8)
            self.mark_square(x,y,player)
            return
        
        if(not self.available_square(x//(WIDTH//3), y//(HEIGHT//3))):
            print("Invalid square")
            return
        self.mark_square(x//(WIDTH//3), y//(HEIGHT//3),player)
        if(x< WIDTH/3):
            x = WIDTH/6

        elif(x<(WIDTH/3)*2):
            x = (WIDTH/3) + WIDTH/6
        else:
            x = (WIDTH/3)*2 + WIDTH/6

        if(y< HEIGHT/3):
            y = HEIGHT/6

        elif(y<(HEIGHT/3)*2):
            y = (HEIGHT/3) + HEIGHT/6
        else:
            y = (HEIGHT/3)*2 + HEIGHT/6
        
        pygame.draw.line(screen, CROSS_COLOR, [x-30, y-30], [x+30, y+30], 8)
        pygame.draw.line(screen, CROSS_COLOR, [x-30, y+30], [x+30, y-30], 8)
           



    
    def check_win(self, board,player):
        # Vertical win check
        for col in range(3):
            if board[0][col] == player and board[1][col] == player and board[2][col] == player:
                self.draw_vertical_winning_line(col, player)
                return True

        # Horizontal win check
        for row in range(3):
            if board[row][0] == player and board[row][1] == player and board[row][2] == player:
                self.draw_horizontal_winning_line(row, player)
                return True

        # Ascending diagonal win check
        if board[2][0] == player and board[1][1] == player and board[0][2] == player:
            self.draw_ascending_diagonal(player)
            return True

        # Descending diagonal win check
        if board[0][0] == player and board[1][1] == player and board[2][2] == player:
            self.draw_descending_diagonal(player)
            return True

        return False
    
    def draw_vertical_winning_line(self, col, player):
        arr = [WIDTH//6,(WIDTH//3) + WIDTH//6, (WIDTH//3)*2 + WIDTH//6]
        color = LOSS_COLOR if player == 2 else WIN_COLOR
        pygame.draw.line(screen, color, (arr[col],15 ), ( arr[col],HEIGHT - 15), 10)
        

    def draw_horizontal_winning_line(self, row, player):
        arr = [HEIGHT//6,(HEIGHT//3) + HEIGHT//6, (HEIGHT//3)*2 + HEIGHT//6]
        color = LOSS_COLOR if player == 2 else WIN_COLOR
        pygame.draw.line(screen, color, (arr[row],15 ), ( arr[row],WIDTH - 15), 10)
        

    def draw_ascending_diagonal(self, player):
        color = LOSS_COLOR if player == 2 else WIN_COLOR
        pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 10)

    def draw_descending_diagonal(self, player):
        color = LOSS_COLOR if player == 2 else WIN_COLOR
        pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 10)
    
    def restart(self):
        self.__init__()

        
    
    








        
def print_board(board):
    for row in board:
        print(' | '.join(str(cell) for cell in row))
        print('-' * (len(board[0]) * 4 - 1))  # Adjust for vertical lines

def main():
    game = Game()
    ai = game.ai

    while True:
        if(game.player == 2 and not game.game_over):
            row,col = ai.bestValue(game.board,game.player)
            game.draw_square(row,col, game.player)
            print(row,col)
            if is_board_full(game.board) or game.check_win(game.board,game.player):
                game.game_over = True
            game.player = 2 if game.player == 1 else 1  # Switch players
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                mouseX = event.pos[0]  # X coordinate
                mouseY = event.pos[1]  # Y coordinate
                print(mouseX,mouseY)
                game.draw_square(mouseX,mouseY, game.player)
                if is_board_full(game.board) or game.check_win(game.board,game.player):
                    game.game_over = True
                game.player = 2 if game.player == 1 else 1  # Switch players
                    
                
            pygame.display.update()
            
        

main()