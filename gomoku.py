from random import randint
from time import sleep

'''
Decidi usar duas classes nesse projeto, caso fosse uma plataforma de jogos, a classe principal Gomoku poderia ser uma subclasse de "Jogos", herdando a maioria dos atributos.
Falando sobre os atributos, o "size" serve para flexibilizar o tamanho do tabuleiro automaticamente quando ele é criado (no atributo "board", cria-se uma matriz cheia de zeros que é alterada a cada jogada).
Eu optei por deixar todos os atributos "private", para dar uma dificultada e aumentar a segurança do código, sempre consultando dentro das classes cada ação.
O restante dos atributos foi feito para dinamizar os modos de jogo e tornar funcional o modo jogador x jogador, máquina x máquina e jogador x máquina
O "x" e o "y" denotam a última jogada feita (eles são iniciados na metade do tabuleiro para sempre que a máquna começar, ela jogue perto do centro, eu também explico depois as jogadas da máquina).
Existem também alguns comandos "sleep" no código para deixar o jogo mais imersivo.
'''

class Gomoku:
    def __init__(self, size=19, pvp_mode = 1, machine_turn = False):
        self.__board = [[0 for _ in range(size)] for _ in range(size)]
        self.__size = size
        self.__pvp_mode = pvp_mode
        self.__machine_turn = machine_turn
    
    def get_props(self):
        return {"size": self.__size, "board": self.__board}
    
    def get_game_modes(self):
        return {"pvp_mode": self.__pvp_mode, "machine_turn": self.__machine_turn}

    def modify_machine_turn(self, plays_next):
        self.__machine_turn = plays_next

    def new_play(self, y, x, current_player, game_control):
        self.__board[y][x] = current_player
        game_control.put_coordinates(y, x)

    '''
    Método que exibe o tabuleiro na tela, com linhas e colunas numeradas.
    Caso o campo tenha sido preenchido, é printado "X" para o jogador 1 e "0" para o jogador 2.
    '''
    
    def print_board(self):
        i = 1
        print()
        
        for row in self.__board:
            if i < 10:
                print("0", i, sep = "", end=" ")
                
            else:
                print(i, end=" ")
            i += 1

            for column in row:
                if column == 1:
                    print("X", end="   ")
                elif column == 2:
                    print("0", end="   ")
                else:
                    print(".", end="   ")

            print()
            print()
        print("  ", end=" ")
        i = 1
        while i <= len(self.__board):
            if i < 10:
                print("0", i, sep = "", end="  ")
            else:
                print(i, end="  ")
            i += 1
            
        print()
        print()
        sleep(1)

'''
A classe Control tem como objetivo complementar a classe principal, ela verifica se o jogo ainda está em andamento e altera o jogador atual.
O "x" e o "y" denotam a última jogada feita (eles são iniciados na metade do tabuleiro para sempre que a máquna começar, ela jogue perto do centro, eu também explico depois as jogadas da máquina).
'''

class Control():
    def __init__(self, size = 19):
        self.__current_player = 2
        self.__moves = 0
        self.__x = size // 2 + 1
        self.__y = size // 2 + 1
        
    def get_props(self):
        return {"current_player": self.__current_player,
                "moves": self.__moves,
                "x": self.__x,
                "y": self.__y}

    def put_current_player(self, new_current_player):
        self.__current_player = new_current_player

    def put_coordinates(self, y, x):
        self.__y, self.__x = y, x
        self.__moves += 1

    '''
    Esse método verifica se ouve vitória na última jogada, baseado no "x" e "y" atual.
    Para encontrar a vitória, um ponteiro passa, a partir da coordenada, por todas as direções e sentidos possíveis, aumentando a contagem se o valor encontrado é equivalente ao jogador atual.
    Quando ele analiza uma nova direção, a contagem reseta. Se ela chegar a 5, a função retorna verdadeiro e o jogo acaba, caso contrário, jogo que segue.
    '''
    
    def find_win(self, game):
        game_size = game.get_props()["size"]
        game_board = game.get_props()["board"]

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for dx, dy in directions:
            count = 1

            for target in [1, -1]:
                nx, ny = self.__x + target * dx, self.__y + target * dy

                while 0 <= nx < game_size and 0 <= ny < game_size and game_board[ny][nx] == self.__current_player:
                    count += 1
                    nx += target * dx
                    ny += target * dy
                    
            if count >= 5:
                return True
        return False

'''
Função principal que cria e modifica a classe Gomoku
'''

def play_match():
    
    '''
    Essa é a parte de configuração, que vai definir, ao criar as classes, qual o modo de jogo.
    No caso de Jogador x Máquina, também é definido quem será o primeiro a jogar.
    '''
    
    size = 19
    
    pvp_mode = int(input('Digite 0 para jogar com máquinas ou 1 para Jogador x Jogador: '))

    while not 0 <= pvp_mode <= 1:
        print('Entrada inválida!')
        pvp_mode = int(input('Digite 0 para jogar com máquinas ou 1 para Jogador x Jogador: '))
    
    machine_turn = False
    if not pvp_mode:
        only_machines = int(input('Máquina x Jogador (0) ou Máquina x Máquina (1)? '))

        while not 0 <= only_machines <= 1:
            print('Entrada inválida!')
            only_machines = int(input('Máquina x Jogador (0) ou Máquina x Máquina (1)? '))

        if not only_machines:
            machine_starts = int(input('Quem começa? Você (0) ou a Máquina (1)? '))

            while not 0 <= machine_starts <= 1:
                print('Entrada inválida!')
                machine_starts = int(input('Quem começa? Você (0) ou a Máquina (1)? '))

            if machine_starts:
                machine_turn = True
        else:
            machine_turn = True

    game = Gomoku(size, pvp_mode, machine_turn)
    commands = Control(size)

    game.print_board()
     
    '''
    Esta condicional vai rodar enquanto o jogo estiver em andamento, sempre verificando se não houve vitória (chamando o método verificador).
    
    '''

    while not commands.find_win(game) and commands.get_props()["moves"] < size ** 2:
        if commands.get_props()["current_player"] == 1:
            commands.put_current_player(2)
        else:
            commands.put_current_player(1)
            
        if game.get_game_modes()["machine_turn"]:
            print('Vez da máquina!')
            validation = False
                        
            '''
            Aqui é onde a máquina joga, com uma pitada de machine learning, ela sempre randomiza alguma jogada perto da última jogada (se a jogada for a primeira, ela randomiza perto do centro).
            O código também verifica se o campo escolhido está dentro do tamanho pré-definido e se ainda não houve jogada nele.
            Quando a jogada é validada, é atribuido na matriz da classe principal o valor do jogador atual, e na classe de comando é acrescentada o número de jogadas e atualizada a coordenada.
            '''

            while not validation:
                y, x = commands.get_props()["y"], commands.get_props()["x"]
                y += randint(-1, 1)
                x += randint(-1, 1)

                if 0 <= y <= size - 1 and 0 <= x <= size - 1 and not game.get_props()["board"][y][x]:
                    game.new_play(y, x, commands.get_props()["current_player"], commands)

                    sleep(1)
                    print(f'A maquina jogou... {y+1} e {x+1}!')
                    sleep(1)
                    print()

                    validation = True
            
            if not only_machines:
                game.modify_machine_turn(False)
            
        else:
            if game.get_game_modes()["pvp_mode"]:
                print(f'Vez do jogador {commands.get_props()["current_player"]}!')
            else:
                print('Sua vez!')
                                     
            '''
            Aqui temos para os jogadores o mesmo processo de validação que é feito com a máquina, porém individualmente para linhas e colunas.
            '''
       
            validation = False
            while not validation:

                y = int(input('Escolha a linha: ')) - 1
                while not 0 <= y <= size - 1:
                    y = int(input('Posição inválida, tente novamente: ')) - 1
                    
                x = int(input('Escolha a coluna: ')) - 1
                while not 0 <= x <= size - 1:
                    x = int(input('Posição inválida, tente novamente: ')) - 1
                    
                if game.get_props()["board"][y][x]:
                    print('Esta posição já foi preenchida! Tente outra...')
                else:
                    game.new_play(y, x, commands.get_props()["current_player"], commands)
                    validation = True
                    sleep(1)
                    print('Jogada Validada!')
                    sleep(1)
                    print()         

            '''
            O turno da máquina só vai ser ativado no modo Maquina x Jogador.
            Portanto o código da máquina sempre será ignorado no "pvp_mode".
            '''
            
            if not game.get_game_modes()["pvp_mode"]:
                game.modify_machine_turn(True)
        game.print_board()
         
    '''
    Quando a estrutura de repetição se encerra, o código abaixo analiza e escreve qual final teve o jogo.
    '''
    
    if commands.get_props()["moves"] == size ** 2:
        print('É... vocês conseguiram empatar.')
    elif game.get_game_modes()["pvp_mode"]:
        print(f'Parabéns, jogador {commands.get_props()["current_player"]}, você venceu!')      
    elif only_machines:
        print(f'Parabéns, máquina {commands.get_props()["current_player"]}, você randomizou melhor!')
    elif game.get_game_modes()["machine_turn"]:
        print('Parabéns, você venceu!')
    else:
        print('Não foi dessa vez, a máquina venceu...')

'''
A função "play_gomoku" permite que você possa jogar quantas vezes você quiser.
'''
    
def play_gomoku():
    gaming = True
    sleep(1)
    while gaming:
        play_match()
        sleep(1)
        gaming = int(input('Parar (0) ou continuar jogando (1)? '))
    print('Sessão encerrada! Obrigado por jogar.')

print('Iniciando jogo...')
play_gomoku()
