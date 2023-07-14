# VigiaSantos
Vigia Santos é um script de monitoramento em tempo real que permite acessar câmeras de segurança em diferentes locais de Santos. 
Utilizando a rede neural YOLOv3, o programa detecta e rastreia 80 tipos de objetos em tempo real.

Com Vigia Santos, você pode selecionar e visualizar feeds de câmera específicos, incluindo o Canal 6, Canoagem, Travessia da balsa, 
Epitácio Pessoa e Oswaldo Cochrane, Canal 4 (sentido SV), Centro de Paquera do Embaré e Canal 4 (sentido Epitácio Pessoa) e Fonte do sapo.

O programa exibe informações sobre os objetos detectados, como tipo e confiança da detecção.

Para utilizar o Vigia Santos, é necessário ter a YOLOv3 instalada na pasta do Darknet. A YOLOv3 é uma rede neural pré-treinada que 
realiza a detecção de objetos. Ela fornece os arquivos de configuração e pesos necessários para que o programa funcione corretamente.

Além disso, o Vigia Santos utiliza as seguintes bibliotecas:

OpenCV (cv2): Uma biblioteca popular utilizada para processamento de imagens e vídeo. 
Que é responsável por carregar, exibir e manipular os feeds de câmera.

NumPy (np): Uma biblioteca que fornece suporte para cálculos numéricos eficientes em Python. 
Para manipular e processar matrizes de imagem.

Multiprocessing: Um módulo que permite a execução de tarefas em paralelo usando processos separados. 
Para exibir múltiplos feeds de câmera ao mesmo tempo.
