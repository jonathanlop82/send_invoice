import os
import shutil
import pandas as pd
from check_email import check

from sendmail import send_mail
from sendmail2 import send_mail2

import datetime as dt

csv_file = pd.read_csv('db_clients.csv', encoding= 'unicode_escape')

clients_data = pd.DataFrame(csv_file, columns=['Clave','Nombre','Tipo','RUC','Nombre Corto','Correo electronico','Correo electronico 2'])

clientes_sin_correo = clients_data[clients_data['Correo electronico'].isna()]
clientes_sin_correo.to_excel(r'sin_email.xlsx', index=False)

invoice_list = os.listdir('test_invoice')

clientes_sin_email = []
f = open("enviados.txt", "w+")
for invoice in invoice_list:
    client_code = invoice.split("_")[0]
    nombre = clients_data['Nombre'][ clients_data['Clave'] == client_code ].item()
    email1 = clients_data['Correo electronico'][ clients_data['Clave'] == client_code ].item()
    email2 = clients_data['Correo electronico 2'][ clients_data['Clave'] == client_code ].item()
    if email1:
        if check(str(email1)):
            if email2:
                if check(str(email2)):
                    email1 = f'{email1},{email2}'
            #print(f'Factura: {invoice} - Cliente: {client_code} - Nombre: {nombre} - Email: {email1}')
            print(f'Send Mail to { email1 }')
            date_time = dt.datetime.now()
            f.write(f'{date_time} | Send Mail to { email1 }\n')
            titulo = f'***COPIA*** Retail Centenario, S. A. - Factura - Mes: '
            sender = 'facturacion@altaplazamall.com'
            email_to = 'test@altaplazamall.com'
            message = ''
            attach_path = f"test_invoice/{invoice}"
            invoice_name = f'{invoice}'
            send_mail2(titulo, sender, email_to, message, invoice_name, attach_path)
            shutil.move(f"test_invoice/{invoice}", f"enviados/{invoice}")
        else:
            clientes_sin_email.append(f'Clave: {client_code} - Nombre: {nombre} - Email: {email1}')
    else:
        print('Ciente No Existe')
        input()
f.close()
print('CLIENTES SIN CORREO')
for cliente in clientes_sin_email:
    print(cliente)




