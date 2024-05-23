from flask_mail import Message
from flask import current_app
from mail import mail  

def send_email(to, subject, content_body, attachment=None):
    try:
        with current_app.app_context():
            message = Message(subject=subject, recipients=[to], sender=current_app.config['MAIL_USERNAME'], html=content_body)

            if attachment:
                with current_app.open_resource(attachment) as fp:
                    message.html = fp.read()

            mail.send(message)

        return "Email sent successfully"
    except Exception as e:
        print(f"Error sending email: {e}")
        return f"Error sending email: {e}"