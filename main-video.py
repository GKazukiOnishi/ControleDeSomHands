import cv2
import numpy as np
import mediapipe as mp
from utils import mountLandmarksList, conectarPontos, desenharLandmarks, distanciaPontos, getDedosFechados, defineVolume, apertaTecla
from pynput.keyboard import Key
import cvzone

NOME_JANELA = 'Frame'
LARGURA_JANELA = 640
ALTURA_JANELA = 480
FRAMES_TO_CONFIRM = 10
USA_PROFUNDIDADE = True

mediaPipeHands = mp.solutions.hands.Hands()

# Coeficiente angular obtido a partir de uma regressão polinomial de grau 2 - Cálculo de profundidade
distanciaEmPixels = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
distanciaEmCM = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coeficienteAngular = np.polyfit(distanciaEmPixels, distanciaEmCM, 2)
A,B,C = coeficienteAngular

camera = cv2.VideoCapture('video_comandos7.mp4')
camera.set(3, LARGURA_JANELA)
camera.set(4, ALTURA_JANELA)

escalaFixaVolume = [0, 100]

profundidadeCMT = None
tamanhoMao = None
tamanhoMaoReferenciaBase = 400
profundidadeCMTBase = 20
escalaRefDistanciaDedos = [20, 300]

escalaProporcionalDistanciaDedos = None

framesCounter = 0
dedosFechadosAux = []
calculaVolume = False

mensagem = ""

while True:
  leuOFrame, frame = camera.read()
  frameMao = None

  if not leuOFrame:
    break

  frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  resultado = mediaPipeHands.process(frameRGB)

  if resultado.multi_hand_landmarks:
    for hand_index, hand_landmarks in enumerate(resultado.multi_hand_landmarks):
      direitaEsquerda = resultado.multi_handedness[hand_index].classification[0].label

      landmarksList = mountLandmarksList(hand_landmarks.landmark, frame.shape)
      desenharLandmarks(frame, landmarksList)

      conectarPontos(frame, landmarksList, 4, 8)

      dedosFechados = getDedosFechados(landmarksList)
      #print(dedosFechados)

      tamanhoPunho = distanciaPontos(landmarksList, 0, 17)
      profundidadeCMT = (A*tamanhoPunho**2)+(B*tamanhoPunho)+C
      #print(f"Profundidade {profundidadeCMT}, distanciaDedaoIndicador {distanciaPontos(landmarksList, 4, 8)}")

      if dedosFechados != dedosFechadosAux:
        framesCounter = 0
        dedosFechadosAux = dedosFechados
        calculaVolume = False

      if framesCounter == FRAMES_TO_CONFIRM:
        if dedosFechados == [True, True, True, True, True] or dedosFechados == [False, True, True, True, True]:
          print("Mão fechada")
          mensagem = "Mao Fechada"
          escalaProporcionalDistanciaDedos = None
        if dedosFechados == [False, False, False, False, False]:
          print("Mão aberta")
          mensagem = "Mao Aberta"
          tamanhoMao = distanciaPontos(landmarksList, 0, 12)
          print(f"Tamanho da mão {tamanhoMao}")
        if dedosFechados == [False, False, True, True, True]:
          print("Faz o L")
          mensagem = "Faz o L"
          calculaVolume = True

          if USA_PROFUNDIDADE:
            refInferior = (escalaRefDistanciaDedos[0] * profundidadeCMTBase) / profundidadeCMT
            refSuperior = (escalaRefDistanciaDedos[1] * profundidadeCMTBase) / profundidadeCMT
          else:
            refInferior = (escalaRefDistanciaDedos[0] / tamanhoMaoReferenciaBase) * tamanhoMao
            refSuperior = (escalaRefDistanciaDedos[1] / tamanhoMaoReferenciaBase) * tamanhoMao

          escalaProporcionalDistanciaDedos = [refInferior, refSuperior]

          print(f"Referência Inferior {refInferior}, Referência Superior {refSuperior}, tamanhoReferenciaBase {tamanhoMaoReferenciaBase}, tamanhoMao {tamanhoMao}, profundidadeCMTBase {profundidadeCMTBase}, profundidadeCMT {profundidadeCMT}")
        if dedosFechados == [False, False, True, True, False]:
          print("Volta Música")
          mensagem = "Voltar Musica"
          apertaTecla(Key.media_previous)
        if dedosFechados == [False, True, True, True, False]:
          mensagem = "Proxima Musica"
          print("Proxima Musica")
          apertaTecla(Key.media_next)
        if dedosFechados == [False, False, False, True, True]:
          print("Play/Pause")
          mensagem = "Play/Pause"
          apertaTecla(Key.media_play_pause)

      if calculaVolume:
        distanciaDedaoIndicador = distanciaPontos(landmarksList, 4, 8)
        volumeXDist = None
        if escalaProporcionalDistanciaDedos is not None:
          volumeXDist = np.interp(distanciaDedaoIndicador, escalaProporcionalDistanciaDedos, escalaFixaVolume)
        else:
          volumeXDist = None
        #print(f"Distância {distanciaDedaoIndicador}, Volume {volumeXDist}, escalaProporcionalDistanciaDedos {escalaProporcionalDistanciaDedos}, profundidadeCMT {profundidadeCMT}")
        
        #defineVolume(volumeXDist)
        if volumeXDist > 70.00:
          defineVolume(volumeXDist)
          mensagem = "Aumentar Volume"
      
        if volumeXDist < 20.00:
          defineVolume(volumeXDist)
          mensagem = "Diminuir Volume"

  if mensagem is not None:
    cvzone.putTextRect(frame,mensagem,(25,55))
  cv2.imshow(NOME_JANELA, frame)
  
  if cv2.waitKey(25) & 0xFF == ord('q'):
    break
  
  framesCounter += 1

camera.release()
cv2.destroyAllWindows()