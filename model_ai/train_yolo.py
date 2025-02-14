from ultralytics import YOLO
import os

dataset_path = "../model_ai/dataset"
yaml_path = os.path.join(dataset_path, "data.yaml")

# Carregar o modelo YOLOv8 pré-treinado
modelo = YOLO("yolov8n.pt")  # Versão pequena do modelo para treinar mais rápido

# Treinar o modelo com o dataset
modelo.train(
    data="../dataset/data.yaml",
    epochs=3,  # Número de épocas
    batch=16,  # Tamanho do lote
    imgsz=640,  # Tamanho das imagens
    device="cpu"  # Usar GPU se disponível, ou mude para "cpu"
)

print("Treinamento concluído!")
