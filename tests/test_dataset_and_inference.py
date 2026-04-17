import importlib.util
import sys
import types
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DATA_PATH = ROOT / "src" / "deepphenotree" / "_sample_data.py"
INFERENCE_PATH = ROOT / "src" / "deepphenotree" / "inference.py"


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _load_inference_module(module_name: str):
    ultralytics = types.ModuleType("ultralytics")
    ultralytics.RTDETR = object
    ultralytics.YOLO = object

    sahi = types.ModuleType("sahi")
    sahi_models = types.ModuleType("sahi.models")
    sahi_models_ultralytics = types.ModuleType("sahi.models.ultralytics")
    sahi_predict = types.ModuleType("sahi.predict")

    class _PlaceholderDetectionModel:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

    def _placeholder_get_sliced_prediction(*args, **kwargs):
        raise AssertionError("This stub should be replaced in the test")

    sahi_models_ultralytics.UltralyticsDetectionModel = (
        _PlaceholderDetectionModel
    )
    sahi_predict.get_sliced_prediction = _placeholder_get_sliced_prediction

    torch = types.ModuleType("torch")

    class _CudaModule:
        @staticmethod
        def is_available():
            return False

    torch.cuda = _CudaModule()

    previous = {
        name: sys.modules.get(name)
        for name in [
            "ultralytics",
            "sahi",
            "sahi.models",
            "sahi.models.ultralytics",
            "sahi.predict",
            "torch",
        ]
    }

    sys.modules["ultralytics"] = ultralytics
    sys.modules["sahi"] = sahi
    sys.modules["sahi.models"] = sahi_models
    sys.modules["sahi.models.ultralytics"] = sahi_models_ultralytics
    sys.modules["sahi.predict"] = sahi_predict
    sys.modules["torch"] = torch

    try:
        return _load_module(module_name, INFERENCE_PATH)
    finally:
        for name, original in previous.items():
            if original is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original


def test_deepphenotree_data_loads_and_pads_images(monkeypatch):
    sample_data = _load_module("test_sample_data_module", SAMPLE_DATA_PATH)

    images = {
        "Flowering_belgium.png": np.full((2, 3, 3), 11, dtype=np.uint8),
        "Flowering_italy.png": np.full((4, 2, 3), 22, dtype=np.uint8),
        "Flowering_spain.png": np.full((3, 5, 3), 33, dtype=np.uint8),
        "Flowering_switzerland.png": np.full((1, 4, 3), 44, dtype=np.uint8),
    }

    def fake_imread(path):
        return images[Path(path).name].copy()

    monkeypatch.setattr(sample_data.cv2, "imread", fake_imread)
    monkeypatch.setattr(sample_data.cv2, "cvtColor", lambda image, _: image)

    data = sample_data.DeepPhenoTreeData("Flowering")

    assert data.names == ["Belgium", "Italy", "Spain", "Switzerland"]
    assert data.data.shape == (4, 5, 3, 4)
    np.testing.assert_array_equal(data.data[:2, :3, :, 0], images["Flowering_belgium.png"])
    np.testing.assert_array_equal(data.data[:4, :2, :, 1], images["Flowering_italy.png"])
    np.testing.assert_array_equal(data.data[:3, :5, :, 2], images["Flowering_spain.png"])
    np.testing.assert_array_equal(data.data[:1, :4, :, 3], images["Flowering_switzerland.png"])
    assert np.all(data.data[2:, 3:, :, 0] == 0)


@pytest.mark.parametrize("task", ["Flowering", "Fruitlet", "Fruit"])
def test_deepphenotree_data_accepts_all_supported_tasks(monkeypatch, task):
    sample_data = _load_module(f"test_sample_data_{task}", SAMPLE_DATA_PATH)

    monkeypatch.setattr(
        sample_data.cv2,
        "imread",
        lambda _: np.zeros((2, 2, 3), dtype=np.uint8),
    )
    monkeypatch.setattr(sample_data.cv2, "cvtColor", lambda image, _: image)

    data = sample_data.DeepPhenoTreeData(task)

    assert data.data.shape == (2, 2, 3, 4)
    assert data.names == ["Belgium", "Italy", "Spain", "Switzerland"]


def test_deepphenotree_data_rejects_unknown_task():
    sample_data = _load_module("test_sample_data_invalid", SAMPLE_DATA_PATH)

    with pytest.raises(ValueError, match="Task must be one of"):
        sample_data.DeepPhenoTreeData("Leaves")


def test_yolo_inferencer_preprocess_converts_grayscale_float_image():
    inference = _load_inference_module("test_inference_preprocess")
    inferencer = inference.YoloInferencer("Flowering")
    image = np.array([[0.0, 0.5], [1.0, 0.25]], dtype=np.float32)

    processed = inferencer.preprocess(image)

    assert processed.shape == (2, 2, 3)
    assert processed.dtype == np.uint8
    np.testing.assert_array_equal(processed[..., 0], processed[..., 1])
    np.testing.assert_array_equal(processed[..., 1], processed[..., 2])
    assert processed[1, 0, 0] == 255


@pytest.mark.parametrize(
    ("task", "expected_suffix", "expected_threshold"),
    [
        ("Flowering", "Flowering/best.pt", 0.529),
        ("Fruitlet", "Fruitlet/best.pt", 0.539),
        ("Fruit", "Fruit/best.pt", 0.594),
    ],
)
def test_yolo_inferencer_predict_boxes_uses_expected_model_and_returns_rectangles(
    monkeypatch, task, expected_suffix, expected_threshold
):
    inference = _load_inference_module(f"test_inference_predict_{task}")
    created_models = []

    class FakeDetectionModel:
        def __init__(self, **kwargs):
            created_models.append(kwargs)

    class FakeBBox:
        def __init__(self, coords):
            self._coords = coords

        def to_xyxy(self):
            return self._coords

    class FakePrediction:
        def __init__(self, coords):
            self.bbox = FakeBBox(coords)

    def fake_get_sliced_prediction(image, detection_model, **kwargs):
        assert isinstance(detection_model, FakeDetectionModel)
        assert image.dtype == np.uint8
        assert kwargs["slice_height"] == 640
        assert kwargs["slice_width"] == 640
        return types.SimpleNamespace(
            object_prediction_list=[
                FakePrediction((10, 20, 30, 40)),
                FakePrediction((1, 2, 3, 4)),
            ]
        )

    monkeypatch.setattr(
        inference, "UltralyticsDetectionModel", FakeDetectionModel
    )
    monkeypatch.setattr(
        inference, "get_sliced_prediction", fake_get_sliced_prediction
    )

    boxes = inference.YoloInferencer(task).predict_boxes(
        np.ones((8, 8, 3), dtype=np.float32)
    )

    assert len(created_models) == 1
    assert created_models[0]["device"] == "cpu"
    assert created_models[0]["confidence_threshold"] == expected_threshold
    assert created_models[0]["model_path"].endswith(expected_suffix)
    np.testing.assert_array_equal(
        boxes,
        np.array(
            [
                [[20, 10], [20, 30], [40, 30], [40, 10]],
                [[2, 1], [2, 3], [4, 3], [4, 1]],
            ]
        ),
    )


def test_yolo_inferencer_predict_boxes_returns_empty_array_for_no_detections(
    monkeypatch,
):
    inference = _load_inference_module("test_inference_empty")

    class FakeDetectionModel:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    monkeypatch.setattr(
        inference, "UltralyticsDetectionModel", FakeDetectionModel
    )
    monkeypatch.setattr(
        inference,
        "get_sliced_prediction",
        lambda *args, **kwargs: types.SimpleNamespace(
            object_prediction_list=[]
        ),
    )

    boxes = inference.YoloInferencer("Fruit").predict_boxes(
        np.zeros((4, 4, 3), dtype=np.uint8)
    )

    assert boxes.shape == (0, 4, 2)

