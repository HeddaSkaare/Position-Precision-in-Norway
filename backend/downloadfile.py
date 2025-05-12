import requests
import gzip
import logging
import os
import gdown

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
folder = os.path.join(CURRENT_DIR, "unzipped")

def lastned(day, year):
    print(day)
    filename_gz = f'BRD400DLR_S_{year}{day}0000_01D_MN.rnx.gz'
    filename_unzipped = filename_gz[:-3]  # fjerner .gz

    gz_path = os.path.join(CURRENT_DIR, filename_gz)
    unzipped_path = os.path.join(folder, filename_unzipped)

    os.makedirs(folder, exist_ok=True)

    url = f'https://cddis.nasa.gov/archive/gnss/data/daily/{year}/brdc/{filename_gz}'

    token = os.getenv('EARTHDATA_TOKEN')
    if not token:
        raise EnvironmentError("EARTHDATA_TOKEN er ikke satt i miljøvariabler")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    if not os.path.isfile(unzipped_path):
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            print("Feil ved nedlasting:", r.status_code)
            print("Svar fra serveren:", r.text[:500])
            raise Exception(f"Kunne ikke laste ned fila {filename_gz}. Status: {r.status_code}")

        #print("[DEBUG] Response snippet:", r.text[:500], flush=True)

        with open(gz_path, 'wb') as fd:
            fd.write(r.content)

        with open(gz_path, 'rb') as fd:
            try:
                gzip_fd = gzip.GzipFile(fileobj=fd)
                data = gzip_fd.read()
            except gzip.BadGzipFile as e:
                print("Feil ved utpakking av gzip:", e)
                raise

        os.remove(gz_path)

        with open(unzipped_path, 'wb') as f:
            f.write(data)

        return unzipped_path
    else:
        print('File Exists')
        return unzipped_path




def ensure_raster():
    raster_path = os.path.join("data", "merged_raster.tif")
    if not os.path.exists(raster_path):
        print("Laster ned merged_raster.tif fra Google Drive...")
        os.makedirs("data", exist_ok=True)
        rasterURL = os.getenv('RASTER_URL')
        # file_id = "1AbCDefGhIjKlMnOpQrStUvWxYz"  # ← legg inn ID-en fra lenken
        # url = f"https://drive.google.com/uc?id={file_id}"

        gdown.download(rasterURL, raster_path, quiet=False)
