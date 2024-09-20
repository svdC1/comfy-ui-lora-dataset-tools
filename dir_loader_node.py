import charloratools as clt
import torch
from pathlib import Path
from comfy_execution.graph_utils import GraphBuilder


class DirLoaderNode:
    """
    Custom node which loads all images from a directory in a
    batch torch tensor. The width and height of all images
    are upscaled to match those of the largest image file in the
    directory using PIL's Image.LANCZOS.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "directory_path": ("STRING", {
                "default": ""
            })
        }}

    @classmethod
    def IS_CHANGED(cls, directory_path: str):
        return float("NaN")

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load_images"
    CATEGORY = "LoRaDatasetTools/loaders"
    OUTPUT_NODE = True

    def load_images(self, directory_path: str):
        # Validating path
        if not directory_path.strip():
            raise RuntimeError("Please provide a directory path!")

        elif not Path(directory_path).resolve().exists():
            raise RuntimeError("Directory doesn't exist!")

        elif not Path(directory_path).resolve().is_dir():
            raise RuntimeError("Path isn't a directory!")

        # Loading images
        try:
            graph = GraphBuilder()
            p = Path(directory_path).resolve()
            imgs = clt.utils.dir_path_to_img_batch(p)
            # [B,C,W,H] - > [B,W,H,C]
            imgs = torch.permute(imgs, (0, 2, 3, 1))
            graph.node("PreviewImage",
                       images=imgs,
                       prompt=None,
                       extra_pnginfo=None)
            return {"result": (imgs,),
                    "expand": graph.finalize(), }

        except Exception as e:
            raise RuntimeError(
                f"There was an error while loading images : {e}")
