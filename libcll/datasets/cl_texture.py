import torch
from torch.utils.data import Dataset
import torchvision
import torchvision.transforms as transforms
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.preprocessing import LabelEncoder
from libcll.datasets.cl_base_dataset import CLBaseDataset
from libcll.datasets.utils import get_transition_matrix


class CLTexture(CLBaseDataset):
    """

    Parameters
    ----------
    root : str
        path to store dataset file.

    train : bool
        training set if True, else testing set.

    transform : callable, optional
        a function/transform that takes in a PIL image and returns a transformed version.

    target_transform : callable, optional
        a function/transform that takes in the target and transforms it.

    download : bool
        if true, downloads the dataset from the internet and puts it in root directory. If dataset is already downloaded, it is not downloaded again.

    Attributes
    ----------
    data : Tensor
        the feature of sample set.

    targets : Tensor
        the complementary labels for corresponding sample.

    true_targets : Tensor
        the ground-truth labels for corresponding sample.

    num_classes : int
        the number of classes.

    input_dim : int
        the feature space after data compressed into a 1D dimension.

    """

    def __init__(
        self,
        root="./data/texture",
        train=True,
        transform=None,
        target_transform=None,
        download=True,
    ):
        data = fetch_openml(data_id=40499)
        self.data = data.data.to_numpy()
        self.targets = LabelEncoder().fit_transform(data.target)

        self.root = root
        self.transform = transform
        self.target_transform = target_transform
        self.val_split = 0.9
        self.num_classes = 11
        self.input_dim = 40
        rng = np.random.default_rng(seed=1126)
        idx = rng.permutation(len(self.targets))

        if train:
            self.data = torch.Tensor(self.data[idx[: int(self.val_split * len(idx))]])
            self.targets = torch.Tensor(
                self.targets[idx[: int(self.val_split * len(idx))]]
            )
        else:
            self.data = torch.Tensor(self.data[idx[int(self.val_split * len(idx)) :]])
            self.targets = torch.Tensor(
                self.targets[idx[int(self.val_split * len(idx)) :]]
            )
    
    def build_dataset(self, train=True, num_cl=0, transition_matrix=None, noise=None, seed=1126):
        if train:
            dataset = self(train=True)
            Q = get_transition_matrix(transition_matrix, dataset.num_classes, noise, seed)
            dataset.gen_complementary_target(num_cl, Q)
        else:
            dataset = self(train=False)
        return dataset
