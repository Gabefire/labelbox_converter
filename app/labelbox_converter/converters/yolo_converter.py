import labelbox as lb
from .labelbox_converter import _lb_converter
from ultralytics.engine.results import Results
import numpy as np
from PIL import Image
import io

class Yolo_Converter(_lb_converter):
    def __init__(self, project_id: str, client: lb.Client, ontology_mapping: dict[str:str]) -> None:
        """Class to integrate YoloV8 annotations with labelbox

        Args:
            project_id (str): labelbox project id
            client (lb.client): labelbox client
            ontology_mapping (dict[str:str]): Dictionary mapping YoloV8 classes to labelbox feature name.
        """
        super().__init__(project_id, client, ontology_mapping)
    
    def create_yolo_bbox_annotation_predictions(yolo_results: Results, global_keys: list[str]) -> None:
        """Convert YOLOV8 model results to labelbox bbox annotations format

        Args:
            yolo_results (list[ultralytics.engine.results.Results]): YoloV8 prediction results.
            global_keys (list[str]): List of labelbox global keys for image. Must be same order as results.
        """
        
        results = []

        for i,result in enumerate(yolo_results):
            prediction = {"global_key": global_keys[i],
                          "predictions": []}
            for bbox in result.boxes:
                start_x, start_y, end_x, end_y = bbox.xyxy.tolist()[0]
                prediction["predictions"].append({"answer": bbox.cls, "points": {"start_x": start_x, "start_y": start_y, "end_x": end_x, "end_y": end_y}})
            
            results.append(prediction)

        super().create_bbox_labels(results)
    
    def create_yolo_segment_annotation_predictions(yolo_results: Results, global_keys: list[str], image_sizes: list[tuple[int, int]]) -> None:
        """Convert YOLOV8 model results to labelbox segment annotations format

        Args:
            yolo_results (list[ultralytics.engine.results.Results]): YoloV8 prediction results.
            global_keys (list[str]): List of labelbox global keys for image. Must be same order as results.
            image_sizes (list[tuple[int, int]]): List of image size (W, H). Must be same order as results
        """
        
        results = []

        for x,result in enumerate(yolo_results):
            prediction = {"global_key": global_keys[x],
                          "predictions": []}
            for i, mask in enumerate(result.masks.data):
                mask: np = (mask.numpy() * 255).astype("uint8")
                img = Image.fromarray(mask, "L")
                img = img.resize(image_sizes[x])
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                encoded_image_bytes = img_byte_arr.getvalue()
                prediction["predictions"].append({
                                                "answer": int(result.boxes[i].cls), 
                                                "mask": encoded_image_bytes,
                                                "color": (255,255,255)
                                                })
            results.append(prediction)


        super().create_segment_labels(results)
    
    def create_yolo_polygon_annotation_predictions(yolo_results: Results, global_keys: list[str]) -> None:
        """Convert YOLOV8 model results to labelbox polygon annotations format

        Args:
            yolo_results (list[ultralytics.engine.results.Results]): YoloV8 prediction results.
            global_keys (list[str]): List of labelbox global keys for image. Must be same order as results.
        """
        
        results = []

        for x,result in enumerate(yolo_results):
            prediction = {"global_key": global_keys[x],
                          "predictions": []}
            for i, coordinates in enumerate(result.masks.xy):
                prediction["predictions"].append({"answer": int(result.boxes[i].cls), "points": [(coordinate[0],coordinate[1]) for coordinate in coordinates]})
            
            results.append(prediction)
        
        super().create_polygon_labels(results)