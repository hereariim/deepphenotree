import numpy as np
from ultralytics import RTDETR, YOLO
from sahi.models.ultralytics import UltralyticsDetectionModel
from sahi.predict import get_sliced_prediction
import torch
from pathlib import Path

MODEL_Flowering = Path.home() / "deepphenotree" / "src" / "models" / "Flowering" / "best.pt"
MODEL_Fruitlet = Path.home() / "deepphenotree" / "src" / "models" / "Fruitlet" / "best.pt"
MODEL_Fruit = Path.home() / "deepphenotree" / "src" / "models" / "Fruit" / "best.pt"

class YoloInferencer:
    def __init__(self, task: str):
        """Charge un modèle YOLO unique"""
        self.task = task
        # self.model = YOLO(model_path)

    def preprocess(self, image: np.ndarray) -> np.ndarray:
        """Prépare l'image pour YOLO (RGB, uint8)"""
        if image.ndim == 2:
            image = np.stack([image] * 3, axis=-1)
        if image.dtype != np.uint8:
            image = (255 * image / image.max()).astype(np.uint8)
        return image

    def predict_boxes(self, image: np.ndarray) -> np.ndarray:
        """Retourne des rectangles pour napari Shapes layer"""
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        image = self.preprocess(image)
        if self.task == "Flowering":
            self_model = UltralyticsDetectionModel(
                model_path=str(MODEL_Flowering),
                confidence_threshold=0.529,
                device=device
            )
        elif self.task == "Fruitlet":
            self_model = UltralyticsDetectionModel(
                model_path=str(MODEL_Fruitlet),
                confidence_threshold=0.539,
                device=device
            )
        else:
            self_model = UltralyticsDetectionModel(
                model_path=str(MODEL_Fruitlet),
                confidence_threshold=0.539,
                device=device
            )
    
        results = get_sliced_prediction(
            image,
            self_model,
            slice_height=640,
            slice_width=640,
            overlap_height_ratio=0.2,
            overlap_width_ratio=0.2,
        )

        if results.object_prediction_list is None or len(results.object_prediction_list) == 0:
            return np.empty((0, 4, 2))

        rectangles = []
        for pred in results.object_prediction_list:
            x1, y1, x2, y2 = pred.bbox.to_xyxy()
            rectangles.append(
                [
                    [y1, x1],  # top-left
                    [y1, x2],  # top-right
                    [y2, x2],  # bottom-right
                    [y2, x1],  # bottom-left
                ]
            )

        return np.array(rectangles)
