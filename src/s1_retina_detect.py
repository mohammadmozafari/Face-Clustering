import cv2
import torch
import argparse
import numpy as np
import matplotlib.pyplot as plt
from detection import RetinaFace
from utils.datasets import ImageDataset
from torch.utils.data import DataLoader
from detection.data import cfg_mnet, cfg_re50
from detection.utils.load_utils import load_model
from detection.utils.nms.py_cpu_nms import py_cpu_nms
from detection.layers.functions.prior_box import PriorBox
from detection.utils.box_utils import decode, decode_landm

def main(args):
    cfg = None
    if args.network == "mobile0.25":
        cfg = cfg_mnet
    elif args.network == "resnet50":
        cfg = cfg_re50

    device = None
    if args.device == 'cpu':
        device = torch.device('cpu')
    elif args.device == 'gpu':
        device = torch.device('cuda:0')

    rf = RetinaFace(cfg=cfg, phase='test')
    rf = load_model(rf, args.trained_model, (args.device == 'cpu'))
    rf.eval()
    rf = rf.to(device)

    ids = ImageDataset('./data/paths_1_2_.csv', (540, 540))
    ldr = DataLoader(ids, batch_size=1, shuffle=False, num_workers=1)
    for imgs, path, h, w in ldr:

        print(path)

        imgs = imgs.type(torch.FloatTensor)
        imgs = imgs.permute((0, 3, 1, 2))
        imgs = imgs.to(device)
        print(imgs.shape)

        loc, conf, landms = rf(imgs)

        priorbox = PriorBox(cfg, image_size=(540, 540))
        priors = priorbox.forward()
        priors = priors.to(device)
        prior_data = priors.data
        boxes = decode(loc.data.squeeze(0), prior_data, cfg['variance'])
        boxes = boxes.cpu().numpy()
        print(boxes)
        # boxes = boxes * scale / resize
        scores = conf.squeeze(0).data.cpu().numpy()[:, 1]
        landms = decode_landm(landms.data.squeeze(0),
                              prior_data, cfg['variance'])
        # scale1 = torch.Tensor([img.shape[3], img.shape[2], img.shape[3], img.shape[2],
                            #    img.shape[3], img.shape[2], img.shape[3], img.shape[2],
                            #    img.shape[3], img.shape[2]])
        # scale1 = scale1.to(device)
        # landms = landms * scale1 / resize
        landms = landms.cpu().numpy()

        # ignore low scores
        inds = np.where(scores > args.confidence_threshold)[0]
        boxes = boxes[inds]
        landms = landms[inds]
        scores = scores[inds]

        # keep top-K before NMS
        order = scores.argsort()[::-1]
        # order = scores.argsort()[::-1][:args.top_k]
        boxes = boxes[order]
        landms = landms[order]
        scores = scores[order]

        print(scores)

        # do NMS
        dets = np.hstack((boxes, scores[:, np.newaxis])).astype(
            np.float32, copy=False)
        keep = py_cpu_nms(dets, args.nms_threshold)
        print(keep)
        # keep = nms(dets, args.nms_threshold,force_cpu=args.cpu)
        dets = dets[keep, :]
        landms = landms[keep]

        print(dets)

        # keep top-K faster NMS
        # dets = dets[:args.keep_top_k, :]
        # landms = landms[:args.keep_top_k, :]

        dets = np.concatenate((dets, landms), axis=1)


        break


    # img = cv2.imread('./data/diff-ratios/jp (2).jpg', cv2.COLOR_BGR2RGB)
    # img = img.astype(np.float32)
    # img = img.transpose(2, 0, 1)
    # img = torch.from_numpy(img).unsqueeze(0)
    # img = img.to(device)

    # loc, conf, landms = rf(img)

    # for i in range(loc.shape[1]):
    #     print(loc[0, i, :])
    #     print(conf[0, i, :])
    #     print()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Detect faces using RetinaFace')
    parser.add_argument('--network', help='Network architecture')
    parser.add_argument('--trained_model', help='Trained state_dict file path to open')
    parser.add_argument('--device', help='cpu or gpu')
    parser.add_argument('--confidence_threshold', default=0.99, type=float, help='confidence_threshold')
    parser.add_argument('--nms_threshold', default=0.4, type=float, help='nms_threshold')
    args = parser.parse_args()

    main(args)
