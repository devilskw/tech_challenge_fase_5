import logging
import cv2
from tqdm import tqdm

from src.threat.analyzer import ThreatAnalyzer

class VideoAnalyzer(ThreatAnalyzer):
  def __init__(self, cfg: dict):
    super().__init__(cfg)
    self.log = logging.getLogger(__name__)

  def analyze(self, video_filename: str):
    if not self.cfg['analyzer']['video']['active']:
      return
    try:
      cap, out, prop = self.prepare_analyzer(video_filename)
      self.log.info(f"Total de frames que serão analisados: {prop.total_frames}")
      id_frame = 0
      has_threat_alerts = False
      for _ in tqdm(range(prop.total_frames), desc="Percentual de processamento do vídeo"):
        id_frame += 1

        ret, frame = self.__read_frame__(id_frame, cap)
        if not ret:
          self.log.warning(f"Não foi possível ler o frame {id_frame} do vídeo. Saindo...")
          break

        frame, alert = self.__analyze_frame__(id_frame, frame, video_filename, False)
        if alert:
          has_threat_alerts = True

        out = self.__save_video__(out, frame)
        if cv2.waitKey(self.WAIT_KEY) & 0xFF == ord('q'):
          break
      if has_threat_alerts:
        self.__send_threat_alert__()
    except Exception as e:
      self.log.error(f"Ocorreu um erro ao processar o vídeo: {e}")
      raise e
    finally:
      out.release()
      cap.release()
      cv2.destroyAllWindows()
