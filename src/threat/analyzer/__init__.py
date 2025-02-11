import logging
from logging import Logger
from abc import ABC, abstractmethod
import os
from src.threat.analyzer.analyzers import TrainedModelBasedAnalyzer
from src.threat.analyzer.video_properties import VideoProperties
import cv2
from cv2 import VideoCapture, VideoWriter
from cv2.typing import MatLike
from src.utils.csv import CsvUtils
from src.threat.alert import ThreatAlert
class ThreatAnalyzer(ABC):

  cfg: dict
  webcam_activated: bool
  WAIT_KEY = 1
  WEBCAM_INPUT_SET_CODE = 0 # Quando for ativar a webcam ao invés de passar um arquivo de vídeo, é necessário passar o valor 0.
  log: Logger
  model_analyzer: TrainedModelBasedAnalyzer

  def __init__(self, cfg: dict):
    self.cfg = cfg
    self.log = logging.getLogger(__name__)
    self.webcam_activated = self.cfg['analyzer']['webcam']['active']
    self.model_analyzer = TrainedModelBasedAnalyzer(cfg)

  def prepare_analyzer(self, video_filename: str) -> tuple[VideoCapture, VideoWriter, VideoProperties]:
    cap = VideoCapture(self.WEBCAM_INPUT_SET_CODE if self.webcam_activated else os.path.join(self.cfg['analyzer']['video']['path']['in'], video_filename))
    self.log.debug('Lendo as propriedades do video ou webcam.')
    prop = VideoProperties(
      width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
      height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
      fps=int(cap.get(cv2.CAP_PROP_FPS)),
      total_frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
      codec = cv2.VideoWriter_fourcc(*'mp4v')
    )
    self.log.debug('Criando o objeto VideoWriter.')
    out = VideoWriter(filename=os.path.join(os.path.join(self.cfg['analyzer']['video']['path']['out'], video_filename)), fourcc=prop.codec, fps=prop.fps, frameSize=(prop.width, prop.height))
    return cap, out, prop

  def __read_frame__(self, id_frame, cap: cv2.VideoCapture):
    self.log.debug(f"Lendo o frame {id_frame} do vídeo ou webcam.")
    return cap.read()

  def __send_threat_alert__(self):
    alert = ThreatAlert(self.cfg)
    alert.send_email(dest=self.cfg['analyzer']['threats']['email']['dest'], subject=self.cfg['analyzer']['threats']['email']['subject'], message=self.cfg['analyzer']['threats']['email']['message'])

  def __save_image__(self, image_filename, frame):
    img_file = os.path.join(self.cfg['analyzer']['threats']['path']['out'], image_filename)
    cv2.imwrite(img_file, frame)

  def __save_video__(self, out: cv2.VideoWriter, frame: MatLike):
    self.log.debug('Escrevendo o frame processado no vídeo de saída.')
    out.write(frame)
    return out

  def __save_report__(self, data: list, report_filename: str, first_row: bool = False):
    report_file = os.path.join(self.cfg['analyzer']['threats']['path']['out'], report_filename)
    return CsvUtils.save_csv(report_file, data, first_row)

  def __generate_threat_report__(self, cat, probs, image_filename, video_name, id_frame):
    first_row = id_frame == 1
    data =[]
    if first_row:
      header = ['id_frame', 'category', 'probability', 'image_filename']
      data.append(header)
    data.append([id_frame, cat, float(probs.real[1]) if len(probs.real)> 0 else 'error', image_filename])
    self.__save_report__(data, os.path.join(self.cfg['analyzer']['threats']['path']['out'], f"_{video_name}_threat_report.csv"), first_row)

  def __analyze_frame__(self, id_frame: int, frame: MatLike, video_filename, webcam: bool):
    frame, cat, bbox , probs  = self.model_analyzer.analyze_frame(frame, id_frame)

    # if (cat== "threat" and len(probs.real) >0 and probs.real[1] > 0.90): # se a categoria tiver certa/alta probabilidade de ameaça
    alert = (cat == "threat")
    if alert:
      image_filename = video_filename.replace(".mp4", f"_{id_frame}.png")
      self.__save_image__(image_filename, frame)
      self.__generate_threat_report__(cat, probs, image_filename, video_filename.replace(".mp4", ""), id_frame )

    return frame, alert

  @abstractmethod
  def analyze(self, video_filename:str|None = None):
    self.log.debug('Iniciando a análise do vídeo ou webcam')