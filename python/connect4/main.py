import numpy as np
import pygame
import sys
import math

from sal_timer import timer


class Constant:
    # colors ...
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)

    # shapes size ...
    SQUARESIZE = 100
    RADIUS = int(SQUARESIZE/2 - 5)

    # dims ...
    ROW_COUNT = 6
    COLUMN_COUNT = 7
    WIDTH = COLUMN_COUNT * SQUARESIZE
    HEIGHT = (ROW_COUNT + 1) * SQUARESIZE
    SIZE = (WIDTH, HEIGHT)

    # states ...
    GAME_OVER = False
    PLAYER_TURN = 0
    GAME_OVER_TIME_WAIT = 3000

    # values ...
    PIECE_VALUE_TO_IGNORE = -100
    NO_PLAYER_PIECE_VALUE = 0
    FIRST_PLAYER_PIECE_VALUE = 1
    SECOND_PLAYER_PIECE_VALUE = 2

    @staticmethod
    def get_current_piece_value():
        return {
            '0': Constant.FIRST_PLAYER_PIECE_VALUE,
            '1': Constant.SECOND_PLAYER_PIECE_VALUE,
        }.get(str(Constant.PLAYER_TURN), Constant.NO_PLAYER_PIECE_VALUE)

    @staticmethod
    def is_game_over():
        if Constant.GAME_OVER:
            pygame.time.wait(Constant.GAME_OVER_TIME_WAIT)


class Board:
    def __init__(self, screen):
        # args ...
        self.screen = screen

        # const ...
        self.ROW_COUNT = Constant.ROW_COUNT
        self.COLUMN_COUNT = Constant.COLUMN_COUNT
        # fonts ...
        self.FONT_1 = pygame.font.SysFont("monospace", 75)

        # factor ....
        self.board = self.create_board()
        self.print_board()

    def create_board(self):
        return np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))

    def print_board(self):
        print('-'*10, 'BOARD', '-'*10)
        # print(self.board)
        print(np.flip(self.board, 0))
        print('-' * 27)
        print('CURRENT PLAYER : <{}>'.format(Constant.PLAYER_TURN))
        print(self.get_board_hash())

    def get_board_hash(self):
        return self.board.flatten()

    def draw_board(self):
        # ...
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                # ...
                self.draw_rect(c, r)
                self.draw_black_circle(c, r)

        # TODO ...
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == 1:
                    self.draw_red_circle(c, r)
                elif self.board[r][c] == 2:
                    self.draw_yellow_circle(c, r)

        # ...
        # pygame.display.update()

    def draw_header(self):
        # ...
        pygame.draw.rect(
            self.screen,
            Constant.BLACK,
            (
                0,
                0,
                Constant.WIDTH,
                Constant.SQUARESIZE
            )
        )

        # ...
        for num in range(Constant.COLUMN_COUNT):
            label = self.FONT_1.render(str(num), 2222, Constant.RED)
            self.screen.blit(label, (num * (Constant.WIDTH / Constant.COLUMN_COUNT) + 5, 10))

    def draw_rect(self, col, row):
        '''
            # 1. draws a rectangle
            # https://stackoverflow.com/questions/19780411/pygame-drawing-a-rectangle
            #
            pygame.draw.rect(screen, [red, blue, green], [left, top, width, height], filled)

            # 2.draws a rectangle
            # https://sites.cs.ucsb.edu/~pconrad/cs5nm/topics/pygame/drawing/
            #
            pygame.draw.rect(screen, colour, (x,y,width,height), thickness)
                1. (x,y,width,height) is a Python tuple
                2. x,y are the coordinates of the upper left hand corner
                3. width, height are the width and height of the rectangle
                4. thickness is the thickness of the line. If it is zero, the rectangle is filled
        '''
        pygame.draw.rect(
            self.screen,
            Constant.BLUE,
            (
                col * Constant.SQUARESIZE,
                row * Constant.SQUARESIZE + Constant.SQUARESIZE,
                Constant.SQUARESIZE,
                Constant.SQUARESIZE
            )
        )

    def draw_black_circle(self, col, row):
        '''
            # 1. draws a circle
            # https://sites.cs.ucsb.edu/~pconrad/cs5nm/topics/pygame/drawing/
            #
            pygame.draw.circle(screen, color, (x,y), radius, thickness)
                1. (x,y) is a Python tuple for the center,
                2. radius is the radius
                3. thickness is the thickness of the line. If it is zero, the rectangle is filled
        '''
        pygame.draw.circle(
            self.screen,
            Constant.BLACK,
            (
                int(col * Constant.SQUARESIZE + Constant.SQUARESIZE / 2),
                int(row * Constant.SQUARESIZE +
                    Constant.SQUARESIZE + Constant.SQUARESIZE / 2)
            ),
            Constant.RADIUS
        )

    def draw_red_circle(self, col, row):
        pygame.draw.circle(
            self.screen,
            Constant.RED,
            (
                int(col * Constant.SQUARESIZE + Constant.SQUARESIZE / 2),
                Constant.HEIGHT -
                int(row * Constant.SQUARESIZE + Constant.SQUARESIZE / 2)
            ),
            Constant.RADIUS
        )

    def draw_yellow_circle(self, col, row):
        pygame.draw.circle(
            self.screen,
            Constant.YELLOW,
            (
                int(col * Constant.SQUARESIZE + Constant.SQUARESIZE / 2),
                Constant.HEIGHT -
                int(row * Constant.SQUARESIZE + Constant.SQUARESIZE / 2)
            ),
            Constant.RADIUS
        )

    def print_winner_player_name(self):
        text = "Player {} wins!!".format(Constant.PLAYER_TURN)
        label = self.FONT_1.render(text, Constant.PLAYER_TURN, Constant.RED)
        self.screen.blit(label, (40, 10))

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[self.ROW_COUNT - 1][col] == 0

    def get_next_open_row(self, col):
        for r in range(Constant.ROW_COUNT):
            if self.board[r][col] == 0:
                return r

    def refresh(self):
        self.draw_board()
        pygame.display.update()


class Judge:
    def __init__(self, board):
        self.board = board.board

        # const ...
        self.ROW_COUNT = Constant.ROW_COUNT
        self.COLUMN_COUNT = Constant.COLUMN_COUNT

    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT - 3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT - 3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(3, self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True


class Player:
    def __init__(self, name, isBot=False, isIntelligent=False, model=''):
        self.name = name
        self.isBot = isBot
        self.isIntelligent = isIntelligent

    def ask_for_move(self):
        if self.isBot:
            return self.ask_bot()
        else:
            return self.ask_human()

    def ask_human(self):
        for event in pygame.event.get():
            # I. ...
            if event.type == pygame.QUIT:
                sys.exit()

            # II. ...
            if event.type == pygame.KEYDOWN:
                if event.unicode == 'q':
                    sys.exit()

                if event.unicode == '0':
                    return int(event.unicode)
                    # self.handel_action(event.unicode)

                if event.unicode == '1':
                    return int(event.unicode)
                    # self.handel_action(event.unicode)

                if event.unicode == '2':
                    return int(event.unicode)
                    # self.handel_action(event.unicode)

                if event.unicode == '3':
                    return int(event.unicode)
                    # self.handel_action(event.unicode)

                if event.unicode == '4':
                    return int(event.unicode)
                    # self.handel_action(event.unicode)

                if event.unicode == '5':
                    return int(event.unicode)
                    # self.handel_action(event.unicode)

                if event.unicode == '6':
                    return int(event.unicode)
                    # self.handel_action(event.unicode)
        return Constant.PIECE_VALUE_TO_IGNORE

    def ask_bot(self):
        if self.isIntelligent:
            pass
        else:
            return self.random_choice()

    def random_choice(self):
        return np.random.choice(list(range(0, Constant.COLUMN_COUNT)))


class Game:
    def __init__(self, player1: Player, player2: Player):
        # args ...
        self.p1 = player1
        self.p2 = player2
        self.CHANGE_PLAYER = False

        # ...
        pygame.init()
        self.screen = pygame.display.set_mode(Constant.SIZE)
        self.board = Board(self.screen)
        self.judge = Judge(self.board)

        # actions ...
        self.board.draw_board()
        self.board.refresh()

    def check_winners(self):
        if self.judge.winning_move(Constant.get_current_piece_value()):
            # label = myfont.render("Player 1 wins!!", 1, const.RED)
            # screen.blit(label, (40, 10))
            print('<>'*20)
            print('PLayer {} win !!'.format(Constant.PLAYER_TURN))
            print('<>'*20)
            Constant.GAME_OVER = True
            self.board.print_winner_player_name()

    def check_game_over(self):
        if Constant.GAME_OVER:
            pygame.time.wait(Constant.GAME_OVER_TIME_WAIT)

    def check_player_turn(self):
        if self.CHANGE_PLAYER:
            Constant.PLAYER_TURN += 1
            Constant.PLAYER_TURN = Constant.PLAYER_TURN % 2
            self.CHANGE_PLAYER = False
            self.board.print_board()

    def get_current_player(self):
        return {
            '0': self.p1,
            '1': self.p2,
        }.get(str(Constant.PLAYER_TURN), None)

    def handel_action(self, selected_col_by_player):
        # ...
        if selected_col_by_player == Constant.PIECE_VALUE_TO_IGNORE:
            return

        # ...
        if self.board.is_valid_location(selected_col_by_player):
            # ...
            selected_row_by_player = self.board.get_next_open_row(
                selected_col_by_player)

            # ...
            self.board.drop_piece(
                selected_row_by_player,
                selected_col_by_player,
                Constant.get_current_piece_value()
            )

            # ...
            self.check_winners()
            self.CHANGE_PLAYER = True
        else:
            # NOTE maybe her we should add points
            print(">>> Pleas select another column current is full <<<")
            print(">>> Still player <{}> turn <<<".format(Constant.PLAYER_TURN))
            self.CHANGE_PLAYER = False

    def start_game(self):
        while not Constant.GAME_OVER:
            selected_col_by_player = Constant.PIECE_VALUE_TO_IGNORE
            selected_col_by_player = self.get_current_player().ask_for_move()
            self.handel_action(selected_col_by_player)

            # TODO ...
            self.board.draw_header()
            self.board.refresh()
            self.check_player_turn()
            self.check_game_over()

@timer
def main():
    print('Welcome To Game Mind')
    # Bot VS Bot ...
    # bot1 = Player('Bot1', isBot=True, isIntelligent=False)
    # bot2 = Player('Bot2', isBot=True, isIntelligent=False)
    # bots_game = Game(bot1, bot2)
    # bots_game.start_game()

    # Human VS Bot...
    # player1 = Player('P1')
    # player_bot = Player('Bot', isBot=True, isIntelligent=False)
    # humans_game = Game(player1, player_bot)
    # humans_game.start_game()

    # Human VS Human...
    player1 = Player('P1')
    player2 = Player('p1')
    humans_game = Game(player1, player2)
    humans_game.start_game()


if __name__ == '__main__':
    print('========================================== START ==========================================')
    # ...
    main()
    print('========================================== END ============================================')
