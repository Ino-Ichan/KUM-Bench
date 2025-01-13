import argparse
import json
import re
import sys
from pathlib import Path

from datasets import load_dataset
from tqdm import tqdm

from kum_bench.api_model import OpenAIModel
from kum_bench.prompts import SCORING_PROMPT_TEMPLATE

TEMPERATURE = 1.0
N_GENERATIONS = 5


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_file", type=str, required=True)
    return parser.parse_args()


def extract_score(response: str) -> int:
    match = re.search(r"## Score\s+(\d+)", response)
    if match:
        return int(match.group(1))
    return 0


if __name__ == "__main__":
    args = parse_args()

    model = OpenAIModel("gpt-4o-2024-11-20")

    dataset = load_dataset("Inoichan/KUM-Bench", split="test")

    target_file = Path(args.target_file)
    with open(target_file, "r") as f:
        results = json.load(f)

    scoring_results = []
    scores = []

    for i, row in tqdm(enumerate(dataset), dynamic_ncols=True):
        year = row["year"]
        problem_number = row["problem_number"]
        question = row["question"]
        reference_answer = row["reference_answer"]

        student_answer = results[i]["response"]
        student_year = results[i]["year"]
        student_problem_number = results[i]["problem_number"]

        # check if the year and problem number match
        if year != student_year or problem_number != student_problem_number:
            print(
                f"Year or problem number does not match: {year} != {student_year} or {problem_number} != {student_problem_number}"
            )
            sys.exit(1)

        prompt = SCORING_PROMPT_TEMPLATE.format(
            question=question,
            reference_answer=reference_answer,
            student_answer=student_answer,
        )

        responses = model.generate(
            prompt, temperature=TEMPERATURE, n_generations=N_GENERATIONS
        )
        scoring_results.append(
            {
                "year": year,
                "problem_number": problem_number,
                "question": question,
                "responses": responses,
            }
        )

        problem_scores = []
        for response in responses:
            score = extract_score(response)
            problem_scores.append(score)

        # discard the lowest and highest scores
        problem_scores = sorted(problem_scores)[1:-1]

        # calculate the average score
        average_score = sum(problem_scores) / len(problem_scores)
        scores.append(average_score)

    print(f"Average score: {sum(scores) / len(scores)}")
    print(f"Total score: {sum(scores)} / {len(scores) * 5}")

    final_report = {
        "average_score": sum(scores) / len(scores),
        "total_score": sum(scores),
        "total_problem_count": len(scores),
        "total_score_percentage": sum(scores) / (len(scores) * 5) * 100,
        "scoring_results": scoring_results,
    }

    with open(target_file.with_suffix(".scoring.json"), "w") as f:
        json.dump(final_report, f, indent=4, ensure_ascii=False)
