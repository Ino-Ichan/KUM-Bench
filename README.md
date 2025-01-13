<h1 align="center">
    <img src="./imgs/kum-bench-image.jpg" alt="Logo" style="height: 12em; display: inline-block; vertical-align: middle;"> <br>KUM-Bench
</h1>

[![GitHub Link](https://img.shields.io/badge/GitHub-Repo-blue.svg)](https://github.com/Ino-Ichan/KUM-Bench)
[![HuggingFace Link](https://img.shields.io/badge/HuggingFace-Dataset-yellow.svg)](https://huggingface.co/datasets/Inoichan/KUM-Bench)


## KUM-Bench: A Benchmark for Advanced Japanese Reasoning Capabilities

Kyoto University Math Entrance Exam Benchmark (KUM-Bench) is a benchmark designed to evaluate advanced Japanese reasoning capabilities using mathematics entrance exam questions from Kyoto University. As one of the most prestigious universities in Japan, Kyoto University’s entrance examinations demand a high level of problem-solving skills. This benchmark leverages the inherently challenging and original nature of the math entrance exam problems, providing an excellent resource for testing Large Language Models (LLMs) in Japanese reasoning tasks.

## Overview

- **Target Years**: 2023 and 2024 math entrance exams (both Liberal Arts (文系) and Science (理系) tracks).  
- **Rationale**: By using recent entrance exam questions, this benchmark aims to reduce data contamination risks.  
- **Content**: 
  - Problems have been converted to LaTeX format using o1.  
  - Solutions are based on available sample solutions, then converted to LaTeX format with o1.  
- **Regular Updates**: Because Kyoto University publishes new entrance exam problems annually, KUM-Bench can be updated frequently to ensure contamination-free evaluation for LLMs.  

## Scoring Methodology

1. We employ an LLM-based scoring system, assigning a maximum of 5 points per question.  
2. For numerical-answer questions, a correct solution yields 5 points; partial credit is awarded based on the correctness of the derivation steps.  
3. Symbolic or proof-based questions are also evaluated on a 5-point scale, comparing the reasoning and final answer with reference solutions.  
4. To reduce variance, each solution is evaluated 5 times using an LLM with `temperature=1.0`.  
   - The highest and lowest scores are discarded.  
   - The final score for the solution is the average of the remaining 3 scores.  
5. Since there are 28 questions, the total score is out of 140.  

## Example Results

Below are some example scores obtained by different models on KUM-Bench (out of 140):

| Model                          | Score (out of 140) |
|--------------------------------|--------------------|
| gpt-4o                         | 72                 |
| gemini-1.5.pro                 | 89.6               |
| gemini-2.0.flash.exp           | 96                 |
| gemini-2.0.flash.thinking.exp  | 112                |

You can find detailed output logs in the [./outputs](./outputs) directory.

## Installation

To install the required Python packages:
```bash
pip install -r requirements.txt
```

## Inference

To run the benchmark inference:
```bash
python kum_bench/inference.py --model_name <model_name> --output_dir <output_dir>
```

Replace `<model_name>` with an API model name and `<output_dir>` with your desired directory for outputs.

## Scoring

To evaluate your model’s output against KUM-Bench:
```bash
python kum_bench/scoring.py --target_file <target_file>
```

Replace `<target_file>` with the path to your inference outputs that you wish to score.

## License and Data Usage

- **Code**: This project is licensed under the MIT License.  
- **Data**: For details regarding redistribution of the original exam materials, please consult Kyoto University’s official policy:  
  [https://www.kyoto-u.ac.jp/ja/admissions/undergrad/past-eq/copyright-policy](https://www.kyoto-u.ac.jp/ja/admissions/undergrad/past-eq/copyright-policy)

---

## Citation

If you use this benchmark, please use the following citation:

```
@misc{kum-bench,
  title={KUM-Bench: A Benchmark for Advanced Japanese Reasoning Capabilities},
  author={Yuichi Inoue},
  year={2025},
  url={https://github.com/Ino-Ichan/KUM-Bench},
}
```
