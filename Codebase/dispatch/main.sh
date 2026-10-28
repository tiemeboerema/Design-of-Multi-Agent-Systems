#!/bin/bash
set -e

for memory_size in $(seq 10 10 200); do
    sbatch Codebase/dispatch/memory_run.sh --mem_size="$memory_size" "$@"
done
