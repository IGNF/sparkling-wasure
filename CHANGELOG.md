
# Change Log
All notable changes to this project will be documented in this file.
 
 
## [Unreleased] - 2026-10-09
 
sparkling-wasure with only the main algorithm, removing colorize and mesh23dtile of the workflow to put them into separate repositories.
 
### Changed

Removing [1caa863](https://github.com/lcaraffa/sparkling-wasure/commit/1caa863):
- ign-pdal-tools used as dependency (in "./services/extern/").
- tools' folder in "./service/" (colorize and mesh23dtile)
- calls in the runtime pipeline (run_examples.sh and run_workflow.sh)
- imports and building part in the building pipeline ("./src/docker/Dockerfile-base-Ubuntu-devel")
 

## [1.0.0] - 2026-09-29
  
The debbuging version of the original algorithm.
 
### Added
 
Documentation [7aa57b6](https://github.com/lcaraffa/sparkling-wasure/commit/7aa57b6):
- Presentation of the algorithm
- Runtime and building pipeline diagrams
- Building parameters lifetime diagram
- List of runtime and building variables
- List of library used

### Changed

Minor changes [e7db004](https://github.com/lcaraffa/sparkling-wasure/commit/e7db004):
- algo-env.sh: value of variables consistent with local execution.
- Dockerfile: adapt writing to remove warning.
 
### Fixed

Building issues [e7db004](https://github.com/lcaraffa/sparkling-wasure/commit/e7db004):
- Miniconda installation in Dockerfile issue fixed.
- py3dtiles version fixed.
- laspy dependency fixed.

Algorithm issues:
- The code no longer crashes when the algorithm processes only one ply file during 3DTiles generation [36d2c61](https://github.com/lcaraffa/sparkling-wasure/commit/36d2c61).

Result issues:
- 3DTiles visibility and georeferencing in iTowns fixed [36d2c61](https://github.com/lcaraffa/sparkling-wasure/commit/36d2c61).
 

## [0.0.0] - 2025-11-12
 
### Added

- [sparkling-wasure](https://github.com/lcaraffa/sparkling-wasure)
  Initial release. Create from 3D point cloud data (like LIDAR-HD) the 3D model of the surface in several .ply files.
  Possibility to colorize the output mesh and create 3DTiles, organized in different LODs, viewable on iTowns.
  The algorithm is parallelized with Apache Spark. 