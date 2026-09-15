#!/usr/bin/env pybricks-micropython
"""
LEGO® MINDSTORMS® EV3 - Color Sorter (Classificador de Cores)
Requer: LEGO® EV3 MicroPython v2.0
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Button, Color, Stop
from pybricks.media.ev3dev import ImageFile, SoundFile
from pybricks.tools import wait, StopWatch

# Cores esperadas para separação (Azul, Verde, Amarelo, Vermelho)
POSSIBLE_COLORS = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW]
BELT_SPEED = 300
FEED_SPEED = 450

# Inicializa o bloco EV3
ev3 = EV3Brick()

# 1. Aumentar o volume do speaker para o máximo (100%)
ev3.speaker.set_volume(100)
# Configura opções de voz para soar com mais clareza e presença
ev3.speaker.set_speech_options(language='en', speed=120, pitch=50)

# Inicializa os motores da esteira (Porta D) e alimentador/dispenser (Porta A)
belt_motor = Motor(Port.D)
feed_motor = Motor(Port.A)

# Inicializa o Sensor de Toque (Porta 1) usado para zerar a esteira
touch_sensor = TouchSensor(Port.S1)

# Inicializa o Sensor de Cor (Porta 3)
color_sensor = ColorSensor(Port.S3)


def ler_cor_confirmada():
    """Confirma a cor usando várias leituras RGB para diferenciar azul e verde."""

    leituras = []

    for _ in range(3):
        cor = color_sensor.color()
        rgb = color_sensor.rgb()

        if cor not in POSSIBLE_COLORS:
            return None

        leituras.append((cor, rgb))
        wait(50)

    vermelho = sum(leitura[1][0] for leitura in leituras) / 3
    verde = sum(leitura[1][1] for leitura in leituras) / 3
    azul = sum(leitura[1][2] for leitura in leituras) / 3

    cor_sensor = leituras[1][0]

    if cor_sensor in (Color.BLUE, Color.GREEN):

        if azul > verde * 1.20:
            return Color.BLUE

        elif verde > azul * 1.20:
            return Color.GREEN

        return None

    if leituras[0][0] == leituras[1][0] == leituras[2][0]:
        return cor_sensor

    return None

def ejetar_peca():
    """
    Rotina inteligente com anti-travamento para ejetar a peça:
    - Velocidade reduzida para proporcionar mais torque e uma descida controlada.
    - Ângulo de descida de 190° para liberar melhor a peça do mecanismo.
    - Monitoramento de stall e timeout (StopWatch): se a peça enroscar ou o motor travar,
      ele NUNCA congela o robô; interrompe o avanço e recolhe imediatamente para 0°.
    """
    watch = StopWatch()

    # --- 1. Desce/avança o empurrador para liberar a peça ---
    watch.reset()
    feed_motor.run_target(FEED_SPEED, 210, then=Stop.HOLD, wait=False)
    while not feed_motor.control.done():
        if feed_motor.control.stalled() or watch.time() > 1200:
            # Faz uma pressao curta adicional para liberar pecas presas.
            feed_motor.run_time(FEED_SPEED, 300, then=Stop.HOLD)
            break
        wait(10)

    wait(700)  # Da tempo para a peca cair completamente no compartimento

    # --- 2. Retrai o empurrador de volta para a posição inicial de descanso (0°) ---
    watch.reset()
    feed_motor.run_target(FEED_SPEED, 0, then=Stop.HOLD, wait=False)
    while not feed_motor.control.done():
        if feed_motor.control.stalled() or watch.time() > 1200:
            # Se enroscar ao voltar, recua com torque controlado até o batente
            feed_motor.run_until_stalled(-450, duty_limit=50)
            feed_motor.reset_angle(0)
            break
        wait(10)


while True:
    # --- 1. Calibração inicial do alimentador (Dispenser) ---
    # Gira até travar no fim mecânico e recua 200 graus para a posição de espera
    feed_motor.run_until_stalled(120, duty_limit=50)
    feed_motor.run_angle(FEED_SPEED, -200)
    # Define a posição de descanso como exatamente ZERO graus absoluto
    feed_motor.reset_angle(0)

    # --- 2. Calibração da esteira (Homing) ---
    # Move a esteira para trás até pressionar o Sensor de Toque
    belt_motor.run(-BELT_SPEED)
    while not touch_sensor.pressed():
        pass
    belt_motor.stop()
    wait(1000)
    belt_motor.reset_angle(0)  # Define este ponto como posição zero da esteira

    # Lista para salvar a sequência de cores escaneadas
    color_list = []

    # --- 3. Fase de Leitura/Escaneamento das peças ---
    while len(color_list) < 8:
        ev3.screen.load_image(ImageFile.RIGHT)
        ev3.screen.print("Pecas lidas: " + str(len(color_list)))

        # Aguarda a leitura de uma cor ou o botão de centro para iniciar antes
        while True:
            pressed = Button.CENTER in ev3.buttons.pressed()
            color = ler_cor_confirmada()
            if pressed or color is not None:
                break

        if pressed:
            # Pressionou o botão central: finaliza a inserção de peças mais cedo
            break

        # Cor detectada: confirma com bip e adiciona na lista
        ev3.speaker.beep(1000, 100)
        color_list.append(color)

        # Aguarda a peça sair da frente do sensor para não ler duplicado
        while color_sensor.color() in POSSIBLE_COLORS:
            wait(50)
        ev3.speaker.beep(2000, 100)

        # Mostra ícone indicando que pode apertar o centro se já terminou
        ev3.screen.load_image(ImageFile.BACKWARD)
        wait(2000)

    # Notificação sonora de início da separação
    ev3.speaker.play_file(SoundFile.READY)
    ev3.screen.load_image(ImageFile.EV3)
    # Volume máximo (100%)
    ev3.speaker.set_volume(100)
    # Ajuste de velocidade e tom para a voz ficar mais limpa e alta
    ev3.speaker.set_speech_options(language='en', speed=120, pitch=50)

    # --- 4. Fase de Separação (Sorting) ---
    for color in color_list:
        wait(1000)

        # Posiciona a esteira no compartimento de cada cor
        if color == Color.BLUE:
            ev3.speaker.say('blue')
            belt_motor.run_target(BELT_SPEED, 120)
            wait(1000)
        elif color == Color.GREEN:
            ev3.speaker.say('green')
            belt_motor.run_target(BELT_SPEED, 240)
            wait(1000)
        elif color == Color.YELLOW:
            ev3.speaker.say('yellow')
            belt_motor.run_target(BELT_SPEED, 360)
            wait(1000)
        elif color == Color.RED:
            ev3.speaker.say('red')
            belt_motor.run_target(BELT_SPEED, 480)
            wait(1000)

        # Ejeta a peça com a rotina anti-travamento
        ejetar_peca()