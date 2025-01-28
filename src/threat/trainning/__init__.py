from utils.rar import RarUtils

class TrainningThreatModel:

  cfg: dict

  def __init__(self, cfg: dict):
    self.cfg = cfg
    self.__prepare_zipped_dataset__()

  def __prepare_zipped_dataset__(self):
    if not self.cfg['training']['active'] or self.cfg['training']['test']:
      return
    RarUtils.unrar(self.cfg['training']['filename'], output_path=self.cfg['training']['output'])

  def 
    