import generate_qr
url = "https://dc1b-189-139-112-223.ngrok-free.app"
qr = generate_qr.make(url)
qr.show()
qr.save("qrcode.png")
if (qr.save("qrcode.png")):
    print("QR code saved successfully.")
else:
    print("Failed to save QR code.")

#Fuction for overwrite the existing file


# This code generates a QR code for the specified URL and saves it as "qrcode.png".