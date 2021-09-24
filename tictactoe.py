import math
import random

random.seed()


class TicTacToe:
    def __init__(self, initial_condition=None):
        # set empty game grid
        self.grid = [['_', '_', '_'],
                     ['_', '_', '_'],
                     ['_', '_', '_']]
        # set player to 'X' ( = True, 'O' = False)
        self.player = True
        if initial_condition is not None:
            initial_condition = initial_condition.upper()
            # defensive check
            if len(initial_condition) == 9 and \
                    initial_condition.count('X') + \
                    initial_condition.count('O') + \
                    initial_condition.count('_') == 9:
                # filling test with 'initial_condition' string's char,
                # parsed by blocks of 3 chars with a comprehension
                self.grid = [list(initial_condition[3 * i:3 * i + 3]) for i in range(3)]
                # defining who start
                if initial_condition.count('X') != initial_condition.count('O'):
                    self.player = False
            else:
                print('Wrong initial condition')

    def __str__(self):
        render = '---------\n'
        for i in range(3):
            render += f'| {" ".join(self.grid[i])} |\n'.replace('_', ' ')
        render += '---------'
        return render
        # use case:
        # ---------
        # | X O X |
        # |   O X |
        # | O   X |
        # ---------
        #

    # --- Getters -----------------------------------------

    def has_initial_condition(self):
        return self.grid.count(['_', '_', '_']) != 3

    def get_turn_player(self):
        return 'X' if self.player else 'O'

    def get_string_grid(self):
        string_grid = ''
        for row in self.grid:
            string_grid += ''.join(row)
        return string_grid

    # --- Game core ---------------------------------------

    def place_move(self, coordinates):
        coordinates_list = coordinates.split()
        if len(coordinates_list) != 2:
            return 'not_coordinates_pair'
        x, y = coordinates_list
        if not x.isdigit() or not y.isdigit():
            return 'not_number_symbol'
        x, y = int(x) - 1, int(y) - 1
        if x < 0 or x > 2 or y < 0 or y > 2:
            return 'out_of_range'
        if self.grid[x][y] != '_':
            return 'occupied_cell'
        self.grid[x][y] = 'X' if self.player else 'O'
        self.player = not self.player
        return self.game_state(x, y)

    def undo_move(self, coordinates):
        x, y = coordinates[0] - 1, coordinates[1] - 1
        self.grid[x][y] = '_'
        self.player = not self.player

    def game_state(self, x, y):
        # player who made the previous move
        possible_winner = not self.player
        # check win on vertical line
        if self.grid[0][y] == self.grid[1][y] == self.grid[2][y]:
            return 'X' if possible_winner else 'O'
        # check win on horizontal line
        if self.grid[x][0] == self.grid[x][1] == self.grid[x][2]:
            return 'X' if possible_winner else 'O'
        # check win on the main diagonal
        if x == y and self.grid[0][0] == self.grid[1][1] == self.grid[2][2]:
            return 'X' if possible_winner else 'O'
        # check win on the secondary diagonal
        if x + y == 2 and self.grid[0][2] == self.grid[1][1] == self.grid[2][0]:
            return 'X' if possible_winner else 'O'
        # check if a cell is empty
        string_grid = self.get_string_grid()
        if string_grid.count('_'):
            return 'not_finished'
        else:
            return 'draw'

    # --- Strategical analysis ----------------------------

    def get_coordinates(self, difficulty):
        if difficulty == 'easy':
            random_coordinates = self.get_random_coordinates()
            return f'{random_coordinates[0]} {random_coordinates[1]}'
        elif difficulty == 'medium':
            relevant_coordinates = self.get_relevant_coordinates()
            return f'{relevant_coordinates[0]} {relevant_coordinates[1]}'
        else:  # difficulty == 'hard':
            best_coordinates = self.get_best_coordinates()
            return f'{best_coordinates[0]} {best_coordinates[1]}'

    def get_blank_coordinates(self):
        string_grid = self.get_string_grid()
        blank_coordinates = [(position // 3 + 1, position % 3 + 1) for position in range(9)
                             if string_grid[position] == '_']
        return blank_coordinates

    # -- Easy strategy --------------------------

    def get_random_coordinates(self):
        return random.choice(self.get_blank_coordinates())

    # -- Medium strategy ------------------------

    def get_relevant_coordinates(self):
        blank_coordinates = self.get_blank_coordinates()
        neighbours = [(1, 2), (0, 2), (0, 1)]
        for coordinates in blank_coordinates:
            row, column = coordinates[0] - 1, coordinates[1] - 1
            # check possible action on horizontal line
            # by watching neighbours provided by the pair
            # in the neighbours list
            if self.grid[row][neighbours[column][0]] == self.grid[row][neighbours[column][1]] != '_':
                return coordinates
            # check possible action on vertical line
            if self.grid[neighbours[row][0]][column] == self.grid[neighbours[row][1]][column] != '_':
                return coordinates
            # check possible action on first diagonal
            if row == column and \
                    self.grid[neighbours[row][0]][neighbours[column][0]] == \
                    self.grid[neighbours[row][1]][neighbours[column][1]] != '_':
                return coordinates
            # check possible action on second diagonal
            if row + column == 2 and \
                    self.grid[neighbours[row][0]][neighbours[column][1]] == \
                    self.grid[neighbours[row][1]][neighbours[column][0]] != '_':
                return coordinates
        return random.choice(blank_coordinates)

    # -- Hard strategy --------------------------

    def get_best_coordinates(self):
        computer_player = 'X' if self.player else 'O'
        best_score = -math.inf
        best_coordinates = None
        for coordinates in self.get_blank_coordinates():
            move_result = self.place_move(f'{coordinates[0]} {coordinates[1]}')
            score = self.min_max_algorithm(move_result, computer_player)
            self.undo_move(coordinates)
            if score > best_score:
                best_score = score
                best_coordinates = coordinates
        return best_coordinates

    def min_max_algorithm(self, move_result, computer_player, maximizing=False):
        if move_result == 'draw':
            return 0
        elif move_result != 'not_finished':
            return 1 if computer_player == move_result else -1

        scores = []
        for coordinates in self.get_blank_coordinates():
            move_result = self.place_move(f'{coordinates[0]} {coordinates[1]}')
            scores.append(self.min_max_algorithm(move_result, computer_player, not maximizing))
            self.undo_move(coordinates)

        return max(scores) if maximizing else min(scores)


# === FUNCTIONAL EXECUTION ==========================================

def new_game():
    game = TicTacToe()
    while True:
        command = input('Input command: ').lower().split()
        # check if a preset grid is given, then overwrite the existing one
        # then restart cycle for another overwrite or starting the game
        if command[0] == 'preset':
            game = TicTacToe(command[1])
            print(game)
            continue

        if command[0] == 'start' and len(command) == 3 and \
                command[1] in ['user', 'easy', 'medium', 'hard'] and \
                command[2] in ['user', 'easy', 'medium', 'hard']:
            print(game)
            break
        elif command[0] == 'exit':
            return None
        else:
            print('Bad parameters!')
            continue
    return game, command[1], command[2]


def play(game_settings):
    game, x_player, o_player = game_settings
    while True:
        turn_player = game.get_turn_player()
        # manual or auto X player move
        if (x_player == 'user' and turn_player == 'X') or \
                (o_player == 'user' and turn_player == 'O'):
            coordinates = input('Enter the coordinates: ')
            move_result = game.place_move(coordinates)
        else:
            auto_move_difficulty = x_player if turn_player == "X" else o_player
            print(f'Making move level "{auto_move_difficulty}"')
            coordinates = game.get_coordinates(auto_move_difficulty)
            move_result = game.place_move(coordinates)

        # continuation case
        if move_result == 'not_finished':
            print(game)
            continue
        # conclusion cases
        if move_result == 'draw':
            print(game)
            print('Draw\n')
            break
        if move_result == 'X':
            print(game)
            print('X wins\n')
            break
        if move_result == 'O':
            print(game)
            print('O wins\n')
            break
        # wrong input
        if move_result == 'not_number_symbol' or \
                move_result == 'not_coordinates_pair':
            print('You should enter numbers!')
            continue
        if move_result == 'out_of_range':
            print('Coordinates should be from 1 to 3!')
            continue
        if move_result == 'occupied_cell':
            print('This cell is occupied! Choose another one!')
            continue


# === INIT ==========================================================

def init():
    while True:
        game_settings = new_game()
        if game_settings is None:
            break
        play(game_settings)


init()
