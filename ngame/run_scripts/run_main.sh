#!/bin/bash
# $1 GPU Device ID
# $2 Model Type (SiameseXML etc.)
# $3 Dataset
# $4 version
# $5 seed
# eg. ./run_main.sh 0 NGAME LF-AmazonTitles-131K 0 22

# export CUDA_VISIBLE_DEVICES=1
model_type=$2
dataset=$3
version=$4
seed=$5

work_dir=$(cd ../../ && pwd)

current_working_dir=$(pwd)
CUDA_VISIBLE_DEVICES=1 python -W ignore ../runner.py "${model_type}" "${work_dir}" ${version} "../../ngame/configs/NGAME/ddc.json" "${seed}"