# Spotlight
SpotLight enables users to emphasize important spans within their prompt and steers the LLMs attention towards those spans.

## Overview
SpotLight is an inference-time lifecycle component that lets you "highlight" critical instructions, dynamically steering the model's attention without any retraining.
SpotLight only works with locally loaded HuggingFace Transformer models.

## Architecture
Given a user prompt with a critical instruction, this component will boost the attention score of the highlighted instruction. This allows the LLM to follow that specific instruction given its higher attention score.

## Results
The bar graphs below show how SpotLight leads to improved end to end performance of LLMs.

![spotlight_results](../../assets/img_spotlight_results.png)

## Getting Started


### When to Use This Component
Use Spotlight when your LLM is failing to follow critical instructions in complex prompts. It is an inference-time hook and does not involve any training or changes to model weights.

> [!IMPORTANT]
> SpotLight only works with locally loaded HuggingFace Transformer models


### Quick Start

1. Initialize the SpotLight config and component objects.

```python
from altk.pre_llm.core.config import SpotLightConfig
from altk.pre_llm.spotlight.spotlight import SpotLightComponent

# SpotLightConfig accepts the HF model path and generation arguments
# NOTE: torch may require the PYTORCH_ENABLE_MPS_FALLBACK=1 environment variable
config = SpotLightConfig(model_path="Qwen/Qwen2.5-1.5B-Instruct",
                         generation_kwargs={
                             'max_new_tokens=': 128,
                             'do_sample': False,
                         }
                         )
spotlight = SpotLightComponent(config=config)
```

2. Define the input messages and spans within the prompt to emphasize. Provide these while running SpotLight, along with an optional `alpha` parameter, that defines the amount of emphasis the LLM should place on the span.
> [!NOTE]
> To maintain consistency with the rest of this framework, we use LangChain's message format. SpotLight does support the traditional HF chat format as well.

```python
from altk.core.toolkit import AgentPhase
from altk.pre_llm.core.config import SpotLightMetadata, SpotLightRunInput

messages = [
  {
    "role": "user",
    "content": "List the capitals of the following countries - USA, Italy, Greece. Always give me the answer in JSON format."
  }
]
emph_span = ["Always give me the answer in JSON format."]

run_input = SpotLightRunInput(
    messages=messages,
    metadata=SpotLightMetadata(emph_strings=emph_span, alpha=0.1),
)
result = spotlight.process(run_input, phase=AgentPhase.RUNTIME)
prediction = result.output.prediction
print(prediction)
```
> [!NOTE]
> If the emphasized span is not present in the prompt, SpotLight will raise an error

```bash
"""
{
  "capitals": {
    "USA": "Washington D.C.",
    "Italy": "Rome",
    "Greece": "Athens"
  }
}
"""
```

> [!TIP]
> You can emphasize multiple spans by providing them as a list of lists -- `emph_span = [[span_1], [span_2]]`
 

### Ready to get started?
Go to our GitHub repo and run this [example](https://github.com/AgentToolkit/agent-lifecycle-toolkit/blob/main/examples/spotlight.ipynb) or get the code running by following the instructions in the [README](https://github.com/AgentToolkit/agent-lifecycle-toolkit/blob/main/altk/pre_llm/spotlight/README.md).



## References
Venkateswaran, Praveen, and Danish Contractor. "Spotlight Your Instructions: Instruction-following with Dynamic Attention Steering." arXiv preprint arXiv:2505.12025 (2025). https://arxiv.org/pdf/2505.12025
