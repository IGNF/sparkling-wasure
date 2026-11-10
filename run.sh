#!/bin/bash
source ./algo-env.sh

INPUT_DIR=${PWD}/inputs/
PARAMS=${INPUT_DIR}/params.xml
OUTPUT_DIR=${PWD}/outputs/
CMD="${APP_DIR}/run_workflow.sh --input_dir ${INPUT_DIR} --output_dir ${OUTPUT_DIR} --params ${PARAMS}"
run_cmd_container

