import evaluate 

rouge = evaluate.load('rouge')

predictions = ["He was extremely happy last night"]
references = ["He was happy last night"]

results = rouge.compute(predictions=predictions,references=references)
print(results)
