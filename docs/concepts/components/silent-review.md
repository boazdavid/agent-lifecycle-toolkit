# Silent Review
A prompt-based component to automatically identify silent errors in tool calls - errors that do not produce explicit error messages.

It evaluates whether a tool's response is relevant, accurate, and complete relative to the user’s query.

## Overview

Silent Review is designed to be integrated into agent pipelines to assess tool outputs, particularly for:

- Verbose outputs: Responses that are long or complex.
- Tabular outputs: Structured data that requires context-aware evaluation.

The component analyzes the tool response based on:

1. User query
2. Tool response
3. Tool specification (Optional)
4. Tool input
5. Tool type

It returns one of three outcomes:

1. Accomplished – The tool fully satisfies the user query.
2. Partially Accomplished – The tool partially satisfies the user query.
3. Not Accomplished – The tool fails to satisfy the query.

## Architecture
Silent Review works by prompting a large language model (LLM) to evaluate the tool response in the context of the user’s query and the tool’s specification.

Integration into an agent pipeline is straightforward:

![Architecture Diagram](../../assets/img_silent_error_review.png)

**Key points:**
- Works for any structured or JSON-like tool response.
- Can be plugged post-tool execution in an agent pipeline.
- Uses the LLM to reason about relevance, completeness, and correctness.

## Results
Silent Review improves the overall reliability of agent tool calls by catching silent errors that would otherwise go unnoticed.

**Evaluation Dataset**

The evaluation results are based on the BIRD dataset, which includes SQL databases, natural language questions created by human annotators, and corresponding ground-truth SQL queries. This dataset is designed to evaluate large language models' ability to execute tool calls effectively.

For more details, refer to the paper: [Invocable APIs derived from NL2SQL datasets for LLM Tool-Calling Evaluation](https://arxiv.org/pdf/2506.11266)

**Evaluation Metrics:**
- Micro Win Rate: Average performance across individual data subsets.
- Macro Win Rate: Overall performance across all samples in all subsets.

| Method               | Micro Win Rate (%) | Micro Avg. Loop | Macro Win Rate (%) | Macro Avg. Loop |
|---------------------|:----------------:|:----------------:|:----------------:|:----------------:|
| React without Review | 6.8          | 8.72           | 6.1          | 8.51           |
| React with Review    | 12.7          | 7.77           | 10.4          | 7.90           |

**Insights:**
- Adding Silent Review nearly doubles the micro win rate, indicating more queries are fully or partially accomplished.
- Average loop counts decrease slightly, showing that fewer iterations are needed to reach successful query completion.

## Getting Started

### When it is recommended to Use This Component:
Best suited for tool responses that are verbose and/or based on tabular responses.


### Quick Start
The below example should give you an idea of how to plug in this component into your agent pipeline:

```python
from altk.post_tool.silent_review.silent_review import SilentReviewForJSONDataComponent
from altk.post_tool.core.toolkit import SilentReviewRunInput
from altk.core.toolkit import AgentPhase

input_data = SilentReviewRunInput(
    messages=[
        {"role": "user", "content": "Tell me the weather"},
        {"role": "assistant", "content": "Calling the weather tool now"}
    ],
    tool_spec={
        "name": "get_weather",
        "description": "Gets weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    },
    tool_response={
        "name": "get_weather",
        "result": {"city": "NYC", "temperature": "75F", "condition": "Sunny"}
    }
)

reviewer = SilentReviewForJSONDataComponent()
result = reviewer.process(data=input_data, phase=AgentPhase.RUNTIME)
print(result.outcome.value)

# possible outcomes

# NOT_ACCOMPLISHED = 0
# PARTIAL_ACCOMPLISH = 0.5
# ACCOMPLISHED = 1

```


### Interface
Expected input:
- user query,
- tool response,
- tool specification,
- tool input,
- tool type

Expected output:
- Accomplished | Partially Accomplished | Not Accomplished

### Ready to get started?
Go to our GitHub repo and run this [example](https://github.com/AgentToolkit/agent-lifecycle-toolkit/blob/main/examples/silent_review.ipynb) or get the code running by following the instructions in the [README](https://github.com/AgentToolkit/agent-lifecycle-toolkit/blob/main/altk/post_tool/silent_review/README.md).
