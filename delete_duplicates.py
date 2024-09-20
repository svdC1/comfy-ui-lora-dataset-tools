import charloratools as clt
import torch
from pathlib import Path
import numpy as np
from PIL import Image
import tempfile


class DeleteDuplicatesNode:
    """
    Custom node which compares the hashes of all images
    in a batch and deletes the images with repeated hashes.
    Takes as input the torch tensor image batch and a string
    representing which hashing function to use.
    The available ones are :

    ['sha256','phash',
     'dhash','crop_resistant',
     'avg_hash']
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "images": ("IMAGE", {}),
            "hashtype": (["sha256",
                          "phash",
                          "dhash",
                          "crop_resistant",
                          "avg_hash"], {})
        }}

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "filter_images"
    CATEGORY = "LoRaDatasetTools/filters"

    def filter_images(self,
                      images: torch.Tensor,
                      hashtype: str):
        # Saving Images

        images_np = images.cpu().numpy()
        temp_dir_load = tempfile.TemporaryDirectory()
        tmp_path_load = Path(temp_dir_load.name).resolve()
        # Iterate through each image in the batch
        for idx in range(images_np.shape[0]):
            image_np = images_np[idx]
            image_np = (image_np * 255).astype(np.uint8)
            # Convert the numpy array (H, W, C) into a PIL Image
            image_pil = Image.fromarray(image_np)
            # Construct the file path and save the image
            file_path = tmp_path_load/f"filter_{idx}.jpg"
            image_pil.save(file_path)

        gm = clt.SysFileManager.GalleryManager(path=tmp_path_load,
                                               hashtype=hashtype)
        try:
            gm.delete_duplicates()

        except Exception as e:
            raise RuntimeError(f"Error while filtering images : {e}")

        img_tensor = clt.utils.dir_path_to_img_batch(tmp_path_load)
        imgs = torch.permute(img_tensor, (0, 2, 3, 1))
        temp_dir_load.cleanup()
        return (imgs,)
