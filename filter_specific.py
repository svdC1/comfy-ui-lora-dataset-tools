import charloratools as clt
import torch
from pathlib import Path
import numpy as np
from PIL import Image
import tempfile


class FilterSpecificNode:
    """
    A custom node for filtering images without a
    provided reference image.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "images": ("IMAGE", {}),
            "reference_image": ("IMAGE", {}),
            "distance_threshold": ("FLOAT", {"default": 0.6,
                                             "min": 0,
                                             "max": 1.0}),
            "distance_function": (["euclidean", "cosine"], {}),
            "pretrained_model": (['vggface2', 'casia-webface'], {}),


            "min_face_size": ("INT", {"default": 20,
                                      "min": 1,
                                      'max': 900}),
            "prob_threshold": ("FLOAT", {"default": 0.9,
                                         "min": 0.0,
                                         "max": 1.0}),

        }}

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "filter_images"
    CATEGORY = "LoRaDatasetTools/filters"

    def filter_images(self,
                      images: torch.Tensor,
                      min_face_size: int,
                      prob_threshold: float,
                      reference_image: torch.Tensor,
                      distance_threshold: float,
                      pretrained_model: str,
                      distance_function: str):
        # Saving Images

        images_np = images.cpu().numpy()
        ref_img_np = reference_image.cpu().squeeze(0).numpy()
        # ref_img_np = torch.permute(ref_img_np, (0, 2, 3, 1))
        temp_dir_load = tempfile.TemporaryDirectory()
        temp_dir_ref = tempfile.TemporaryDirectory()
        temp_dir_save = tempfile.TemporaryDirectory()
        tmp_path_load = Path(temp_dir_load.name).resolve()
        tmp_path_ref = Path(temp_dir_ref.name).resolve()
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

        ref_img_np = (ref_img_np * 255).astype(np.uint8)
        ref_img_pil = Image.fromarray(ref_img_np)
        ref_fp = tmp_path_ref/"ref_img.jpg"
        ref_img_pil.save(ref_fp)

        if prob_threshold == 0:
            prob_threshold = None
        fr_instance = clt.FilterAI.FaceRecognizer(path=tmp_path_load)
        try:
            fr_instance.filter_images_without_specific_face(
                ref_img_path=ref_fp,
                distance_function=distance_function,
                distance_threshold=distance_threshold,
                pretrained_model=pretrained_model,
                output_dir=tmp_path_save,
                min_face_size=min_face_size,
                prob_threshold=prob_threshold,
                )
        except clt.errors.NoImagesInDirectoryError:
            raise RuntimeError("No faces detected!")

        img_tensor = clt.utils.dir_path_to_img_batch(tmp_path_save)
        imgs = torch.permute(img_tensor, (0, 2, 3, 1))
        temp_dir_ref.cleanup()
        temp_dir_load.cleanup()
        temp_dir_save.cleanup()
        return (imgs,)
