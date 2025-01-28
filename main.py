import logging
import os

from utils.json import JsonUtils


logging.basicConfig(level=logging.INFO)


config = JsonUtils.load_json("assets/config/config.json")

