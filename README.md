# TubeFetch

<div align="center">
  <img src="https://github.com/AndreaGirlando/TubeFetch/blob/main/TubeFetch.frontend/public/assets/logo.png" alt="Logo TubeFetch" width="200"/>
</div>

## Descrizione

**TubeFetch** è un progetto che permette di scaricare canzoni da una playlist di Spotify o YouTube. È possibile scaricare l'intera playlist o scegliere delle canzoni specifiche da scaricare. Il progetto è composto da due parti principali: il **frontend** e le **API**. Entrambe le parti possono essere avviate tramite **Docker** utilizzando il comando `docker compose up`.

### Funzionalità
- Inserisci un link di una playlist di Spotify o YouTube.
- Scegli se scaricare tutte le canzoni della playlist o solo quelle selezionate.
- Le canzoni vengono scaricate in formato audio.

## Come avviare il progetto

Per avviare il progetto, assicurati di avere **Docker** e **Docker Compose** installati sul tuo computer.

1. Clona il repository:
    ```bash
    git clone <URL del repository>
    ```

2. Naviga nella cartella del progetto:
    ```bash
    cd <nome della cartella>
    ```

3. Avvia entrambe le parti del progetto (frontend e API) con Docker Compose:
    ```bash
    docker compose up
    ```

4. Il frontend sarà disponibile su [http://localhost:4200](http://localhost:4200).

## Avvertenze

Non mi assumo alcuna responsabilità sull'uso che verrà fatto di questo progetto. L'uso del software è a proprio rischio e non deve violare i diritti d'autore o le politiche delle piattaforme di streaming come Spotify o YouTube.
