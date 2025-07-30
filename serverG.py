import socket
import sys
import logging
from greenpass import GreenPass

TESSERA_LEN = 20

def main():
    if len(sys.argv) != 3:
        print("Utilizzo: python serverG.py <Indirizzo_IP_ServerV> <Porta_ServerV>")
        sys.exit(1)

    serverv_address = sys.argv[1]
    serverv_port = int(sys.argv[2])

    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_port = 1020  # Porta su cui il Server G accetta le connessioni
        server_address = ("0.0.0.0", server_port)

        listen_socket.bind(server_address)
        listen_socket.listen(5)

        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger("serverG")

        logger.info(f"ServerG in ascolto sulla porta {server_port}...")

        while True:
            client_socket, client_address = listen_socket.accept()

            try:
                tessera_sanitaria = client_socket.recv(TESSERA_LEN).decode()
                service_code = client_socket.recv(1).decode()
                print(service_code)
                logger.info(f"Ricevuta tessera sanitaria: {tessera_sanitaria}, Service Code: {service_code}")





                serverv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                serverv_socket.connect((serverv_address, serverv_port))

                message = f"{tessera_sanitaria} {service_code}"

                # Invia la tessera sanitaria e il service_code al Server V

                serverv_socket.sendall(message.encode())



                green_pass_str = serverv_socket.recv(1024).decode()



                serverv_socket.close()

                # Attendere una risposta dal Server V prima di inviarla al client
                if green_pass_str:
                    client_socket.sendall(green_pass_str.encode())
                    logger.info(f"Ricevuto il Green Pass da ServerV: {green_pass_str}")
            except socket.error as se:
                logger.error(f"Errore di socket: {se}")
            except Exception as e:
                logger.error(f"Errore durante la gestione del client: {e}")
                print(f"Errore durante la gestione del client: {e}")
            finally:
                client_socket.close()

    except socket.error as se:
        logger.error(f"Errore di socket: {se}")
    except Exception as e:
        logger.error(f"Errore durante l'esecuzione del ServerG: {e}")
    finally:
        listen_socket.close()

if __name__ == "__main__":
    main()
