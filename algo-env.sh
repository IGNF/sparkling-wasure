## Docker 
export NAME_IMG_BASE=ddt_img_base_devel
export CONTAINER_NAME_SHELL="ddt_container_shell"
export CONTAINER_NAME_COMPILE="ddt_container_compile"
export DO_USE_LOCAL_BUILD="TRUE"
export DDT_MAIN_DIR_DOCKER=${DDT_MAIN_DIR} ## Used when called inside docker


if [[ ${DO_USE_LOCAL_BUILD} == "TRUE" ]]; then
    export APP_DIR="${PWD}"
    export MOUNT_LOCAL=" -v ${APP_DIR}/:${APP_DIR} "
else
    export APP_DIR="/app/wasure/"
fi

function run_cmd_container
{

    OUTPUT_ROOT=$(dirname ${OUTPUT_DIR})/
    CMD_DOCKER="docker run  \
       -u 0 \
       -v ${INPUT_DIR}:${INPUT_DIR} -v ${OUTPUT_ROOT}:${OUTPUT_ROOT} ${MOUNT_LOCAL} \
       --rm \
       -it \
       -e NAME_IMG_BASE=${NAME_IMG_BASE} -e DDT_MAIN_DIR_DOCKER=${DDT_MAIN_DIR_DOCKER} \
       -e CONTAINER_NAME_SHELL=${CONTAINER_NAME_SHELL} -e CONTAINER_NAME_COMPILE=${CONTAINER_NAME_COMPILE} \
       -e NUM_PROCESS=${NUM_PROCESS} \
       ${NAME_IMG_BASE} /bin/bash -c \"${CMD}\""
    eval ${CMD_DOCKER}
}
