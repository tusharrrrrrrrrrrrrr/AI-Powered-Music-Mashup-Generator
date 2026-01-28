from flask import Flask, request
from mashup_engine import create_mashup
import smtplib
from email.message import EmailMessage
import zipfile
import os

app = Flask(__name__)

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

@app.route("/")
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Mashup Generator</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gradient-to-br from-indigo-600 to-purple-700 min-h-screen flex items-center justify-center">

        <div class="bg-white shadow-2xl rounded-2xl p-10 w-full max-w-lg">
            <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">🎵 AI Mashup Generator</h1>

            <form method="post" action="/create" class="space-y-5">

                <div>
                    <label class="block text-gray-700 font-semibold mb-1">Singer Name</label>
                    <input name="singer" required
                        class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                        placeholder="e.g. Arijit Singh">
                </div>

                <div>
                    <label class="block text-gray-700 font-semibold mb-1">Number of Videos</label>
                    <input name="n" type="number" min="11" required
                        class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                        placeholder="Must be greater than 10">
                </div>

                <div>
                    <label class="block text-gray-700 font-semibold mb-1">Clip Duration (seconds)</label>
                    <input name="dur" type="number" min="21" required
                        class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                        placeholder="Must be greater than 20">
                </div>

                <div>
                    <label class="block text-gray-700 font-semibold mb-1">Your Email</label>
                    <input name="email" type="email" required
                        class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                        placeholder="example@gmail.com">
                </div>

                <button type="submit"
                    class="w-full bg-indigo-600 text-white font-bold py-2 rounded-lg hover:bg-indigo-700 transition duration-300">
                    🚀 Create Mashup
                </button>
            </form>
        </div>

    </body>
    </html>
    '''


@app.route("/create", methods=["POST"])
def create():
    singer = request.form["singer"]
    n = int(request.form["n"])
    dur = int(request.form["dur"])
    email = request.form["email"]
    ROLL_NO = "102303674"
    output_file = f"{ROLL_NO}.mp3"
    path = create_mashup(singer, n, dur, output_file)

    zip_path = f"output/{ROLL_NO}.zip"
    print("ZIP exists:", os.path.exists(zip_path))

    with zipfile.ZipFile(zip_path, 'w') as z:
        z.write(path, arcname=f"{ROLL_NO}.mp3")
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        return "Email credentials missing"
    
    send_email(email, zip_path)
    return "Mashup sent to email!"

def send_email(to, file_path):
    try:
        msg = EmailMessage()
        msg['Subject'] = "Your Mashup"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to
        msg.set_content("Mashup attached.")

        with open(file_path, 'rb') as f:
            msg.add_attachment(f.read(), maintype='application', subtype='zip', filename='mashup.zip')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("Email sent successfully!")

    except Exception as e:
        print("EMAIL ERROR:", e)


if __name__ == "__main__":
    app.run(debug=False)

