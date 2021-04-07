import os
import sys
import time
import torch
import numpy as np
from torch.utils.data import DataLoader
from src.utils.datasets import FaceDataset
from src.utils.inception_resnet_v1 import InceptionResnetV1

root_folder = '.\\results\\lfw_bboxes_540x648_1face' if len(sys.argv) <= 1 else sys.argv[1]
num_images = 13233 if len(sys.argv) <= 2 else int(sys.argv[2])
device = torch.device('cuda:0')

bounding_box_files = os.listdir(root_folder)
bounding_box_files = [os.path.join(root_folder, bbfile) for bbfile in bounding_box_files]

at = 0
embeddings = np.zeros((num_images, 512))
net = InceptionResnetV1(pretrained='vggface2', device=device)
tick = time.time()
begin = time.time()
for bounding_box_file in bounding_box_files:
    ds = FaceDataset(bounding_box_file)
    dl = DataLoader(ds, shuffle=False, batch_size=64)
    for faces in dl:
        faces = faces.to(device)
        result = net(faces)
        bsize = result.shape[0]
        embeddings[at:at+bsize, :]
        at += bsize
        tock = time.time()
        print('Processed {}/{} faces. ({:.2f} faces per second)'.format(at, num_images, bsize/(tock-tick))) 
        tick = time.time()
end = time.time()
print()
print('Average speed: {:.2f} faces per second'.format(num_images/(end-begin)))

# if more than 100,000 give error (It cannot evaluate)

