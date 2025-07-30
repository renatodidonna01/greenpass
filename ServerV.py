import socket
from greenpass import GreenPass
from datetime import datetime, timedelta



# Lista per conservare i Green Pass
green_pass_list = []

def process_green_pass(data_to_process):
    try:
        tessera_sanitaria, data_scadenza_formattata, valida = data_to_process.split(",")
        green_pass = GreenPass(tessera_sanitaria, int(valida), datetime.strptime(data_scadenza_formattata, "%Y-%m-%d"))
        green_pass_list.append(green_pass)


        response = "Green Pass ricevuto con successo"
        return response
    except Exception as e:
        print(f"Errore durante l'elaborazione del Green Pass: {e}")
        return "Errore durante l'elaborazione del Green Pass"

data_attuale = datetime.now()

def process_server_g_request(tessera_sanitaria, service_code):
    try:
        # Cerca il Green Pass nella lista in base alla tessera sanitaria
        for green_pass in green_pass_list:
            if green_pass.tessera == tessera_sanitaria:
                if service_code == 1 and green_pass.valida != 1:
                    # Convalida il Green Pass se non è già convalidato
                    green_pass.valida = 1

                    # Calcola il Green Pass
                    green_pass.data_scadenza = data_attuale + timedelta(days=180)
                    return green_pass.to_string()
                if(service_code==1 and green_pass.valida==1):
                       return green_pass.to_string()


                elif service_code == 2:
                    # Invalida il Green Pass
                    green_pass.valida = 0
                    green_pass.data_scadenza =data_attuale

                    return green_pass.to_string()
                else:
                    return "Servizio non valido"

        # Se la tessera sanitaria non corrisponde a nessun Green Pass, restituisci un messaggio di errore
        return "Tessera Sanitaria non trovata"

    except Exception as e:
        print(f"Errore durante la gestione della richiesta da Server G: {e}")
        return "Errore durante la gestione della richiesta da Server G"

# Funzione per ottenere il Green Pass associato a un codice fiscale (CF)
def get_green_pass_by_cf(tessera_sanitaria):
    for green_pass in green_pass_list:
        if green_pass.tessera == tessera_sanitaria:
            return green_pass.to_string()

def main():
    listen_socket = None  # Inizializza listen_socket con un valore vuoto
    try:
        server_port = 1027

        # Creiamo un socket per la comunicazione con il Server V
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("127.0.0.1", server_port)
        listen_socket.bind(server_address)
        listen_socket.listen(5)

        print(f"ServerV in ascolto sulla porta {server_port}...")

        while True:
            client_socket, client_address = listen_socket.accept()
            print(f"Connessione accettata da {client_address[0]}:{client_address[1]}")

            try:
                data = client_socket.recv(1024)
                data_received = data.decode()

                if data_received.startswith("CENTRO_VACCINALE:"):
                    data_to_process = data_received[len("CENTRO_VACCINALE:"):].strip()
                    print(data_to_process)

                    # Chiamata alla funzione per elaborare il Green Pass
                    response = process_green_pass(data_to_process)

                else:
                    split_data = data_received.split(" ")

                    if len(split_data) == 2:
                        tessera_sanitaria = split_data[0]
                        service_code = int(split_data[1])
                        print(service_code)


                        if service_code == 0:
                            # Restituisci il Green Pass associato alla tessera sanitaria
                            green_pass = get_green_pass_by_cf(tessera_sanitaria)

                            if green_pass:
                                response = green_pass
                            else:
                                response = "Tessera Sanitaria non trovata"
                        else:
                            # Verifica il tipo di servizio richiesto
                            if service_code in [1, 2]:
                                # Processa la richiesta da Server G
                                updated_green_pass = process_server_g_request(tessera_sanitaria, service_code)
                                response = updated_green_pass
                            else:
                                response = "Servizio non valido"
                    else:
                        response = "Richiesta non valida"

                # Invia una risposta al mittente
                client_socket.sendall(response.encode())

            except Exception as e:
                print(f"Errore durante la gestione della richiesta: {e}")
            finally:
                client_socket.close()

    except Exception as e:
        print(f"Errore durante l'esecuzione del ServerV: {e}")
    finally:
        listen_socket.close()

if __name__ == "__main__":
    main()
