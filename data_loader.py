# 定义数据集
from PIL import Image
import torch
from torch.utils.data import Dataset
from torchvision import transforms as T
from torch.utils import data


class ComDataset(Dataset):
    def __init__(self, clean_path, com_path, list_path, transform, mode, selected_attrs):
        self.path1 = clean_path 
        self.path2 = com_path
        self.transform = transform  
        self.list_path = list_path
        self.selected_attrs = selected_attrs
        self.mode = mode
        self.train_dataset = []
        self.test_dataset = []
        self.attr2idx = {}
        self.idx2attr = {}
        self.preprocess()

        if self.mode == 'train':
            self.num_images = len(self.train_dataset)
        else:
            self.num_images = len(self.test_dataset)

    def __len__(self):
        return self.num_images

    def preprocess(self):
        """Preprocess the CelebA attribute file."""
        lines = [line.rstrip() for line in open(self.list_path, 'r')]
        all_attr_names = lines[1].split()
        for i, attr_name in enumerate(all_attr_names):
            self.attr2idx[attr_name] = i
            self.idx2attr[i] = attr_name
        lines = lines[2:]
        for i, line in enumerate(lines):
            split = line.split()
            filename = split[0]
            values = split[1:]

            label = []
            for attr_name in self.selected_attrs:
                idx = self.attr2idx[attr_name]
                label.append(values[idx] == '1')

            if i < 100:
                self.test_dataset.append([filename, label])
                self.train_dataset.append([filename, label])
            else:
                self.train_dataset.append([filename, label])
        print('Finished preprocessing the dataset...')

    def __getitem__(self, index):
        osn = None
        if 0 <= index < 7500:
            osn = "facebook/"
        elif 7500 <= index < 15000:
            osn = "twitter/"
        elif 15000 <= index < 22500:
            osn = "weibo/"
        else:
            osn = "wechat/"
        dataset = self.train_dataset if self.mode == 'train' else self.test_dataset
        filename, label = dataset[index]
        filepath1 = self.path1 + filename
        filepath2 = self.path2 + osn + filename

        seed = torch.random.seed()
        img1 = Image.open(filepath1)
        torch.random.manual_seed(seed)
        img1 = self.transform(img1)
        img2 = Image.open(filepath2)
        torch.random.manual_seed(seed)
        img2 = self.transform(img2)
        
        return img1,img2,torch.FloatTensor(label)


def get_loader(clean_path, com_path, list_path,image_size=256, 
               batch_size=16, num_workers=1, shuffle=False, mode="train", selected_attrs=[]):
    """Build and return a data loader."""
    transform = []
    if mode == 'train':
        transform.append(T.RandomHorizontalFlip())
    transform.append(T.Resize([image_size,image_size]))
    transform.append(T.ToTensor())
    transform.append(T.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)))
    transform = T.Compose(transform)
    dataset = ComDataset(clean_path,com_path, list_path, transform, mode, selected_attrs)
    data_loader = data.DataLoader(dataset,batch_size=batch_size,shuffle=shuffle,num_workers=num_workers)
    return data_loader


