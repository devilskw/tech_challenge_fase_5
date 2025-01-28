import logging
import cv2
from tqdm import tqdm

from threat.analyzer import ThreatAnalyzer

class VideoAnalyzer(ThreatAnalyzer):
  def __init__(self, cfg: dict):
    super().__init__(cfg)
    self.log = logging.getLogger(__name__)
  
  def analyze(self):
    cap, out, prop = self.prepare_analyzer()
    self.log.info(f"Total de frames que serão analisados: {prop.total_frames}")
    for _ in tqdm(range(prop.total_frames), desc="Percentual de processamento do vídeo"):
      id_frame += 1

      ret, frame = self.__read_frame__(id_frame, cap)
      if not ret:
        self.log.warning(f"Não foi possível ler o frame {id_frame} do vídeo. Saindo...")
        break

      if not self.cfg['test'] or (self.cfg['test'] and (id_frame % 50 == 0)):
        frame = self.__analyze_frame__(id_frame, frame, face_analyzer, gesture_analyzer, video_filename, False)

      out = self.__save_video__(out, frame)
      if cv2.waitKey(self.wait_key) & 0xFF == ord('q'):
        break
    out.release()
    cap.release()
    cv2.destroyAllWindows()