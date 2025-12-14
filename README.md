# Planet-Invasion

Planet Invasion é um jogo de plataforma 2D desenvolvido em Python utilizando a biblioteca PgZero. O jogador controla um herói espacial em uma missão para atravessar planetas perigosos cheios de armadilhas e criaturas hostis.

🎨 Recursos Gráficos (Assets)

Os recursos gráficos (sprites, tiles e fundos) utilizados neste projeto são provenientes do New Platformer Pack criado por Kenney.

    Fonte do Pack: https://kenney.nl/assets/new-platformer-pack

🎮 Gênero

Platformer (Plataforma) - Jogo de visão lateral focado em pular entre plataformas, evitar obstáculos e derrotar inimigos.

✨ Requisitos Mínimos e Tecnologias

O projeto foi desenvolvido estritamente seguindo as regras do ambiente PgZero e o conjunto limitado de bibliotecas permitidas.

    Linguagem: Python 3.x

    Ambiente de Desenvolvimento Recomendado: Mu Editor (Modo Pygame Zero)

    Biblioteca Principal: PgZero

    Módulos Permitidos: PgZero, math, random.

    Exceção: Uso da classe Rect (disponível no PgZero/Pygame).

🚀 Como Jogar

Instalação de Dependências: Certifique-se de ter o Python instalado. Instale o pgzero:

    pip install pgzero

Preparação dos Arquivos: Salve o código principal do jogo (ex: game.py) e garanta que todas as pastas de recursos (sprites em images, sons em sounds, música em music) estejam localizadas na mesma pasta, conforme a estrutura padrão do PgZero.

Execução:

    Mu Editor (Recomendado): Abra o arquivo do jogo no Mu Editor no modo Pygame Zero e clique no botão "Play" (Reproduzir).
        pgzrun game.py

🕹️ Controles

    Ação	Tecla
    Mover Esquerda	Seta Esquerda (←)
    Mover Direita	Seta Direita (→)
    Pular	Barra de Espaço (SPACE)
    Voltar ao Menu	Enter (RETURN) (nas telas de Fim de Jogo/Vitória)

📋 Funcionalidades Implementadas

    Estrutura e Gerenciamento do Jogo

    Menu Principal: Tela inicial completa com botões INICIAR JOGO, SOM: LIGADO/DESLIGADO e SAIR.

    Progressão de Fases: 4 fases distintas (Fase 1 a Fase 4) com layouts crescentes em dificuldade.

    Sistema de Vidas e Pontuação: Gerenciamento de 5 vidas; pontuação é concedida a cada fase concluída.

    Telas Finais: Telas GAME_OVER e WINNER com estética de pixel art e retorno ao menu.

Personagens e Mecânicas de Platformer

    Classe Hero:

        Implementa física básica: gravidade (apply_gravity()) e movimento horizontal.

        Lógica de salto com verificação de plataforma.

        Animações de sprite para parado (idle), andando e estado no ar.

    Inimigos (Classes e Tipos):

        Enemy (Patrulha): Inimigos que se movem horizontalmente dentro de um território definido (patrol_range). (Ex: Slimefire, Bee).

        StaticEnemy (Estático): Inimigos fixos com animação contínua (Ex: Barnacle).

        JumpingFrog (Salto): Novo inimigo que utiliza um timer para iniciar saltos em uma direção, patrulhando seu território de forma intermitente.

    Colisão: Detecção de colisão precisa nos eixos X e Y contra plataformas e detecção de toque com todos os tipos de inimigos, resultando em perda de vida.

Animação de Sprite e Conformidade Técnica

    Animação de Múltiplos Frames: O herói usa 18 frames para a animação idle, garantindo um movimento sutil e cíclico mesmo parado.

    Nomenclatura PEP8: Consistência no uso de nomes em inglês e convenções de estilo de código.

📐 Estrutura do Código

    Constantes: Definições de tamanho, física e velocidade.

    Classes de Personagens: Implementação da lógica de jogo e animação para Hero, Enemy, StaticEnemy e JumpingFrog.

    Lógica de Fases: Funções (load_stageX) para construir o mundo e posicionar os elementos.

    Loop Principal (PgZero): Funções draw(), update(), on_mouse_down(), e on_key_down() que gerenciam o fluxo de jogo e a renderização.
