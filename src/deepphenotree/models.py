from pathlib import Path
import requests
import os
homedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":

    urls = [
            "https://laris-cloud.sien-pdl.fr/index.php/s/qg8ZCFE5gfNposz", #Flowering
            "https://laris-cloud.sien-pdl.fr/index.php/s/SsGmtCGqecYb2qM", #Fruit 
            "https://laris-cloud.sien-pdl.fr/index.php/s/NRrbznkW7z43Ge5", #Fruitlet
    ]

    folders = [
        "Flowering",
        "Fruit",
        "Fruitlet"
    ]

    path = "models"
    out_dir = Path(os.path.join(homedir,path))
    out_dir.mkdir(parents=True, exist_ok=True)

    for share_url,folder in zip(urls,folders):
        download_url = share_url.rstrip("/") + "/download"

        out_dir = Path(os.path.join(homedir,path,folder.replace('.pt','')))
        out_dir.mkdir(parents=True, exist_ok=True)

        out_path = homedir / out_dir / "best.pt"
        if not out_path.exists():
            with requests.get(download_url, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(out_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)