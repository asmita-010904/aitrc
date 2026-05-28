from flask import Flask, render_template, request
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_base64 = None
    user_url = ""

    if request.method == "POST":
        # Get the URL submitted by the user in the HTML form
        user_url = request.form.get("url_input")
        
        if user_url:
            # Configure and generate the QR Code
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(user_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save the image to a memory buffer instead of a physical file
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            
            # Convert the raw image bytes into a base64 text string
            # This lets us embed the image directly into HTML!
            qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Pass the image data and the user's input back to the template
    return render_template("index.html", qr_code=qr_base64, original_url=user_url)

if __name__ == "__main__":
    # debug=True automatically reloads the server when you change code
    app.run(debug=True)