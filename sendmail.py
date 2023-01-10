from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
import smtplib

### Other way to send emails
from email.message import EmailMessage
from email.utils import make_msgid
import mimetypes
from email import encoders

import os



def send_mail(titulo, sender, email_to, message, attach_path):
    msg = EmailMessage()
    #msg = MIMEMultipart()

    # generic email headers
    msg['Subject'] = titulo
    msg['From'] = sender
    msg['To'] = email_to

    # set the plain text body
    msg.set_content(message)

    # now create a Content-ID for the image
    image_cid = make_msgid(domain='altaplazamall.com')
    # if `domain` argument isn't provided, it will 
    # use your computer's name

    # set an alternative html body
    msg.add_alternative("""
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
            <img src="cid:{image_cid}" width="100">
            <p></p>
            <p>Estimado Cliente:</p>
            <p>Adjuntamos a este correo su <strong>Factura</strong> correspondiente al mes corriente.</p>
            <p>Para cualquier consulta sobre este documento o sobre su estado de cuenta, le invitamos a que se comunique con nuestro departamento de Cuentas por Cobrar al Tel.: +(507) 830-7050 o nos escriba a: cobros@altaplazamall.com, donde con gusto le atenderemos.
            </p>
            {message}
            
            </div>
        </body>
    </html>
    """.format(message=message,image_cid=image_cid[1:-1]), subtype='html')
    # image_cid looks like <long.random.number@xyz.com>
    # to use it as the img src, we don't need `<` or `>`
    # so we use [1:-1] to strip them off


    # now open the image and attach it to the email
    

    with open('logo-light.png', 'rb') as img:

        # know the Content-Type of the image
        maintype, subtype = mimetypes.guess_type(img.name)[0].split('/')

        # attach it
        msg.get_payload()[1].add_related(img.read(), 
                                            maintype=maintype, 
                                            subtype=subtype, 
                                            cid=image_cid)
    
    
    #This is the part you had missed.
    #msg.attach( MIMEText(message) )

    #adjunto
    adjunto = MIMEBase('application', "octet-stream")
    adjunto.set_payload( open(attach_path,"rb").read() )
    encoders.encode_base64(adjunto)
    adjunto.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach_path))
    msg.attach(adjunto)


    # the message is ready now
    # you can write it to a file
    # or send it using smtplib
    sender_email = sender
    receiver_email = email_to
    session = smtplib.SMTP("smtp-relay.gmail.com", 587)  # use gmail with port
    session.starttls()  # enable security
    text = msg.as_string()
    session.sendmail(sender_email, receiver_email, text)
    session.quit()
    print("Mail Sent")