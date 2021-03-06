import torch.utils.data
import numpy as np
import torchvision
import torch
from torch import nn
from torch.backends import cudnn
from torch import optim
from torch.nn import functional as F
from torchvision import transforms
import matplotlib.pyplot as plt

def main():
    np.random.seed(seed:=69)
    torch.manual_seed(seed)
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    torch.backends.cudnn.benchmark = True
    torch.multiprocessing.freeze_support()

    transform = transforms.Compose(
        [transforms.ToTensor(),
        transforms.Normalize((.5,.5,.5), (.5,.5,.5))])

    class Net(nn.Module):
        def __init__(self):
            super(Net, self).__init__()
            self.conv1 = nn.Conv2d(3, 6, 5)
            self.pool = nn.MaxPool2d(2, 2)
            self.conv2 = nn.Conv2d(6, 16, 5)
            self.fc1 = nn.Linear(16 * 5 * 5, 120)
            self.fc2 = nn.Linear(120, 84)
            self.fc3 = nn.Linear(84, 10)

        def forward(self, x):
            x = self.pool(F.relu(self.conv1(x)))
            x = self.pool(F.relu(self.conv2(x)))
            x = x.view(-1, 16 * 5 * 5)
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            x = self.fc3(x)
            return x

    net = Net().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(net.parameters(), lr=0.001)

    root = 'E:\Vision'
    trainset = torchvision.datasets.CIFAR10(root=root, train=True, download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=4, shuffle=True, num_workers=2)
    testset = torchvision.datasets.CIFAR10(root=root, train=False, download=True, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=4, shuffle=False, num_workers=2)
    classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

    def imshow(img):
        img = img / 2 + 0.5  # unnormalize
        npimg = img.numpy()
        plt.imshow(np.transpose(npimg, (1, 2, 0)))
        plt.show()

    running_loss = 0
    for epoch in range(1):
        for i, data in enumerate(trainloader):
            inputs, labels = data
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()

            # forward, backward, optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print stats
            running_loss += loss.item()
            steps = 2000
            if i % steps == 0 and i > 0:  # print every 2000 minibatches
                print('[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss / steps))
                running_loss = 0.0

    print('finished training')

    PATH = 'E:\\Models\\pytorch_fun\\poggers.pt'
    torch.save(net.state_dict(), PATH)

    dataiter = iter(testloader)
    images, labels = dataiter.next()

    # print images
    imshow(torchvision.utils.make_grid(images))
    print('ground truth: ', ' '.join('5%s' % classes[labels[j]] for j in range(4)))

if __name__ == '__main__':
    main()