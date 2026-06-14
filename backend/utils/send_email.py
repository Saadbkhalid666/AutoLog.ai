import sib_api_v3_sdk
from configuration.config import Config
from sib_api_v3_sdk.rest import ApiException


def send_email(to_email, subject, html_content):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = Config.BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    sender = {
        "email": Config.SENDER_EMAIL,
        "name": "AutoLog.ai"
    }

    to = [
        {
            "email": to_email,
            "name": "User"
        }
    ]

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        sender=sender,
        to=to,
        subject=subject,
        html_content=html_content
    )

    try:
        response = api_instance.send_transac_email(send_smtp_email)
        print(f"Email sent successfully: {response}")
        return response

    except ApiException as e:
        print(f"Error sending email: {e}")
        return None