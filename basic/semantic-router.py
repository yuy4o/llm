# https://github.com/aurelio-labs/semantic-router

from semantic_router import Route
from pydantic.v1 import BaseModel
from typing import Union, List, Any, Optional, Dict,Callable
from langchain.llms.base import BaseLLM

class Route(BaseModel):
    name: str
    utterances: Union[List[str], List[Union[Any, "Image"]]]
    description: Optional[str] = None
    function_schemas: Optional[List[Dict[str, Any]]] = None
    llm: Optional[BaseLLM] = None
    score_threshold: Optional[float] = None

    class Config:
        arbitrary_types_allowed = True

    def __call__(self, query: Optional[str] = None):
        if self.function_schemas:
            if not self.llm:
                raise ValueError(
                    "LLM is required for dynamic routes. Please ensure the `llm` "
                    "attribute is set."
                )
            elif query is None:
                raise ValueError(
                    "Query is required for dynamic routes. Please ensure the `query` "
                    "argument is passed."
                )
            # if a function schema is provided we generate the inputs
            extracted_inputs = self.llm.extract_function_inputs(
                query=query, function_schemas=self.function_schemas
            )
            func_call = extracted_inputs
        else:
            # otherwise we just pass None for the call
            func_call = None
        return RouteChoice(name=self.name, function_call=func_call)

    async def acall(self, query: Optional[str] = None):
        if self.function_schemas:
            if not self.llm:
                raise ValueError(
                    "LLM is required for dynamic routes. Please ensure the `llm` "
                    "attribute is set."
                )
            elif query is None:
                raise ValueError(
                    "Query is required for dynamic routes. Please ensure the `query` "
                    "argument is passed."
                )
            # if a function schema is provided we generate the inputs
            extracted_inputs = await self.llm.async_extract_function_inputs(  # type: ignore # openai-llm
                query=query, function_schemas=self.function_schemas
            )
            func_call = extracted_inputs
        else:
            # otherwise we just pass None for the call
            func_call = None
        return RouteChoice(name=self.name, function_call=func_call)

    # def to_dict(self) -> Dict[str, Any]:
    #     return self.dict()

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        if self.llm is not None:
            data["llm"] = {
                "module": self.llm.__module__,
                "class": self.llm.__class__.__name__,
                "model": self.llm.name,
            }
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)

    @classmethod
    def from_dynamic_route(
        cls, llm: BaseLLM, entities: List[Union[BaseModel, Callable]], route_name: str
    ):
        """
        Generate a dynamic Route object from a list of functions or Pydantic models using LLM
        """
        schemas = function_call.get_schema_list(items=entities)
        dynamic_route = cls._generate_dynamic_route(
            llm=llm, function_schemas=schemas, route_name=route_name
        )
        dynamic_route.function_schemas = schemas
        return dynamic_route

    @classmethod
    def _parse_route_config(cls, config: str) -> str:
        # Regular expression to match content inside <config></config>
        config_pattern = r"<config>(.*?)</config>"
        match = re.search(config_pattern, config, re.DOTALL)

        if match:
            config_content = match.group(1).strip()  # Get the matched content
            return config_content
        else:
            raise ValueError("No <config></config> tags found in the output.")

    @classmethod
    def _generate_dynamic_route(
        cls, llm: BaseLLM, function_schemas: List[Dict[str, Any]], route_name: str
    ):
        logger.info("Generating dynamic route...")

        formatted_schemas = "\n".join(
            [json.dumps(schema, indent=4) for schema in function_schemas]
        )
        prompt = f"""
        You are tasked to generate a single JSON configuration for multiple function schemas. 
        Each function schema should contribute five example utterances. 
        Please follow the template below, no other tokens allowed:

        <config>
        {{
            "name": "{route_name}",
            "utterances": [
                "<example_utterance_1>",
                "<example_utterance_2>",
                "<example_utterance_3>",
                "<example_utterance_4>",
                "<example_utterance_5>"]
        }}
        </config>

        Only include the "name" and "utterances" keys in your answer.
        The "name" should match the provided route name and the "utterances"
        should comprise a list of 5 example phrases for each function schema that could be used to invoke
        the functions. Use real values instead of placeholders.

        Input schemas:
        {formatted_schemas}
        """

        llm_input = [Message(role="user", content=prompt)]
        output = llm(llm_input)
        if not output:
            raise Exception("No output generated for dynamic route")

        route_config = cls._parse_route_config(config=output)

        logger.info(f"Generated route config:\n{route_config}")

        if is_valid(route_config):
            route_config_dict = json.loads(route_config)
            route_config_dict["llm"] = llm
            return Route.from_dict(route_config_dict)
        raise Exception("No config generated")


politics = Route(
    name="常识问题",
    utterances=[
        "怎么做西红柿炒鸡蛋",
        "地球是圆的吗",
        "如何修炼九阴真经",
        "李白的外号叫什么",
        "帮我写一篇500字的论文",
        "碳的化学式是什么",
        
    ],
)


chitchat = Route(
    name="检索问题",
    utterances=[
        "什么是SBOM",
        "软件供应链的定义是什么",
        "介绍一下融合4A系统",
        "Windows端的用户登录不上系统怎么办",
        "SBOM包含哪些组件",
    ],
)

routes = [politics, chitchat]
print(routes)

from semantic_router.encoders import HuggingFaceEncoder
encoder = HuggingFaceEncoder(name="/data/jiangyy/semantic/Qwen2-0.5B")

print(encoder)

# from semantic_router.layer import RouteLayer

# rl = RouteLayer(encoder=encoder, routes=routes)

# print(rl)

# print(rl("水的化学式是什么").name)


# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("/data/jiangyy/semantic/Qwen2-7B")
model = AutoModelForCausalLM.from_pretrained("/data/jiangyy/semantic/Qwen2-7B")

print(model)
print(11111111111111)
print(tokenizer)