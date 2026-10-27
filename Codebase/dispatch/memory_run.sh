#!/bin/bash
#SBATCH --job-name=memory_run
#SBATCH --time=06:00:00
#SBATCH --mem=16G
#SBATCH --output=logs/memory_run_%A_%a.out
#SBATCH --error=logs/memory_run_%A_%a.err

cd /scratch/$USER/Design-of-MA-Systems
module load uv

uv run Codebase/full_memory_run.py "$@"
