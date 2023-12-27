import cv2
import multiprocessing


V = "\033[31m"  # vermelho
R = "\033[35m"  # roxo

def show_menu():
    print("-" * 58)
    print("EL Vigilante - Héric Moura's Final Project _- CS50Python")

        print(" --------------->  Choose the location  <-----------------")
        print("[0] Canal 6 \n"
            "[1] Canoagem (Canoeing) \n"
            "[2] Praça do Sapo (Frog Square) \n"
            "[3] Travessia do FerryBoat (FerryBoat Crossing) \n"
            "[4] Epitácio Pessoa e Oswaldo Cochrane \n"
            "[5] Canal 4 \n"
            "[6] Centro de Paquera do Embaré (Embaré Flirting Center) \n"
            "[7] Canal 4 (Epitácio Pessoa) \n"
            "[8] Canal 4 sentido Conselheiro Lafayete \n"
            "[q] Sair (Exit)")

        entry = input().strip().split(',')
        if "q" in entry:
            return ["q"]
        elif all(e.isdigit() and 0 <= int(e) <= 8 for e in entry):
            return entry
        else:
            print("Invalid input! Please enter a number from 0 to 8 or 'q'")


def show_feed_camera(lugar, url):
    print(f"Opening {lugar} camera...")
    window_name = f'El Vigilante Santos - Displaying cam {lugar}'
    while True:
        cap = cv2.VideoCapture(url)
        ret, img = cap.read()
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, img)

        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


def select_camera(cameras):
    while True:
        entrada = show_menu()
        if entrada == ["q"]:
            break
        elif entrada == [""]:
            continue
        processos = []
        for item in entrada:
            if item in cameras:
                lugar = cameras[item]["lugar"]
                url = cameras[item]["url"]
                processo = multiprocessing.Process(target=show_feed_camera, args=(lugar, url))
                processo.start()
                processos.append(processo)
        for processo in processos:
            processo.join()


def main():
    cameras = {
"0" : {"lugar": "Canal 6","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1593/snap_c1.jpg?1677157043869"},
"1" : {"lugar": "Canoagem","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1464/snap_c1.jpg?1677191520757"},
"2" : {"lugar": "Praca do Sapo","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1517/snap_c1.jpg?1677240440260"},
"3" : {"lugar": "Travessia da balsa","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1455/snap_c1.jpg?1677248602110"},
"4" : {"lugar": "Epitacio Pessoa com Oswaldo Chocrane","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1584/snap_c1.jpg?1677311079649",},
"5" : {"lugar": "Epitacio Pessoa","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1578/snap_c1.jpg?1677311184499",},
"6" : {"lugar": "CPE","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1561/snap_c1.jpg?1677311246793",},
"7" : {"lugar": "Canal 4","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1591/snap_c1.jpg?1677311286046",},
"8" : {"lugar": "Rodoviaria","url": "https://egov.santos.sp.gov.br/santosmapeada/css/img/cameras/cam1588/snap_c1.jpg?1677694193298"}}

    select_camera(cameras)

if __name__ == "__main__":
    main()
