import socket
import sys
from greenpass import GreenPass

LUNGHEZZA_TESSERA_SANITARIA = 20


def main():
    if len(sys.argv) != 3:
        print("Utilizzo: python clientT.py <Indirizzo_IP_ServerG> <TesseraSanitaria>")
        sys.exit(1)

    try:
        socket_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        serverG_address = sys.argv[1]
        tessera_sanitaria = sys.argv[2]

        if len(tessera_sanitaria) != LUNGHEZZA_TESSERA_SANITARIA:
            print("Tessera Sanitaria non valida")
            sys.exit(1)

        serverG_port = 1020
        serverG_address = (serverG_address, serverG_port)

        socket_fd.connect(serverG_address)



        while True:
            print("Quale servizio si vuole utilizzare?")
            print("Inserisci '1' per validare il Green Pass")
            print("Inserisci '2' per invalidare il Green Pass")
            service_code = input(">> ").strip()

            if service_code not in ['1', '2']:
                print("Scelta non valida. Inserisci '1' o '2'.")
                continue

            # Invia sia la tessera sanitaria che il codice del servizio al Server G come stringa
            message = f"{tessera_sanitaria}{service_code}"
            print(message)
            # Invia il messaggio al Server G
            socket_fd.sendall(message.encode())

            print("Richiesta inviata al Server G")

            # Ricevi il Green Pass come stringa dal Server G
            green_pass_str = socket_fd.recv(1024).decode()

            if not green_pass_str:
                print("Nessun dato ricevuto dal Server G")
                break

            # Mostra il Green Pass come stringa
            print(f"Ricevuto il Green Pass dal Server G:\n{green_pass_str}")
            break
    except socket.error as e:
        print(f"Errore durante la connessione: {e}")
    except Exception as e:
        print(f"Errore durante la ricezione del Green Pass: {e}")
    finally:
        socket_fd.close()


if __name__ == "__main__":
    main()
