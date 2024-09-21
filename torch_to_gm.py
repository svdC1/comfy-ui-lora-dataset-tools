import charloratools as clt
import torch
from pathlib import Path
from PIL import Image
import numpy as np


class TorchToGMNode:
    """
    Custom node to save a torch image batch tensor as a directory inside the
    outputs folder and return a Gallery Manager instance.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "images": ("IMAGE", {}),
            "folder_prefix": ("STRING", {"default": "LDT"}),
            "hashtype": (["sha256",
                          "phash",
                          "dhash",
                          "crop_resistant",
                          "avg_hash"], {})
            }
                }

    @classmethod
    def IS_CHANGED(cls, images: torch.Tensor,
                   folder_prefix: str,
                   hashtype: str):
        return float("NaN")

    RETURN_TYPES = ("GM", )
    FUNCTION = "save_images"
    CATEGORY = "LoRaDatasetTools/conversions"
    OUTPUT_NODE = True

    def save_images(self, images: torch.Tensor,
                    folder_prefix: str,
                    hashtype: str):

        custom_node_folder = Path(__file__).resolve()
        custom_nodes = custom_node_folder.parent.resolve()
        base_path = custom_nodes.parent.parent.resolve()
        output_folder = base_path / "output"
        new_dir_name = f"{folder_prefix}_{clt.utils.GetUniqueDtStr()}"
        outdir = output_folder / new_dir_name
        # saving images
        try:
            clt.utils.dirisvalid(outdir, create_if_not_found=True)
            images_np = images.cpu().numpy()
            for idx in range(images_np.shape[0]):
                image_np = images_np[idx]
                image_np = (image_np * 255).astype(np.uint8)
                # Convert the numpy array (H, W, C) into a PIL Image
                image_pil = Image.fromarray(image_np)
                # Construct the file path and save the image
                file_path = outdir/f"gm_save_{idx}.jpg"
                image_pil.save(file_path)

            gm = clt.SysFileManager.GalleryManager(path=outdir,
                                                   hashtype=hashtype)
            return (gm, )

        except Exception as e:
            raise RuntimeError(
                f"There was an error while saving images : {e}")
