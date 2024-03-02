import unittest
import boto3
import base64
from botocore.exceptions import ClientError
from moto import mock_secretsmanager
from src.aws_secrets import AWSSecretManager
from unittest import mock


class TestAWSSecretManager(unittest.TestCase):

    def setUp(self) -> None:
        pass

    @mock_secretsmanager
    def test_get_secret_success(self) -> None:
        # set up mock boto client resource
        conn = boto3.client("secretsmanager", region_name="eu-west-1")
        conn.create_secret(Name="my-secret", SecretString="totally-secret")
        # call custom class
        aws_object = AWSSecretManager("my-secret", "eu-west-1")
        aws_object.get_secret()

    @mock_secretsmanager
    def test_get_secret_wrong_secret_name(self) -> None:
        # set up mock boto client resource
        conn = boto3.client("secretsmanager", region_name="eu-west-1")
        conn.create_secret(Name="wrong-secret", SecretString="totally-secret")
        with self.assertRaises(ClientError):
            # call custom class
            aws_object = AWSSecretManager("my-secret", "eu-west-1")
            aws_object.get_secret()

    @mock_secretsmanager
    def test_get_secret_decryption_failure(self) -> None:
        # set up mock boto client resource
        conn = boto3.client("secretsmanager", region_name="eu-west-1")
        conn.create_secret(Name="my-secret",
                           SecretString="totally-secret")
        # call custom class
        aws_object = AWSSecretManager("my-secret", "eu-west-1")
        secret = aws_object.get_secret()
        self.assertNotEqual(None, secret)

    @mock_secretsmanager
    def test_get_secret_b64decode(self) -> None:
        # base64 encode secret string
        secret = "totally-secret"
        secret_bytes = secret.encode('ascii')
        base64_bytes = base64.b64encode(secret_bytes)
        # set up mock boto client resource
        conn = boto3.client("secretsmanager", region_name="eu-west-1")
        conn.create_secret(Name="my-secret", SecretBinary=base64_bytes)
        # call custom class
        aws_object = AWSSecretManager("my-secret", "eu-west-1")
        aws_object.get_secret()

    def test_get_secrets_invalid_request_exception(self):
        session = mock.Mock()
        client = mock.Mock()
        session.client = client
        client.get_secret_value.side_effect = ClientError(
            {
                'Error': {
                    'Code': 'InvalidRequestException',
                    'Message': 'The provided param/s are incorrect.',
                }
            },
            'GetSecret',
        )
        with self.assertRaises(ClientError):
            aws_object = AWSSecretManager("my-secret", "eu-west-1")
            aws_object.get_secret(session=session, client=client)


    def test_get_secrets_invalid_parameter_exception(self):
        session = mock.Mock()
        client = mock.Mock()
        session.client = client
        client.get_secret_value.side_effect = ClientError(
            {
                'Error': {
                    'Code': 'InvalidParameterException',
                    'Message': 'The provided param/s are incorrect.',
                }
            },
            'GetSecret',
        )
        with self.assertRaises(ClientError):
            aws_object = AWSSecretManager("my-secret", "eu-west-1")
            aws_object.get_secret(session=session, client=client)

    def test_get_secrets_decryption_failure_exception(self):
        session = mock.Mock()
        client = mock.Mock()
        session.client = client
        client.get_secret_value.side_effect = ClientError(
            {
                'Error': {
                    'Code': 'DecryptionFailure',
                    'Message': "The requested secret can't be decrypted using the "
                               "provided KMS key",
                }
            },
            'GetSecret',
        )
        with self.assertRaises(ClientError):
            aws_object = AWSSecretManager("my-secret", "eu-west-1")
            aws_object.get_secret(session=session, client=client)

    def test_get_secrets_internal_service_error_exception(self):
        session = mock.Mock()
        client = mock.Mock()
        session.client = client
        client.get_secret_value.side_effect = ClientError(
            {
                'Error': {
                    'Code': 'InternalServiceError',
                    'Message': "An error occurred on service side",
                }
            },
            'GetSecret',
        )
        with self.assertRaises(ClientError):
            aws_object = AWSSecretManager("my-secret", "eu-west-1")
            aws_object.get_secret(session=session, client=client)
