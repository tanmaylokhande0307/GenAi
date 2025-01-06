### Transformers

Transformers are piece of architecture which is a combination of blocks called encoders and decoders
whose main task is essentially to produce next words.
The training is done in a semi supervised way, ie it is trained on an unsupervised dataset and then finetuned with labelled data
It works on attention mechanism that is it calculates how much attention to give a particular word of a sentence and then predict the next word depending on the weights assigned to each word in a sentence