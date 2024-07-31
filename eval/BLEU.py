import evaluate

bleu = evaluate.load("bleu")

predictions = ["They cancelled the match because it was raining "]
references = ["They cancelled the match because of bad weather"]

results = bleu.compute(predictions=predictions, references=references)
print(results)
