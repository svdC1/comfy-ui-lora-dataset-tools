"""
@author: svdC1
@title: LoRaDatasetTools
@nickname: LDT
@description: This custom node provides quality of life functionalities for
managing an image training dataset.
"""


from .dir_loader_node import DirLoaderNode
from .filter_node import FilterFacesNode
from .draw_detection_box_node import DrawDetectionBoxNode
from .dir_loader_selector import DirLoaderSelectorNode
from .filter_specific import FilterSpecificNode
from .filter_multiple import FilterFacesMultipleNode
from .html_gallery_node import HTMLGalleryNode
from .delete_duplicates import DeleteDuplicatesNode
from .load_gm_node import GMLoaderNode
from .gm_to_torch import GMToTorchNode
from .torch_to_gm import TorchToGMNode
from .add_gm_node import AddGMNode
from .face_similarity_node import FaceSimNode

NODE_CLASS_MAPPINGS = {
  "Directory Loader": DirLoaderNode,
  "Directory Selector": DirLoaderSelectorNode,
  "Filter Images Without Faces": FilterFacesNode,
  "Detect Faces and Draw Detection Box": DrawDetectionBoxNode,
  "Filter Images Without Specific Face": FilterSpecificNode,
  "Filter Images With Multiple Faces": FilterFacesMultipleNode,
  "Save As HTML Image Gallery": HTMLGalleryNode,
  "Delete Duplicates": DeleteDuplicatesNode,
  "Load Gallery Manager": GMLoaderNode,
  "Gallery Manager to Batch": GMToTorchNode,
  "Batch to Gallery Manager": TorchToGMNode,
  "Add Gallery Manager": AddGMNode,
  "Face Similarity": FaceSimNode
}

WEB_DIRECTORY = './js'
__all__ = ['NODE_CLASS_MAPPINGS', "WEB_DIRECTORY"]
