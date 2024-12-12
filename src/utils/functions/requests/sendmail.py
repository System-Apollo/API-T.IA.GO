import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_welcome_email(user):
    """Envia e-mail de boas-vindas ao usuário registrado."""
    subject = "Bem-vindo ao TIAGO – Sua Nova Experiência em Inteligência Jurídica!"
    body = f"""
    Olá {user.username},

    É um prazer tê-lo(a) conosco.

    Gostaríamos de apresentar o TIAGO, sua nova solução de inteligência artificial para o setor jurídico:

    📜 Quem é o TIAGO?
    Com 32 anos, o TIAGO combina sua expertise como advogado com especialização em tecnologia da informação e análise 
    de dados. Ele está aqui para simplificar sua vida no setor jurídico e trazer inovação ao seu dia a dia.

    ✨ O que esperar?

    Atendimento amigável e personalizado.
    Soluções eficientes para seus desafios jurídicos.
    Suporte rápido e acessível sempre que você precisar.
    💡 Por que escolher o TIAGO?
    Moderno, simpático e intelectualmente curioso, o TIAGO é projetado para oferecer uma experiência fluida, ajudando você 
    a focar no que realmente importa enquanto ele cuida das análises e respostas de forma precisa.

    Estamos felizes em tê-lo(a) como parte da nossa comunidade. Se tiver dúvidas ou precisar de ajuda, conte conosco – o TIAGO 
    está sempre por aqui para facilitar sua vida!

    Atenciosamente,
    Equipe MF DIGITAL LAW
    Sua experiência inteligente no setor jurídico
    """
    send_email(to=user.email, subject=subject, body=body)

def send_email(to, subject, body):
    sender_email = os.getenv("CREDENCIAL_GMAIL_USER")
    sender_password =  os.getenv("CREDENCIAL_GMAIL_USER")  # Use variáveis de ambiente para armazenar isso com segurança.

    # Configuração do servidor SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Criar o e-mail
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Enviar o e-mail
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to, msg.as_string())
