import cv2
import torch
import argparse
import numpy as np
from detection import RetinaFace
from detection.data import cfg_mnet, cfg_re50
from detection.utils.load_utils import load_model

def main(args):
    cfg = None
    if args.network == "mobile0.25":
        cfg = cfg_mnet
    elif args.network == "resnet50":
        cfg = cfg_re50

    rf = RetinaFace(cfg=cfg, phase='test')
    rf = load_model(rf, args.trained_model, (args.device == 'cpu'))
    rf.eval()
    device = torch.device('cpu' if args.device == 'cpu' else 'cuda:0')
    rf = rf.to(device)

    img = cv2.imread('./data/diff-ratios/jp (2).jpg', cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32)
    img = img.transpose(2, 0, 1)
    img = torch.from_numpy(img).unsqueeze(0)
    img = img.to(device)

    loc, conf, landms = rf(img)

    for i in range(loc.shape[1]):
        print(loc[0, i, :])
        print(conf[0, i, :])
        print()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Detect faces using RetinaFace')
    parser.add_argument('--network', help='Network architecture')
    parser.add_argument('--trained_model', help='Trained state_dict file path to open')
    parser.add_argument('--device', help='cpu or gpu')
    args = parser.parse_args()

    main(args)
