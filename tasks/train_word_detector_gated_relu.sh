#!/bin/bash
PYTHONPATH=$(pwd):$PYTHONPATH pipenv run python training/run_experiment.py --gpu=1 --save '{"dataset": "IamWordsDataset", "model": "LineDetectorModel", "network": "fcn_gated_relu", "train_args": {"batch_size": 12, "epochs": 40}, "dataset_args": {"image_dim": 512, "num_classes": 3} }'
