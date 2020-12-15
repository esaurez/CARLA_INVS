#!/usr/bin/env python3
import os
import subprocess as sp
import torch
from averaging import average_weights
import pdb
import copy
import time
from sys import argv

if int(argv[1]) <= 9:
    sp.run(['bash', '-c', "cd tools; python3 train.py --cfg_file cfgs/pretrain11.yaml --batch_size 1 --workers 0 --epochs 1"])
    sp.run(['bash', '-c', "cd tools; python3 train.py --cfg_file cfgs/pretrain21.yaml --batch_size 1 --workers 0 --epochs 1"])
    sp.run(['bash', '-c', "cd tools; python3 train.py --cfg_file cfgs/pretrain31.yaml --batch_size 1 --workers 0 --epochs 1"])
    pass


if int(argv[1]) >= 10:
    sp.run(['bash', '-c', 'cd tools; python3 train.py --cfg_file cfgs/pretrain12.yaml --batch_size 1 --workers 0 --epochs 5 --pretrained_model ../model/model_avg.pth']) #return model_0
    sp.run(['bash', '-c', 'cd tools; python3 train.py --cfg_file cfgs/pretrain22.yaml --batch_size 1 --workers 0 --epochs 5 --pretrained_model ../model/model_avg.pth']) #return model_1
    sp.run(['bash', '-c', 'cd tools; python3 train.py --cfg_file cfgs/pretrain32.yaml --batch_size 1 --workers 0 --epochs 5 --pretrained_model ../model/model_avg.pth']) #return model_1
    pass


# if int(argv[1]) == 2:
#     sp.run(['bash', '-c', 'cd tools; python3 train.py --cfg_file cfgs/pretrain13.yaml --batch_size 1 --workers 0 --epochs 10 --pretrained_model ../model/model_avg.pth']) #return model_0
#     sp.run(['bash', '-c', 'cd tools; python3 train.py --cfg_file cfgs/pretrain23.yaml --batch_size 1 --workers 0 --epochs 10 --pretrained_model ../model/model_avg.pth']) #return model_1
#     sp.run(['bash', '-c', 'cd tools; python3 train.py --cfg_file cfgs/pretrain33.yaml --batch_size 1 --workers 0 --epochs 10 --pretrained_model ../model/model_avg.pth']) #return model_1
#     pass



model_dict0 = torch.load('./model/checkpoint_epoch_0.pth'); params0 = model_dict0['model_state']
model_dict1 = torch.load('./model/checkpoint_epoch_1.pth'); params1 = model_dict1['model_state']
model_dict2 = torch.load('./model/checkpoint_epoch_2.pth'); params2 = model_dict2['model_state']
# pdb.set_trace()

w_locals = []
w_locals.append(params0)
w_locals.append(params1)
w_locals.append(params2)
params_avg = average_weights(w_locals)

del(params0)
del(params1)
del(params2)
os.remove('model/checkpoint_epoch_0.pth')
os.remove('model/checkpoint_epoch_1.pth')
os.remove('model/checkpoint_epoch_2.pth')

torch.save({'model_state':params_avg,
            'optimizer_state': model_dict0['optimizer_state'],
            # 'epoch': model_dict0['epoch'],
            'accumulated_iter': model_dict0['accumulated_iter']
            },'model/model_avg.pth')

del(params_avg)


print('---------------------------------Average---------------------------------------------- %r.'%argv[1])
