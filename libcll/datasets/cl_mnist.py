import torchvision
import torchvision.transforms as transforms
from PIL import Image
from libcll.datasets.cl_base_dataset import CLBaseDataset
from libcll.datasets.utils import get_transition_matrix


class CLMNIST(torchvision.datasets.MNIST, CLBaseDataset):
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
        root="./data/mnist",
        train=True,
        transform=transforms.ToTensor(),
        target_transform=None,
        download=True,
    ):
        super(CLMNIST, self).__init__(
            root, train, transform, target_transform, download
        )
        self.num_classes = 10
        self.input_dim = 1 * 28 * 28

    def __getitem__(self, index):
        img, target = self.data[index], self.targets[index]
        img = Image.fromarray(img.numpy(), mode="L")

        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            target = self.target_transform(target)

        return img, target

    @classmethod
    def build_dataset(self, dataset_name=None, train=True, num_cl=0, transition_matrix=None, noise=None, seed=1126):
        if train:
            dataset = self(train=True)
            Q = get_transition_matrix(transition_matrix, dataset.num_classes, noise, seed)
            dataset.gen_complementary_target(num_cl, Q)
        else:
            dataset = self(train=False)
        return dataset
