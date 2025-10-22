from openai.types.chat import ChatCompletionMessageParam
from agere.commander import PASS_WORD, handler
from typing import Iterable, AsyncIterable
from agere.commander import PASS_WORD, Job, tasker
from agere.commander import CommanderAsync


class OpenaiHandler:
    """A handler for processing OpenAI responses"""

    def __init__(self, context: list[ChatCompletionMessageParam]):
        self.context = context
        self.available_functions = {"get_current_weather": get_current_weather}

    @handler(PASS_WORD)
    async def user_handler(self, self_handler, user_gen: AsyncIterable) -> None:
        """Handling the part of the message sent to the user by LLM

        Args:
            user_gen (AsyncIterable): A iterable object including the message to user.
        """
        message_list = []
        
        # Collect and print message.
        print("\n\033[31mGPT:\033[0m")
        async for char in user_gen:
            print(char, end='', flush=True)
            message_list.append(char)
        print("\n")
            
        # Save response to context.
        collected_message = ''.join(message_list)
        if collected_message:
            self.context.append({"role": "assistant", "content": collected_message})
    
    @handler(PASS_WORD)
    async def function_call_handler(self, self_handler, function_call_gen: AsyncIterable) -> None:
        """Handling the part of the message to call tools

        Args:
            function_call_gen (AsyncIterable): A iterable object including the message to call tools.
        """
        function_result_dict = {}
	
		# Complete the function call here and save the results in function_result_dict
        
        if not function_result_dict:
            return
			
        # send the function response to GPT
        messages = [
            {
                "tool_call_id": function_result["tool_call_id"],
                "role": "tool",
                "name": function_result["function_name"],
                "content": function_result["function_result"],
            } for function_result in function_result_dict.values()
        ]
		
        # add response to context
        self.context.append(
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {"id": one_function_call["tool_call_id"], "function": {"arguments": str(one_function_call["function_args"]), "name": one_function_call["function_name"]}, "type": "function"} for one_function_call in function_result_dict.values()
                ]
            }
        )
        self.context.extend(messages)
		
        try:
            response = await asyncio.to_thread(openai_chat, context=self.context)
        except Exception as e:
            raise e

        await self_handler.put_job(ResponseJob(response=response, context=self.context))
        
class ResponseHandler:
    """A handler to handle response from LLM"""
    def __init__(self, context: list[ChatCompletionMessageParam]):
        self.context = context

    @handler(PASS_WORD)
    async def handle_response(
        self,
        self_handler,
        response,
    ):
        """handler that handle response from LLM"""
        make_role_generator = await async_dispatcher_tools_call_for_openai(
            source=LLMAsyncAdapter().llm_to_async_iterable(response=response),
        )
        to_user_gen = make_role_generator("to_user")
        function_call_gen = make_role_generator("function_call")
        self_handler.call_handler(OpenaiHandler(self.context).user_handler(user_gen=to_user_gen))
        self_handler.call_handler(OpenaiHandler(self.context).function_call_handler(function_call_gen=function_call_gen))
        
class ChatJob(Job):
    def __init__(self, context: list[ChatCompletionMessageParam]):
        # context stores your conversation history and puts the message to be sent at the end
        self.context = context
        super().__init__()

    @tasker(PASS_WORD)
    async def task(self):
        response = openai_chat(context=self.context)
        job = ResponseJob(response=response, context=self.context)
        job.add_callback_functions(
            which="at_job_end",
            functions_info={
                "function": self.new_chat_callback,
                "inject_task_node": True
            },
        )
        await self.put_job(job)

    async def new_chat_callback(self, task_node: ChatJob):
        prompt = input("\033[32mYOU:\033[0m\n")
        if prompt == "exit":
            await self.exit_commander(return_result="QUIT")
            return
        self.context.append({"role": "user", "content": prompt})
        new_job = ChatJob(context=self.context)
        await task_node.put_job(job=new_job, parent=task_node.commander)
    
class ResponseJob(Job):
    def __init__(
        self,
        response: Iterable,
        context: list[ChatCompletionMessageParam],
    ):
        super().__init__()
        self.response = response
        self.context = context

    @tasker(PASS_WORD)
    async def task(self):
        handler = ResponseHandler(self.context).handle_response(response=self.response)
        return handler
    
if __name__ == "__main__":
    commander = CommanderAsync()
    context: list[ChatCompletionMessageParam] = []
    prompt = input("\033[32mYOU:\033[0m\n")
    if prompt == "exit":
        print("QUIT")
    else:
        context.append({"role": "user", "content": prompt})
        init_job = ChatJob(context)
        out = commander.run(init_job)
        print(out)