import logging
import os
from typing import Callable, List, Set
from langchain.tools import BaseTool
from pydantic import Field

from ...core.llm import ValidatingLLMClient
from ...core.toolkit import AgentPhase, ComponentBase, ComponentConfig, ComponentInput
from .toolguard import ToolGuardSpec, generate_guard_specs
from .toolguard.llm.i_tg_llm import I_TG_LLM

logger = logging.getLogger(__name__)

class ToolGuardSpecComponentConfig(ComponentConfig):
    pass

class ToolGuardSpecBuildInput(ComponentInput):
    policy_text: str = Field(description="Text of the policy document file")
    tools: List[Callable] | List[BaseTool] | str
    work_dir: str

ToolGuardSpecs=List[ToolGuardSpec]

class ToolGuardSpecComponent(ComponentBase):
    
    def __init__(self, config:ToolGuardSpecComponentConfig):
        super().__init__(config=config)
        
    @classmethod
    def supported_phases(cls) -> Set[AgentPhase]:
        return {AgentPhase.BUILDTIME, AgentPhase.RUNTIME}

    def _build(self, data: ToolGuardSpecBuildInput) -> ToolGuardSpecs:
        raise NotImplementedError("Please use the aprocess() function in an async context")

    async def _abuild(self, data: ToolGuardSpecBuildInput) -> ToolGuardSpecs:
        os.makedirs(data.work_dir, exist_ok=True)
        return await generate_guard_specs(
            policy_text=data.policy_text,
            tools=data.tools,
            work_dir=data.work_dir,
            llm=TG_LLMEval(self.config.llm_client)
        )
        

class TG_LLMEval(I_TG_LLM):
    def __init__(self, llm_client: ValidatingLLMClient):
        if not isinstance(llm_client, ValidatingLLMClient):
            print("llm_client is a ValidatingLLMClient")
            exit(1)
        self.llm_client = llm_client

    async def chat_json(self, messages: list[dict], schema=dict) -> dict:
        return self.llm_client.generate(
            prompt=messages, schema=schema, retries=5, schema_field=None
        )

    async def generate(self, messages: list[dict]) -> str:
        return self.llm_client.generate(
            prompt=messages, schema=str, retries=5, schema_field=None
        )
