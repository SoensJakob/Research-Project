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
    train_set = core.Dataset("data/train/",transform=custom_transforms)#L1
    test_set = core.Dataset("data/valid/")#L2
    loader=core.DataLoader(train_set, batch_size=2, shuffle=True)#L3
    model = core.Model(["0","1","2","3"])#L4

    losses = model.fit(loader, test_set, epochs=25, lr_step_size=5, learning_rate=0.001, verbose=True)

    # plt.plot(losses)
    # plt.show()

    model.save("model_weights_v1.pth")
