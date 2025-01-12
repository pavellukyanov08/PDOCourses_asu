from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime

# Task 1
private_key = ed25519.Ed25519PrivateKey.generate()
public_key = private_key.public_key()

password = b"my_secret_password"

with open("private_key.pem", 'wb') as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password)
    ))

with open("public_key.pem", 'wb') as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))


# Task 3
message = "Hi, I'm Pavel! I'm using asymmetric cryptography."

signature = private_key.sign(message.encode('utf-8'))

with open("signature.bin", 'wb') as f:
    f.write(signature)


# Task 4
with open("public_key.pem", 'rb') as f:
    public_key = serialization.load_pem_public_key(f.read())

with open("signature.bin", 'rb') as f:
    loaded_signature = f.read()

try:
    public_key.verify(loaded_signature, message.encode('utf-8'))
    print("Signature successfully verified.")
except Exception as e:
    print("Signature verification failed: ", e)



# Task 5
# data for CSR
subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "RU"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Altai Region"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Barnaul"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Altai State University"),
    x509.NameAttribute(NameOID.COMMON_NAME, "my_asu.ru"),
])

# creating CSR
csr = x509.CertificateSigningRequestBuilder().subject_name(subject).sign(
    private_key, algorithm=None
)

with open("csr.pem", 'wb') as f:
    f.write(csr.public_bytes(serialization.Encoding.PEM))


