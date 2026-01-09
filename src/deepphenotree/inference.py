import numpy as np
from ultralytics import YOLO


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
        image = self.preprocess(image)
        if self.task == "Flowering" or self.task == "Fruitlet":
            self_model = YOLO("yolov8n.pt")
        else:
            self_model = YOLO("yolov8n.pt")  # Default model
        results = self_model(image, verbose=False)[0]

        if results.boxes is None or len(results.boxes) == 0:
            return np.empty((0, 4, 2))

        boxes_xyxy = results.boxes.xyxy.cpu().numpy()
        rectangles = []
        for x1, y1, x2, y2 in boxes_xyxy:
            rectangles.append(
                [
                    [y1, x1],  # top-left
                    [y1, x2],  # top-right
                    [y2, x2],  # bottom-right
                    [y2, x1],  # bottom-left
                ]
            )
        return np.array(rectangles)
