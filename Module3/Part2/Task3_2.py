from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime
import random


def generate_base_certificate():
    """Создает базовый (самоподписанный) сертификат."""
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "RU"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Алтайский край"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Барнаул"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Base CA"),
        x509.NameAttribute(NameOID.COMMON_NAME, "baseca.example.com"),
    ])

    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(subject)
        .public_key(public_key)
        .serial_number(random.randint(1, 2**64))
        .not_valid_before(datetime.datetime.now(datetime.UTC))
        .not_valid_after(datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=365))
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=1), critical=True
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_cert_sign=True,
                crl_sign=True,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,  # Установлено явно
                encipher_only=False,
                decipher_only=False,
                content_commitment=False,
            ),
            critical=True,
        )
        .sign(private_key, hashes.SHA256())
    )

    # Сохранение ключа и сертификата
    with open("Module3/Part2/base_private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open("Module3/Part2/base_certificate.pem", "wb") as f:
        f.write(certificate.public_bytes(serialization.Encoding.PEM))

    return private_key, certificate


def generate_intermediate_certificate(base_key, base_cert):
    """Создает промежуточный сертификат, подписанный базовым."""
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "RU"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Москва"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Москва"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Intermediate CA"),
        x509.NameAttribute(NameOID.COMMON_NAME, "intermediateca.example.com"),
    ])

    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(base_cert.subject)
        .public_key(public_key)
        .serial_number(random.randint(1, 2**64))
        .not_valid_before(datetime.datetime.now(datetime.UTC))
        .not_valid_after(datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=365))
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=0), critical=True
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_cert_sign=True,
                crl_sign=True,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                encipher_only=False,
                decipher_only=False,
                content_commitment=False,
            ),
            critical=True,
        )
        .sign(base_key, hashes.SHA256())
    )

    with open("Module3/Part2/intermediate_private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open("Module3/Part2/intermediate_certificate.pem", "wb") as f:
        f.write(certificate.public_bytes(serialization.Encoding.PEM))

    return private_key, certificate


def generate_final_certificate(intermediate_key, intermediate_cert):
    """Создает конечный сертификат, подписанный промежуточным."""
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "RU"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Санкт-Петербург"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Санкт-Петербург"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Final User"),
        x509.NameAttribute(NameOID.COMMON_NAME, "finaluser.example.com"),
    ])

    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(intermediate_cert.subject)
        .public_key(public_key)
        .serial_number(random.randint(1, 2**64))
        .not_valid_before(datetime.datetime.now(datetime.UTC))
        .not_valid_after(datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=10))
        .add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_cert_sign=False,
                crl_sign=False,
                key_encipherment=True,
                data_encipherment=True,
                key_agreement=False,
                encipher_only=False,
                decipher_only=False,
                content_commitment=False,
            ),
            critical=True,
        )
        .sign(intermediate_key, hashes.SHA256())
    )

    with open("Module3/Part2/final_private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open("Module3/Part2/final_certificate.pem", "wb") as f:
        f.write(certificate.public_bytes(serialization.Encoding.PEM))

    return private_key, certificate


def main():
    base_key, base_cert = generate_base_certificate()
    intermediate_key, intermediate_cert = generate_intermediate_certificate(base_key, base_cert)
    final_key, final_cert = generate_final_certificate(intermediate_key, intermediate_cert)
    print("Сертификаты успешно созданы!")


if __name__ == "__main__":
    main()