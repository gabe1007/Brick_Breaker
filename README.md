![alt text](image.png)

# Brick Breaker com Controle de Gestos

## Descrição
Este projeto é uma uma adaptação do famoso jogo de Brick Breaker. Recententemente eu criei um script que utiliza as bibliotecas MediaPipe e PyGui para controlar o cursor do mouse, decidi então criar um exemplo prático para o script. Utilizando Python, Pygame para a interface do jogo, OpenCV para processamento de imagem da webcam, e MediaPipe para detecção de gestos. 

## Funcionalidades
- **Controle de Gestos**: Utilize movimentos da mão para mover a raquete no jogo.
- **Detecção de Gestos com MediaPipe**: Detecta gestos da mão em tempo real usando a webcam.
- **Jogo de Brick Breaker Clássico**: Jogue o clássico jogo de quebrar tijolos com uma nova virada.
- **Interface Gráfica com Pygame**: Uma interface gráfica atraente e intuitiva.
- **Reinício do Jogo com Gestos**: Recomece o jogo juntando o polegar e o indicador.

## Requisitos
- Python 3.x
- Pygame
- OpenCV
- MediaPipe

## Instalação
```bash
pip install -r requirements.txt
````
OBS: Caso você possua mais de uma webcam será necessário alterar o valor aqui:

```bash
cap = cv2.VideoCapture(0)
