import charloratools as clt
import torch
from pathlib import Path
import time
import numpy as np
from PIL import Image
import tempfile


class FilterFacesNode:
    """
    A custom node for filtering images without faces.
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
    FUNCTION = "filter_images"
    CATEGORY = "LoRaDatasetTools"

    def filter_images(self,
                      images: torch.Tensor,
                      min_face_size: int,
                      prob_threshold: float):
        # Saving Images

        # ()
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
            fr_instance.filter_images_without_face(
                output_dir=tmp_path_save,
                min_face_size=min_face_size,
                prob_threshold=prob_threshold)
        except clt.errors.NoImagesInDirectoryError:
            raise RuntimeError("No faces detected!")

        img_tensor = clt.utils.dir_path_to_img_batch(tmp_path_save)
        imgs = torch.permute(img_tensor, (0, 2, 3, 1))
        temp_dir_load.cleanup()
        temp_dir_save.cleanup()
        return (imgs,)
