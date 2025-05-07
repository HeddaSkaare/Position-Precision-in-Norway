import requests
import gzip
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
folder = os.path.join(CURRENT_DIR, "unzipped")

def lastned(day, year):
    print(day)
    filename_gz = f'BRD400DLR_S_{year}{day}0000_01D_MN.rnx.gz'
    filename_unzipped = filename_gz[:-3]  # fjerner .gz

    gz_path = os.path.join(CURRENT_DIR, filename_gz)  # Fila lagres midlertidig i samme mappe som koden
    unzipped_path = os.path.join(folder, filename_unzipped)

    # ✅ Sørg for at mappen for unzipped filer finnes
    os.makedirs(folder, exist_ok=True)

    url = f'https://cddis.nasa.gov/archive/gnss/data/daily/{year}/brdc/{filename_gz}'

    user = os.getenv('EARTHDATA_USER')
    pw = os.getenv('EARTHDATA_PASS')
    print("Brukernavn:", user)
    print("Passord satt:", pw is not None)
    if not os.path.isfile(unzipped_path):
        r = requests.get(url, auth=(user, pw))
        if r.status_code != 200:
            print("Feil ved nedlasting:", r.status_code)
            print("Svar fra serveren:", r.text[:500])  # Vis litt av HTML-feilen hvis den finnes
            raise Exception(f"Kunne ikke laste ned fila {filename_gz}. Status: {r.status_code}")

        # ✅ Lagre den nedlastede gzip-fila midlertidig
        with open(gz_path, 'wb') as fd:
            fd.write(r.content)

        # ✅ Pakk ut fila
        with open(gz_path, 'rb') as fd:
            try:
                gzip_fd = gzip.GzipFile(fileobj=fd)
                data = gzip_fd.read()
            except gzip.BadGzipFile as e:
                print("Feil ved utpakking av gzip:", e)
                raise

        os.remove(gz_path)  # ✅ Slett gzip-fila etter utpakking

        # ✅ Lagre utpakket fil til riktig mappe
        with open(unzipped_path, 'wb') as f:
            f.write(data)

        return unzipped_path
    else:
        print('File Exists')
        return unzipped_path




    
