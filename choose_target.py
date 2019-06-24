
#数据清洗，用于挑选出包含具体目标的图形
import os
import argparse
import numpy as np
import shutil

find_name = "bicycle"
# 图片图像来源，其中存储的是图片的地址,图片标识信息也有规范（可以直接根据图片信息转为标识信息）
img_from = "data/coco/trainvalno5k.txt"
names_path = "data/coco.names"  # class name存储了可以图片的类别信息
if __name__ == "__main__":
    name = dict()
    count = 0
    with open(names_path, 'r') as fp:
        lines = fp.readlines()
    for line in lines:
        line = line.strip()
        if line == '' or line.startswith('#'):
            continue
        name[line] = count
        count += 1
    # find truck belong to what
    out = name[find_name]
    print(out)
    # find all label and images_path
    with open(img_from, 'r') as file:
        img_files_paths = file.readlines()
    count = 1
    total = len(img_files_paths)
    os.makedirs(find_name, exist_ok=True)
    os.makedirs(find_name + "/img", exist_ok=True)
    os.makedirs(find_name + "/label", exist_ok=True)
    new_file = find_name + "/path_instore"
    if not os.path.exists(new_file):
        print("new file created: " + new_file)
    f = open(new_file, "a+")
    for img_file_path in img_files_paths:
        count += 1
        if(count % 100 is 0):
            print("----------%f-----------" % ((count / total)*100))
        # 此为有图片地址转换为标识地址的内容，标识地址必须严格按照以下规则进行更改
        label_file_path = img_file_path.replace("images", "labels").replace(
            ".png", ".txt").replace(".jpg", ".txt")
        label_file_path = label_file_path.rstrip()  # 清楚\n标识
        if(os.path.exists(label_file_path)):
            #label的第一项代表class
            boxes = np.loadtxt(label_file_path).reshape(-1, 5)
            target_num = boxes.shape[0]
            for i in range(target_num):
                class_index = boxes[i, 0]
                if int(class_index) == int(out):  # have the same label
                    # os.path.basename(img_file_path)
                    img_folder_path = os.path.join(
                        os.getcwd(), find_name, "img")
                    # + os.path.basename(label_file_path)
                    label_folder_path = os.path.join(
                        os.getcwd(), find_name, "label")
                    shutil.copy(img_file_path.rstrip(), img_folder_path)
                    shutil.copy(label_file_path.rstrip(), label_folder_path)
                    write_data = os.path.join(
                        os.getcwd(), find_name, os.path.basename(img_file_path))
                    f.write(write_data)
                    break

        else:
            print("path wrong!")