import charloratools as clt
import torch
from pathlib import Path
import time
import numpy as np
from PIL import Image
import tempfile


class DrawDetectionBoxNode:
    """
    A custom node for detecting faces in
    images and drawing a detection bounding box
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "images": ("IMAGE", {}),
            "min_face_size": ("INT", {"default": 20,
                                      "min": 1,
                                      'max': 900}),
            "prob_threshold": ("FLOAT", {"default": 0.9,
                                         "min": 0.0,
                                         "max": 1.0}),

        }}

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return time.time()

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "filter_and_draw_images"
    CATEGORY = "LoRaDatasetTools"

    def filter_and_draw_images(self,
                               images: torch.Tensor,
                               min_face_size: int,
                               prob_threshold: float):
        # Saving Images

        images_np = images.cpu().numpy()
        temp_dir_load = tempfile.TemporaryDirectory()
        temp_dir_save = tempfile.TemporaryDirectory()
        tmp_path_load = Path(temp_dir_load.name).resolve()
        tmp_path_save = Path(temp_dir_save.name).resolve()
        # Iterate through each image in the batch
        for idx in range(images_np.shape[0]):
            image_np = images_np[idx]
            image_np = (image_np * 255).astype(np.uint8)
            # Convert the numpy array (H, W, C) into a PIL Image
            image_pil = Image.fromarray(image_np)
            # Construct the file path and save the image
            file_path = tmp_path_load/f"filter_{idx}.jpg"
            image_pil.save(file_path)

        if prob_threshold == 0:
            prob_threshold = None
        fr_instance = clt.FilterAI.FaceRecognizer(path=tmp_path_load)
        try:
            gm, info = fr_instance.filter_images_without_face(
                output_dir=tmp_path_save,
                min_face_size=min_face_size,
                prob_threshold=prob_threshold,
                return_info=True)
        except clt.errors.NoImagesInDirectoryError:
            raise RuntimeError("No faces detected!")

        info_dict_lst = info['info_dict_lst']
        temp_dir_boxes = tempfile.TemporaryDirectory()
        tmp_path_boxes = Path(temp_dir_boxes.name).resolve()
        fr_instance.save_images_with_detection_box(
            info_dict_lst=info_dict_lst, output_dir=tmp_path_boxes)
        img_tensor = clt.utils.dir_path_to_img_batch(tmp_path_boxes)
        imgs = torch.permute(img_tensor, (0, 2, 3, 1))
        temp_dir_load.cleanup()
        temp_dir_save.cleanup()
        temp_dir_boxes.cleanup()
        return (imgs,)
