from pathlib import Path

# add your tests here...
import numpy as np

from deepphenotree import _sample_data
def test_load_image_passes_string_path_to_cv2(monkeypatch):
    captured = {}

    def fake_imread(path):
        captured["type"] = type(path)
        return np.zeros((2, 2, 3), dtype=np.uint8)

    monkeypatch.setattr(_sample_data.resources, "files", lambda _: Path("/tmp"))
    monkeypatch.setattr(_sample_data.cv2, "imread", fake_imread)
    monkeypatch.setattr(_sample_data.cv2, "cvtColor", lambda image, _: image)

    _sample_data._load_image("Fruit_switzerland.png", "Fruit Switzerland")

    assert captured["type"] is str