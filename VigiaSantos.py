import cv2
import numpy as np
import multiprocessing
import time

def exibir_menu():

    print(V + """
⠀⠀⠀⠀⠀⠀⠈⣷⣄⠀⠀⠀⠀⣾⣷⠀⠀⠀⠀⣠⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢿⠿⠃⠀⠀⠀⠉⠉⠁⠀⠀⠐⠿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀     Bem-vindo ao Vigilante Santos!
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⣶⣶⣶⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⠀⠀⠀⠀⠀⠀    
⠀⠀⠀⣠⣶⣿⣿⡿⣿⣿⣿⡿⠋⠉⠀⠀⠉⠙⢿⣿⣿⡿⣿⣿⣷⣦⡀⠀⠀⠀    Acesso câmeras em tempo real e
⠀⢀⣼⣿⣿⠟⠁⢠⣿⣿⠏⠀⠀⢠⣤⣤⡀⠀⠀⢻⣿⣿⡀⠙⢿⣿⣿⣦⠀⠀    detecção de objetos com a ia
⣰⣿⣿⡟⠁⠀⠀⢸⣿⣿⠀⠀⠀⢿⣿⣿⡟⠀⠀⠈⣿⣿⡇⠀⠀⠙⣿⣿⣷⡄    Yolov3!
⠈⠻⣿⣿⣦⣄⠀⠸⣿⣿⣆⠀⠀⠀⠉⠉⠀⠀⠀⣸⣿⣿⠃⢀⣤⣾⣿⣿⠟⠁
⠀⠀⠈⠻⣿⣿⣿⣶⣿⣿⣿⣦⣄⠀⠀⠀⢀⣠⣾⣿⣿⣿⣾⣿⣿⡿⠋⠁⠀⠀    por Heric M. 2023
⠀⠀⠀⠀⠀⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠛⠿⠿⠿⠿⠿⠿⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢰⣷⡦⠀⠀⠀⢀⣀⣀⠀⠀⠀⢴⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣸⠟⠁⠀⠀⠀⠘⣿⡇⠀⠀⠀⠀⠙⢷⠀⠀⠀⠀⠀⠀⠀⠀""")

    print(R + "-" * 54)
    print(V +
        " [0] Canal 6 \n [1] Canoagem \n [3] Travessia da balsa "
        "\n [4] Epitácio Pessoa e Oswaldo Cochrane (sentido c5) \n [5] Canal 4 (sentido SV) "
        "\n [6] Centro de Paquera do Embaré \n [7] Canal 4 sentido (Epitácio Pessoa) ")
    entrada = input().strip().split(',')
    return entrada

objeto_velocidade = {}

def exibir_feed_camera(lugar, url):
    # Carregue os arquivos de configuração e pesos pré-treinados
    net = cv2.dnn.readNetFromDarknet('build/darknet/x64/yolov3.cfg', 'yolov3.weights')

    # Carregue as classes
    classes = []
    with open('cfg/coco.names', 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    # Obtenha as camadas de saída
    output_layers = ['yolo_82', 'yolo_94', 'yolo_106']

    tempos_deteccao = {}

    while True:
        cap = cv2.VideoCapture(url)
        ret, frame = cap.read()

        if ret:
            # Pré-processamento do quadro
            blob = cv2.dnn.blobFromImage(frame, 0.003, (416, 416), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(output_layers)

            # Lista para armazenar informações de detecção
            class_ids = []
            confidences = []
            boxes = []

            # Loop pelas detecções
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]

                    # Filtro de confiança mínima
                    if confidence > 0.5:
                        # Coordenadas do objeto detectado
                        centro_x = int(detection[0] * frame.shape[1])
                        centro_y = int(detection[1] * frame.shape[0])
                        w = int(detection[2] * frame.shape[1])
                        h = int(detection[3] * frame.shape[0])

                        # Coordenadas do retângulo
                        x = int(centro_x - w / 2)
                        y = int(centro_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            # Aplicar supressão não máxima para eliminar detecções redundantes
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

            # Desenhar caixas delimitadoras e rótulos nas detecções
            fonte = cv2.FONT_HERSHEY_SIMPLEX
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    confidence = confidences[i]
                    objeto_regiao = frame[y:y+h, x:x+w]
                    local = np.round(np.mean(objeto_regiao, axis=(0, 1))).astype(int)
                    cor = (0, 255, 0)  # Cor da caixa delimitadora (verde)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), cor, 1)
                    cv2.putText(frame, f'{label}: {confidence:.2f}', (x, y - 10), fonte, 0.5, cor, 1)
                    print(f"Objeto detectado: {label}, Confiança: {confidence:.2f}")
                    print("Valores de pixel (BGR):", local)

                    # Verificar se o objeto está parado há mais de dezsegundos
                    objeto_id = f"{class_id}-{centro_x}-{centro_y}"
                    if objeto_id in tempos_deteccao:
                        tempo_deteccao, valor_pixel_anterior = tempos_deteccao[objeto_id]
                        tempo_atual = time.time()
                        valor_pixel_atual = tuple(local)
                        if tempo_atual - tempo_deteccao > 10 and valor_pixel_atual == valor_pixel_anterior:
                            print("Objeto está estacionado!")

                    # Atualizar o tempo de detecção do objeto
                    tempos_deteccao[objeto_id] = (time.time(), tuple(local))

            # Exibir o quadro com as detecções
            cv2.namedWindow(f'Vigilante Santos - Exibindo cam {lugar}', cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(f'Vigilante Santos - Exibindo cam {lugar}', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow(f'Vigilante Santos - Exibindo cam {lugar}', frame)

        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

def selecionar_camera(cameras):
    while True:
        entrada = exibir_menu()
        if entrada == [""]:
            break
        processos = []
        for item in entrada:
            if item in cameras:
                lugar = cameras[item]["lugar"]
                url = cameras[item]["url"]
                processo = multiprocessing.Process(target=exibir_feed_camera, args=(lugar, url))
                processo.start()
                processos.append(processo)
        for processo in processos:
            processo.join()

V = "\033[31m"  # vermelho
R = "\033[35m"  # roxo

cameras = {
"0" : {"lugar": "do Canal 6","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1593/snap_c1.jpg?1677157043869"},
"1" : {"lugar": "da Canoagem","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1464/snap_c1.jpg?1677191520757"},
"3" : {"lugar": "da Travessia da balsa","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1455/snap_c1.jpg?1677248602110"},
"4" : {"lugar": "da Epitacio Pessoa com Oswaldo Chocrane","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1584/snap_c1.jpg?1677311079649",},
"5" : {"lugar": "do C4","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1578/snap_c1.jpg?1677311184499",},
"6" : {"lugar": "do CPE","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1561/snap_c1.jpg?1677311246793",},
"7" : {"lugar": "do Canal 4","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1591/snap_c1.jpg?1677311286046"},
"8" : {"lugar": "da fonte do Sapo", "url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1517/snap_c1.jpg?1687433186816",}}

selecionar_camera(cameras)
