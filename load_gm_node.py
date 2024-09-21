import charloratools as clt
import torch
from pathlib import Path
from comfy_execution.graph_utils import GraphBuilder


class GMLoaderNode:
    """
    Custom node which loads all images from a directory to a
    Gallery Manager object which can perform some custom
    functions defined in the extension. Warning :
    The operations performed with Gallery Managers
    take place in the OS file system using the charloratools
    package, for more information please check the package's
    github. While using the operation nodes in ComfyUI you can
    expect their return inside the "output" folder. Uses the
    PreviewImage Node to show the images that were batched
    in the UI.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "directory_path": ("STRING", {
                "default": ""
            }),
            "hashtype": (["sha256",
                          "phash",
                          "dhash",
                          "crop_resistant",
                          "avg_hash"], {})
        }}

    @classmethod
    def IS_CHANGED(cls, directory_path: str, hashtype: str):
        return float("NaN")

    RETURN_TYPES = ("GM", "IMAGE",)
    FUNCTION = "load_gm_node"
    CATEGORY = "LoRaDatasetTools/loaders"
    OUTPUT_NODE = True

    def load_gm_node(self, directory_path: str, hashtype: str):
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
            gm = clt.SysFileManager.GalleryManager(path=p, hashtype=hashtype)
            return {"result": (gm, imgs,),
                    "expand": graph.finalize(), }

        except Exception as e:
            raise RuntimeError(
                f"There was an error while loading images : {e}")
