# Building variables

List of the variables that can be set at build time, with their description and the expected values.
The build pipeline is started with `./src/docker/docker_interface.sh build` (Docker image creation) or `./src/docker/docker_interface.sh compile` (C++ and Scala compilation).

All building variables belong to the **Infrastructure Manager**. The Technician and Project Manager do not intervene in the build process.

The infrastructure manager is the technical expert responsible for the execution environment (servers, cluster, containers, performance, security), in charge of installation, optimization and maintenance of the platform.

- Number of parameters: 10 + library versions (Dockerfile and environment.yml files)


## algo-env.sh
USED BY BOTH `build` AND `compile` FUNCTIONS (sourced at the beginning of each).

| Variable | Type | Default | Description |
|----------|---------|-------------|-------------|
| NAME_IMG_BASE | str | ddt_img_base_devel | Name of the Docker image to build and compile inside. Determines which Dockerfile is used. |
| CONTAINER_NAME_COMPILE | str | ddt_container_compile | Name of the Docker container used during compilation. |

## src/docker/docker_interface.sh — compile function
CLI FLAGS PASSED TO `./src/docker/docker_interface.sh compile [-j NB] [-t TRAITS] [-d] [-f]`.

| Variable | Type | Default | Description |
|----------|---------|-------------|-------------|
| COMPILE_MODE | str | Release | Compile mode. Default is `Release`; pass the `-d` flag to switch to `Debug`. |
| NB_PROC | int | 4 | Number of parallel compilation processes. Passed via `-j. |
| DDT_TRAITS | str | 3 | Dimensionality of the geometric kernel to compile. Values: `2` (2D), `3` (3D), `D2` (dD with d=2), `D3` (dD with d=3). Determines which C++ traits are activated via `#define`. Must match the `dim` parameter used at runtime. |
| DO_FORMAT | flag | (off) | Pass `-f` to run the `astyle` code formatter after compilation. |

## cmake_params.txt
CMAKE OPTIONS INCLUDED BY THE ROOT CMakeLists.txt. THESE ARE COMPILE-TIME TOGGLES.

| Variable | Type | Default | Description |
|----------|---------|-------------|-------------|
| DDT_DEBUG | bool | OFF | Enable DDT debug output. |
| DDT_USE_THREADS | bool | ON | Enable DDT multithreading. |
| DDT_TEST | bool | OFF | Enable DDT unit tests. |
| DDT_USE_HDFS | bool | OFF | Enable HDFS support. |

