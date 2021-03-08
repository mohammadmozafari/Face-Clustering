import torch
import numpy as np
from sklearn.cluster import DBSCAN
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
batch_size = 2
dl = DataLoader(face_ds, batch_size=batch_size, num_workers=0)

net = InceptionResnetV1('vggface2').eval()
embeddings = np.zeros((len(face_ds), 512))
for i, x in enumerate(dl):
    y = None
    with torch.no_grad():
        y = net(x)
    embeddings[i*batch_size:i*batch_size+x.shape[0], :] = y

alg = DBSCAN(eps=1.1, min_samples=2)
labels = alg.fit(embeddings).labels_
print(labels)