from random import randint
from time import sleep

'''
Decidi usar apenas uma classe principal nesse projeto, caso fosse uma plataforma de jogos, a classe Gomoku poderia ser uma subclasse de "Jogos", herdando a maioria dos atributos.
Falando sobre os atributos, o "size" serve para flexibilizar o tamanho do tabuleiro automaticamente quando ele é criado (no atributo "board", cria-se uma matriz cheia de zeros que é alterada a cada jogada).
O restante dos atributos foi feito para dinamizar os modos de jogo e tornar funcional o modo jogador x jogador e jogador x máquina (é possível assistir um máquina x máquina também, lá embaixo é explicado).
O "x" e o "y" denotam a última jogada feita (eles são iniciados na metade do tabuleiro para sempre que a máquna começar, ela jogue perto do centro, eu também explico depois as jogadas da máquina).
Existem também alguns comandos "sleep" no código para deixar o jogo mais imersivo.
'''

class Gomoku:
    def __init__(self, size=19, pvp_mode = 1, machine_turn = 0):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.current_player = 2
        self.moves = 0
        self.pvp_mode = pvp_mode
        self.machine_turn = machine_turn
        self.x = size // 2
        self.y = size // 2
    
    '''
    Método que exibe o tabuleiro na tela, com linhas e colunas numeradas.
    Caso o campo tenha sido preenchido, é printado "X" para o jogador 1 e "0" para o jogador 2.
    '''
    
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
                    print("X", end="   ")
                elif column == 2:
                    print("0", end="   ")
                else:
                    print(".", end="   ")
            print()
            print()
            
        print("  ", end=" ")
        i = 1
        while i <= len(self.board):
            if i < 10:
                print("0", i, sep = "", end="  ")
            else:
                print(i, end="  ")
            i += 1
        print()
        print()
        sleep(1)
     
    '''
    Esse método verifica se ouve vitória na última jogada, baseado no "x" e "y" atual.
    Para encontrar a vitória, um ponteiro passa, a partir da coordenada, por todas as direções e sentidos possíveis, aumentando a contagem se o valor encontrado é equivalente ao jogador atual.
    Quando ele analiza uma nova direção, a contagem reseta. Se ela chegar a 5, a função retorna verdadeiro e o jogo acaba, caso contrário, jogo que segue.
    '''
    
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

'''
Função principal que cria e modifica a classe Gomoku
'''

def play_match():
    
    '''
    Essa é a parte de configuração, que vai definir, ao criar a classe, qual o modo de jogo.
    No caso de Jogador x Máquina, também é definido quem será o primeiro a jogar.
    '''
    
    size = 19
    
    pvp_mode = int(input('Jogador x Máquina (0) ou Jogador x jogador (1)? '))
    while not 0 <= pvp_mode <= 1:
        print('Entrada inválida!')
        pvp_mode = int(input('Jogador x Máquina (0) ou Jogador x jogador (1)? '))
        
    if not pvp_mode:
        machine_turn = int(input('Quem começa? Você (0) ou a Máquina (1)? '))
        while not 0 <= machine_turn <= 1:
            print('Entrada inválida!')
            machine_turn = int(input('Quem começa? Você (0) ou a Máquina (1)? '))
        game = Gomoku(size, pvp_mode, machine_turn)
        
    else:
        game = Gomoku(size, pvp_mode)
    game.print_board()
     
    '''
    Esta condicional vai rodar enquanto o jogo estiver em andamento, sempre verificando se não houve vitória (chamando o método verificador).
    
    '''

    while not game.find_win() and game.moves < size ** 2:
        if game.current_player == 1:
            game.current_player = 2
        else:
            game.current_player = 1
            
        if game.machine_turn:
            print('Vez da máquina!')
            validation = False
                        
            '''
            Aqui é onde a máquina joga, com uma pitada de machine learning, ela sempre randomiza alguma jogada perto da última jogada (se a jogada for a primeira, ela randomiza perto do centro).
            O código também verifica se o campo escolhido está dentro do tamanho pré-definido e se ainda não houve jogada nele.
            Quando a jogada é validada, é atribuido na matriz o valor do jogador atual.
            '''
    
            while not validation:
                game.y += randint(-1, 1)
                game.x += randint(-1, 1)
                if 0 <= game.y <= size - 1 and 0 <= game.x <= size - 1 and not game.board[game.y][game.x]:
                    game.board[game.y][game.x] = game.current_player
                    sleep(1)
                    print(f'A maquina jogou... {game.y+1} e {game.x+1}!')
                    sleep(1)
                    print()
                    validation = True
                                    
            '''
            Se a linha abaixo for deletada, e um jogo Máquina x Jogador for iniciado, com a máquina começando, você verá duas máquinas se degladiando por muito tempo (sério, nenhuma tá afim de ganhar).
            '''
    
            game.machine_turn = 0
            
        else:
            if game.pvp_mode:
                print(f'Vez do jogador {game.current_player}!')
            else:
                print('Sua vez!')
                                     
            '''
            Aqui temos para os jogadores o mesmo processo de validação que é feito com a máquina, porém individualmente para linhas e colunas.
            '''
       
            validation = False
            while not validation:
                game.y = int(input('Escolha a linha: ')) - 1
                while not 0 <= game.y <= size - 1:
                    game.y = int(input('Posição inválida, tente novamente: ')) - 1
                    
                game.x = int(input('Escolha a coluna: ')) - 1
                while not 0 <= game.x <= size - 1:
                    game.x = int(input('Posição inválida, tente novamente: ')) - 1
                    
                if game.board[game.y][game.x]:
                    print('Esta posição já foi preenchida! Tente outra...')
                else:
                    sleep(1)
                    print('Jogada Validada!')
                    sleep(1)
                    print()
                    game.board[game.y][game.x] = game.current_player
                    validation = True
                                    
            '''
            O turno da máquina só vai ser ativado no modo Maquina x Jogador.
            Portanto o código da máquina sempre será ignorado no "pvp_mode".
            Após isso, o tabuleiro é exibido e a quantidade de jogadas acrescenta, independente do modo de jogo.
            '''
            
            if not game.pvp_mode:
                game.machine_turn = 1
        game.moves += 1
        game.print_board()
         
    '''
    Quando a estrutura de repetição se encerra, o código abaixo analiza e escreve qual final teve o jogo.
    '''
    
    if game.moves == size ** 2:
        print('É... vocês conseguiram empatar.')
    elif game.pvp_mode:
        print(f'Parabéns, jogador {game.current_player}, você venceu!')        
    elif game.machine_turn:
        print('Parabéns, você venceu!')
    else:
        print('Não foi dessa vez, a máquina venceu...')

'''
A função "play_gomoku" permite que você possa jogar quantas vezes você quiser.
'''
    
def play_gomoku():
    gaming = 1
    sleep(1)
    while gaming:
        play_match()
        sleep(1)
        gaming = int(input('Parar (0) ou continuar jogando (1)? '))
    print('Sessão encerrada! Obrigado por jogar.')

print('Iniciando jogo...')
play_gomoku()
