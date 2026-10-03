import csv
def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
   # TODO
    album = {} # dizionario vuoto
    try:
        filein = open(file_path, "r") # apertura del file
        filein.readline() # salto l'intestazine --> legge la prima riga
        reader = csv.reader(filein)

        # codice, titolo, autore, mese, anno
        # lettura del file
        for riga in reader:
            codice = riga[0]
            titolo = riga[1]
            autore = riga[2]
            mese = int(riga[3])
            anno = int(riga[4])

            foto = {'codice': codice, 'titolo': titolo, 'autore': autore, 'mese': mese, 'anno': anno}

            # album ha come chiave l'anno e come valore la lista di foto scattate durante l'anno
            # se l'anno non è presente nell'album allora aggiunge la prima foto
            # se l'anno esiste già aggiunge la foto alla lista di foto di quell'anno
            if anno not in album:
                album[anno] = [foto]
            else:
                album[anno].append(foto)
        filein.close() # chiusura file

    except FileNotFoundError: # eccezione
        print("File non trovato!")
        return None

    return album

def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    # TODO
    # controllo validità mese inserito
    if mese < 1 or mese > 12:
        return None

    # controllo se il codice è già presente nell'album
    for anno_chiave in album:
        for foto in album[anno_chiave]:
            if foto['codice'] == codice:
                return None

    # aggiornamento del file
    try:
        fileout = open(file_path, "a") # apriamo il file per poter accodare le nuove infomazioni
        riga = f"{codice},{titolo},{autore},{mese},{anno}\n"
        # aggiunge la riga al fondo del nostro file con le informazioni inserite dall'utente
        # dopo aver verificato che queste siano valide
        fileout.write(riga)
        fileout.close()
    except FileNotFoundError: # eccezioni
        print("File non trovato!")
        return None

    nuova_foto = {'codice': codice, 'titolo': titolo, 'autore': autore, 'mese': mese, 'anno': anno}

    # aggiornamento del nostro album
    if anno not in album:
        album[anno] = [nuova_foto]
    else:
        album[anno].append(nuova_foto)

    return nuova_foto


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    # TODO
    # il ciclo esterno scorre gli anni dentro l'album mentre quello interno scorre le singole foto
    # presenti nella lista di quell'anno
    for anno in album:
        for foto in album[anno]:
            if foto['codice'] == codice:
                return foto['codice'] + "," + foto['titolo'] + "," + foto['autore'] + "," + str(foto['mese']) + "," + str(foto['anno'])

    return False


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # TODO
    if anno not in album:
        return None

    lista_titoli = []
    for foto in album[anno]:
        lista_titoli.append(foto['titolo'])

    lista_titoli_ordinati = sorted(lista_titoli)
    return lista_titoli_ordinati


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip().capitalize() # per rendere la prima
            # lettera maiuscola in modo da poter ordinare i titoli in modo corretto
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
