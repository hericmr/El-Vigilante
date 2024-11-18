import cv2
import requests
import numpy as np
from ultralytics import YOLO
import time

class TrafficMonitor:
    def __init__(self, camera_url, model_path='yolov8n.pt', vehicle_classes=None, pedestrian_class=0):
        """
        Inicializa a instância do monitor de tráfego.

        :param camera_url: URL da câmera para monitoramento
        :param model_path: Caminho para o modelo YOLO pré-treinado
        :param vehicle_classes: Lista de classes relacionadas a veículos
        :param pedestrian_class: Classe para pedestres (default é 0)
        """
        self.camera_url = camera_url
        self.model = YOLO(model_path)
        self.vehicle_classes = vehicle_classes if vehicle_classes else [2, 3, 5, 7]  # Defaults: car, motorcycle, bus, truck
        self.pedestrian_class = pedestrian_class  # Classe de pedestres (0)

    def fetch_frame(self):
        """
        Captura uma imagem da câmera URL.

        :return: Frame da câmera como matriz OpenCV ou None se falhar
        """
        try:
            response = requests.get(self.camera_url, timeout=10)
            if response.status_code == 200:
                img_array = np.array(bytearray(response.content), dtype=np.uint8)
                frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                return frame
            else:
                print(f"Erro ao acessar a URL: {response.status_code}")
                return None
        except Exception as e:
            print(f"Erro ao capturar imagem: {e}")
            return None

    def process_frame(self, frame):
        """
        Aplica o modelo YOLO ao frame capturado e retorna o frame anotado e o número de veículos e pedestres detectados.

        :param frame: Imagem OpenCV
        :return: Frame anotado, número de veículos detectados e número de pedestres detectados
        """
        try:
            results = self.model(frame)
            detections = results[0].boxes.data.cpu().numpy()
            
            # Contagem de veículos e pedestres
            vehicle_count = sum(1 for detection in detections if int(detection[5]) in self.vehicle_classes)
            pedestrian_count = sum(1 for detection in detections if int(detection[5]) == self.pedestrian_class)
            
            annotated_frame = results[0].plot()
            return annotated_frame, vehicle_count, pedestrian_count
        except Exception as e:
            print(f"Erro ao processar frame: {e}")
            return frame, 0, 0

    def annotate_frame(self, frame):
        """
        Adiciona informações sobre o número de veículos detectados e pedestres detectados no frame.

        :param frame: Imagem OpenCV
        :return: Frame anotado com texto adicional
        """
        try:
            annotated_frame, vehicle_count, pedestrian_count = self.process_frame(frame)
            return annotated_frame, vehicle_count, pedestrian_count
        except Exception as e:
            print(f"Erro ao adicionar texto ao frame: {e}")
            return frame, 0, 0

    def display_info(self, vehicle_count, pedestrian_count):
        """
        Exibe informações sobre o número de veículos, pedestres e alerta de trânsito em uma janela separada.

        :param vehicle_count: Número de veículos detectados
        :param pedestrian_count: Número de pedestres detectados
        """
        info_window = np.zeros((200, 750, 3), dtype=np.uint8)  # Janela de informações preta

        # Exibe o status de trânsito com base no número de veículos
        if vehicle_count <= 12:
            text_color = (0, 255, 0)  # Verde para trânsito normal
            cv2.putText(info_window, f"TRANSITO NORMAL - Veiculos: {vehicle_count}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)
        elif 12 < vehicle_count <= 14:
            text_color = (0, 255, 255)  # Amarelo para trânsito médio
            cv2.putText(info_window, f"TRANSITO MEDIO - Veiculos: {vehicle_count}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)
        else:
            text_color = (0, 0, 255)  # Vermelho para alerta de trânsito
            cv2.putText(info_window, f"ALERTA! TRANSITO DETECTADO! Veiculos: {vehicle_count}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)

        # Exibe o número de pedestres detectados separadamente
        cv2.putText(info_window, f"Pedestres detectados: {pedestrian_count}", (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Exibe a janela de informações
        cv2.imshow("Informações de Trânsito", info_window)

    def display(self, window_name="Traffic Monitor", delay=2):
        """
        Exibe o feed da câmera com detecções e informações sobre o número de veículos e pedestres.

        :param window_name: Nome da janela
        :param delay: Intervalo entre atualizações em segundos
        """
        print(f"Exibindo feed da câmera: {self.camera_url}")
        
        # Cria a janela para o feed da câmera em tela cheia
        cv2.namedWindow(window_name, cv2.WINDOW_FULLSCREEN)

        while True:
            frame = self.fetch_frame()
            if frame is not None:
                annotated_frame, vehicle_count, pedestrian_count = self.process_frame(frame)

                # Exibe a imagem com o feed da câmera
                cv2.imshow(window_name, annotated_frame)

                # Exibe as informações do tráfego em uma janela separada
                self.display_info(vehicle_count, pedestrian_count)
            else:
                print("Não foi possível obter o frame. Tentando novamente...")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Finalizando monitoramento.")
                break

            time.sleep(delay)

        cv2.destroyAllWindows()


if __name__ == "__main__":
    # URL da câmera para monitoramento
    camera_url = "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1542/snap_c1.jpg?&t=1731955106282&t=1731955116008"

    # Inicializa o monitor de tráfego e inicia o monitoramento
    monitor = TrafficMonitor(camera_url)
    monitor.display(window_name="Vigilante - Medidor de transito na Ana Costa")
