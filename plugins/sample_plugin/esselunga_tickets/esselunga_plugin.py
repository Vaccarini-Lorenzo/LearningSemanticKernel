import requests
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from typing import Annotated


class EsselungaPlugin:
    """
    Description: EsselungaPlugin provides a set of functions to get esselunga receipts.

    """
    @kernel_function(name="GetReceipts", description="Gets all the receipts from esselunga (an italian supermarket)")
    def get_receipts(self) -> Annotated[str, "The esselunga receipts data"]:
        response = requests.get("http://localhost:8000/api/fetch_receipts")
        return response.json()
