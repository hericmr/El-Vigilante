import cv2
from time import sleep

def exibir_menu():
    print(R + "-" * 54)
    print(V + """
⠀⠀⠀⠀⠀⠀⠈⣷⣄⠀⠀⠀⠀⣾⣷⠀⠀⠀⠀⣠⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢿⠿⠃⠀⠀⠀⠉⠉⠁⠀⠀⠐⠿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀       V1G14
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⣶⣶⣶⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⠀⠀⠀⠀⠀⠀    Acesso a cameras
⠀⠀⠀⣠⣶⣿⣿⡿⣿⣿⣿⡿⠋⠉⠀⠀⠉⠙⢿⣿⣿⡿⣿⣿⣷⣦⡀⠀⠀⠀        de Santos
⠀⢀⣼⣿⣿⠟⠁⢠⣿⣿⠏⠀⠀⢠⣤⣤⡀⠀⠀⢻⣿⣿⡀⠙⢿⣿⣿⣦⠀⠀
⣰⣿⣿⡟⠁⠀⠀⢸⣿⣿⠀⠀⠀⢿⣿⣿⡟⠀⠀⠈⣿⣿⡇⠀⠀⠙⣿⣿⣷⡄
⠈⠻⣿⣿⣦⣄⠀⠸⣿⣿⣆⠀⠀⠀⠉⠉⠀⠀⠀⣸⣿⣿⠃⢀⣤⣾⣿⣿⠟⠁
⠀⠀⠈⠻⣿⣿⣿⣶⣿⣿⣿⣦⣄⠀⠀⠀⢀⣠⣾⣿⣿⣿⣾⣿⣿⡿⠋⠁⠀⠀    por Heric M. 2023
⠀⠀⠀⠀⠀⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠛⠿⠿⠿⠿⠿⠿⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢰⣷⡦⠀⠀⠀⢀⣀⣀⠀⠀⠀⢴⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣸⠟⠁⠀⠀⠀⠘⣿⡇⠀⠀⠀⠀⠙⢷⠀⠀⠀⠀⠀⠀⠀⠀""")

    print(R + " --------------->  Escolha o local  <-----------------")
    print(V +
        " [0] Canal 6 \n [1] Canoagem \n [2] Praça do sapo \n [3] Travessia da balsa "
        "\n [4] Epitácio Pessoa e Oswaldo Cochrane (sentido c5) \n [5] Canal 4 (sentido SV) "
        "\n [6] Centro de Paquera do Embaré \n [7] Canal 4 sentido (Epitácio Pessoa) \n [8] Canal 4 sentido Conselheiro Lafayete")
    entrada = input().strip().split(',')
    return entrada


def exibir_feed_camera(lugar, url):
    contador = 1
    while True:
        print(R + f'Abrindo {contador}º frame da camera {lugar} em tempo real... ')
        cap = cv2.VideoCapture(url)
        sleep(6)
        ret, img = cap.read()
        cv2.imshow(f'Vigilante Santos - Exibindo cam {lugar} ', img)
        contador += 1

        if cv2.waitKey(1) == ord("q"):
            exit(0)
        cv2.destroyAllWindows()


def selecionar_camera(cameras):
    entrada = exibir_menu()
    for chave in entrada:
        lugar = cameras[f"{chave}"]["lugar"]
        url = cameras[f"{chave}"]["url"]
        exibir_feed_camera(lugar, url)

V = "\033[31m"  # vermelho
R = "\033[35m"  # roxo

cameras = {
"0" : {"lugar": "do Canal 6","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1593/snap_c1.jpg?1677157043869"},
"1" : {"lugar": "da Canoagem","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1464/snap_c1.jpg?1677191520757"},
"2" : {"lugar": "da Praça do Sapo","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1517/snap_c1.jpg?1677240440260"},
"3" : {"lugar": "da Travessia da balsa","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1455/snap_c1.jpg?1677248602110"},
"4" : {"lugar": "da Epitácio Pessoa com Oswaldo Chocrane","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1584/snap_c1.jpg?1677311079649",},
"5" : {"lugar": "da Epitacio Pessoa","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1578/snap_c1.jpg?1677311184499",},
"6" : {"lugar": "do CPE","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1561/snap_c1.jpg?1677311246793",},
"7" : {"lugar": "do Canal 4","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1591/snap_c1.jpg?1677311286046",},
"8" :{"lugar": "Rodoviária","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1588/snap_c1.jpg?1677694193298"}}

selecionar_camera(cameras)

