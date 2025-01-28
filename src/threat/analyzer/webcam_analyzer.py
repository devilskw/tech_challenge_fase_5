import logging
import cv2

from threat.analyzer import ThreatAnalyzer

class WebCamAnalyzer(ThreatAnalyzer):
  def __init__(self, cfg: dict):
    super().__init__(cfg)
    self.log = logging.getLogger(__name__)

  def analyze(self):
    cap, out, _ = self.prepare_analyzer()
    while cap.isOpened():
      id_frame += 1
      ret, frame = self.__read_frame__(id_frame, cap)
      if not ret:
        self.log.warning(f"Não foi possível ler o frame {id_frame} do vídeo. Saindo...")
        break
      frame = self.__analyze_frame__(id_frame, frame, face_analyzer, gesture_analyzer, video_filename, True)
      out = self.__save_video__(out, frame)
      cv2.imshow("Teste webcam", frame)
      if cv2.waitKey(self.wait_key) == 27 or cv2.getWindowProperty("Teste webcam", cv2.WND_PROP_VISIBLE) < 1: # esc key pressed == 27 ou fechar a janela
        break
    out.release()
    cap.release()
    cv2.destroyAllWindows()