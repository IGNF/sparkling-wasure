# Library dependencies

Complete list of all libraries and dependencies used by the project, organized by installation source.


## src/docker/Dockerfile-base-Ubuntu-devel

### Base image

| Name | Version | Description |
|------|---------|-------------|
| ubuntu | 24.04 | Base OS for the Docker image. |

### General build tools (apt)

| Name | Version | Description |
|------|---------|-------------|
| cmake | system | Build system generator for C/C++ projects. |
| g++ | system | GNU C++ compiler. |
| build-essential | system | Meta-package: gcc, g++, make, dpkg-dev. |
| git | system | Version control system. |
| nano | system | Terminal text editor (for debugging inside container). |
| sudo | system | Execute commands as another user. |
| gdb | system | GNU debugger for C/C++. |
| wget | system | Command-line file downloader. |

### Boost (apt)

| Name | Version | Description |
|------|---------|-------------|
| libboost-all-dev | system | Complete Boost C++ library (system, filesystem, program_options used). |
| libboost-dev | system | Boost core headers (also pulled by libboost-all-dev). |

### LiDAR format dependencies (apt)

| Name | Version | Description |
|------|---------|-------------|
| xsdcxx | system | XML Schema to C++ data binding compiler. |
| libxerces-c-dev | system | XML parser library (C++) used by xsdcxx. |

### Eigen (apt)

| Name | Version | Description |
|------|---------|-------------|
| libeigen3-dev | system | C++ template library for linear algebra (matrices, vectors). |

### CGAL and geometry dependencies (apt)

| Name | Version | Description |
|------|---------|-------------|
| libcgal-dev | system | Computational Geometry Algorithms Library. Core geometric algorithms (Delaunay, mesh generation). |
| libcgal-qt5-dev | system | CGAL Qt5 visualization support. |
| libtbb-dev | system | Intel Threading Building Blocks. Used by CGAL for parallel algorithms. |
| libann-dev | system | Approximate Nearest Neighbors (system package, supplements bundled version). |
| libtinyxml-dev | system | Small XML parser for C++. |

### Numerical / graphics dependencies (apt)

| Name | Version | Description |
|------|---------|-------------|
| libpng-dev | system | PNG image format library. |
| liblapack-dev | system | Linear Algebra PACKage (Fortran routines). |
| libblas-dev | system | Basic Linear Algebra Subprograms. |
| ffmpeg | system | Multimedia framework for video/audio encoding. |
| openexr | system | High dynamic range image format tools. |
| libtiff-dev | system | TIFF image format library. |
| libopenexr-dev | system | OpenEXR development headers. |
| libsuitesparse-dev | system | Sparse matrix solvers (CHOLMOD, UMFPACK, etc.). |
| libgl1-mesa-dev | system | OpenGL development headers (Mesa). |
| libglu1-mesa-dev | system | OpenGL Utility Library (Mesa). |
| libxml2-dev | system | XML C parser (libxml2). |
| imagemagick | system | Image format conversion and manipulation tool. |

### Database (apt)

| Name | Version | Description |
|------|---------|-------------|
| libpq-dev | system | PostgreSQL client library (C headers). |

### Scala (apt)

| Name | Version | Description |
|------|---------|-------------|
| scala | system | Scala programming language runtime and compiler. |

### Java (apt)

| Name | Version | Description |
|------|---------|-------------|
| openjdk-8-jdk | 8 | Java Development Kit. Required by Spark, sbt, and Hadoop. |

### Spark / Hadoop / sbt (downloaded archives)

| Name | Version | URL | Description |
|------|---------|-----|-------------|
| Apache Spark | 3.5.0 | https://archive.apache.org/dist/spark/spark-3.5.0/ | Distributed computing framework. Pre-built with Hadoop 3 and Scala 2.13. |
| sbt | 1.0.0 | https://github.com/sbt/sbt/releases/download/v1.0.0/ | Scala Build Tool for compiling the Spark module. |
| Hadoop | 2.7.7 (source) | https://archive.apache.org/dist/hadoop/core/hadoop-2.7.7/ | Compiled from source to produce HDFS native libraries (libhdfs). |

### Python / Conda (downloaded)

| Name | Version | Description |
|------|---------|-------------|
| Miniconda3 | (not pinned) | Minimal Conda installer. Used to create isolated Python environments. |
| py3dtiles | v9.0.0 | 3D Tiles format library. Force-installed from https://gitlab.com/py3dtiles/py3dtiles over the conda version. |


## services/mesh23dtile/environment.yml (conda env: mesh23Dtile)

### Conda packages

| Name | Version | Channel | Description |
|------|---------|---------|-------------|
| python | 3.10 | defaults | Python interpreter. |
| pip | (not pinned) | defaults | Python package installer. |
| laspy | (not pinned) | defaults | Read/write LAS/LAZ LiDAR files in Python. |

### Pip packages

| Name | Version | Description |
|------|---------|-------------|
| pymeshlab | 2021.10 | Python bindings for MeshLab mesh processing filters. |
| matplotlib | (not pinned) | Plotting library. Used for colormap generation. |
| numpy | (not pinned) | Numerical array library. |
| pandas | (not pinned) | Data analysis and manipulation. |
| pyproj | (not pinned) | Coordinate reference system transformations (wraps PROJ). |
| plyfile | (not pinned) | Read/write PLY mesh format in Python. |
| trimesh | (not pinned) | 3D mesh loading and manipulation. |
| py3dtilers | (not pinned) | 3D Tiles generation from various input formats. Installed from https://github.com/VCityTeam/py3dtilers. |


## services/extern/ign-pdal-tools/environment.yml (conda env: pdaltools)

### Conda packages

| Name | Version | Channel | Description |
|------|---------|---------|-------------|
| python | 3.11.* | conda-forge | Python interpreter. |
| pdal | >=2.6.* | conda-forge | Point Data Abstraction Library for LiDAR processing. |
| python-pdal | 3.2.* | conda-forge | Python bindings for PDAL. |
| requests | (not pinned) | conda-forge | HTTP library for WMS image downloads. |
| gdal | (not pinned) | conda-forge | Geospatial Data Abstraction Library (raster/vector I/O). |
| lastools | (not pinned) | conda-forge | LAS/LAZ processing tools (Python wrapper). |
| laspy | (not pinned) | conda-forge | Read/write LAS/LAZ files. |
| tqdm | (not pinned) | conda-forge | Progress bar for long-running operations. |

### Dev dependencies (conda)

| Name | Version | Description |
|------|---------|-------------|
| pre-commit | (not pinned) | Git hooks for automated linting on commit. |
| black | (not pinned) | Python code formatter. |
| isort | (not pinned) | Python import sorter. |
| flake8 | (not pinned) | Python code linter / style checker. |
| pytest | (not pinned) | Python test framework. |
| requests-mock | (not pinned) | Mock HTTP requests in tests. |
| build | (not pinned) | Python package builder (PEP 517). |
| twine | (not pinned) | PyPI package upload tool. |


## services/extern/ (bundled C++ libraries, compiled during build)

| Name | Version | Description | Used by |
|------|---------|-------------|---------|
| ANN | 1.1.2 | Approximate Nearest Neighbor searching in arbitrary dimensions. | wasure (via FindANN.cmake) |
| CImg | 1.59 | Single-header C++ image processing toolkit. | wasure (via FindCIMG.cmake) |
| double-conversion | 3.1.5 | IEEE double to/from string conversion routines (from Google V8). | ddt + wasure (via FindDouble-conversion.cmake) |
| graphcut (MAXFLOW) | 3.01 | Min-cut/max-flow graph-cut algorithm for energy minimization. | wasure (via FindGRAPHCUT.cmake) |
| LAStools (LASlib + LASzip) | ~2017 | C++ API for reading/writing LAS and LAZ LiDAR files. | wasure (via FindLAS.cmake) |
| libhdfs | (Hadoop 2.7.7) | C client library for HDFS access. Requires JVM. | ddt + wasure (via FindHDFS.cmake) |
| OpenGM 2 | 2.3.1 | C++ template library for discrete factor graph models and inference. Unmaintained. | Present but not directly linked via a Find module. |
| QPBO | 1.3 | Quadratic Pseudo-Boolean Optimization using roof duality / max-flow. | wasure (via FindQPBO.cmake) |
| tinyply | 2.2 | Single-header C++11 PLY mesh format reader/writer. | wasure (via FindTINYPLY.cmake) |
| convertcloud | 0.1.0 | Python utility for point cloud format conversion (PCD, PLY, XYZ, etc.). | Not linked via CMake. Python utility. |
| ign-pdal-tools | ~1.7.2 | Python tools (IGN) for LiDAR colorization, stitching, and standardization. | Used by colorize.sh at runtime. |


## src/spark/build.sbt (Scala/Spark dependencies)

| Name | Version | Description |
|------|---------|-------------|
| Scala | 2.13.0 | Scala language version for the Spark module. |
| spark-core | 3.5.0 | Apache Spark core distributed computing library. |
| spark-sql | 3.5.0 | Apache Spark SQL for structured data processing. |
| spark-graphx | 3.5.0 | Apache Spark graph processing library. |