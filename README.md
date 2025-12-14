# Planet-Invasion

Planet Invasion é um jogo de plataforma 2D desenvolvido em Python utilizando a biblioteca PgZero. O jogador controla um herói espacial em uma missão para atravessar planetas perigosos cheios de armadilhas e criaturas hostis.
🎮 Gênero

Platformer (Plataforma) - Jogo de visão lateral focado em pular entre plataformas, evitar obstáculos e derrotar inimigos.
✨ Requisitos Mínimos

O projeto foi desenvolvido estritamente seguindo as regras do ambiente PgZero.

    Linguagem: Python 3.x

    Biblioteca Principal: PgZero (requer Pygame subjacente)

    Módulos Permitidos: PgZero, math, random.

🚀 Como Jogar

    Instalação: Certifique-se de ter o Python instalado. Instale o pgzero e, se necessário, o Pygame (que é uma dependência):
    Bash

pip install pgzero

Execução: Salve o código principal do jogo (como game.py) e a pasta de recursos (images, sounds, music) na mesma pasta. Execute o jogo usando o comando pgzrun:
Bash

    pgzrun game.py

🕹️ Controles
Ação	Tecla
Mover Esquerda	Seta Esquerda (←)
Mover Direita	Seta Direita (→)
Pular	Barra de Espaço (SPACE)
Voltar ao Menu	Enter (RETURN) (nas telas de Fim de Jogo/Vitória)
📋 Funcionalidades Implementadas
Menu e Estrutura do Jogo

    Menu Principal: Tela inicial com botões clicáveis:

        INICIAR JOGO

        SOM: LIGADO/DESLIGADO (Alterna música de fundo e efeitos sonoros)

        SAIR

    Múltiplas Fases (CURRENT_STAGE): O jogo é dividido em 4 fases distintas, cada uma com diferentes layouts de plataformas e conjuntos de inimigos.

    Condições de Fim de Jogo: GAME_OVER (vidas esgotadas) e WINNER (conclusão da Fase 4).

    HUD (Head-Up Display): Exibe o número de vidas restantes (corações), a fase atual e a pontuação.

Personagens e Mecânicas

    Classe Hero: Implementa a física de plataforma:

        Gravidade (GRAVITY).

        Movimento Horizontal e limites de tela.

        Salto (JUMP_FORCE) com verificação de plataforma.

        Animação de sprite para idle e walk_right/left (movimento e parado).

    Classes Enemy e StaticEnemy:

        Enemy: Representa inimigos móveis (Ex: Slimefire, Bee, Mouse) que patrulham um patrol_range definido. Implementa animações de movimento.

        StaticEnemy: Representa inimigos fixos ou armadilhas (Ex: Barnacle) que usam animação de ataque contínua.

    Colisão: Gerenciamento de colisão com plataformas (Eixos X e Y), inimigos e o objetivo final (goal). A colisão com inimigos ou queda do mapa resulta em perda de vida (lose_life).

Animação e Estética

    Animação de Sprite: Animações cíclicas (animate e animation_images_list) para o herói, inimigos e o objetivo.

    Estilo Visual: Telas de GAME_OVER e WINNER estilizadas com efeitos visuais e pixel art para maior impacto.

📐 Estrutura do Código

O código é organizado em seções lógicas:

    Constantes: Definição de tamanhos, velocidades, estados do jogo e botões do menu.

    Preparação de Assets: Funções para criar listas de frames de animação.

    Classes: Definição de Hero, Enemy e StaticEnemy.

    Criação de Fases (load_stageX): Funções que definem o layout das plataformas, a posição do objetivo e a localização dos inimigos para cada fase.

    Gerenciamento de Jogo: Funções advance_stage, reset_game, lose_life.

    Colisão: Funções collision_platform_x e collision_platform_y.

    Loop Principal (PgZero): Funções draw, update, on_mouse_down e on_key_down.
