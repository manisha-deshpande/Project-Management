import pyotp
import qrcode
import time

# Try to read the secret key from the file
try:
    with open("secret_key.txt", "r") as f:
        secret = f.read().strip()
# If the file doesn't exist, generate a new secret key and save it to the file
except FileNotFoundError:
    secret = pyotp.random_base32()
    with open("secret_key.txt", "w") as f:
        f.write(secret)

# Create a PyOTP object using the secret key
totp = pyotp.TOTP(secret)

# Generate the provisioning URI for the QR code
provisioning_uri = totp.provisioning_uri("user@example.com", issuer_name="MyApp")

# Print the provisioning URI
print("Provisioning URI: ", provisioning_uri)

# Create a QR code object
qr = qrcode.QRCode(version=None, box_size=10, border=4)

# Add the provisioning URI to the QR code
qr.add_data(provisioning_uri)

# Generate the QR code image
qr.make(fit=True)

# Print the QR code as ASCII art
qr.print_ascii()

# Wait for the user to set up their authenticator app and enter a code
code = input("Enter the code from your authenticator app: ")

# Verify the code
if totp.verify(code):
    print("Authentication successful!")
else:
    print("Authentication failed.")
