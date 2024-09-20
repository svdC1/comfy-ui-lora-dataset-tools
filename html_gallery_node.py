import charloratools as ctl
from pathlib import Path
import torch
import tempfile
from PIL import Image
import numpy as np


class HTMLGalleryNode:
    """
    Custom node to generate a standalone HTML image gallery
    from a torch tensor batch of images. The gallery is saved
    in the output's folder as 'generated_img_gallery.html' or
    'generated_img_gallery_{unique_datetime_string}' if there's
    already a file with that name. The gallery uses js and css
    distributed by public cdn's to improve the display experience.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "images": ("IMAGE", {}),
        }}

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    RETURN_TYPES = ()
    FUNCTION = "generate_img_gallery"
    CATEGORY = "LoRaDatasetTools/misc"
    OUTPUT_NODE = True

    def generate_img_gallery(self, images: torch.Tensor):
        temp_dir_load = tempfile.TemporaryDirectory()
        tmp_path_load = Path(temp_dir_load.name).resolve()
        images_np = images.cpu().numpy()
        for idx in range(images_np.shape[0]):
            image_np = images_np[idx]
            image_np = (image_np * 255).astype(np.uint8)
            # Convert the numpy array (H, W, C) into a PIL Image
            image_pil = Image.fromarray(image_np)
            # Construct the file path and save the image
            file_path = tmp_path_load/f"filter_{idx}.jpg"
            image_pil.save(file_path)

        custom_node_folder = Path(__file__).resolve()
        custom_nodes = custom_node_folder.parent.resolve()
        base_path = custom_nodes.parent.parent.resolve()
        output_folder = base_path / "output"

        gm = ctl.SysFileManager.GalleryManager(path=tmp_path_load)
        gm.to_html_img_gallery(output_dir=output_folder)
        return {}
