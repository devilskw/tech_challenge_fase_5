import logging
from logging import Logger
from abc import ABC, abstractmethod
import os
from video_properties import VideoProperties
import cv2
from cv2 import VideoCapture, VideoWriter
from cv2.typing import MatLike
from utils.csv import CsvUtils
from threat.alert import ThreatAlert
class ThreatAnalyzer(ABC):

  cfg: dict
  webcam_activated: bool
  wait_key = 1
  input_video: any
  log: Logger

  def __init__(self, cfg: dict):
    self.cfg = cfg
    self.webcam_activated = cfg.get('webcam', False)
    self.input_video = 0 if self.webcam_activated else os.path.join(cfg.get('path_in'), cfg.get('video_filename'))
    self.log = logging.getLogger(__name__)

  def prepare_analyzer(self) -> tuple[VideoCapture, VideoWriter, VideoProperties]:
    cap = VideoCapture(self.input_video)
    self.log.debug('Lendo as propriedades do video ou webcam.')
    prop = VideoProperties(
      width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
      height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
      fps=int(cap.get(cv2.CAP_PROP_FPS)),
      total_frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
      codec = cv2.VideoWriter_fourcc(*'mp4v')
    )
    self.log.debug('Criando o objeto VideoWriter.')
    out = VideoWriter(filename=os.path.join(self.cfg.get('path_out'), self.cfg.get('video_filename')), fourcc=prop.codec, fps=prop.fps, frameSize=(prop.width, prop.height))
    return cap, out, prop

  def __send_threat_alert__(self):
    alert = ThreatAlert(self.cfg)
    alert.send_email(dest=self.cfg.get('email'), subject='Alerta de perigo', message='O video foi processado e o algoritmo identificou um perigo.')

  def __save_video_image__(self, filename, frame):
    img_file = os.path.join(self.path_out, filename)
    cv2.imwrite(img_file, frame)

  def __save_video__(self, out: cv2.VideoWriter, frame: MatLike):
    self.log.debug('Escrevendo o frame processado com landmark no vídeo de saída.')
    out.write(frame)
    return out

  def __append_gestures_report__(self, filename, id_frame, gestures, first_row = False):
    data = []
    header = ['id_frame', 'id_gesture', 'gesture_name', 'gesture_description']
    if (first_row):
      data.append(header)
    for gesture in gestures:
      data.append([id_frame, gesture['id_gesture'], gesture['gesture_name'], gesture['gesture_description']])
    csv_file = os.path.join(self.path_out, filename)
    CsvUtils.save_csv(csv_file, data, first_row)
    return len(gestures)

  @abstractmethod
  def analyze(self):
    self.log.debug('Iniciando a análise do vídeo')