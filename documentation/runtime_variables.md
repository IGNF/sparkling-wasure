# Runtime variables

List of the variables that can be set at runtime by the different actors of the project, with their description and the expected values.

- TECHNICIAN: 8 parameters
- PROJECT MANAGER: 35 parameters
- INFRASTRUCTURE MANAGER: 26 parameters

## Technician

Operator in charge of the operational execution of the pipeline via the interface or the provided scripts, with limited intervention to guided actions (launch, monitoring, results retrieval).

### run_examples.sh

| Variable | Type | Default | Description |
|----------|---------|-------------|-------------|
| INPUT_DIR | str | | Path to the directory containing .las/.laz point cloud files. |
| OUTPUT_DIR | str | | Path to the directory where all outputs will be written. |
| PARAMS | str | void.xml | Path to the XML metadata file containing algorithm parameters. If not provided, a void file is used and Scala defaults apply. |
| --debug | CLI flag | (off) | Enables interactive Spark shell mode instead of batch execution. |

### run_workflow.sh

| Variable | Type | Default | Description |
|----------|---------|-------------|-------------|
| DO_COLORIZE | bool | TRUE | If TRUE, runs the colorization step to add RGB/IR colors to the 3D mesh tiles. |
| DO_LOD | bool | TRUE | If TRUE, generates 3D Tiles with multiple Levels of Detail from the output mesh. |

### C++ exe parameters (services/wasure/include/wasure_params.hpp)

| Variable | Type | Default | Description |
|----------|---------|-------------|-------------|
| verbose | int | 0 | Verbose output level. Set to 1 to enable detailed console output during C++ execution. |
| dump_ply | bool | false | If true, writes intermediate PLY mesh files to disk for visual inspection. |


## Project Manager

Responsible for the framing and functional configuration of processing, defining the technical configurations and execution scenarios to be applied by technicians according to business objectives.

### services/wasure/workflow/workflow_preprocess.scala
DEFAULT VALUES IN THE SCALA FILE, CAN BE OVERRIDDEN BY THE XML FILE.

| Variable | Type | Default | Description |
|----------|---------|-------------|-------------|
| dim | int | 3 | Dimensionality of the geometric kernel (3 for 3D point clouds). Must match `DDT_TRAITS` used at build time. |
| max_ppt | int | 500000 | Maximum number of points per tile. Decrease if memory issues occur during processing. |
| bbox | str | "" | Bounding box filter (`xmin x xmax : ymin x ymax : zmin x zmax`). If empty, computed automatically from input data. Points outside are ignored. |
| algo_seed | int | (random) | Random seed for algorithm reproducibility. A random value is generated if not specified. |
| mode | int | 1 | Wasure processing mode. Controls the surface reconstruction pipeline variant. |
| pscale | float | 0.05 | Accuracy of the reconstruction. Lower values give higher precision but increase computation time. |
| nb_samples | float | 40 | Number of ray samples for the integral computation. Higher values improve accuracy at the cost of speed. |
| ndtree_depth | int | -1 | Depth of the octree spatial subdivision. If -1, auto-calculated from `log(total_points / max_ppt) / log(3)`. |
| rat_ray_sample | float | 0 | Ray sampling ratio. Controls the proportion of rays used during surface reconstruction. |
| min_ppt | int | 50 | Minimum number of points per tile. Tiles with fewer points are discarded. |
| algo_opt | str | seg_lagrange_weight | Name of the optimization algorithm used in the distributed graph-cut. |
| dst_scale | float | -1 | DST (Dempster-Shafer Theory) scaling factor. If -1, computed automatically. |
| lambda | float | 2 | Regularization weight for the graph-cut smoothing term. Higher values produce smoother surfaces. |
| max_opt_it | int | 50 | Maximum number of iterations during the distributed graph-cut optimization. |
| do_stats | bool | false | If true, computes and outputs statistics about the reconstruction process. |
| coef_mult | float | 5 | Coefficient multiplier applied to the data term in the energy function. |
| regexp_filter | str | "" | Regex pattern to filter input filenames. Only files matching the pattern are processed. If empty, all .las/.laz files are used. |

### datas/../wasure_metadata.xml
IN THIS XML FILE, THE PARAMETERS IN WORKFLOW_PREPROCESS.SCALA CAN BE OVERRIDDEN BY THE USER, BUT THE DEFAULT VALUES ARE THE ONES IN THE SCALA FILE.

### services/wasure/workflow/workflow_wasure.scala
DEFAULT VALUES IN THE SCALA FILE, CAN BE OVERRIDDEN BY THE XML FILE (except dump_mode).

| Variable | Type | Default | Description |
|----------|---------|-------------|-------------|
| do_profile | bool | false | If true, enables execution profiling (not used yet in current version). |
| plot_lvl | int | 1 | Detail level of PLY output meshes. Higher values produce more detailed intermediate outputs. |
| dump_debug | bool | false | If true, writes debug data (intermediate triangulations, labels) to disk. |
| datatype | str | "" | Data type identifier. Set automatically to "files" by the preprocessing step. |
| stats_mod_it | int | max_opt_it / 2 | Iteration interval at which statistics are computed (only effective when do_stats is true). |
| dump_mode | str | NONE | HARDCODED (not overridable by XML). Force-set to NONE regardless of XML value. |

### C++ compile-time constants (services/wasure/include/input_params.hpp)
VALUES ARE `#define` CONSTANTS. CHANGING THEM REQUIRES RECOMPILATION.

| Variable | Type | Default | Description |
|----------|---------|-------------|-------------|
| ANGLE_SCALE | float | 0.003 | Angular scale for ray casting in aerial LiDAR mode. Use 0.005 for ground-based, 0.02 for 2D. |
| GSPS_CONST | float | 0.05 | Geometric scale used in the point simplification step. |
| NUM_ITER_TESSEL | int | 10 | Number of iterations for the tessellation refinement step. |
| DIM_SIZE_NB | int | 50 | Number of neighbors used in KNN queries for dimensionality estimation. |
| GLOB_SMOOTH | int | 1 | Global smoothing parameter applied to the triangulation. |
| MAX_TRIANGLE_SIZE | int | 500 | Maximum allowed triangle size (in point cloud units). Triangles exceeding this are discarded. |


### services/colorize/colorize.sh
FLAGS PASSED TO THE IGN PDAL COLORIZATION TOOL.

| Variable | Type | Default | Description |
|----------|---------|-------------|-------------|
| --rvb | flag | enabled | Enables RGB colorization from orthophotos via WMS. |
| --ir | flag | enabled | Enables infrared colorization from IRC orthophotos via WMS. |
| --check-images | flag | enabled | Validates that downloaded WMS images are not blank before applying colors. |


### services/mesh23dtile/mesh23dtile.py
HARDCODED CONSTANTS FOR 3D TILES LOD GENERATION.

| Variable | Type | Default | Description |
|----------|---------|-------------|-------------|
| target_face_num | int | 100000 | Target number of faces after mesh decimation per tile. Controls output mesh density. |
| max_depth | int | 5 | Maximum octree depth for the LOD hierarchy. Determines the number of detail levels. |
| geom_error | list[int] | [20,10,5,2,1,0] | Geometric error threshold per LOD level (from coarsest to finest). Controls when each level is rendered. |



## Infrastructure Manager

Technical expert responsible for the execution environment (servers, cluster, containers, performance, security), in charge of installation, optimization and maintenance of the platform.

### algo-env.sh

| Variable | Type | Default | Description |
|----------|---------|-------------|-------------|
| NAME_IMG_BASE | str | ddt_img_base_devel | Name of the Docker image used for pipeline execution. |
| CONTAINER_NAME_SHELL | str | ddt_container_shell | Name of the Docker container created for interactive shell access. |
| DO_USE_LOCAL_BUILD | bool | FALSE | If TRUE, runs using local build directory instead of Docker image. APP_DIR is set to `${PWD}`. |
| NUM_PROCESS | int | 4 | Number of parallel processes for colorization and LOD creation steps. |
| CURRENT_PLATEFORM | str | local | Execution mode: `local` (standalone), `master` (Spark master node), `slave` (Spark worker node). |
| MASTER_IP_SPARK | str | localhost | IP address of the Spark master node. Set to actual IP in cluster mode. |
| SPARK_EXECUTOR_MEMORY | str | 16G | Memory allocated to each Spark executor for running distributed tasks. |
| SPARK_DRIVER_MEMORY | str | 16G | Memory allocated to the Spark driver for job coordination and scheduling. |
| SPARK_WORKER_MEMORY | str | 16G | Total memory available for a Spark worker node hosting executors. |

### services/wasure/workflow/workflow_preprocess.scala
DEFAULT VALUES IN THE SCALA FILE, CAN BE OVERRIDDEN BY THE XML FILE.

| Variable | Type | Default | Description |
|----------|---------|-------------|-------------|
| ddt_kernel | str | "build-spark-Release-" + dim | Name of the C++ kernel build folder inside the build directory. Must match the compilation output. |
| StorageLevel | str | DISK_ONLY | Spark RDD persistence level for main data. Options: MEMORY_ONLY, MEMORY_AND_DISK, DISK_ONLY. |
| StorageLevelLoop | str | DISK_ONLY | Spark RDD persistence level for loop-scoped data. Options: MEMORY_ONLY, MEMORY_AND_DISK, DISK_ONLY. |
| spark_core_max | int | Spark defaultParallelism | Maximum number of Spark cores used. Defaults to the cluster's total available parallelism. |


### services/wasure/workflow/workflow_wasure.scala
HARDCODED VALUES IN THE SCALA FILE, NOT OVERRIDDEN BY THE XML FILE.

| Variable | Type | Default | Description |
|----------|---------|-------------|-------------|
| do_checkpoint | bool | false | If true, enables Spark checkpointing to allow RDD recovery after failures. |
| checkpoint_dir_string | str | "/home/laurent/shared_spark/checkpoint/" | Directory path for Spark checkpoint storage. Must be accessible by all workers. |
| rep_value | int | 100 | Number of Spark partitions used when repartitioning RDDs. |

### src/scala/run_algo_spark.sh
SPARK RUNTIME CONFIGURATION PASSED VIA `--conf` FLAGS. HARDCODED IN THE SCRIPT.

| Variable | Type | Default | Description |
|----------|---------|-------------|-------------|
| spark.rdd.compress | bool | true | Enables compression of serialized RDD partitions to reduce memory/disk usage. |
| spark.eventLog.enabled | bool | true | Enables Spark event logging for monitoring via the Spark History Server. |
| spark.memory.fraction | float | 0.2 | Fraction of JVM heap used for Spark execution and storage (rest is for user data structures). |
| spark.memory.storageFraction | float | 0.8 | Fraction of `spark.memory.fraction` reserved for cached RDD storage vs. execution. |
| spark.worker.cleanup.enabled | bool | true | Enables periodic cleanup of worker application directories. |
| spark.worker.cleanup.interval | int | 350 | Interval in seconds between worker directory cleanups. |
| spark.memory.offHeap.enabled | bool | true | Enables off-heap memory allocation outside the JVM heap. |
| spark.memory.offHeap.size | str | 10g | Amount of off-heap memory available per executor. |
| spark.network.timeout | int | 10000000 | Network timeout in milliseconds for Spark RPCs and shuffles. |
| spark.serializer | str | KryoSerializer | Serializer used for Spark shuffles and RDD serialization. Kryo is faster than Java default. |
