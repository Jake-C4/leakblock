from PIL import Image
import torchvision.transforms as T
from timm.models import create_model
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Use a pretrained model for NSFW detection (e.g., from NudeNet or similar)
model = create_model('mobilenetv3_small_050', pretrained=True, num_classes=2)
model.to(device)
model.eval()

transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
])

def is_nsfw(image: Image.Image) -> bool:
    img_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(img_tensor)
        probs = torch.softmax(output, dim=1)[0]
        return probs[1] > 0.85  # If class 1 is NSFW and confidence > 85%
