import charloratools as clt
import torch
import tempfile
from pathlib import Path


class AddGMNode:
    """
    Custom node which adds all images from 2
    Gallery Manager nodes into a single
    torch image batch tensor (Will duplicate the repeated images in
    the result.), Also Returns a Gallery Manager Object.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "GM_1": ("GM", {
                "forceInput": True
            }),
            "GM_2": ("GM", {
                "forceInput": True
            })
        }}

    @classmethod
    def IS_CHANGED(cls, GM_1: clt.SysFileManager.GalleryManager,
                   GM_2: clt.SysFileManager.GalleryManager,):
        return float("NaN")

    RETURN_TYPES = ("GM", "IMAGE")
    FUNCTION = "add_gm_nodes"
    CATEGORY = "LoRaDatasetTools/operations"
    OUTPUT_NODE = True

    def add_gm_nodes(self, GM_1: clt.SysFileManager.GalleryManager,
                     GM_2: clt.SysFileManager.GalleryManager,):

        # Loading images
        try:
            temp1 = tempfile.TemporaryDirectory()
            temp2 = tempfile.TemporaryDirectory()
            tmp1_path = Path(temp1.name).resolve()
            tmp2_path = Path(temp2.name).resolve()
            custom_node_folder = Path(__file__).resolve()
            custom_nodes = custom_node_folder.parent.resolve()
            base_path = custom_nodes.parent.parent.resolve()
            output_folder = base_path / "output"
            unique_folder_name = f'LDT_Add_{clt.utils.GetUniqueDtStr()}'
            unique_outfolder = output_folder / unique_folder_name
            clt.utils.dirisvalid(path=unique_outfolder,
                                 create_if_not_found=True)
            for (img_manager) in GM_1:
                img_manager.copy_to(tmp1_path)
            for (img_manager) in GM_2:
                img_manager.copy_to(tmp2_path)

            tmp_gm1 = clt.SysFileManager.GalleryManager(path=tmp1_path,
                                                        hashtype=GM_1.hashtype)
            tmp_gm2 = clt.SysFileManager.GalleryManager(path=tmp2_path,
                                                        hashtype=GM_2.hashtype)
            tmp_gm1 += tmp_gm2

            for (img_manager) in tmp_gm1:
                img_manager.copy_to(unique_outfolder)

            imgs = clt.utils.dir_path_to_img_batch(unique_outfolder)

            # [B,C,W,H] - > [B,W,H,C]
            imgs = torch.permute(imgs, (0, 2, 3, 1))

            gm_r = clt.SysFileManager.GalleryManager(path=unique_outfolder,
                                                     hashtype=GM_1.hashtype)

            temp1.cleanup()
            temp2.cleanup()
            return (gm_r, imgs,)

        except Exception as e:
            raise RuntimeError(
                f"There was an error while loading images : {e}")
