import requests
import zipfile
import tempfile
from pathlib import Path
import shutil
from napari.utils.notifications import show_info, show_warning, show_error

DATA_URL = "https://laris-cloud.sien-pdl.fr/index.php/s/mWzFw8PDE2dDdG8/download"  # URL du fichier zip à télécharger

EXPECTED_FOLDER_NAME = "sample_data"  # nom du dossier contenu dans le zip

def ensure_data():

    package_dir = Path(__file__).resolve().parent
    if (package_dir / EXPECTED_FOLDER_NAME).exists():
        print("Dataset already exists. No action needed.")
        return
    zip_path = package_dir / "sample_data.zip"
    show_info("Downloading dataset from Nextcloud...")


    with requests.get(DATA_URL, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    show_info("Extracting dataset...")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(package_dir)

    show_info("Dataset successfully installed.")
    if zip_path.exists():
        zip_path.unlink()
        print("Fichier supprimé.")
    else:
        print("Fichier introuvable.")
