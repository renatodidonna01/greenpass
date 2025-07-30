import socket
import sys


def main():
    if len(sys.argv) != 3:
        print("Utilizzo: python client_A.py <Indirizzo_IP_CentroVaccinale> <TesseraSanitaria>")
        sys.exit(1)

    centro_vaccinale_address = sys.argv[1]
    tessera_sanitaria = sys.argv[2]

    # Verifica se la tessera sanitaria è esattamente di 20 caratteri
    if len(tessera_sanitaria) != 20:
        print("La tessera sanitaria deve essere esattamente di 20 caratteri.")
        sys.exit(1)



    # Creazione del socket
    socket_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connessione al Centro Vaccinale
        socket_fd.connect((centro_vaccinale_address, 1024))

        # Invia la tessera sanitaria al Centro Vaccinale
        socket_fd.sendall(tessera_sanitaria.encode())

        print("Tessera Sanitaria consegnata al Centro Vaccinale")

    except Exception as e:
        print("Errore durante la connessione o l'invio della tessera sanitaria:", e)

    finally:
        socket_fd.close()

if __name__ == "__main__":
    main()
