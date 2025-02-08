import logging
import os

from src.threat.trainning import TrainningThreatModel
from src.utils.json import JsonUtils


logging.basicConfig(level=logging.INFO)


config = JsonUtils.load_json("assets/config/config.json")

train = TrainningThreatModel(config)
train.train_model()