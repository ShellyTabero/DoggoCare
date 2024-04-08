import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, models
from sklearn.model_selection import train_test_split
from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Define dataset class
class DogEmotionDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.emotions = os.listdir(root_dir)
        self.num_classes = len(self.emotions)
        self.images = []
        self.labels = []
        for i, emotion in enumerate(self.emotions):
            emotion_dir = os.path.join(root_dir, emotion)
            for image_name in os.listdir(emotion_dir):
                image_path = os.path.join(emotion_dir, image_name)
                self.images.append(image_path)
                self.labels.append(i)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image_path = self.images[idx]
        label = self.labels[idx]
        image = Image.open(image_path)
        if self.transform:
            image = self.transform(image)
        return image, label


data_transforms = transforms.Compose([
    transforms.Resize((375, 500)),  # Resize images to original size
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


root_dir = 'Dog Emotion'
dataset = DogEmotionDataset(root_dir, transform=data_transforms)

train_data, test_data = train_test_split(dataset, test_size=0.2, random_state=50)

train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
test_loader = DataLoader(test_data, batch_size=32, shuffle=False)
model = models.inception_v3(pretrained=True)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, len(dataset.emotions))  # Change output layer to match number of classes
model = model.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

# Train the model
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    for images, labels in train_loader:
        print(labels)
        images = images.to(device)
        labels = labels.to(device)
        optimizer.zero_grad()
        outputs, _ = model(images)  # Get logits from the model
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

    train_loss = running_loss / len(train_loader)
    train_accuracy = 100. * correct / total

    # Evaluate the model
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)  # Get logits from the model
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

    test_accuracy = 100. * correct / total

    print(f"Epoch [{epoch + 1}/{num_epochs}], "
          f"Train Loss: {train_loss:.4f}, "
          f"Train Accuracy: {train_accuracy:.2f}%, "
          f"Test Accuracy: {test_accuracy:.2f}%")


#torch.save(model.state_dict(), 'model_weights.pth')
#torch.save(model, 'model.pth')

