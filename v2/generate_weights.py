from detecto import core, utils, visualize
from detecto.visualize import show_labeled_image, plot_prediction_grid
from torchvision import transforms
import torch
import matplotlib.pyplot as plt
import numpy as np
import json, itertools, time



device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)

custom_transforms = transforms.Compose([
transforms.ToPILImage(),
transforms.Resize(640),
transforms.RandomHorizontalFlip(0.5),
transforms.ColorJitter(saturation=0.2),
transforms.ToTensor(),
utils.normalize_transform(),
])

if __name__ == "__main__":
    train_set = core.Dataset("data/train/",transform=custom_transforms)
    test_set = core.Dataset("data/valid/")
    loader=core.DataLoader(train_set, batch_size=2, shuffle=True)
    model = core.Model(["nav","frame","heading","text","checkbox","input","button","container","footer"])

    losses = model.fit(loader, test_set, epochs=15, lr_step_size=5, learning_rate=0.001, verbose=True)

    # plt.plot(losses)
    # plt.show()

    model.save("model_weights_v2.pth")
