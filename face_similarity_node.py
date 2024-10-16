import torch
from torchvision import transforms
from PIL import Image, ImageDraw, ImageFont
from charloratools.facenet_pytorch import MTCNN, InceptionResnetV1
from charloratools.utils import distance_function


class FaceSimNode:
    """
    Custom Node for checking the cosine similarity or euclidean distance
    between two face embeddings generated by facenet_pytorch's Inception
    Resnet. The faces are detected from the images provided using
    MTCNN, also with facenet_pytorch's implementation.
    Returns both images provided with the face aligned (cropped from image)
    and prewhitened besides returning a white image with the
    similarity written as black text in the image's center
    as a percentage.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {'image_1': ("IMAGE", {}),
                             'image_2': ("IMAGE", {}),
                             'method': (['euclidean', 'cosine'], {})
                             }}

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "face_sim"
    CATEGORY = "LoRaDatasetTools/filters"

    def face_sim(self, image_1: torch.Tensor,
                 image_2: torch.Tensor,
                 method: str):

        # [B,H,W,C]
        img1_size = image_1.size(dim=0)
        img2_size = image_2.size(dim=0)
        # Validate Inputs
        if img1_size > 1:
            raise TypeError(f"Please provide only 1 image, got {img1_size}")

        if img2_size > 1:
            raise TypeError(f"Please provide only 1 image, got {img2_size}")

        # Remove batch dimension [H,W,C]
        image_1 = image_1[0]
        image_2 = image_2[0]
        try:
            # [C,H,W]
            image_1 = torch.permute(image_1, (2, 0, 1))
            image_2 = torch.permute(image_2, (2, 0, 1))
            to_pil = transforms.ToPILImage()
            to_torch = transforms.ToTensor()
            img1_pil = to_pil(image_1).convert('RGB')
            img2_pil = to_pil(image_2).convert('RGB')
        except Exception as e:
            raise RuntimeError(f"Error converting images to PIL format:{e}")

        # Initialize MTCNN for face detection
        mtcnn = MTCNN(keep_all=False,
                      selection_method='probability',
                      min_face_size=20)
        # Load pre-trained FaceNet model
        resnet = InceptionResnetV1(pretrained='vggface2').eval()

        try:
            # boxes, probs
            b1, p1 = mtcnn.detect(img1_pil)
            b2, p2 = mtcnn.detect(img2_pil)

            if b1 is None or len(b1) > 1:
                raise TypeError("Image 1 contains multiple or no faces.")
            if b2 is None or len(b1) > 1:
                raise TypeError("Image 1 contains multiple or no faces.")
        except Exception as e:
            raise RuntimeError(f"Error when detecting faces: {e}")

        try:
            # Add Batch Dim to Result [B,C,H,W]
            img1_aligned = mtcnn(img1_pil).unsqueeze(0)
            img2_aligned = mtcnn(img2_pil).unsqueeze(0)
            emb_1 = resnet(img1_aligned)
            emb_2 = resnet(img2_aligned)
        except Exception as e:
            raise RuntimeError(f"Error Generating Embeddings:{e}")

        try:
            distance = distance_function(emb_1, emb_2, method=method)
            distance = distance.item()
            if method == 'cosine':
                distance_p = distance*100
            else:
                distance_p = distance
        except Exception as e:
            raise RuntimeError(f"Error calculating distance:{e}")

        try:
            if method == 'cosine':
                text = f'Similarity:\n{distance_p:.2f}%'
                font = ImageFont.load_default(size=80)
            else:
                exp = '(Higher = Less Equal)'
                text = f'Euclidean Distance\n{exp}:\n{distance_p:.2f}'
                font = ImageFont.load_default(size=50)
            image = Image.new('RGB', (800, 800), color='white')
            draw = ImageDraw.Draw(image)
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            position = ((800 - text_width) // 2, (800 - text_height) // 2)
            draw.text(position, text, fill='black', font=font)
        except Exception as e:
            raise RuntimeError(f"Error Creating 'Show Distance' Image:{e}")

        try:
            # Convert Display Img to Tensor [C,H,W]
            d_img = to_torch(image)
            # [B,C,H,W]
            d_img = d_img.unsqueeze(0)
            # Convert Back to Comfy Display Type[B,H,W,C]
            d_img = torch.permute(d_img, (0, 2, 3, 1))
            # Aligned image at 800x800
            mtcnn2 = MTCNN(keep_all=False, selection_method='probability',
                           image_size=800, margin=100)
            # [B,C,H,W]
            aligned1 = mtcnn2(img1_pil).unsqueeze(0)
            aligned2 = mtcnn2(img2_pil).unsqueeze(0)
            # [B,H,W,C]
            aligned1 = torch.permute(aligned1, (0, 2, 3, 1))
            aligned2 = torch.permute(aligned2, (0, 2, 3, 1))
            out = torch.cat((d_img, aligned1, aligned2))
        except Exception as e:
            raise RuntimeError(f"Error Generating Display Images:{e}")
        return (out,)
