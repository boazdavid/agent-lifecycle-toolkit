# ToolGuards for Enforcing Agentic Policy Adherence
An agent lifecycle solution for enforcing business policy adherence in agentic workflows. Enabling this component has demonstrated up to a **20‑point improvement** in end‑to‑end agent accuracy when invoking tools.

## Table of Contents
- [Overview](#overview)
- [When to Use This Component](#when-it-is-recommended-to-use-this-component)
- [LLM Configuration Requirements](#llm-configuration-requirements)
- [Quick Start](#quick-start)
- [Parameters](#parameters)
  - [Constructor Parameters](#constructor-parameters)
  - [Build Phase Input Format](#build-phase-input-format)
  - [Run Phase Input Format](#run-phase-input-format)
  - [Run Phase Output Format](#run-phase-output-format)



## Overview

Business policies (or guidelines) are normally detailed in company documents, and have traditionally been hard-coded into automatic assistant platforms. Contemporary agentic approaches take the "best-effort" strategy, where the policies are appended to the agent's system prompt, an inherently non-deterministic approach, that does not scale effectively. Here we propose a deterministic, predictable and interpretable two-phase solution for agentic policy adherence at the tool-level: guards are executed prior to function invocation and raise alerts in case a tool-related policy deem violated.

This component enforces **pre‑tool activation policy constraints**, ensuring that agent decisions comply with business rules **before** modifying system state. This prevents policy violations such as unauthorized tool calls or unsafe parameter values.

## ToolGuardSpecComponent
This component gets a set of tools and a policy document and generated multiple ToolGuard specifications, known as `ToolGuardSpec`s. Each specification is attached to a tool, and it declares a precondition that must apply before invoking the tool. The specification has a `name`, `description`, list of `refernces` to the original policy document, a set of declerative `compliance_examples`, describing test cases that the toolGuard should allow the tool invocation, and `violation_examples`, where the toolGuard should raise an exception.

This componenet supports only a `build` phase. The generate specifications are returned as output, and are also saved to a specified file system directory.
The specifications are aimed to be used as input into our next component - the `ToolGuardCodeComponent` described below. 

The two components are not concatenated by design. As the geneartion involves a non-deterministic language model, the results need to be reviewed by a human. Hence, the output specification files should be reviewed and optionaly edited. For example, removing a wrong compliance example.

### Usage example
see [simple calculator test](../../tests/pre_tool_guard_toolkit/test_toolguard_specs.py)

### Component Configuarion
This component expects an LLM client configuarion:
```python
from altk.toolkit_core.llm import get_llm  

LLMClient = get_llm("litellm.output_val")
llm_client = LLMClient(...)
toolguard_component = ToolGuardSpecComponent(
    ToolGuardSpecComponentConfig(llm_client=llm_client)
)
```

Here is a concerete example with `litellm` and `azure`:
Environment variables:
```bash
export AZURE_OPENAI_API_KEY="<your key>"
export AZURE_API_BASE="https://your.azure.endpoint"
export AZURE_API_VERSION="2024-08-01-preview"
```
code:
```python
from altk.toolkit_core.llm import get_llm  

LLMClient = get_llm("litellm.output_val")
llm_client = LLMClient(
    model_name="gpt-4o-2024-08-06",
    custom_llm_provider="azure",
)

```
## ToolGuardCodeComponent

This components enfoorces policy adherence through a two-phase process:

(1) **Buildtime**: Given a set of `ToolGuardSpec`s, generates policy validation code - `ToolGuard`s.
Similar to ToolGuard Specifications, generated `ToolGuards` are a good start, but they may contain errors. Hence, they should be also reviewed by a human.

(2) **Runtime**: ToolGuards are deployed within the agent's flow, and are triggered before agent's tool invocation. They can be deployed into the agent loop, or in an MCP Gateway. 
The ToolGuards checks if a planned action complies with the policy. If it violates, the agent is prompted to self-reflect and revise its plan before proceeding. 


### Usage example
see [simple calculator test](../../tests/pre_tool_guard_toolkit/test_toolguard_code.py)

### Component Configuarion

Backed by Mellea, which requires parameters aligning to:
```python
mellea.MelleaSession.start_session(
    backend_name=...,
    model_id=...,
    backend_kwargs=...    # any additional arguments
)
```
The `melea` session parameters can be provided explicitely, or loaded from environment variables:

| Environment Variable           | Mellea Parameter | Description                                                        |
| ------------------------------ | ---------------- | ------------------------------------------------------------------ |
| `TOOLGUARD_GENPY_BACKEND_NAME` | `backend_name`   | Which backend to use (e.g., `openai`, `anthropic`, `vertex`, etc.) |
| `TOOLGUARD_GENPY_MODEL_ID`     | `model_id`       | Model name / deployment id                                         |
| `TOOLGUARD_GENPY_ARGS`         | `backend_kwargs` | JSON dict of any additional connection/LLM parameters              |

Example (Claude-4 Sonnet through OpenAI-compatible endpoint):
```bash
export TOOLGUARD_GENPY_BACKEND_NAME="openai"
export TOOLGUARD_GENPY_MODEL_ID="GCP/claude-4-sonnet"
export TOOLGUARD_GENPY_ARGS='{"base_url":"https://your-litellm-endpoint","api_key":"<your key>"}'
```
