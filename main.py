import logging
import os

from src.threat.analyzer.video_analyzer import VideoAnalyzer
from src.threat.trainning import TrainningThreatModel
from src.utils.json import JsonUtils


logging.basicConfig(level=logging.INFO)


config = JsonUtils.load_json("assets/config/config.json")

train = TrainningThreatModel(config)
train.train_model()
train.analyze_model()

analyzer = VideoAnalyzer(config)
for video_filename in config['analyzer']['video']['filenames']:
  analyzer.analyze(video_filename)