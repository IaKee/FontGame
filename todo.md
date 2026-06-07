- Colocar barra de progresso borderless na parte de cima da  janela (contagem regressiva em barra), a cor vai fazendo o gradiente entre azul e vermelho, quanto menos tempo tem restante, caso o tempo acabe, voce perde
- Ao inves de selecionar direto uma opção, ela fica marcada, e precisa de um confirmar, ou enter para confirmar a seleção
- Caso a resposta esteja certa, muda direto para a proxima questão
- As alternativas devem ser exibidas com 2 por linha, e 6 no total (modelo genio quiz)
- Todas as fontes utilizadas na UI da aplicação devem ser comic sans (externas ao jogo em si) 
- Ao inves de 3 modos diferentes de dificuldades, colocar sistema de dificuldade, com fatores de dificuldade que o jogador pode escolher antes de iniciar um jogo, sendo os itens abaixo. Fatores com numero mais baixo devem ser os mais fáceis. Fatores com número mais alto devem pontuar mais: 
  > tamanho da fonte aleatorio - fatores de randomização 1, 2 e 3 (incluindo tamanhos diferentes entre letras das palavras da frase)
  > cores diferentes - fatores de randomização 1, 2 e 3 (cores diferentes entre letras, a cor das letras nunca deve ser IGUAL a do fundo, mas pode ser um pouco diferente)
  > fonte usada em cada alternativa - fatores 1, 2 e 3 - sendo que no fator 1 a resposta usa a fonte com o proprio nome, no 2 é usada a fonte padrao comic sans em todas alternativas, e na 3 é usada uma fonte aleatória para cada alternativa
  > quanto tempo o texto de exemplo vai ficar sendo exibido, entre infinito, 5 segundos e .5 segundos
  > tempo útil para acertar, entre tempo fixo, tempo fixo menor, e tempo cada vez menor (diminuindo gradualmente de 15 segundos a 3)
  > fontes utilizadas, entre somente as padroes do windows excluindo dingbats e fontes estranhas, todas do windows e todas as instaladas no sistema atual
  
- O unico modo de jogo deve ser o infinito, até onde o jogador conseguir pontuar
- A pontuação de cada um desses fatores, e nível de fator deve ser balanceada, com um sistema de pesos
- No final, game over é apresentado a pontuação total atingida. Cada palavra da tela de game over deve ser de uma fonte diferente. Na tela de game over devem aparecer os acertos realizados, com a frase de exemplo que foi realizada, e quanto tempo o jogador levou para marcar aquele acerto


















área de descansso de cursor do live share: 