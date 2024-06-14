from torchvision import transforms
import torch

class ImagePreprocessor():
    def __init__(self, resolution=(1024, 1024)) -> None:
        self.transform_image = transforms.Compose([
            transforms.Resize(resolution),    # 1. keep consistent with the cv2.resize used in training 2. redundant with that in path_to_image()
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])

    def proc(self, image):
        image = self.transform_image(image)
        return image

def tensor_to_pil(tenor_im):
    im = tenor_im.cpu().clone()
    im = im.squeeze(0)
    tensor2pil = transforms.ToPILImage()
    im = tensor2pil(im)
    return im

def remove_background(model,image):
    image_2 = image.copy()
    original_shape = image.size
    image_preprocessor = ImagePreprocessor()
    
    input_images = image_preprocessor.proc(image).unsqueeze(0).to('cuda')
    og_image = image.resize((1024, 1024))
    with torch.no_grad():
        scaled_preds = model(input_images)[-1].sigmoid()
    for idx_sample in range(scaled_preds.shape[0]):
        res = torch.nn.functional.interpolate(
            scaled_preds[idx_sample].unsqueeze(0),
            size=og_image.size,
            mode='bilinear',
            align_corners=True
        )
    output=tensor_to_pil(res)   # test set dir + file name

    image_2.putalpha(output.resize(original_shape).convert('L'))
    return image_2