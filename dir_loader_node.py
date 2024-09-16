import charloratools as clt
import os
import torch
from server import PromptServer
from pathlib import Path
import time
import logging

class DirLoaderNode:
  """
  Custom node which loads all images from a directory.
  """
  
  @classmethod
  def INPUT_TYPES(cls):
    return {"required":{
      "directory_path":("STRING",{
        "default":""
      })
    }}
  
  @classmethod
  def IS_CHANGED(cls,**kwargs):
    return time.time()
    
    
    
  RETURN_TYPES=("IMAGE",)
  FUNCTION= "load_images"
  CATEGORY= "LoRaDatasetTools"
  
  def load_images(self,directory_path:str):
    #Validating path
    if not directory_path.strip():
      PromptServer.instance.send_sync("LoRaDatasetTools.validation_error", {
                "message": "Please provide a directory path!"
            })
      raise RuntimeError("Please provide a directory path!")
    
    if not Path(directory_path).resolve().exists():
      PromptServer.instance.send_sync("LoRaDatasetTools.validation_error",{
        "message":"The path provided is invalid !"
      })
      raise RuntimeError("Directory doesn't exist!")
    
    if not Path(directory_path).resolve().is_dir():
      PromptServer.instance.send_sync("LoRaDatasetTools.validation_error",{
        "message":"The path provided is not a directory !"
      })
      raise RuntimeError("Path isn't a directory!")
    
    #Loading images
    try:
      gm=clt.SysFileManager.GalleryManager(directory_path)
      imgs=clt.utils.dir_path_to_img_batch(gm.path)
      imgs=torch.permute(imgs,(0,2,3,1))
      return (imgs,)
    
    except Exception as e:
      PromptServer.instance.send_sync("LoRaDatasetTools.validation_error",{
        "message":f"There was an error while loading images : {e}"
      })
      raise RuntimeError(f"There was an error while loading images : {e}")