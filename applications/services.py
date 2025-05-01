def score_submission(predictions, ground_truth):
    return sum(p == g for p, g in zip(predictions, ground_truth)) / len(predictions)
