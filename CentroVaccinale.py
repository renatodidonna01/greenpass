import socket
import sys
import threading
from greenpass import GreenPass
from datetime import datetime, timedelta


serverv_port = 1027



def client_handler(client_socket):
    try:
        tessera_sanitaria = client_socket.recv(1024).decode()

        print(f"Ricevuta tessera sanitaria: {tessera_sanitaria}")

        data_attuale = datetime.now()

        # Calcola il Green Pass
        data_scadenza = data_attuale+timedelta(days=180)

        data_scadenza_formattata=data_scadenza.strftime("%Y-%m-%d")

        valida=1

        green_pass_data = f"{tessera_sanitaria},{data_scadenza_formattata},{valida}"

        message = f"CENTRO_VACCINALE:{green_pass_data}"



        client_to_serverv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client_to_serverv.connect(("127.0.0.1", serverv_port))
            client_to_serverv.sendall(message.encode())
            print("Green Pass inviato al ServerV")
        except Exception as e:
            print(f"Errore durante la connessione o l'invio al ServerV: {e}")
        finally:
            client_to_serverv.close()

    except Exception as e:
        print(f"Errore durante la gestione del client: {e}")
    finally:
        client_socket.close()

def main():
    if len(sys.argv) != 2:
        print("Utilizzo: python centro_vaccinale_server.py <Porta>")
        sys.exit(1)

    server_port = int(sys.argv[1])

    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("0.0.0.0", server_port)

    listen_socket.bind(server_address)
    listen_socket.listen(5)

    print(f"Il Centro Vaccinale è in attesa di connessioni sulla porta {server_port}...")

    while True:
        try:
            client_socket, client_address = listen_socket.accept()
            print(f"Connessione accettata da {client_address[0]}:{client_address[1]}")

            client_thread = threading.Thread(target=client_handler, args=(client_socket,))
            client_thread.start()

        except Exception as e:
            print(f"Errore durante l'accettazione della connessione: {e}")

if __name__ == "__main__":
    main()
