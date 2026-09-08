#!/usr/bin/env python3

import argparse
import os
import re
import random
import subprocess
import xml.etree.ElementTree as ET
import math


# ---- Utility functions ----

def get_param(params, key, default=""):
    return params.get(key, default)


def list_las_files(input_dir, regexp_filter):
    """ List LAS/LAZ files, filtered by regexp_filter """
    re_filter = re.compile(regexp_filter) if regexp_filter else None
    las_files = []
    for root, _dirs, files in os.walk(input_dir):
        for f in sorted(files):
            if f.lower().endswith((".las", ".laz")):
                path = os.path.join(root, f)
                if re_filter is None or re_filter.search(path):
                    las_files.append(path)

    if not las_files:
        raise SystemExit("ERROR: 0 LAZ/LAS FOUND")
    
    return las_files

    
def build_cmd(params, extra_params):
    """Build command line from params_wasure + extra params."""
    cmd = [params["exec_path"]]
    all_params = {**params, **extra_params}
    for k, v in all_params.items():
        if k != "exec_path":
            cmd += [f"--{k}", str(v)]
    return cmd


def run_exe(cmd, stdin_lines):
    """Run the C++ executable with stdin lines, return stdout lines."""
    stdin_data = "\n".join(stdin_lines) + "\n"
    result = subprocess.run(cmd, input=stdin_data, capture_output=True, text=True)
    print(f"returncode: {result.returncode}")
    if result.stderr:
        print(f"stderr: {result.stderr}")
    if result.returncode != 0:
        raise SystemExit(f"ERROR: {cmd[0]} failed with return code {result.returncode}")
    return result.stdout.splitlines()


def parse_bbox_lines(lines):
    """Extract bbox floats from 's' lines: [xmin, xmax, ymin, ymax, zmin, zmax, nbpoints]."""
    bboxes = []
    for line in lines:
        if not line or line[0] != "s":
            continue
        parts = line.split("z", 1)
        if len(parts) < 2:
            continue
        vals = [float(x) for x in parts[1].split() if x]
        bboxes.append(vals)
    return bboxes


def aggregate_bboxes(bboxes):
    """Reduce bboxes: min/max/min/max/min/max per axis, sum nb points."""
    agg = list(bboxes[0])
    for b in bboxes[1:]:
        agg[0] = min(agg[0], b[0])
        agg[1] = max(agg[1], b[1])
        agg[2] = min(agg[2], b[2])
        agg[3] = max(agg[3], b[3])
        agg[4] = min(agg[4], b[4])
        agg[5] = max(agg[5], b[5])
        agg[6] += b[6]
    return agg


# ---- Main ----

def main():
    parser = argparse.ArgumentParser(description="Preprocess input data for Wasure workflow.")

    parser.add_argument("-i", "--input", required=True, help="Path to the input data directory.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output data directory.")
    parser.add_argument("-p", "--params", required=False, help="Path to the parameters file (optional).")
    parser.add_argument("-b", "--build", required=True, help="Path to the build directory (optional).")
    parser.add_argument("-r", "--seed", required=False, help="Seed for random number generation (optional).")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode (optional).")

    args = parser.parse_args()

    input_dir = args.input.replace("//", "/")
    output_dir = args.output.replace("//", "/")
    build_dir = args.build.replace("//", "/")

    if not input_dir or not output_dir:
        raise SystemExit("ERROR: input or output directory is empty")

    os.makedirs(output_dir, exist_ok=True)


    # Parse XML params file
    xml_params = {}
    if args.params and os.path.isfile(args.params):
        tree = ET.parse(args.params)
        dataset = tree.find(".//datasets")
        if dataset is not None:
            first_dataset = list(dataset)[0]
            for child in first_dataset:
                xml_params[child.tag] = child.text.strip() if child.text else ""

    print(f"Loaded {len(xml_params)} parameter(s) from {args.params or 'defaults'}")
   
    dim = int(get_param(xml_params, "dim", "3"))
    ddt_kernel_dir = get_param(xml_params, "ddt_kernel", f"build-spark-Release-{dim}")
    build_dir = os.path.join(build_dir, ddt_kernel_dir)
    max_ppt = int(get_param(xml_params, "max_ppt", "500000"))
    bbox = get_param(xml_params, "bbox", "")
    algo_seed = args.seed or get_param(xml_params, "algo_seed", str(random.randint(0, 99999)))
    wasure_mode = get_param(xml_params, "mode", "1")
    pscale = float(get_param(xml_params, "pscale", "0.05"))
    nb_samples = float(get_param(xml_params, "nb_samples", "40"))
    ndtree_depth = int(get_param(xml_params, "ndtree_depth", "-1"))
    rat_ray_sample = float(get_param(xml_params, "rat_ray_sample", "0"))
    min_ppt = int(get_param(xml_params, "min_ppt", "50"))
    main_algo_opt = get_param(xml_params, "algo_opt", "seg_lagrange_weight")
    dst_scale = float(get_param(xml_params, "dst_scale", "-1"))
    lambda_val = float(get_param(xml_params, "lambda", "2"))
    max_opt_it = int(get_param(xml_params, "max_opt_it", "50"))
    do_stats = get_param(xml_params, "do_stats", "false").lower() == "true"
    coef_mult = float(get_param(xml_params, "coef_mult", "5"))
    regexp_filter = get_param(xml_params, "regexp_filter", "")

    params = {
        "dim": dim,
        "ddt_kernel": ddt_kernel_dir,
        "max_ppt": max_ppt,
        "bbox": bbox,
        "algo_seed": algo_seed,
        "mode": wasure_mode,
        "pscale": pscale,
        "nb_samples": nb_samples,
        "ndtree_depth": ndtree_depth,
        "rat_ray_sample": rat_ray_sample,
        "min_ppt": min_ppt,
        "algo_opt": main_algo_opt,
        "dst_scale": dst_scale,
        "lambda": lambda_val,
        "max_opt_it": max_opt_it,
        "do_stats": do_stats,
        "coef_mult": coef_mult,
        "regexp_filter": regexp_filter,
        "ddt_main_dir": os.environ.get("DDT_MAIN_DIR", ""),
        "output_dir": output_dir,
    }

    cpp_exec_path = os.path.join(build_dir, "bin", "wasure-stream-exe")

    params_wasure = {
        "exec_path": cpp_exec_path,
        "dim": str(dim),
        "input_dir": input_dir,
        "output_dir": output_dir,
    }


    las_files = list_las_files(input_dir, regexp_filter)
    print(f"\n======== LOAD DATA: {len(las_files)} file(s) =============")


    # First pass computes the original global bounding box.
    print("[1/2] Running compute_bbox...")
    bbox_cmd = build_cmd(params_wasure, {"step": "compute_bbox", "label": "struct"})
    # Format: <key> <list_size> p 1 <idx> f <filepath> (protocol from print_rdde_vdat)
    stdin_lines = [f"{i} 1 p 1 {i} f {path}" for i, path in enumerate(las_files)]

    bbox_output = run_exe(bbox_cmd, stdin_lines)
    bboxes_ori = parse_bbox_lines(bbox_output)

    if not bboxes_ori:
        raise SystemExit("ERROR: compute_bbox returned no bbox data")

    bba_ori = aggregate_bboxes(bboxes_ori)
    print(f"Original bbox: {bba_ori}")


    # Second pass preprocesses every file using that shared bounding box.
    print("[2/2] Running preprocess...")
    bbox_ori_str = f"{bba_ori[0]}x{bba_ori[1]}:{bba_ori[2]}x{bba_ori[3]}:{bba_ori[4]}x{bba_ori[5]}"
    preprocess_cmd = build_cmd(params_wasure, {"step": "preprocess", "bbox": bbox_ori_str, "label": "struct"})
    preprocess_output = run_exe(preprocess_cmd, stdin_lines)
    bboxes = parse_bbox_lines(preprocess_output)

    if not bboxes:
        raise SystemExit("ERROR: preprocess returned no bbox data")

    bba = aggregate_bboxes(bboxes)
    print(f"Processed bbox: {bba}")


    # Derived calculations
    smax = max(bba[1] - bba[0], bba[3] - bba[2])
    smax_ori = max(bba_ori[1] - bba_ori[0], bba_ori[3] - bba_ori[2])
    tot_nbp = bba[6]
    ndtree_depth_calc = max(round(math.log(tot_nbp / max_ppt) / math.log(3)), 0) if tot_nbp > 0 else 0

    params["bbox"] = f"{bba[0]}x{bba[0] + smax}:{bba[2]}x{bba[2] + smax}:{0.0}x{10000.0}"
    params["bbox_ori"] = f"{bba_ori[0]}x{bba_ori[0] + smax_ori}:{bba_ori[2]}x{bba_ori[2] + smax_ori}:{bba_ori[4]}x{10000.0}"
    if ndtree_depth == -1:
        params["ndtree_depth"] = ndtree_depth_calc
    params["datatype"] = "files"
    params["max_ppt"] = max_ppt
    print(f"Computed ndtree_depth: {params['ndtree_depth']}")


    # Export wasure_metadata_3d_gen.xml
    xml_lines = ['<env>', '\t<datasets>', '\t\t<generated>']
    for k, v in params.items():
        if str(v) and k not in ("do_expand", "output_dir"):
            xml_lines.append(f"\t\t\t<{k}>{v}</{k}>")
    xml_lines += ['\t\t</generated>', '\t</datasets>', '</env>']

    xml_path = os.path.join(output_dir, "wasure_metadata_3d_gen.xml")
    with open(xml_path, "w") as f:
        f.write("\n".join(xml_lines) + "\n")
    print(f"Written {xml_path}")


if __name__ == "__main__":
    main()
