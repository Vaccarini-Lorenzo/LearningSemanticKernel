import asyncio

from kernel_tests import KernelTests


async def main():
    kernel_tests = KernelTests()
    kernel_tests.link_azureoai_service("azureoai_test_id", ".env")
    await kernel_tests.execute_simplest_test()
    await kernel_tests.execute_image_content_test()
# Run the main function
if __name__ == "__main__":
    asyncio.run(main())