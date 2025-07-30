import socket
import sys

LUNGHEZZA_TESSERA_SANITARIA = 20

def main():
    if len(sys.argv) != 3:
        print("Utilizzo: python clientS.py <Indirizzo_IP_ServerG> <TesseraSanitaria>")
        sys.exit(1)

    try:
        socket_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        serverG_address = sys.argv[1]
        tessera_sanitaria = sys.argv[2]

        if len(tessera_sanitaria) != LUNGHEZZA_TESSERA_SANITARIA:
            print("Tessera Sanitaria non valida")
            sys.exit(1)

        serverG_port = 1020
        service_code=0
        serverG_address = (serverG_address, serverG_port)

        socket_fd.connect(serverG_address)

        message = f"{tessera_sanitaria}{service_code}"
        print(message)
        # Invia la tessera sanitaria al Server G
        socket_fd.sendall(message.encode())

        # Ricevi il Green Pass come stringa dal Server G
        green_pass_str = socket_fd.recv(1024).decode()

        if green_pass_str:
            # Visualizza il Green Pass
            print(f"Ricevuto il Green Pass dal Server G:\n{green_pass_str}")
        else:
            print("Nessun dato ricevuto dal Server G")

    except socket.error as e:
        print(f"Errore durante la connessione: {e}")
    except Exception as e:
        print(f"Errore durante la ricezione del Green Pass: {e}")
    finally:
        socket_fd.close()

if __name__ == "__main__":
    main()
