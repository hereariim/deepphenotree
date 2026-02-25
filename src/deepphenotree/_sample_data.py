"""
This module is an example of a barebones sample data provider for napari.

It implements the "sample data" specification.
see: https://napari.org/stable/plugins/building_a_plugin/guides.html#sample-data

Replace code below according to your needs.
"""

from __future__ import annotations
from pathlib import Path
import numpy as np
from typing import Tuple, List
import cv2

def make_sample_data():
    """Generates an image"""
    # Return list of tuples
    # [(data1, add_image_kwargs1), (data2, add_image_kwargs2)]
    # Check the documentation for more information about the
    # add_image_kwargs
    # https://napari.org/stable/api/napari.Viewer.html#napari.Viewer.add_image
    return [(np.random.rand(512, 512), {})]

  

class DeepPhenoTreeData:
    
    VALID_TASKS = ["Flowering", "Fruitlet", "Fruit"]

    def __init__(self, task: str):
        if task not in self.VALID_TASKS:
            raise ValueError(
                f"Task must be one of {self.VALID_TASKS}, got '{task}'"
            )
        self.pth_main = Path(__file__).parent / "sample_data"
        self.task = task
        self.data, self.names = self._load_data()

    def _load_data(self) -> Tuple[np.ndarray, List[str]]:
        if self.task == "Flowering":
            images_files = [
                self.pth_main / "Flowering_belgium.png",
                self.pth_main / "Flowering_italy.png",
                self.pth_main / "Flowering_spain.png",
                self.pth_main / "Flowering_switzerland.png",
            ]
        elif self.task == "Fruitlet":
            images_files = [
                self.pth_main / "Fruitlet_belgium.png",
                self.pth_main / "Fruitlet_italy.png",
                self.pth_main / "Fruitlet_spain.png",
                self.pth_main / "Fruitlet_switzerland.png",
            ]
        else:
            images_files = [
                self.pth_main / "Fruit_belgium.png",
                self.pth_main / "Fruit_italy.png",
                self.pth_main / "Fruit_spain.png",
                self.pth_main / "Fruit_switzerland.png",
            ]
        localisation = ["Belgium", "Italy", "Spain", "Switzerland"]
        images_list = []
        heights = []
        widths = []
        for img_path in images_files:
            img = cv2.imread(str(img_path))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            images_list.append(img)
            h, w = img.shape[:2]
            heights.append(h)
            widths.append(w)
        Hmax = max(heights)
        Wmax = max(widths)

        padded_images = []

        for img in images_list:
            h, w = img.shape[:2]

            pad_h = Hmax - h
            pad_w = Wmax - w

            padded = np.pad(
                img,
                ((0, pad_h), (0, pad_w),(0,0)),
                mode="constant",
                constant_values=0,
            )

            padded_images.append(padded)

        data = np.stack(padded_images, axis=-1)  # (H, W, N)
        return data,localisation

from importlib import resources
import cv2

def _load_image(name, display_name):
    image_path = resources.files("deepphenotree.sample_data").joinpath(name)
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return [(image, {"name": display_name})]


def load_fruit_switzerland():
    return _load_image("Fruit_switzerland.png", "Fruit Switzerland")
def load_fruit_belgium():
    return _load_image("Fruit_belgium.png", "Fruit Belgium")
def load_fruit_spain():
    return _load_image("Fruit_spain.png", "Fruit Spain")
def load_fruit_italy():
    return _load_image("Fruit_italy.png", "Fruit Italy")

def load_fruitlet_switzerland():
    return _load_image("Fruitlet_switzerland.png", "Fruitlet Switzerland")
def load_fruitlet_belgium():
    return _load_image("Fruitlet_belgium.png", "Fruitlet Belgium")
def load_fruitlet_spain():
    return _load_image("Fruitlet_spain.png", "Fruitlet Spain")
def load_fruitlet_italy():
    return _load_image("Fruitlet_italy.png", "Fruitlet Italy")

def load_flowering_switzerland():
    return _load_image("Flowering_switzerland.png", "Flowering Switzerland")
def load_flowering_belgium():
    return _load_image("Flowering_belgium.png", "Flowering Belgium")
def load_flowering_spain():
    return _load_image("Flowering_spain.png", "Flowering Spain")
def load_flowering_italy():
    return _load_image("Flowering_italy.png", "Flowering Italy")