from semantic_kernel import Kernel
from semantic_kernel.connectors.ai import PromptExecutionSettings, FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings, AzureChatCompletion
from semantic_kernel.contents import ChatHistory, ChatMessageContent, AuthorRole, ImageContent
from semantic_kernel.functions import KernelArguments
from semantic_kernel.planners import SequentialPlanner
from semantic_kernel.planners.function_calling_stepwise_planner import (
    FunctionCallingStepwisePlanner,
    FunctionCallingStepwisePlannerOptions,
)
from plugins.sample_plugin.email.email_plugin import EmailPlugin
from plugins.sample_plugin.esselunga_tickets.esselunga_plugin import EsselungaPlugin


class KernelTests:
    def __init__(self):
        self.kernel = Kernel()
        self.execution_settings = AzureChatPromptExecutionSettings()
        self.chat_completion_id = None
        self.plugins = None
        self.plugin_dir = "./plugins"

    def link_azureoai_service(self, service_id, env_path):
        azure_chat_completion = AzureChatCompletion(
            service_id=service_id,
            env_file_path=env_path
        )
        self.kernel.add_service(azure_chat_completion)
        self.chat_completion_id = service_id

    def add_plugins(self):
        self.plugins = []
        self.plugins.append(self.kernel.add_plugin(parent_directory=self.plugin_dir, plugin_name="sample_plugin"))
        self.plugins.append(self.kernel.add_plugin(plugin_name="EmailPlugin", plugin=EmailPlugin()))
        self.plugins.append(self.kernel.add_plugin(plugin_name="EsselungaPlugin", plugin=EsselungaPlugin()))

    def __getService__(self, service_id):
        return self.kernel.get_service(service_id)

    async def run_text_content(self):
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

    async def run_image_content(self):
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

    async def run_rand_function(self, num, formatting):
        random_function = self.plugins["random_numbers"]
        result = await self.kernel.invoke(random_function, num=num, formatting=formatting)
        print(result)

    async def run_planner(self, query):
        planner = SequentialPlanner(self.kernel, self.chat_completion_id)
        sequential_plan = await planner.create_plan(goal=query)
        print("The plan's steps are:")
        for step in sequential_plan._steps:
            print(
                f"- {step.description.replace('.', '') if step.description else 'No description'} using {step.metadata.fully_qualified_name} with parameters: {step.parameters}"
            )

    async def execute_planner(self, query):
        options = FunctionCallingStepwisePlannerOptions(
            max_iterations=10,
            max_tokens=4000,
        )
        planner = FunctionCallingStepwisePlanner(service_id=self.chat_completion_id, options=options)
        result = await planner.invoke(self.kernel, query)
        print(result)

    async def execute_planner_auto_invocation(self):
        execution_settings = AzureChatPromptExecutionSettings()
        execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

        chat_completion_service = self.__getService__(self.chat_completion_id)
        chat_history = ChatHistory()
        while True:
            query = input("> ")
            chat_history.add_message(ChatMessageContent(
                role=AuthorRole.USER,
                content=query
            ))
            model_response = await chat_completion_service.get_chat_message_content(
                chat_history=chat_history,
                settings=execution_settings,
                kernel=self.kernel
            )
            chat_history.add_message(ChatMessageContent(
                role=AuthorRole.ASSISTANT,
                content=str(model_response)
            ))
            print(model_response)

