# Codexa NumPy v2

Codexa NumPy is a decoder-only language model built from scratch with a NumPy-based tensor and automatic differentiation engine. It includes Transformer layers, a byte-level BPE tokenizer, data preparation, training, checkpointing and text generation. An optional CuPy backend supports CUDA arrays; PyTorch is not a runtime dependency.

## Project layout

| Directory | Responsibility |
| --- | --- |
| [LLM-Architecture](LLM-Architecture/) | Tensor operations, backends, layers and losses |
| [LLM-Data](LLM-Data/) | Dataset preparation, loading and provenance |
| [LLM-From-Scratch](LLM-From-Scratch/) | Canonical package, tests, configuration and command-line tools |
| [LLM-Inference](LLM-Inference/) | Text generation and sampling |
| [LLM-Memory](LLM-Memory/) | Placeholder for future memory work |
| [LLM-Specialist](LLM-Specialist/) | Placeholder for future specialist work |
| [LLM-Tokenizer](LLM-Tokenizer/) | Byte-level BPE tokenizer |
| [LLM-Training](LLM-Training/) | Training, optimizers and checkpoints |
| [workspace-infrastructure](workspace-infrastructure/) | Workspace navigation information |

The implementation lives in `LLM-From-Scratch/src/llm_numpy`. Component directories point to this shared implementation; they are not separate packages.

## Install and run

Python 3.11 or later is required. From the repository root:

```sh
cd LLM-From-Scratch
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python -m pip install --no-deps -e .
.venv/bin/python -m pytest -q tests
.venv/bin/python -m llm_numpy.cli.environment_report
.venv/bin/python -m llm_numpy.cli.chat_codexa --help
```

For GPU setup, see [CUDA documentation](LLM-From-Scratch/docs/CUDA_BACKEND.md) and `requirements-cuda.lock`. Checkpoints and datasets are not included; generation and training commands that use them require separately supplied assets. Review dataset provenance and run the documented preflight before training.

## Status

The numerical engine, tokenizer, training and generation code are implemented and covered by tests. Memory and Specialist are documentation-only placeholders. CUDA requires a compatible NVIDIA setup; validation results and historical model records do not imply that trained weights or datasets are bundled. See the [project README](LLM-From-Scratch/README.md), [model card](LLM-From-Scratch/MODEL_CARD.md), and [dataset card](LLM-From-Scratch/DATASET_CARD.md) for details.
