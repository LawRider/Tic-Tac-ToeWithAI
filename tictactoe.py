from random import randint
from operator import itemgetter


class TicTacToe:
    def __init__(self):
        self.iterator = None
        self.inp = None
        self.symbol = None
        self.board = {'11': 0, '12': 1, '13': 2,
                      '21': 3, '22': 4, '23': 5,
                      '31': 6, '32': 7, '33': 8}
        self.win_combos = [[0, 1, 2], [3, 4, 5], [6, 7, 8],  # horizontal lines
                           [0, 3, 6], [1, 4, 7], [2, 5, 8],  # vertical lines
                           [0, 4, 8], [2, 4, 6]]  # diagonal lines

    def menu(self):
        while True:
            args = input('Input command: ').lower().split()
            if args[0] == 'exit':
                exit()
            elif len(args) != 3:
                print('Bad parameters!')
                continue
            else:
                self.iterator = iter(args[1:] * 10)
                self.inp = list(' ' * 9)
                self.symbol = ('X', 'O')
                self.print_board()

    def print_board(self):
        cells = self.inp
        print('-' * 9)
        for i in range(0, 8, 3):
            print(f'| {cells[i]} {cells[i + 1]} {cells[i + 2]} |')
        print('-' * 9)
        self.check_status()

    def check_status(self):
        result = self.is_end()
        if result is not None:
            if result == ' ':
                print('Draw')
            else:
                print(f'{result} wins')
            self.menu()
        self.game()

    def is_end(self):
        # For each of win combinations, check corresponding elements
        # of board (self.inp) if there are 3 'X' or 'O' in a row
        for combo in self.win_combos:
            rows = itemgetter(*combo)(self.inp)
            if rows.count('X') == 3:
                return 'X'
            elif rows.count('O') == 3:
                return 'O'
        if ' ' in self.inp:
            return None
        return ' '

    def game(self):
        next_move = next(self.iterator)
        if next_move == 'user':
            self.human_play()
        else:
            self.ai_play(next_move)

    def human_play(self):
        try:
            # Converted to int and then to str to raise exception
            # if user entered not numbers
            inp_coord = [int(_) for _ in input('Enter the coordinates: ').split()]
            coord = ''.join([str(_) for _ in inp_coord])
            try:
                if self.inp[self.board[coord]] != ' ':
                    print('This cell is occupied! Choose another one!')
                    return self.human_play()
                else:
                    return self.move(coord)
            except KeyError:
                print('Coordinates should be from 1 to 3!')
                return self.human_play()
        except ValueError:
            print('You should enter numbers!')
            return self.human_play()

    def ai_play(self, level):
        print(f'Making move level "{level}"')
        if level == 'easy':
            self.easy_logic()
        elif level == 'medium':
            self.medium_logic()
        elif level == 'hard':
            self.hard_logic()

    def easy_logic(self):
        while True:
            index = randint(0, 8)
            if self.inp[index] == ' ':
                # Get appropriate key (coordinates) for an index
                self.move(list(self.board.keys())[index])

    def medium_logic(self):
        # For each of win combinations, check corresponding elements
        # of board (self.inp) if there is 1 empty cell to proceed
        for combo in self.win_combos:
            if itemgetter(*combo)(self.inp).count(' ') == 1:
                for index in combo:
                    if self.inp[index] == ' ':
                        self.move(list(self.board.keys())[index])
        self.easy_logic()

    def hard_logic(self):
        while True:
            if self.symbol[0] == 'X':
                _, index = self.min()
            else:
                _, index = self.max()
            self.move(list(self.board.keys())[index])

    def min(self):
        # Possible values for minv are:
        # -1 - win
        # 0  - draw
        # 1  - loss
        # We're initially setting it to 2 as worse than the worst case:
        minv = 2
        index = None
        result = self.is_end()

        # If the game came to an end, the function needs to return
        # the evaluation function of the end. That can be:
        # -1 - loss
        # 0  - draw
        # 1  - win
        if result == 'X':
            return -1, 0
        elif result == 'O':
            return 1, 0
        elif result == ' ':
            return 0, 0

        for i in range(0, 9):
            if self.inp[i] == ' ':
                self.inp[i] = 'X'
                m, max_i = self.max()
                if m < minv:
                    minv = m
                    index = i
                self.inp[i] = ' '

        return minv, index

    def max(self):
        # Possible values for maxv are:
        # -1 - loss
        # 0  - draw
        # 1  - win
        # We're initially setting it to -2 as worse than the worst case:
        maxv = -2
        index = None
        result = self.is_end()

        if result == 'X':
            return -1, 0
        elif result == 'O':
            return 1, 0
        elif result == ' ':
            return 0, 0

        for i in range(0, 9):
            if self.inp[i] == ' ':
                # On the empty field player 'O' makes a move and calls Min
                # That's one branch of the game tree.
                self.inp[i] = 'O'
                m, min_i = self.min()
                # Fixing the maxv value if needed
                if m > maxv:
                    maxv = m
                    index = i
                # Setting back the field to empty
                self.inp[i] = ' '

        return maxv, index

    def move(self, input_coord):
        self.inp[self.board[input_coord]] = self.symbol[0]
        self.symbol = self.symbol[::-1]
        self.print_board()


if __name__ == '__main__':
    tictactoe = TicTacToe()
    tictactoe.menu()
