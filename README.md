# ![LDT Logo](https://imagedelivery.net/YCQ3OFRYiR1R_AeUslNHiw/51f4586d-9481-4420-54d2-216cd3114900/w=1280,h=640px,fit=crop)

>![publish](https://github.com/svdC1/comfy-ui-lora-dataset-tools/actions/workflows/publish.yml/badge.svg)

### A custom node for ComfyUI providing nodes to facilitate the process of image gathering,filtering and processing when creating a training dataset to use for training loras.

# Nodes

### Directory Loader
>   Loads all images from a directory in a
    batch torch tensor. The width and height of all images
    are upscaled to match those of the largest image file in the
    directory using PIL's `Image.LANCZOS`

### Directory Selector
>   Loads all images from a direcotry as list of torch tensors,
    allowing the user to preview images like the built-in 
    ```"Preview Image"``` node and select one from the list
    to be the node's output.

### Filter Images Without Faces
>   Takes as input a batch of images and returns only those which
    contain at least one face in it using `facenet_pytorch`'s implementation
    of `MTCNN`

### Load Gallery Manager
>   Custom node which loads all images from a directory to a
    Gallery Manager object which can perform some custom
    functions defined in the extension.
    ```Warning:```
    **The operations performed with Gallery Managers
    take place in the OS file system using the charloratools
    package, for more information please check the [package's
    github](https://github.com/svdC1/charloratools). While using the operation nodes in ComfyUI you can expect their return inside the "output" folder.** Uses the
    ```Preview Image Node``` to show the images that were batched
    in the UI.

### Gallery Manager to Batch & Batch to Gallery Manager
>   Custom nodes which allow easy conversion between 
    ```GalleryManager``` outputs and ```torch's tensor batches of
    images```

### Add Gallery Manager
>   Custom node which ```adds all images from 2
    Gallery Manager nodes into a single
    torch image batch``` tensor **(Will duplicate the repeated images in
    the result.)**, Also Returns a Gallery Manager Object.
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

### Delete Duplicates
>   Compares the hashes of all images
    in a batch and deletes the images with repeated hashes.
    Takes as input the torch tensor image batch and a string
    representing which hashing function to use.
    The available ones are :
    ```sha256```, ```P-Hash```,```D-Hash```,```Average-Hash ``` and ```Crop-Resistant-Hash```

### Save As HTML Image Gallery

>   Generates a standalone HTML image gallery from a torch tensor batch of images. The gallery is saved in the output's folder as  ```generated_img_gallery.html``` or ```generated_img_gallery_{unique_datetime_string}``` if there's already a file with that name. The gallery uses js and css distributed by public cdn's to improve the display experience.

### Filter Images With Multiple Faces

>   Filters images with multiple faces -
    Takes as input a torch image batch and returns only
    those which have only a single face on it.
    
# Roadmap

 - Implement the rest of [charloratools](https://www.github.com/svdC1/charloratools) functionalities.

