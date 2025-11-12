from datasets import load_dataset  # type: ignore
from ragas import evaluate
from ragas.metrics import answer_relevancy, faithfulness


def run_ragas(predict_fn, path="tests/eval_set.jsonl"):
    ds = load_dataset("json", data_files=path, split="train")
    # predict_fn: q -> (answer, contexts_texts)
    preds = []
    for row in ds:
        ans, ctxs = predict_fn(row["question"])
        preds.append(
            {
                "question": row["question"],
                "answer": ans,
                "contexts": [c[:1500] for c in ctxs],
            }
        )
    return evaluate(preds, metrics=[faithfulness, answer_relevancy])
