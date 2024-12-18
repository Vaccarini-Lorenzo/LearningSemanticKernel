import asyncio

from kernel_tests import KernelTests


async def main():
    kernel_tests = KernelTests()
    service_id = "azureoai_test_id"
    kernel_tests.link_azureoai_service(service_id, ".env")
    kernel_tests.add_plugins()
    # await kernel_tests.run_text_content()
    # await kernel_tests.run_image_content()
    # await kernel_tests.run_rand_function("10", "{num_0; num_1; ... num_n}")
    # await kernel_tests.run_planner("How can I generate 10 random numbers and send them via email?")
    # await kernel_tests.execute_planner("Generate 10 random numbers and send them via email")
    await kernel_tests.execute_planner_auto_invocation()
# Run the main function
if __name__ == "__main__":
    asyncio.run(main())