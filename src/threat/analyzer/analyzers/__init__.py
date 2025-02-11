import logging
import cv2
from cv2.typing import MatLike
from fastai.vision.all import *

from src.threat.trainning import TrainningThreatModel


class TrainedModelBasedAnalyzer:

  cfg: dict
  learn: Learner

  def __init__(self, cfg: dict):
    self.cfg = cfg
    self.log = logging.getLogger(__name__)
    self.__load_trained_model__()

  def __load_trained_model__(self):
    self.learn = load_learner(f"{self.cfg['training']['output_path']}\\{self.cfg['training']['model_filename']}")

  def analyze_frame(self, frame: MatLike, id_frame: int):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (256, 256))
    p_class, p_bbox, p_prob = self.learn.predict(image) # https://forums.fast.ai/t/prediction-on-video-input-file/41029
    return frame, p_class, p_bbox, p_prob