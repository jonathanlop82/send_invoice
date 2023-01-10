import email, smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from email import encoders
from email.mime.base import MIMEBase

from email.utils import make_msgid
import mimetypes


def send_mail2(titulo, sender, email_to, message, invoice_name, attach_path):

    sender_email = sender
    receiver_email = email_to
    #password = input("Type your password and press enter:")

    message = MIMEMultipart()
    message["Subject"] = titulo
    message["From"] = sender_email
    message["To"] = receiver_email
    #message["Cc"] = "soporte@altaplazamall.com"



    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""
    html = """\
    <html>
        <head>
            <style>
                div {
                        margin-top: 0%;
                        margin-bottom: 0%;
                        margin-right: 5%;
                        margin-left: 5%; }
                h1,h2, h3 {text-align: center;}
                table {text-align: center;}
                td { text-align: center;}
                p { font-family: sans-serif, Arial, Helvetica;
                    color:grey;
                    font-size: 16px;}
                #report { text-align: center;}
            </style>
        </head>
    """+"""
        <body>
            <div>
            <img src="cid:0" width="100">
            <p></p>
            <p>Estimado Cliente:</p>
            <p>Adjuntamos a este correo su <strong>Factura</strong> correspondiente al mes corriente.</p>
            <p>Para cualquier consulta sobre este documento o sobre su estado de cuenta, le invitamos a que se comunique con nuestro departamento de Cuentas por Cobrar al Tel.: +(507) 830-7050 o nos escriba a: cobros@altaplazamall.com, donde con gusto le atenderemos.
            </p>
            
            </div>
        </body>
    </html>
    """


    # Turn these into plain/html MIMEText objects
    # part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    #message.attach(part1)
    message.attach(part2)

    # Add body to email
    #message.attach(MIMEText(body, "plain"))

    # to add an attachment is just add a MIMEBase object to read a picture locally.
    with open('logo-light.png', 'rb') as f:
        # set attachment mime and file name, the image type is png
        mime = MIMEBase('image', 'png', filename='logo-light.png')
        # add required header data:
        mime.add_header('Content-Disposition', 'attachment', filename='logo-light.png')
        mime.add_header('X-Attachment-Id', '0')
        mime.add_header('Content-ID', '<0>')
        # read attachment file content into the MIMEBase object
        mime.set_payload(f.read())
        # encode with base64
        encoders.encode_base64(mime)
        # add MIMEBase object to MIMEMultipart object
        message.attach(mime)


    filename = attach_path # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {invoice_name}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    #with smtplib.SMTP("smtp-relay.gmail.com", 587, context=context) as server:
    with smtplib.SMTP("smtp-relay.gmail.com", 587) as server:
        #server.login(sender_email, password)
        server.starttls()
        server.sendmail(
            sender_email, receiver_email.split(','), text
        )