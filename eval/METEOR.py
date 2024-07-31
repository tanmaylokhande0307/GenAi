import evaluate

meteor = evaluate.load('meteor')

predictions = ["They cancelled the match because it was raining"]
references = ["They cancelled the match because of bad weather"]

results = meteor.compute(predictions=predictions,references=references)
print(results)
