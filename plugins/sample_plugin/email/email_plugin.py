from semantic_kernel.functions.kernel_function_decorator import kernel_function
from typing import Annotated

class EmailPlugin:
    """
    Description: EmailPlugin provides a set of functions to send emails.

    Usage:
        kernel.import_plugin_from_object(EmailPlugin(), plugin_name="email")

    Examples:
        {{email.SendEmail}} => Sends an email with the provided subject and body.
    """

    @kernel_function(name="SendEmail", description="Given an e-mail and message body, send an e-email")
    def send_email(self, recipient: Annotated[str, "the recipient of the email"], body: Annotated[str, "the body of the email"]) -> Annotated[str, "the output is a string"]:
        """Sends an email with the provided subject and body."""
        print(f"Sending email to {recipient}, body: {body}")
        return f"Email sent with subject: {recipient} and body: {body}"

    @kernel_function(name="GetEmailAddress", description="Given a name, find the email address")
    def get_email_address(self, input: Annotated[str, "the name of the person"]):
        print("Fetching the email")
        email = ""
        if input == "Jane":
            email = "janedoe4321@example.com"
        elif input == "Paul":
            email = "paulsmith5678@example.com"
        elif input == "Mary":
            email = "maryjones8765@example.com"
        else:
            email = "johndoe1234@example.com"
        return email