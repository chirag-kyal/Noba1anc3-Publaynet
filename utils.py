import os
import random
from detectron2.structures import BoxMode
import cv2
from detectron2.utils.visualizer import Visualizer
from matplotlib import pyplot as plt

def get_textImg_dicts(images, img_dir):

    dataset_dicts = []
    cnt = 0
    for i, (_, image) in enumerate(images.items()):

        record = {}
        filename = os.path.join(img_dir, image["file_name"])
        if not os.path.exists(filename):
            cnt += 1
            continue
        record["file_name"] = filename
        print(filename)

        height, width = cv2.imread(filename).shape[:2]
        record["height"] = height
        record["width"] = width

        annos = image['annotations']
        objs = []
        for anno in annos:
            x = anno["bbox"][0]
            y = anno["bbox"][1]
            w = anno["bbox"][2]
            h = anno["bbox"][3]

            obj = {
                "bbox": [x, y, w, h],
                "bbox_mode": BoxMode.XYWH_ABS,
                "category_id": anno['category_id'] - 1,
                "iscrowd": 0
            }
            objs.append(obj)
        record["annotations"] = objs
        dataset_dicts.append(record)

    print('textImg dits lenght :', len(dataset_dicts))
    print('len of images :', len(images))
    print('miss imgs :', cnt)

    return dataset_dicts


def draw_textImg_dicts(dataset_dicts, smp_num, textImg_metadata):

    for d in random.sample(dataset_dicts, smp_num):
        print('visualize...')
        img = cv2.imread(d["file_name"])
        visualizer = Visualizer(img[:, :, ::-1], metadata=textImg_metadata, scale=0.5)
        vis = visualizer.draw_dataset_dict(d)
        img = vis.get_image()[:, :, ::-1]
        path = './output/images/' + d["file_name"].split('/')[3]
        cv2.imwrite(path, img)

    print('visualize finished')

def draw_predImg_dicts(dataset_dicts, smp_num, textImg_metadata, predictor):

    for d in random.sample(dataset_dicts, smp_num):
        img = cv2.imread(d["file_name"])
        outputs = predictor(img)
        print(outputs)
        visualizer = Visualizer(img[:, :, ::-1], metadata=textImg_metadata, scale=0.5)
        vis = visualizer.draw_instance_predictions(outputs['instances'].to('cpu'))
        img = vis.get_image()[:, :, ::-1]
        path = './output/images/' + d["file_name"].split('/')[3]
        cv2.imwrite(path, img)
