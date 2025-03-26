# whatsapp_notifier/app.py

import datetime
import pywhatkit as kit
from flask import Flask, render_template, request, flash, redirect, url_for
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

        phone_number = re.sub(r"\D", "", phone_number)
        if phone_number.startswith("0"):
            phone_number = "+40" + phone_number[1:]
        elif not phone_number.startswith("+40"):
            phone_number = "+40" + phone_number

        print(f"[DEBUG] Formatted number: {phone_number}")

        message = (
            f"*Curățătoria Octavia Ecol Mangalia*\n\n"
            f"✅Bună ziua! Comanda cu numărul #{order_number} este gata de ridicare. Vă mulțumim!\n\n"
            f"🕑Program: Luni - Sâmbătă, 08:00 - 18:00"
        )

        now = datetime.datetime.now()
        target_time = now + datetime.timedelta(minutes=2)
        hour = target_time.hour
        minute = target_time.minute

        try:
            kit.sendwhatmsg(phone_number, message, hour, minute, wait_time=10, tab_close=True)
            flash("Mesaj WhatsApp trimis cu succes!", "success")
        except Exception as e:
            flash(f"Eroare la trimiterea mesajului: {e}", "danger")

        return redirect(url_for("index"))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
