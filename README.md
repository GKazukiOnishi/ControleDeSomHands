# Gestos com a Mão Utilizando MediaPipe

Este é um projeto que utiliza a biblioteca MediaPipe para reconhecimento de gestos da mão em tempo real. O projeto é capaz de reconhecer diferentes gestos da mão, como mão aberta, mão fechada, fazendo o sinal do L, sinal Hang-Loose, sinal Rock n Roll, 3 dedos levantados (Indicador, Dedo Médio e Polegar), dessa forma serão executadas ações correspondentes com base nos gestos reconhecidos.

## Funcionalidades

- Reconhecimento de gestos da mão em tempo real.
- Execução de ações correspondentes com base nos gestos reconhecidos, como controlar o volume, avançar ou retroceder músicas e pausar/reproduzir músicas.

## Dependências

- OpenCV (cv2)
- NumPy
- MediaPipe
- pynput
- math
- cvzone

## Como Reproduzir o Programa

1. Certifique-se de ter todas as dependências instaladas. Você pode instalá-las via pip:

2. Baixe o arquivo `utils.py` que contém as funções utilitárias necessárias para o projeto.

3. Copie o código do script fornecido `main.py` para um arquivo Python.

4. Execute o script Python.

5. Uma janela será aberta mostrando a câmera. Coloque a sua mão dentro da área de visão da câmera e comece a fazer gestos para ver o reconhecimento em tempo real.

    Sinais:
        
        * Sinal 3 Dedos Levantados (Indicador, Dedo Médio e Polegar) = Pausar/Play na faixa;
        * Sinal Hang-Loose = Retroceder a faixa;
        * Sinal Rock n Roll = Avançar a faixa;
        * Sinal L = Aumentar e diminuir volume (Abrindo o sinal do L, o volume aumentará. Fechando o sinal do L, o volume diminuirá.).

6. Para sair do programa, basta clicar no ‘X’ para finalizar o programa.

## Configurações e Ajustes

- O script possui algumas configurações que podem ser ajustadas, como o número de frames para confirmar um gesto (`FRAMES_TO_CONFIRM`), se deseja usar a profundidade para calcular o volume (`USA_PROFUNDIDADE`), entre outros. Você pode modificar essas configurações diretamente no código-fonte.




## Feito por

Grupo Cicada

Breno de Souza Silva (88332)
breno.desouza20@gmail.com

Felipe Otto da Silva (89108)
imerkzx@gmail.com

Gabriel Kazuki Onishi (87182)
gkazuki.onishi@gmail.com

Pedro Martins Procopio Argentati (88246)
pedro.argentatii@gmail.com

Rafael Tannous (87486)
tannousrafael@gmail.com



