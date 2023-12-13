import cv2
import mediapipe as mp
import pygame
import threading
import math

# Inicialização do Pygame e definição das cores básicas
pygame.init()  # Inicializa todos os módulos importados do pygame
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
width, height = 800, 600
gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption('Brick Breaker com Controle de Gestos')
clock = pygame.time.Clock()  # Cria um relógio para controlar a taxa de quadros por segundo

# Configurações iniciais do OpenCV e MediaPipe
cap = cv2.VideoCapture(0)  # Inicia a captura de vídeo pela webcam
hand_detector = mp.solutions.hands.Hands()  # Inicializa o detector de mãos

# Definição das variáveis iniciais do jogo
ball_x = width // 2  # Posição inicial X da bola (centro horizontal)
ball_y = height // 2  # Posição inicial Y da bola (centro vertical)
ball_dx = 3  # Velocidade inicial da bola no eixo X
ball_dy = -3  # Velocidade inicial da bola no eixo Y
paddle_x = width // 2  # Posição inicial X da raquete (centro horizontal)
paddle_y = height - 50  # Posição Y da raquete (50 pixels acima da borda inferior)
paddle_width = 100  # Largura da raquete
paddle_height = 20  # Altura da raquete
brick_width = 50  # Largura de cada tijolo
brick_height = 20  # Altura de cada tijolo
num_bricks = width // brick_width  # Número de tijolos por linha
bricks = [[True for _ in range(num_bricks)] for _ in range(5)]  # Matriz de tijolos (5 linhas)
score = 0  # Pontuação inicial
game_started = False  # Controla o início do jogo
game_over_displayed = False  # Controla se a mensagem de game over foi exibida


# Abaixo estão as funções para desenhar elementos na tela

def draw_ball(ball_x, ball_y):
    # Desenha a bola na tela
    # ball_x, ball_y: Posição atual da bola
    pygame.draw.circle(gameDisplay, red, [ball_x, ball_y], 10)  # Desenha um círculo vermelho


def draw_paddle(paddle_x, paddle_y):
    # Desenha a raquete na tela
    # paddle_x, paddle_y: Posição atual da raquete
    pygame.draw.rect(gameDisplay, white,
                     [paddle_x, paddle_y, paddle_width, paddle_height])  # Desenha um retângulo branco


def draw_bricks():
    # Desenha os tijolos na tela
    for i in range(5):  # Loop para cada linha de tijolos
        for j in range(num_bricks):  # Loop para cada tijolo na linha
            if bricks[i][j]:  # Se o tijolo ainda não foi destruído desenha um tijolo na posição correspondente
                pygame.draw.rect(gameDisplay, blue, [j * brick_width, i * brick_height, brick_width, brick_height])


def draw_score():
    # Exibe a pontuação na tela
    font = pygame.font.SysFont('arial', 36)  # Define a fonte e tamanho do texto
    text = font.render(f'Pontuação: {score}', True, white)  # Cria o texto com a pontuação
    gameDisplay.blit(text, [10, 10])  # Coloca o texto na tela


# As funções a seguir são para exibir mensagens na tela

def draw_start_message():
    # Exibe a mensagem inicial para começar o jogo
    font = pygame.font.SysFont('arial', 31)
    text = font.render('Junte polegar com o indicador para começar o jogo', True, white)  # Cria o texto da mensagem
    text_rect = text.get_rect(center=(width / 2, height / 2))  # Centraliza o texto
    gameDisplay.blit(text, text_rect)  # Coloca o texto na tela


def draw_game_over_message():
    # Exibe a mensagem de game over
    font = pygame.font.SysFont('arial', 50)  # Define a fonte e tamanho do texto
    text = font.render('Game Over', True, red)  # Cria o texto da mensagem
    text_rect = text.get_rect(center=(width / 2, height / 2))  # Centraliza o texto
    gameDisplay.blit(text, text_rect)  # Coloca o texto na tela


# Função para verificar se todos os tijolos foram destruídos
def all_bricks_destroyed():
    # Verifica se todos os valores na matriz de tijolos são False
    return all(not brick for row in bricks for brick in row)


# Função para reiniciar o jogo
def reset_game():
    # Reinicializa as variáveis do jogo para o estado inicial
    global ball_x, ball_y, ball_dx, ball_dy, paddle_x, game_started, score, bricks, game_over_displayed
    ball_x = width // 2
    ball_y = height // 2
    ball_dx = 3
    ball_dy = -3
    paddle_x = width // 2
    score = 0
    bricks = [[True for _ in range(num_bricks)] for _ in range(5)]  # Recria a matriz de tijolos
    game_started = False
    game_over_displayed = False  # Reseta a flag de game over


# Função para verificar a colisão com os tijolos
def check_collision_with_bricks():
    # Verifica se a bola colidiu com algum tijolo
    global ball_dy, ball_dx, score
    collision_detected = False

    ball_center_x = ball_x
    ball_center_y = ball_y

    for i in range(5):  # Loop para cada linha de tijolos
        for j in range(num_bricks):  # Loop para cada tijolo na linha
            if bricks[i][j]:  # Se o tijolo ainda não foi destruído
                brick_x = j * brick_width
                brick_y = i * brick_height
                brick_rect = pygame.Rect(brick_x, brick_y, brick_width, brick_height)  # Cria um retângulo para o tijolo

                # Verifica se a bola colidiu com o retângulo do tijolo
                if brick_rect.collidepoint(ball_center_x, ball_center_y):
                    bricks[i][j] = False  # Marca o tijolo como destruído
                    score += 1  # Incrementa a pontuação
                    collision_detected = True

                    # Altera a direção da bola se necessário
                    if ball_center_x < brick_x or ball_center_x > brick_x + brick_width:
                        ball_dx *= -1
                    if ball_center_y < brick_y or ball_center_y > brick_y + brick_height:
                        ball_dy *= -1

                    return collision_detected  # Retorna verdadeiro se houve colisão

    return collision_detected  # Retorna falso se não houve colisão


# Função para exibir a mensagem de reinício do jogo
def draw_restart_message():
    # Exibe a mensagem para reiniciar o jogo
    font = pygame.font.SysFont('arial', 36)  # Define a fonte e tamanho do texto
    text = font.render('Para reiniciar junte polegar e indicador', True, white)  # Cria o texto da mensagem
    text_rect = text.get_rect(center=(width / 2, height / 2 + 50))  # Centraliza o texto
    gameDisplay.blit(text, text_rect)  # Coloca o texto na tela


def gameLoop():
    # Acessa variáveis globais para modificá-las dentro da função
    global ball_x, ball_y, ball_dx, ball_dy, paddle_x, game_started, game_over_displayed

    # Define variáveis para controlar o estado do jogo
    game_over = False
    game_over_displayed = False

    # Loop principal do jogo
    while not game_over:
        # Processa eventos do Pygame (como fechar a janela)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True  # Encerra o jogo se a janela for fechada

        # Se o jogo ainda não começou, exibe a mensagem inicial
        if not game_started:
            gameDisplay.fill(black)  # Limpa a tela
            draw_start_message()  # Desenha a mensagem de início
            # Se o jogo acabou, exibe a mensagem para reiniciar
            if game_over_displayed or all_bricks_destroyed():
                draw_restart_message()

        # Se o jogo começou e não terminou, atualiza a posição da bola e verifica colisões
        elif not game_over_displayed and not all_bricks_destroyed():
            ball_x += ball_dx  # Atualiza posição X da bola
            ball_y += ball_dy  # Atualiza posição Y da bola

            # Verifica colisões com as paredes laterais e superiores
            if ball_x > width - 10 or ball_x < 10:
                ball_dx *= -1  # Inverte a direção horizontal da bola
            if ball_y < 10 or check_collision_with_bricks():
                ball_dy *= -1  # Inverte a direção vertical da bola

            # Verifica colisão com a raquete
            elif ball_y > height - 50 and paddle_x <= ball_x <= paddle_x + paddle_width:
                # Se a bola tocar a raquete, inverte a direção vertical
                if ball_y < height - 40:
                    ball_dy *= -1
                else:
                    # Se não, marca o jogo como terminado
                    game_over_displayed = True

            # Desenha os elementos do jogo
            gameDisplay.fill(black)  # Limpa a tela
            draw_ball(ball_x, ball_y)  # Desenha a bola
            draw_paddle(paddle_x, paddle_y)  # Desenha a raquete
            draw_bricks()  # Desenha os tijolos
            draw_score()  # Desenha a pontuação

        # Se o jogo terminou, exibe a mensagem de game over e reinício
        else:
            draw_game_over_message()  # Desenha a mensagem de game over
            draw_restart_message()  # Desenha a mensagem de reinício

        # Atualiza a tela e controla a taxa de quadros por segundo
        pygame.display.update()
        clock.tick(60)

    # Encerra o Pygame ao sair do loop
    pygame.quit()


def webcam_process():
    global paddle_x, game_started, game_over_displayed
    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks

        if hands:
            hand = hands[0]
            thumb_tip = hand.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
            index_finger_tip = hand.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]

            # Calcula a diferença entre as posições Y do polegar e do indicador
            thumb_y = thumb_tip.y * height
            index_y = index_finger_tip.y * height
            if abs(thumb_y - index_y) < 20:  # Ajuste o limiar conforme necessário
                if not game_started or all_bricks_destroyed() or game_over_displayed:
                    reset_game()
                    game_started = True

            if game_started:
                lm = hand.landmark[8]  # Ponta do dedo indicador
                cx = int(lm.x * width)
                paddle_x = cx - paddle_width // 2

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()


if __name__ == "__main__":
    game_thread = threading.Thread(target=gameLoop)
    webcam_thread = threading.Thread(target=webcam_process)
    game_thread.start()
    webcam_thread.start()
    game_thread.join()
    webcam_thread.join()
