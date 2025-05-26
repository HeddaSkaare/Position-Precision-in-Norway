# Estimation of DOP Along Norwegian Roads, Taking in Terrain as a Factor


## Systemkrav

Python ≥ 3.10

Node.js ≥ 18.x

Git installert

Anbefalt editor: VS Code

## Starte backend

1. Start en terminal

2. Naviger til backend-mappen:

```bash
 cd backend
```

3. Opprett et virtuelt miljø:

- <b> Mac/Linux: </b>
```bash
python3 -m venv venv
```

- <b>Windows (PowerShell):</b>
```bash
python -m venv venv
```


4. Aktiver det virtuelle miljøet:

- <b> Mac/Linux: </b>
```bash
source venv/bin/activate
```
- <b>Windows (PowerShell):</b>
```bash
.\venv\Scripts\Activate.ps1
```

5. Installer alle avhengigheter:
```bash
pip install -r requirements.txt
```


6. Start Flask-serveren:
```bash
python app.py
```

### Starte Frontend

1. Start en ny terminal

2. Naviger til frontend-mappen:
```bash
cd frontend
```

3. Installer nødvendige pakker:
```bash
npm install
```

4. Start frontend-applikasjonen:
```bash
 npm start
```


## Laste ned ephemeris fra CDDIS

For å laste ned GNSS-ephemeris (RINEX/BRDC) fra [CDDIS (NASA's Crustal Dynamics Data Information System)](https://cddis.nasa.gov), må du:

1. Opprette en Earthdata-bruker
2. Lage en `.netrc`-fil i hjemmemappen din

---

### 1. Opprett Earthdata-bruker

1. Gå til: https://urs.earthdata.nasa.gov/users/new
2. Opprett en konto
3. Aktiver kontoen via e-post

---

### 2. Sett opp `.netrc`-fil

#### Plassering:
- På **Mac/Linux**: `~/.netrc`
- På **Windows (WSL/git bash)**: `C:\Users\DittBrukernavn\.netrc` eller bruk WSL sitt `~/.netrc`

#### Innhold:

> _Bytt ut `brukernavn` og `passord` med din Earthdata-pålogging_

```
machine urs.earthdata.nasa.gov
login brukernavn
password passord
```

---

#### Viktig! Rettigheter må være sikre

- På Linux/macOS:
```bash
chmod 600 ~/.netrc
```




