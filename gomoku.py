from random import randint


class Gomoku:
    def __init__(self, size=19, pvp_mode = 1, machine_turn = 0):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.current_player = 2
        self.moves = 0
        self.pvp_mode = pvp_mode
        self.machine_turn = machine_turn
        self.x = 0
        self.y = 0
    
    def print_board(self):
        i = 1
        print()
        for row in self.board:
            if i < 10:
                print("0", i, sep = "", end=" ")
            else:
                print(i, end=" ")
            i += 1
            for column in row:
                if column == 1:
                    print("●", end="   ")
                elif column == 2:
                    print("⓪", end="   ")
                else:
                    print("ᚔ", end="   ")
            print()
            print()
        print("  ", end=" ")
        i = 1
        while i <= len(self.board):
            if i < 10:
                print("0", i, sep = "", end="  ")
            else:
                print(i, end="  ")
            if i % 4 == 0:
                print("", end=" ")
            i += 1
        print()
        print()
    
    def find_win(self):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for target in [1, -1]:
                nx, ny = self.x + target * dx, self.y + target * dy
                while 0 <= nx < self.size and 0 <= ny < self.size and self.board[ny][nx] == self.current_player:
                    count += 1
                    nx += target * dx
                    ny += target * dy
            if count >= 5:
                return True
        return False


def play_match():
    
    pvp_mode = int(input('Jogador x Máquina (0) ou Jogador x jogador (1)? '))
    if not pvp_mode:
        machine_turn = int(input('Quem começa? Você (0) ou a Máquina (1)? '))
        game = Gomoku(19, pvp_mode, machine_turn)
    else:
        game = Gomoku(19, pvp_mode)
    game.print_board()


    while not game.find_win() and game.moves < 361:
        if game.current_player == 1:
            game.current_player = 2
        else:
            game.current_player = 1
        if game.machine_turn:
            print('Vez da máquina!')
            validation = False
            while not validation:
                game.y = randint(0, 18)
                game.x = randint(0, 18)
                if not game.board[game.y][game.x]:
                    game.board[game.y][game.x] = game.current_player
                    
                    print(f'A maquina jogou... {game.y+1} e {game.x+1}!')
                    print()
                    validation = True
            game.machine_turn = 0
        else:
            if game.pvp_mode:
                print(f'Vez do jogador {game.current_player}!')
            else:
                print('Sua vez!')
            validation = False
            while not validation:
                game.y = int(input('Escolha a linha: ')) - 1
                while game.y < 0 or game.y > 18:
                    game.y = int(input('Posição inválida, tente novamente: ')) - 1 
                game.x = int(input('Escolha a coluna: ')) - 1
                while game.x < 0 or game.x > 18:
                    game.x = int(input('Posição inválida, tente novamente: ')) - 1 
                if game.board[game.y][game.x]:
                    print('Esta posição já foi preenchida! Tente outra...')
                else:
                    print('Jogada Validada!')
                    print()
                    game.board[game.y][game.x] = game.current_player
                    validation = True
            if not game.pvp_mode:
                game.machine_turn = 1
        game.moves += 1
        game.print_board()
        print(game.machine_turn)

    if game.moves == 361:
        print('É... vocês conseguiram empatar.')
    elif game.pvp_mode:
        print(f'Parabéns, jogador {game.current_player}, você venceu!')        
    elif game.machine_turn:
        print('Parabéns, você venceu!')
    else:
        print('Não foi dessa vez, a máquina venceu...')


play_match()



