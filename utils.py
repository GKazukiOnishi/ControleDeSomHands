import cv2
import math
from pynput.keyboard import Key, Controller

COR_PONTO = (0, 0, 255)
COR_LINHA = (0, 255, 0)

teclado = Controller()

def mountLandmarksList(landmarks, shape):
  landmarksList = []

  for landmark in landmarks:
    x, y = int(landmark.x * shape[1]), int(landmark.y * shape[0])
    landmarksList.append((x, y, landmark.z))

  return landmarksList

def conectarPontos(imagem, pontos, idx1, idx2):
  cv2.line(imagem, (pontos[idx1][0], pontos[idx1][1]), (pontos[idx2][0], pontos[idx2][1]), COR_LINHA, 1)

def desenharLandmarks(imagem, pontos):
  contador = 0

  for ponto in pontos:
    x, y, z = ponto

    cv2.circle(imagem, (x, y), 5, COR_PONTO, -1)
    cv2.putText(imagem, str(contador), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0, 255, 0), 2)
    contador += 1

  conectarPontos(imagem, pontos, 0, 1)
  conectarPontos(imagem, pontos, 1, 2)
  conectarPontos(imagem, pontos, 2, 3)
  conectarPontos(imagem, pontos, 3, 4)
  conectarPontos(imagem, pontos, 0, 5)
  conectarPontos(imagem, pontos, 5, 6)
  conectarPontos(imagem, pontos, 6, 7)
  conectarPontos(imagem, pontos, 7, 8)
  conectarPontos(imagem, pontos, 5, 9)
  conectarPontos(imagem, pontos, 9, 10)
  conectarPontos(imagem, pontos, 10, 11)
  conectarPontos(imagem, pontos, 11, 12)
  conectarPontos(imagem, pontos, 9, 13)
  conectarPontos(imagem, pontos, 13, 14)
  conectarPontos(imagem, pontos, 14, 15)
  conectarPontos(imagem, pontos, 15, 16)
  conectarPontos(imagem, pontos, 13, 17)
  conectarPontos(imagem, pontos, 17, 18)
  conectarPontos(imagem, pontos, 18, 19)
  conectarPontos(imagem, pontos, 19, 20)
  conectarPontos(imagem, pontos, 0, 17)

def distanciaPontos(pontos, idx1, idx2):
  x1, y1, z1 = pontos[idx1]
  x2, y2, z2 = pontos[idx2]

  return math.hypot(x2 - x1, y2 - y1)

def getDedosFechados(landmarks):
  dedos = []

  distanciaY2a4 = landmarks[4][1] - landmarks[2][1]
  distanciaY2a3 = landmarks[3][1] - landmarks[2][1]
  distanciaX2a4 = landmarks[4][0] - landmarks[2][0]
  distanciaX2a3 = landmarks[3][0] - landmarks[2][0]

  if (abs(distanciaY2a4) < abs(distanciaY2a3) * 1.3) or (abs(distanciaX2a4) < abs(distanciaX2a3) * 1.3):
    dedos.append(True)
  else:
    dedos.append(False)

  for i in range(5, 21, 4):
    if landmarks[i][1] < landmarks[i + 3][1]:
      dedos.append(True)
    else:
      dedos.append(False)

  return dedos

def defineVolume(volume):
  if volume > 70.00:
    teclado.press(Key.media_volume_up)
    teclado.release(Key.media_volume_up)

  if volume < 20.00:
    teclado.press(Key.media_volume_down)
    teclado.release(Key.media_volume_down)

def apertaTecla(tecla):
  teclado.press(tecla)
  teclado.release(tecla)