from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image
import torch

# Load the model and feature extractor from Hugging Face
model_name = "Falconsai/nsfw_image_detection"
extractor = AutoFeatureExtractor.from_pretrained(model_name)
model = AutoModelForImageClassification.from_pretrained(model_name)

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

def is_nsfw(image: Image.Image) -> bool:
    # Resize and convert image to RGB
    image = image.convert("RGB").resize((224, 224))

    # Extract pixel values
    inputs = extractor(images=image, return_tensors="pt").to(device)

    # Run model
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)[0]

    # Get label + probability
    label = probs.argmax().item()
    confidence = probs[label].item()

    # Label 1 is NSFW (per the model's docs)
    if label == 1 and confidence > 0.85:
        print(f"[NSFW DETECTED] Confidence: {confidence:.2f}")
        return True
    return False
