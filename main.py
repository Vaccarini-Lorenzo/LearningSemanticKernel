import asyncio

from kernel_tests import KernelTests


async def main():
    kernel_tests = KernelTests()
    service_id = "azureoai_test_id"
    kernel_tests.link_azureoai_service(service_id, ".env")
    # await kernel_tests.execute_simplest_test()
    # await kernel_tests.execute_image_content_test()

    # How can I invoke this function semantically??
    await kernel_tests.execute_function_test("sample_plugin", "10", "{num_0; num_1; ... num_n}")
    await kernel_tests.execute_function_planner_test(service_id, "How can I generate 100 random numbers? The formatting should be as such: '[num_0, num_1, ..., num_n]")
# Run the main function
if __name__ == "__main__":
    asyncio.run(main())