# inference/sahi_infer.py
import os
import time
from tqdm import tqdm
from PIL import Image
import torch
import numpy as np
from sahi.predict import get_sliced_prediction
from sahi.models.ultralytics import UltralyticsDetectionModel
from sahi.utils.cv import visualize_object_predictions
from pathlib import Path

def sahi_inference(
    path2model,
    path2testimg,
    path2outdir,
    window_height=640,
    window_width=640,
    overlap_h=0.2,
    overlap_w=0.2,
    conf=0.3
):
    output_label_dir = Path(path2outdir) / "labels"
    output_image_dir = Path(path2outdir) / "images"

    output_label_dir.mkdir(parents=True, exist_ok=True)
    output_image_dir.mkdir(parents=True, exist_ok=True)

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    detection_model = UltralyticsDetectionModel(
        model_path=path2model,
        confidence_threshold=conf,
        device=device
    )

    image_files = [f for f in os.listdir(path2testimg) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    start_time = time.time()
    for imagename in tqdm(image_files, desc="Running SAHI Inference on test images"):
        image_path = os.path.join(path2testimg,imagename)
        image_name, _ = os.path.splitext(imagename)
        img = Image.open(image_path)
        img_w, img_h = img.size

        result = get_sliced_prediction(
            image=image_path,
            detection_model=detection_model,
            slice_height=window_height,
            slice_width=window_width,
            overlap_height_ratio=overlap_h,
            overlap_width_ratio=overlap_w,
        )

        label_path = output_label_dir / f"{image_name}.txt"
        with open(label_path, "w") as f:
            for pred in result.object_prediction_list:
                class_id = pred.category.id
                x1, y1, x2, y2 = pred.bbox.to_xyxy()
                x_center = ((x1 + x2) / 2) / img_w
                y_center = ((y1 + y2) / 2) / img_h
                width = (x2 - x1) / img_w
                height = (y2 - y1) / img_h
                f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

        np_image = np.array(img)
        visualize_object_predictions(
            image=np_image,
            object_prediction_list=result.object_prediction_list,
            output_dir=str(output_image_dir),
            file_name=image_name,
            hide_labels=True,
            hide_conf=True,
            rect_th=3
        )
        print(f"{image_name}: {len(result.object_prediction_list)} detections")

    total = time.time() - start_time
    print(f"\nAll predictions completed in {total:.2f}s ({total/60:.2f}min).")
