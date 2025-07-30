# 🟩 Green Pass – Sistema distribuito per la gestione dei certificati COVID-19

Progetto sviluppato nell'ambito del laboratorio di **Reti di Calcolatori** – Università Parthenope, a.a. 2023/2024.  
Il sistema simula una rete distribuita per la **creazione, gestione, verifica e annullamento** del Green Pass tramite più componenti client-server scritti in Python.

---

## 🧩 Architettura del sistema

- **ClientA**: Inserimento dati utente e richiesta creazione Green Pass  
- **CentroVaccinale**: Generazione del Green Pass  
- **ServerV**: Validazione, registrazione e conservazione Green Pass  
- **ClientS**: Verifica della validità di un Green Pass esistente  
- **ServerG**: Gateway intermedio che instrada richieste tra i client e il ServerV  
- **ClientT**: Annullamento o prolungamento Green Pass in base alla situazione sanitaria dell’utente

---

## 🧪 Funzionalità principali

- ✅ Creazione e registrazione Green Pass  
- 🔐 Verifica validità Green Pass tramite codice fiscale  
- ⚠️ Annullamento Green Pass in caso di contagio  
- ♻️ Rinnovo automatico o manuale ogni 6 mesi  
- 🔄 Comunicazione tra server con socket TCP  
- 📜 Logging e gestione degli accessi

---

## 🛠️ Tecnologie

- Python 3  
- Socket TCP/IP  
- Architettura client-server distribuita  
- Logging file-based  
- Input via CLI

---

## ▶️ Istruzioni di esecuzione

1. Avviare il **CentroVaccinale**
   ```bash
   python3 CentroVaccinale.py 1024
   ```

2. Avviare il **ServerV** (gestione validità)
   ```bash
   python3 greenpass.py
   python3 ServerV.py
   ```

3. Avviare il **ServerG** (gateway)
   ```bash
   sudo python3 serverG.py 127.0.0.1
   ```

4. Avviare il **ClientA** (creazione green pass)
   ```bash
   python3 clientA.py 127.0.0.1 CODICEFISCALE
   ```

5. Avviare il **ClientT** (gestione stato)
   ```bash
   python3 clientT.py 127.0.0.1 CODICEFISCALE
   ```

6. Avviare il **ClientS** (verifica green pass)
   ```bash
   python3 clientS.py 127.0.0.1 CODICEFISCALE
   ```

---



## 📄 Licenza

Progetto sviluppato a scopo didattico. Non destinato all'uso in produzione.
