from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import yaml
import os
import random

# Caminho do arquivo de configuração do dataset
dataset_path = "../model_ai/dataset" 
yaml_path = os.path.join(dataset_path, "data.yaml")

print("Caminho data.yaml" ,yaml_path)

# Ler o arquivo data.yaml
with open(yaml_path, "r") as file:
    dataset_info = yaml.safe_load(file)

# Exibir informações do dataset
print("Classes:", dataset_info["names"])
print("Caminho das imagens de treino: ", dataset_info["train"])

# Carregar imagens aleatórias para visualizar
train_path = dataset_info["train"]

image_files = [f for f in os.listdir(train_path) if f.endswith(".jpg")]

# Selecionar aleatoriamente 3 imagens para exibição
sample_images = random.sample(image_files, 3)

# Exibir as imagens
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for i, img_file in enumerate(sample_images):
    img = cv2.imread(os.path.join(train_path, img_file))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    axes[i].imshow(img)
    axes[i].axis("off")
plt.show()
