
import os
import time
import math



# CONFIGURAÇÕES


WIDTH = 100
HEIGHT = 42

FPS = 30
FRAME_TIME = 1 / FPS

DURACAO_CENA = 4

CORES = [
    (255, 0, 150),
    (255, 40, 0),
    (255, 200, 0),
    (0, 255, 150),
    (0, 180, 255),
    (120, 0, 255),
    (255, 0, 255),
]

PREENCHIMENTO = "░▒▓█"



# CAVEIRA


CAVEIRA = [
    r"                 ___-----------___",
    r"           __--~~                 ~~--__",
    r"       _-~~                             ~~-_",
    r"    _-~                                     ~-_",
    r"   /                                           ''",
    r"  |                                             |",
    r" |                                               |",
    r" |                                               |",
    r"|                                                 |",
    r"|                                                 |",
    r"|                                                 |",
    r" |                                               |",
    r" |  |    _-------_               _-------_    |  |",
    r" |  |  /~         ~\           /~         ~\  |  |",
    r"  ||  |             |         |             |  ||",
    r"  || |               |       |               | ||",
    r"  || |              |         |              | ||",
    r"  |   \_           /           \           _/   |",
    r" |      ~~--_____-~    /~V~\    ~-_____--~~      |",
    r" |                    |     |                    |",
    r"|                    |       |                    |",
    r"|                    |  /^\  |                    |",
    r" |                    ~~   ~~                    |",
    r"  \_         _                       _         _/",
    r"    ~--____-~ ~\                   /~ ~-____--~",
    r"         \     /\                 /\     /",
    r"          \    | ( ,           , ) |    /",
    r"           |   | (~(__(  |  )__)~) |   |",
    r"            |   \/ (  (~~|~~)  ) \/   |",
    r"             |   |  [ [  |  ] ]  /   |",
    r"              |                     |",
    r"               \                   /",
    r"                ~-_             _-~",
    r"                   ~--___-___--~",
]


MANDIBULA = [
    r"  \_         _                       _         _/",
    r"    ~--____-~ ~\                   /~ ~-____--~",
    r"         \     /\                 /\     /",
    r"          \    | ( ,           , ) |    /",
    r"           |   | (~(__(  |  )__)~) |   |",
    r"            |   \/ (  (~~|~~)  ) \/   |",
    r"             |   |  [ [  |  ] ]  /   |",
    r"              |                     |",
    r"               \                   /",
    r"                ~-_             _-~",
    r"                   ~--___-___--~",
]


# TERMINAL


def limpar_terminal():
    os.system("cls")


def esconder_cursor():
    print("\033[?25l", end="")


def mostrar_cursor():
    print("\033[?25h", end="")


def preparar_terminal():
    """
    Move o cursor para o início sem limpar a tela inteira.
    Isso é MUITO mais rápido que usar cls a cada frame.
    """
    print("\033[H", end="")



# FRAME


def criar_frame():
    return [
        [" "] * WIDTH
        for _ in range(HEIGHT)
    ]


def colocar(frame, x, y, caractere):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        frame[y][x] = caractere



# FUNDO


def fundo_rave(tempo, intensidade=1.0):

    frame = criar_frame()

    for y in range(HEIGHT):

        for x in range(WIDTH):

            dx = (x - WIDTH / 2) / 2
            dy = y - HEIGHT / 2

            distancia = math.sqrt(
                dx * dx + dy * dy
            )

            valor = (
                math.sin(
                    distancia * 1.7
                    - tempo * 7
                )
                +
                math.sin(
                    x * 0.22
                    + tempo * 4
                )
                +
                math.sin(
                    y * 0.35
                    - tempo * 5
                )
            )

            valor = (valor + 3) / 6

            valor *= intensidade

            indice = int(
                valor * (len(PREENCHIMENTO) - 1)
            )

            indice = max(
                0,
                min(indice, len(PREENCHIMENTO) - 1)
            )

            frame[y][x] = PREENCHIMENTO[indice]

    return frame



# MANDALA


def mandala(tempo, velocidade=1.0):

    frame = criar_frame()

    caracteres = " .·░▒▓█"

    for y in range(HEIGHT):

        for x in range(WIDTH):

            dx = (x - WIDTH / 2) / 2
            dy = y - HEIGHT / 2

            distancia = math.sqrt(
                dx * dx + dy * dy
            )

            angulo = math.atan2(
                dy,
                dx
            )

            valor = (
                math.sin(
                    distancia * 1.4
                    - tempo * 6 * velocidade
                )
                +
                math.sin(
                    angulo * 10
                    + tempo * 2 * velocidade
                )
                +
                math.sin(
                    distancia * 0.7
                    + angulo * 8
                    - tempo * 4
                )
            )

            valor = (valor + 3) / 6

            indice = int(
                valor * (len(caracteres) - 1)
            )

            indice = max(
                0,
                min(indice, len(caracteres) - 1)
            )

            frame[y][x] = caracteres[indice]

    return frame



# DESENHAR CAVEIRA


def desenhar_caveira(
    frame,
    tempo,
    offset_x=0,
    offset_y=0,
    boca=0
):

    inicio_y = (
        HEIGHT // 2
        - len(CAVEIRA) // 2
        - 2
        + offset_y
    )

    inicio_x = (
        WIDTH // 2
        - 28
        + offset_x
    )

    
    # CABEÇA
    

    limite_mandibula = 23

    for y, linha in enumerate(CAVEIRA):

        py = inicio_y + y

        if not 0 <= py < HEIGHT:
            continue

        # Se a boca estiver aberta, não desenhamos
        # a mandíbula original.
        if boca > 0 and y >= limite_mandibula:
            continue

        for x, caractere in enumerate(linha):

            if caractere != " ":

                colocar(
                    frame,
                    inicio_x + x,
                    py,
                    caractere
                )

    
    # BOCA ANIMADA
    

    if boca > 0:

        deslocamento = int(boca * 7)

        for y, linha in enumerate(MANDIBULA):

            py = (
                inicio_y
                + 23
                + y
                + deslocamento
            )

            for x, caractere in enumerate(linha):

                if caractere != " ":

                    colocar(
                        frame,
                        inicio_x + x,
                        py,
                        caractere
                    )



# SÍMBOLOS


def simbolos_orbitando(frame, tempo, velocidade=1.0):

    simbolos = [
        "☠",
        "☣",
        "☢",
        "✦",
        "✧",
        "✺",
        "☯",
        "✹",
        "*",
        "+",
        "#",
        "@",
    ]

    centro_x = WIDTH // 2
    centro_y = HEIGHT // 2

    for i in range(24):

        angulo = (
            i * math.tau / 24
            + tempo * velocidade
        )

        pulso = math.sin(
            tempo * 3 + i
        ) * 3

        raio = 30 + pulso

        x = int(
            centro_x
            + math.cos(angulo) * raio
        )

        y = int(
            centro_y
            + math.sin(angulo)
            * raio
            * 0.45
        )

        colocar(
            frame,
            x,
            y,
            simbolos[i % len(simbolos)]
        )



# ESTRELAS / EXPLOSÕES


def estrelas(frame, tempo):

    simbolos = "*+x✦✧"

    for i in range(80):

        angulo = (
            i * 2.399
            + tempo * 0.4
        )

        distancia = (
            (i * 7)
            % 42
        )

        x = int(
            WIDTH / 2
            + math.cos(angulo)
            * distancia
            * 1.8
        )

        y = int(
            HEIGHT / 2
            + math.sin(angulo)
            * distancia
            * 0.8
        )

        colocar(
            frame,
            x,
            y,
            simbolos[i % len(simbolos)]
        )



# CENA 1 — MANDALA


def cena_1(tempo):

    return mandala(
        tempo,
        1.0
    )



# CENA 2 — MANDALA TURBO


def cena_2(tempo):

    return mandala(
        tempo * 1.8,
        1.8
    )



# CENA 3 — CAVEIRA DANÇANDO


def cena_3(tempo):

    frame = fundo_rave(
        tempo,
        0.8
    )

    # Movimento de dança.
    movimento_x = int(
        math.sin(tempo * 3) * 5
    )

    movimento_y = int(
        math.sin(tempo * 6) * 2
    )

    # Boca abre e fecha 
    boca = (
        math.sin(tempo * 5) + 1
    ) / 2

    desenhar_caveira(
        frame,
        tempo,
        movimento_x,
        movimento_y,
        boca
    )

    simbolos_orbitando(
        frame,
        tempo,
        1.2
    )

    return frame



# CENA 4 — CAVEIRA PULANDO


def cena_4(tempo):

    frame = fundo_rave(
        tempo * 1.3,
        0.9
    )

    # Pulo.
    salto = abs(
        math.sin(tempo * 4)
    )

    movimento_y = -int(
        salto * 6
    )

    movimento_x = int(
        math.sin(tempo * 2) * 8
    )

    boca = (
        math.sin(tempo * 8) + 1
    ) / 2

    desenhar_caveira(
        frame,
        tempo,
        movimento_x,
        movimento_y,
        boca
    )

    estrelas(
        frame,
        tempo
    )

    return frame



# CENA 5 — CAVEIRA MALUCA


def cena_5(tempo):

    frame = criar_frame()

    movimento_x = int(
        math.sin(tempo * 7) * 8
    )

    movimento_y = int(
        math.sin(tempo * 9) * 3
    )

    boca = (
        math.sin(tempo * 10) + 1
    ) / 2

    desenhar_caveira(
        frame,
        tempo,
        movimento_x,
        movimento_y,
        boca
    )

    # Explosão psicodélica atrás.
    for i in range(50):

        angulo = (
            i * math.tau / 50
            + tempo * 2
        )

        raio = (
            10
            + (i % 10) * 2
            + math.sin(tempo * 5 + i)
        )

        x = int(
            WIDTH / 2
            + math.cos(angulo) * raio
        )

        y = int(
            HEIGHT / 2
            + math.sin(angulo)
            * raio
            * 0.5
        )

        colocar(
            frame,
            x,
            y,
            "✦"
        )

    return frame


# CENA 6 — TÚNEL


def cena_6(tempo):

    frame = criar_frame()

    chars = " .·░▒▓█"

    for y in range(HEIGHT):

        for x in range(WIDTH):

            dx = (x - WIDTH / 2) / 2
            dy = y - HEIGHT / 2

            distancia = math.sqrt(
                dx * dx + dy * dy
            )

            onda = math.sin(
                distancia * 0.9
                - tempo * 8
            )

            valor = (
                onda + 1
            ) / 2

            indice = int(
                valor * (len(chars) - 1)
            )

            frame[y][x] = chars[indice]

    desenhar_caveira(
        frame,
        tempo,
        int(math.sin(tempo * 2) * 3),
        int(math.sin(tempo * 4)),
        (math.sin(tempo * 6) + 1) / 2
    )

    return frame



# CENA 7 — CAOS


def cena_7(tempo):

    frame = fundo_rave(
        tempo * 2,
        1.1
    )

    simbolos_orbitando(
        frame,
        tempo,
        2.5
    )

    estrelas(
        frame,
        tempo * 2
    )

    return frame



# CENA 8 — FINAL


def cena_8(tempo):

    frame = mandala(
        tempo * 2.5,
        2.5
    )

    desenhar_caveira(
        frame,
        tempo,
        int(math.sin(tempo * 4) * 3),
        int(math.sin(tempo * 8) * 2),
        (math.sin(tempo * 9) + 1) / 2
    )

    simbolos_orbitando(
        frame,
        tempo,
        2
    )

    return frame



# RENDERIZAÇÃO OTIMIZADA


def renderizar(frame, tempo):

    preparar_terminal()

    linhas = []

    for y, linha in enumerate(frame):

        texto = ""
        cor_anterior = None

        for x, caractere in enumerate(linha):

            if caractere == " ":

                texto += " "
                cor_anterior = None
                continue

            # Mudamos a cor apenas quando necessário.
            indice = (
                x // 6
                + y
                + int(tempo * 10)
            ) % len(CORES)

            cor = CORES[indice]

            if cor != cor_anterior:

                r, g, b = cor

                texto += (
                    f"\033[38;2;"
                    f"{r};{g};{b}m"
                )

                cor_anterior = cor

            texto += caractere

        texto += "\033[0m"

        linhas.append(texto)

    print(
        "\n".join(linhas),
        end=""
    )



# MAIN


def main():

    limpar_terminal()
    esconder_cursor()

    inicio = time.perf_counter()

    try:

        while True:

            agora = time.perf_counter()

            tempo = agora - inicio

            numero_cena = int(
                tempo / DURACAO_CENA
            ) % 8

            tempo_cena = (
                tempo % DURACAO_CENA
            )

            if numero_cena == 0:
                frame = cena_1(tempo)

            elif numero_cena == 1:
                frame = cena_2(tempo)

            elif numero_cena == 2:
                frame = cena_3(tempo)

            elif numero_cena == 3:
                frame = cena_4(tempo)

            elif numero_cena == 4:
                frame = cena_5(tempo)

            elif numero_cena == 5:
                frame = cena_6(tempo)

            elif numero_cena == 6:
                frame = cena_7(tempo)

            else:
                frame = cena_8(tempo)

            renderizar(
                frame,
                tempo
            )

            # ------------------------------------------------
            # FPS ESTÁVEL
            # ------------------------------------------------

            proximo_frame = (
                agora + FRAME_TIME
            )

            atraso = (
                proximo_frame
                - time.perf_counter()
            )

            if atraso > 0:
                time.sleep(atraso)

    except KeyboardInterrupt:

        mostrar_cursor()
        limpar_terminal()

        print(
            "RAVE VISUALS ENCERRADO."
        )


if __name__ == "__main__":
    main()

