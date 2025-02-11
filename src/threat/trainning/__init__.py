from pathlib import Path
from fastai.vision.data import get_image_files
from fastcore.foundation import L
from fastai.metrics import error_rate
from fastai.vision.data import ImageDataLoaders
from fastai.vision.augment import aug_transforms, Resize
from fastai.data.core import DataLoaders
from fastai.vision.models import resnet50
from fastai.vision.data import Normalize
from fastai.vision.core import imagenet_stats
from fastai.callback.fp16 import MixedPrecision

from fastai.vision.all import *

# Referencia: https://docs.fast.ai/tutorial.vision.html

class TrainningThreatModel:

  cfg: dict
  path: Path
  CLASSES_LABEL_REGEX_PATTERN = r'^(.+?)_'
  training_images: L

  def __init__(self, cfg: dict):
    self.cfg = cfg
    self.__load_training_images__()


  def __load_training_images__(self):
    """
    Carrega as imagens de treino do diretorio configurado.

    Atribui a self.path o caminho do diretorio das imagens de treino,
    e a self.training_images a lista de imagens do diretorio de treino.
    """
    self.path = Path(self.cfg['training']['input_path'])
    self.training_images = get_image_files(self.path)

  def prepare_learner(self):
    """
    Prepara o visio learner com os dados para treino do modelo de ameaças para treinar ou carregar modelo treinado.

    Este método usa o 'ImageDataLoaders.from_name_re' para carregar as imagens para treino,
    usando regular expressions para classificar as imagens como ameaças ou não baseada no prefixo do nome do arquivo de imagem.

    Returns:
        Learner: Retorna o visio learner com os dados para treinar ou carregar modelo treinado.
    """
    dls: DataLoaders = ImageDataLoaders.from_name_re(                    # deixamos o prefixo do nome do arquivo indicando se é ou não ameaça, por isso vamos usar este metodo
                        path = self.path,
                        fnames = self.training_images,
                        pat = self.CLASSES_LABEL_REGEX_PATTERN,   # É o regex que vamos usar para classificar as imagens que são ou não ameaças (considerando prefixo anes do '_')
                        item_tfms=Resize(256),                            # Vamos transformar redimensionando as imagens em 256x256
                        num_workers = 0,   # configurado para evitar o RuntimeError: "An attempt has been made to start a new process before the current process has finished its bootstrapping phase. ", para rodar localmente
                        batch_tfms=[*aug_transforms(size=224), Normalize.from_stats(*imagenet_stats)],
                        bs=64)
    if self.cfg['training']['train']:
      dls.show_batch()
    learn = vision_learner(
      dls,
      resnet50, # arquitetura de modelo de backbone do PyTorch que apoia e simplifica na tarefa de treinamento do modelo -  através do "Deep Residual Learning for Image Recognition" para simplificar o treinamento das redes neurais muito mais aprofundadas que as usadas previamente, cehgando até 3,57% de erros em testes realizados, segundo artigo em: https://arxiv.org/abs/1512.03385.
      metrics=error_rate,
      cbs=MixedPrecision(), # MixedPrecision: reduces memory usage and speed up training / EarlyStopping: halt training when validation loss stops improving. / GradientAccumulation: simulates larger batch sizes for memory-constrained environments.
    )
    return learn


  def train_model(self):
    if not self.cfg['training']['train']:
      return
    learn = self.prepare_learner()
    learn.fine_tune(self.cfg['training']['qtd_epoch']) # Starts training the threat model with 5 epoch
    learn.export(f"{self.cfg['training']['output_path']}\\{self.cfg['training']['model_filename']}")

  def analyze_model(self):
    if not self.cfg['training']['debug']:
      return
    learn = load_learner(f"{self.cfg['training']['output_path']}\\{self.cfg['training']['model_filename']}")
    interp = ClassificationInterpretation.from_learner(learn)
    if len(interp.losses) >= 9:
      interp.plot_top_losses(9, nrows=3)
