import lm_eval
# from lm_eval.loggers import WandbLogger

results = lm_eval.simple_evaluate(
    model="hf",
    model_args="pretrained=microsoft/phi-2,trust_remote_code=True,device=cpu",
    tasks="mmlu_abstract_algebra",
    log_samples=True,
)

print(results)

