import charloratools as clt
import torch
from pathlib import Path
from comfy_execution.graph_utils import GraphBuilder


class DirLoaderSelectorNode:
    """
    Custom node which loads all images from a directory as separate
    torch tensors and allows for selection of a single image.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "directory_path": ("STRING", {
                "default": ""
            }),
            "index_number": ("INT", {
                "default": 0
            })
        }}

    @classmethod
    def IS_CHANGED(cls, directory_path: str, index_number: int):
        return float("NaN")

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load_images"
    CATEGORY = "LoRaDatasetTools/loaders"
    OUTPUT_NODE = True

    def load_images(self, directory_path: str, index_number: int):
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
            gm = clt.SysFileManager.GalleryManager(path=p)
            # [B,C,W,H] - > [B,W,H,C]
            imgs = []
            for ip in gm.image_paths:
                t = clt.utils.img_path_to_tensor(ip).unsqueeze(0)
                img = torch.permute(t, (0, 2, 3, 1))
                imgs.append(img)

            graph.node("PreviewImage",
                       images=imgs[index_number],
                       prompt=None,
                       extra_pnginfo=None)
            return {"result": (imgs[index_number],),
                    "expand": graph.finalize(), }

        except Exception as e:
            raise RuntimeError(
                f"There was an error while loading images : {e}")
