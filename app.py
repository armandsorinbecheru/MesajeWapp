import datetime
import pywhatkit as kit
from flask import Flask, render_template, request, flash, redirect
import re
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        order_number = request.form.get("order_number")
        phone_number = request.form.get("phone_number")

        if not order_number or not phone_number:
            flash("Introduceți numărul comenzii și numărul de telefon.", "danger")
            return redirect("/")

        # Format Romanian numbers to +40
        phone_number = re.sub(r"\D", "", phone_number)
        if phone_number.startswith("0"):
            phone_number = "+40" + phone_number[1:]
        elif not phone_number.startswith("+40"):
            phone_number = "+40" + phone_number

        print(f"[DEBUG] Formatted number: {phone_number}")

        message = (
            f"*Curățătoria Xxxxxxx XxxXxx*\n\n"
            f"Bună ziua! Comanda dvs. #{order_number} este gata de ridicare.\n"
            f"Program: Luni - Sâmbătă, 08:00 - 18:00"
        )

        try:
            now = datetime.datetime.now()
            hour = now.hour
            minute = now.minute + 1 if now.minute < 59 else 0
            if now.minute == 59:
                hour = (hour + 1) % 24

            kit.sendwhatmsg(phone_number, message, hour, minute, wait_time=10, tab_close=True)
            flash("Mesaj WhatsApp programat cu succes!", "success")
        except Exception as e:
            flash(f"Eroare la trimiterea mesajului: {e}", "danger")

        return redirect("/")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
