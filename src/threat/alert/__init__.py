import logging
class ThreatAlert:


  def __init__(self, cfg: dict):
    self.cfg = cfg
    self.log = logging.getLogger(__name__)
  
  def send_email(self, dest: str, subject: str, message: str) -> None:
    pass