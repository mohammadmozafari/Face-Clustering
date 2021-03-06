import torch
import numpy as np
from utils.detection import Detection
from torch.utils.data import DataLoader
from utils.face_dataset import FaceDataset
from utils.utility_functions import get_images_paths
from utils.inception_resnet_v1 import InceptionResnetV1

# paths = get_images_paths('.\\data')
# d = Detection('./results/bounding_boxes.csv')
# faces = d.detect_faces(paths)
# print('Faces are detected')

face_ds = FaceDataset('./results/bounding_boxes.csv')
dl = DataLoader(face_ds, batch_size=5, num_workers=0)

net = InceptionResnetV1('vggface2')
embeddings = np.zeros((len(face_ds), 512))
for i, x in enumerate(dl):
    y = None
    with torch.no_grad():
        y = net(x)
    embeddings[i*5:i*5+x.shape[0], :] = y

print(np.linalg.norm((embeddings[0, :] - embeddings[8, :])))
# dist = np.sum(embeddings ** 2, axis=1).reshape(-1, 1) + np.sum(embeddings ** 2, axis=1).reshape(1, -1) - 2 * (embeddings @ embeddings.T)
# print(dist ** 0.5)
