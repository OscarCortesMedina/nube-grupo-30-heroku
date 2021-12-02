import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from constants.constants import EMAIL, EMAIL_PASS, EMAIL_TEST

sender_email = EMAIL
password = EMAIL_PASS

message = MIMEMultipart("alternative")
message["From"] = "Servicio de conversión Grupo 30"


def send_email(username, email, filename, in_extension, out_extension):
    receiver_email = [email]
    message["To"] = ", ".join(receiver_email)

    message["Subject"] = "Conversión de archivo completa"

    html = """
    <html>
<body>
    <h4>Usuario USERNAME, el archivo fue convertido de manera exitosa</h4>
    <p> Nombre del archivo: FILENAME<br>
        Extensión original: IN_EXTENSION<br>
        Extensión de salida: OUT_EXTENSIÓN<br>
    </p>
</body>
</html>
    """
    html = html.replace("USERNAME", username)
    html = html.replace("FILENAME", filename)
    html = html.replace("IN_EXTENSION", in_extension)
    html = html.replace("OUT_EXTENSIÓN", out_extension)

    part = MIMEText(html, "html")

    message.attach(part)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
            server.close()
    except Exception as e:
        print(e)
    finally:
        print("Email sent")


def send_email_tareas():
    receiver_email = [EMAIL_TEST]
    message["To"] = ", ".join(receiver_email)

    message["Subject"] = "Termino prueba de carga"

    html = """
    <html>
<body>
    <h1>Esto es una prueba</h1>
</body>
</html>
    """

    part = MIMEText(html, "html")

    message.attach(part)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
            server.close()
    except Exception as e:
        print(e)
    finally:
        print("Email sent")
