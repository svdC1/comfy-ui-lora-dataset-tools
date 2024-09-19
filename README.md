# LoRa Dataset Tools - A Custom Node For ComfyUI

### A custom node for ComfyUI providing nodes to facilitate the process of image gathering,filtering and processing when creating a training dataset to use for training loras.

# Nodes

### Directory Loader
>   Loads all images from a directory in a
    batch torch tensor. The width and height of all images
    are upscaled to match those of the largest image file in the
    directory using PIL's `Image.LANCZOS`
### Filter Images Without Faces
>   Takes as input a batch of images and returns only those which
    contain at least one face in it using `facenet_pytorch`'s implementation
    of `MTCNN`


### Filter Images Without Specific Face
> Takes as input a batch of images and a single reference image
  and returns images from the batch which contain the reference
  image using `facenet_pytorch`'s implementation of `MTCNN` and 
  `InceptionResnetV1`

### Detect Faces and Draw Detection Boxes
> Takes as input a batch of images and returns only those which
  contain at least one face in it using facenet_pytorch's implementation
  of `MTCNN`. The returned images have the `MTCNN`'s predicted detection
  boxes drawn using `opencv-python` library.

# Roadmap

 - Implement the rest of [charloratools](https://www.github.com/svdC1/charloratools) functionalities.

 - Change the forked `facenet_pytorch` in `charloratools` to load `MTCNN`and `IncepetionResnetV1` using weights only ( currently loading as pickle object which is unsafe )

