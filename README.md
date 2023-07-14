# VigiaSantos
Vigia Santos é um script de monitoramento em tempo real que permite acessar câmeras de segurança em diferentes locais de Santos. 
Utilizando a rede neural YOLOv3, o programa detecta e rastreia 80 tipos de objetos em tempo real.

Basta selecionar uma câmera específica para visualizar os feeds que incluem o Canal 6, Canoagem, Travessia da balsa, 
Epitácio Pessoa e Oswaldo Cochrane, Canal 4, Centro de Paquera do Embaré e Canal 4 e Fonte do sapo. O programa exibe 
informações sobre os objetos detectados, como tipo e confiança da detecção.

É necessário ter a YOLOv3 instalada na pasta do Darknet, juntamente com as bibliotecas:

OpenCV (cv2): Biblioteca para processamento de imagens e vídeo. 
Que é responsável por carregar, exibir e manipular os feeds de câmera.

NumPy (np): que fornece suporte para cálculos numéricos para manipular e processar matrizes de imagem.

Multiprocessing: Um módulo que permite a execução de tarefas em paralelo usando processos separados, para exibir múltiplos 
feeds de câmera ao mesmo tempo.
