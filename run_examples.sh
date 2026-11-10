#!/bin/bash
source ./algo-env.sh

# Example 1
INPUT_DIR=${PWD}/datas/lidar_hd_crop_1/
PARAMS=${INPUT_DIR}/wasure_metadata.xml
OUTPUT_DIR=${PWD}/output_example/lidar_hd_crop_1
CMD="${APP_DIR}/run_workflow.sh --input_dir ${INPUT_DIR} --output_dir ${OUTPUT_DIR} --params ${PARAMS}"
run_cmd_container

# Example 2
INPUT_DIR=${PWD}/datas/lidar_hd_crop_2/
PARAMS=${INPUT_DIR}/wasure_metadata.xml
OUTPUT_DIR=${PWD}/output_example/lidar_hd_crop_2
CMD="${APP_DIR}/run_workflow.sh --input_dir ${INPUT_DIR} --output_dir ${OUTPUT_DIR} --params ${PARAMS}"
run_cmd_container

# Example 2b
## the same dataset with only one tile in order to show the approximation
PARAMS=${INPUT_DIR}/wasure_metadata_v2.xml
OUTPUT_DIR=${PWD}/output_example/lidar_hd_crop_2_v2
CMD="${APP_DIR}/run_workflow.sh --input_dir ${INPUT_DIR} --output_dir ${OUTPUT_DIR} --params ${PARAMS}"
#run_cmd_container

# Example 3
INPUT_DIR=${PWD}/datas/lidar_hd_crop_w/
PARAMS=${INPUT_DIR}/wasure_metadata.xml
OUTPUT_DIR=${PWD}/output_example/lidar_hd_crop_w
CMD="${APP_DIR}/run_workflow.sh --input_dir ${INPUT_DIR} --output_dir ${OUTPUT_DIR} --params ${PARAMS}"
run_cmd_container
