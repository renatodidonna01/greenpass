class GreenPass:
    def __init__(self, tessera, valida, data_scadenza):
        print(f"Creazione di GreenPass con Tessera: {tessera}, Valida: {valida}, Scadenza: {data_scadenza}")
        self.tessera = tessera
        self.valida = valida
        self.data_scadenza = data_scadenza

    def to_string(self):
        return f"Tessera: {self.tessera}, Validità: {self.valida}, Scadenza: {self.data_scadenza}"



