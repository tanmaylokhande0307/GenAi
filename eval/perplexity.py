import numpy as np

# 4 values of probablities 1 for each token based on previous token
# probability of a sentence made by these 4 tokens is the product of the probabilities of these 4 tokens
probabilities = np.array([0.4,0.27,0.55,0.79]) 
sentence_probability = probabilities.prod()
sentence_probability_normalized = sentence_probability ** (1 / len(probabilities))
perplexity = 1 / sentence_probability_normalized
print(perplexity)

