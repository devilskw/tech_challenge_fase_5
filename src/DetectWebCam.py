import cv2
import torch
import random
import os
import smtplib
import glob
from email.message import EmailMessage
from ultralytics import YOLO

# Configurações do modelo e diretório de prints
MODEL_PATH     = "../model_ai/runs/detect/train3/weights/best.pt"
PRINTS_FOLDER  = "../src/detections/webcam/"

# Configurações de e-mail
EMAIL_SENDER    = "jonathan.desenv@gmail.com"
EMAIL_RECEIVER  = "jonathan.desenv@gmail.com"
EMAIL_PASSWORD  = "tkki fcbm sfsk dcyj"

# Criar diretório para os prints, se não existir
os.makedirs(PRINTS_FOLDER, exist_ok=True)

# Carregar modelo YOLO
model = YOLO(MODEL_PATH)

# Abrir webcam
cap = cv2.VideoCapture(0)  # 0 para webcam padrão

# Lista para armazenar frames salvos como prints
saved_frames = []
frame_idx = 0

try:
    while cap.isOpened():  # Mantém o loop ativo apenas enquanto a webcam estiver aberta
        ret, frame = cap.read()
        if not ret:
            break

        # Fazer predições
        results = model(frame)[0]

        # Verificar se há detecções
        detections = results.boxes.data
        if detections.shape[0] > 0:
            for det in detections:
                x1, y1, x2, y2, conf, cls = det.tolist()
                label = f"{model.names[int(cls)]} {conf:.2f}"
                
                # Desenhar bounding box
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Salvar prints aleatórios
                if frame_idx not in saved_frames and random.random() < 0.1:  # 10% de chance de salvar o frame
                    save_path = os.path.join(PRINTS_FOLDER, f"frame_{frame_idx}.jpg")
                    cv2.imwrite(save_path, frame)
                    saved_frames.append(frame_idx)

        # Exibir imagem com detecções
        cv2.imshow("Detecção em Tempo Real", frame)
        
        # Fechar com tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_idx += 1

finally:
    # Finalizar captura e fechar janelas
    cap.release()
    cv2.destroyAllWindows()

    # Função para enviar e-mail
    def send_email():
        print("Enviando e-mail...")

        # Verificar se há imagens capturadas
        image_files = glob.glob(os.path.join(PRINTS_FOLDER, "*.jpg"))
        if not image_files:
            print("Nenhum print detectado, e-mail não será enviado.")
            return

        # Criar a mensagem
        msg = EmailMessage()
        msg["Subject"] = "Alerta: Objetos cortantes detectados na webcam"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg.set_content("Foram detectados objetos cortantes na webcam. Veja os prints anexados.")

        # Adicionar prints como anexos
        for img_path in image_files[:5]:
            with open(img_path, "rb") as img:
                msg.add_attachment(img.read(), maintype="image", subtype="jpeg", filename=os.path.basename(img_path))

        # Enviar e-mail via SMTP
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(msg)
            print("E-mail enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")

    # Chamar função para envio do e-mail
    send_email()

    print("Monitoramento finalizado.")
