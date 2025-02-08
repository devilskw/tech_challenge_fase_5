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
from fastai.vision.all import *

# Referencia: https://docs.fast.ai/tutorial.vision.html

class TrainningThreatModel:

  cfg: dict
  path: Path
  CLASSES_LABEL_REGEX_PATTERN = r'^(.+?)_'
  training_images: L

  def __init__(self, cfg: dict):
    self.cfg = cfg
    if not (self.cfg['training']['active']):
      return
    self.__load_training_images__()


  def __load_training_images__(self):
    """
    Carrega as imagens de treino do diretorio configurado.

    Atribui a self.path o caminho do diretorio das imagens de treino,
    e a self.training_images a lista de imagens do diretorio de treino.
    """
    self.path = Path(self.cfg['training']['input_path'])
    self.training_images = get_image_files(self.path)

  def __prepare_data_for_training__(self):
    """
    Prepara os daods para treino do modelo de ameaças.

    Este método usa o 'ImageDataLoaders.from_name_re' para carregar as imagens para treino,
    usando regular expressions para classificar as imagens como ameaças ou não baseada no prefixo do nome do arquivo de imagem.

    Returns:
        DataLoaders
    """
    data: DataLoaders = ImageDataLoaders.from_name_re(                    # deixamos o prefixo do nome do arquivo indicando se é ou não ameaça, por isso vamos usar este metodo
                        path = self.path,
                        fnames = self.training_images,
                        pat = self.CLASSES_LABEL_REGEX_PATTERN,   # É o regex que vamos usar para classificar as imagens que são ou não ameaças (considerando prefixo anes do '_')
                        item_tfms=Resize(256),                            # Vamos transformar redimensionando as imagens em 256x256
                        batch_tfms=[*aug_transforms(size=224), Normalize.from_stats(*imagenet_stats)],
                        bs=64)
    data.show_batch()
    return data


  def train_model(self):
    data = self.__prepare_data_for_training__()
    learn = cnn_learner(data, resnet50, metrics=error_rate)
    learn.fine_tune(3, 3e-2) # todo parei aqui pra continuar a analisar
    learn.lr_find()

