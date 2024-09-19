from .dir_loader_node import DirLoaderNode
from .filter_node import FilterFacesNode
from .draw_detection_box_node import DrawDetectionBoxNode

NODE_CLASS_MAPPINGS = {
  "Directory Loader": DirLoaderNode,
  "Filter Images Without Faces": FilterFacesNode,
  "Detect Faces and Draw Detection Box": DrawDetectionBoxNode
}

WEB_DIRECTORY = './js'
__all__ = ['NODE_CLASS_MAPPINGS']
