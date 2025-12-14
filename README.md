# Planet-Invasion

Planet Invasion é um jogo de plataforma 2D desenvolvido em Python utilizando a biblioteca PgZero. O jogador controla um herói espacial em uma missão para atravessar planetas perigosos cheios de armadilhas e criaturas hostis.

🎨 Recursos Gráficos (Assets)

Os recursos gráficos (sprites, tiles e fundos) utilizados neste projeto são provenientes do New Platformer Pack criado por Kenney.

    Fonte do Pack: https://kenney.nl/assets/new-platformer-pack

🎮 Gênero

Platformer (Plataforma) - Jogo de visão lateral focado em pular entre plataformas, evitar obstáculos e derrotar inimigos, sendo um dos gêneros explicitamente permitidos nos requisitos do projeto.
✨ Requisitos Mínimos e Tecnologias

O projeto foi desenvolvido estritamente seguindo as regras do ambiente PgZero e o conjunto limitado de bibliotecas permitidas.

    Linguagem: Python 3.x

    Ambiente de Desenvolvimento Recomendado: Mu Editor (Modo Pygame Zero)

    Biblioteca Principal: PgZero (requer Pygame subjacente)

    Módulos Permitidos: PgZero, math, random.

    Exceção: Uso da classe Rect (disponível no PgZero/Pygame).

🚀 Como Jogar

    Instalação de Dependências: Certifique-se de ter o Python instalado. Instale o pgzero e o Pygame (que é uma dependência subjacente):
    Bash

pip install pgzero

Preparação dos Arquivos: Salve o código principal do jogo (ex: game.py) e garanta que todas as pastas de recursos (sprites em images, sons em sounds, música em music) estejam localizadas na mesma pasta.

Execução:

    Mu Editor (Recomendado): O projeto foi desenvolvido e é idealmente executado no Mu Editor no modo Pygame Zero. Basta abrir o arquivo do jogo e clicar no botão "Play" (Reproduzir).

    Linha de Comando: Alternativamente, execute o jogo usando o comando pgzrun:
    Bash

        pgzrun game.py

🕹️ Controles:
Ação	Tecla
Mover Esquerda	Seta Esquerda (←)
Mover Direita	Seta Direita (→)
Pular	Barra de Espaço (SPACE)
Voltar ao Menu	Enter (RETURN) (nas telas de Fim de Jogo/Vitória)
📋 Funcionalidades Implementadas:
Estrutura e Gerenciamento do Jogo

    Menu Principal: Implementação completa do menu inicial (estado "MENU") com os seguintes botões funcionais:

        INICIAR JOGO

        SOM: LIGADO/DESLIGADO (Alterna a reprodução da música de fundo e sons via music.play() e music.stop()).

        SAIR (Finaliza o programa via raise SystemExit).

    Progressão de Fases: O jogo possui 4 fases (TOTAL_STAGES). O jogador avança usando a função advance_stage() ao colidir com o goal.

    Sistema de Vidas e Pontuação: O herói começa com 5 vidas (MAX_LIVES). Perder todas as vidas leva ao estado GAME_OVER. Pontos são adicionados a cada fase concluída.

    Telas Finais: Telas dedicadas para os estados WINNER e GAME_OVER, permitindo o retorno ao menu via tecla ENTER.

Personagens e Mecânicas de Platformer:

    Classe Hero:

        Gerencia a posição e velocidade (vx, vy) do herói.

        Aplica a física de gravidade (apply_gravity()) e permite o salto (jump()) se o herói estiver sobre uma plataforma.

        Inclui verificação de morte por queda (se hero.actor.top > HEIGHT).

    Classes Enemy e StaticEnemy:

        Enemy (Móvel): Implementa movimento horizontal e patrulha dentro de um patrol_range definido, representando o "território" dos inimigos. (Ex: Slimefire, Bee, Mouse).

        StaticEnemy (Estático): Representa ameaças fixas que dependem apenas de animação. (Ex: Barnacle).

    Colisão: Funções dedicadas (collision_platform_x, collision_platform_y) para lidar com a interação do herói com as plataformas, prevenindo a passagem e ajustando o vy ao pousar.

Animação de Sprite e Conformidade:

    Animação do Herói: A função Hero.animate() controla a troca de frames usando HERO_IDLE_SPEED e HERO_WALK_SPEED, garantindo animações para o estado parado (hero_idle_images, 18 frames) e o estado movendo-se (hero_walk_right/left_images, 2 frames).

    Animação de Inimigos: Inimigos móveis e estáticos possuem animações de sprite que mudam continuamente e ciclicamente.

        Exemplo: Barnacles estáticos são animados via clock.schedule_interval(animate_barnacles, ...) com uma taxa de ataque.

    Nomenclatura PEP8: Todas as classes, variáveis e funções usam nomes claros e descritivos em inglês, seguindo as convenções (PascalCase para classes, snake_case para funções/variáveis).

📐 Estrutura do Código:

O arquivo de código é estruturado para clareza:

    Constantes: Parâmetros de jogo, física, animação, e definições de botões do menu.

    Preparação de Assets: Funções para carregar e listar frames de animação.

    Classes: Definição de Hero, Enemy e StaticEnemy.

    Criação de Fases (load_stageX): Lógica para construir o layout do mapa, plataformas e posicionamento de inimigos para cada uma das 4 fases.

    Gerenciamento de Jogo: Funções advance_stage, reset_game, lose_life.

    Funções de Colisão: Lógica de collision_platform_x e collision_platform_y.

    Agendamento de Animações: Uso do clock.schedule_interval para animar inimigos estáticos e o objetivo.

    Loop Principal (PgZero): Funções principais do framework: draw(), update(), on_mouse_down(), e on_key_down().
