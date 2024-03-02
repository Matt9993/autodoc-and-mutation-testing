"""AWS Secrets management helper module."""
import base64
import logging

import boto3
from botocore.exceptions import ClientError


log = logging.getLogger(__name__)


class AWSSecretManager:
    """
    Class to represent an AWS Secrets Manager object.
    """

    def __init__(self, secret_name: str, region_name: str = "eu-west-1"):
        """
        Init method of the AWSSecretManager class.

        Args:
            secret_name (str): the AWS name or ARN of the secret
            to retrieve
            region_name (str): AWS region name to be used,
            default value: 'eu-west-1'
        """
        self.region_name = region_name
        self.secret_name = secret_name

    def get_secret(self, **kwargs) -> str:
        """
        Obtain a specific secret value from the AWS Secrets Manager.

        Uses the self.secret_name class property as an argument.
        given the secret name

        Returns:
            (str): Specific secret value from AWS Secrets Manager
        """
        session = boto3.session.Session() if not kwargs else kwargs["session"]
        secrets_client = session.client(
            service_name="secretsmanager", region_name=self.region_name
        ) if not kwargs else kwargs["client"]

        try:
            get_secret_value_response = secrets_client.get_secret_value(
                SecretId=self.secret_name, **kwargs
            )
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ResourceNotFoundException":
                log.warning(
                    "The requested secret "
                    + self.secret_name
                    + " was not found"
                )
                raise e
            elif error_code == "InvalidRequestException":
                log.warning("The request was invalid due to:", e.response["Error"])
                raise e
            elif error_code == "InvalidParameterException":
                log.warning("The request had invalid params:", e.response["Error"])
                raise e
            elif error_code == "DecryptionFailure":
                log.warning(
                    "The requested secret can't be decrypted using the "
                    "provided KMS key:",
                    e.response["Error"],
                )
                raise e
            elif error_code == "InternalServiceError":
                log.warning("An error occurred on service side:", e.response["Error"])
                raise e
        else:
            if "SecretString" in get_secret_value_response:
                secret_value = get_secret_value_response["SecretString"]

            else:
                secret_value = base64.b64decode(
                    get_secret_value_response["SecretBinary"]
                ).decode("ascii")

            return secret_value if secret_value else "No secret value was specified."
