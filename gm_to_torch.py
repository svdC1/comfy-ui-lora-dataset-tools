import charloratools as clt
import torch


class GMToTorchNode:
    """
    Custom node to perform node expansion on the Directory
    Loader Node but accepting a Gallery Manager instance
    instead of a directory path for convenience.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "GM": ("GM", {"forceInput": True})
        }}

    @classmethod
    def IS_CHANGED(cls, GM: clt.SysFileManager.GalleryManager):
        return float("NaN")

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "gm_to_torch"
    CATEGORY = "LoRaDatasetTools/conversions"
    OUTPUT_NODE = True

    def gm_to_torch(self, GM: clt.SysFileManager.GalleryManager):

        # Loading images
        try:
            p = GM.path
            imgs = clt.utils.dir_path_to_img_batch(p)
            # [B,C,W,H] - > [B,W,H,C]
            imgs = torch.permute(imgs, (0, 2, 3, 1))
            return (imgs,)

        except Exception as e:
            raise RuntimeError(
                f"There was an error while loading images : {e}")
