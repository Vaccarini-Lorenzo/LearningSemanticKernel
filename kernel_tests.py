from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings, AzureChatCompletion
from semantic_kernel.contents import ChatHistory, ChatMessageContent, AuthorRole, ImageContent
from semantic_kernel.planners import SequentialPlanner

class KernelTests:
    def __init__(self):
        self.kernel = Kernel()
        self.execution_settings = AzureChatPromptExecutionSettings()
        self.chat_completion_id = None
        self.plugin_dir = "./plugins"

    def link_azureoai_service(self, service_id, env_path):
        azure_chat_completion = AzureChatCompletion(
            service_id=service_id,
            env_file_path=env_path
        )
        self.kernel.add_service(azure_chat_completion)
        self.chat_completion_id = service_id

    def __getService__(self, service_id):
        return self.kernel.get_service(service_id)

    async def execute_simplest_test(self):
        chat_history = ChatHistory()
        chat_history.add_message(ChatMessageContent(
            role=AuthorRole.SYSTEM,
            content="Your name is Lorenzo"
        ))
        chat_history.add_message(ChatMessageContent(
            role=AuthorRole.USER,
            content="What's your name?"
        ))
        chat_completion_service = self.__getService__(self.chat_completion_id)
        model_response = await chat_completion_service.get_chat_message_content(
            chat_history=chat_history,
            settings=self.execution_settings
        )
        print(model_response)

    async def execute_image_content_test(self):
        chat_history = ChatHistory()
        chat_history.add_message(ChatMessageContent(
            role=AuthorRole.USER,
            content="What's the image content?",
            items=[
                # Doesn't work with SVGs
                ImageContent(uri="https://www.elegantthemes.com/blog/wp-content/uploads/2020/08/hello-world.png")
            ]
        ))
        chat_completion_service = self.__getService__(self.chat_completion_id)
        model_response = await chat_completion_service.get_chat_message_content(
            chat_history=chat_history,
            settings=self.execution_settings
        )
        print(model_response)

    async def execute_function_test(self, plugin_name, num, formatting):
        sample_plugins = self.kernel.add_plugin(parent_directory=self.plugin_dir, plugin_name=plugin_name)
        random_function = sample_plugins["random_numbers"]
        result = await self.kernel.invoke(random_function, num=num, formatting=formatting)
        print(result)

    async def execute_function_planner_test(self, service_id, query):
        planner = SequentialPlanner(self.kernel, service_id)
        sequential_plan = await planner.create_plan(goal=query)
        print("The plan's steps are:")
        for step in sequential_plan._steps:
            print(
                f"- {step.description.replace('.', '') if step.description else 'No description'} using {step.metadata.fully_qualified_name} with parameters: {step.parameters}"
            )



