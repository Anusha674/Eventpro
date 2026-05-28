from flask_mail import Mail, Message

mail = Mail()


def init_mail(app):
    """Initialize Flask-Mail with the app."""
    mail.init_app(app)


def send_booking_confirmation(to_email, customer_name, event_name, booking_id, date):
    """Send booking confirmation email."""
    try:
        msg = Message(
            subject=f'Booking Confirmation - {event_name}',
            sender='noreply@eventmanager.com',
            recipients=[to_email]
        )
        msg.html = f"""
        <div style="font-family: 'Inter', sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #4F46E5, #7C3AED); padding: 30px; border-radius: 16px 16px 0 0; text-align: center;">
                <h1 style="color: white; margin: 0;">🎉 Booking Confirmed!</h1>
            </div>
            <div style="background: #fff; padding: 30px; border: 1px solid #e5e7eb; border-radius: 0 0 16px 16px;">
                <p>Dear <strong>{customer_name}</strong>,</p>
                <p>Your booking has been confirmed. Here are the details:</p>
                <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Booking ID</td><td style="padding: 8px; border-bottom: 1px solid #eee;">#{booking_id}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Event</td><td style="padding: 8px; border-bottom: 1px solid #eee;">{event_name}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Date</td><td style="padding: 8px; border-bottom: 1px solid #eee;">{date}</td></tr>
                </table>
                <p>Thank you for choosing our Event Management System!</p>
            </div>
        </div>
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False


def send_payment_receipt(to_email, customer_name, amount, payment_mode, event_name):
    """Send payment receipt email."""
    try:
        msg = Message(
            subject=f'Payment Receipt - {event_name}',
            sender='noreply@eventmanager.com',
            recipients=[to_email]
        )
        msg.html = f"""
        <div style="font-family: 'Inter', sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #059669, #10B981); padding: 30px; border-radius: 16px 16px 0 0; text-align: center;">
                <h1 style="color: white; margin: 0;">💳 Payment Successful!</h1>
            </div>
            <div style="background: #fff; padding: 30px; border: 1px solid #e5e7eb; border-radius: 0 0 16px 16px;">
                <p>Dear <strong>{customer_name}</strong>,</p>
                <p>Your payment has been received successfully.</p>
                <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Amount</td><td style="padding: 8px; border-bottom: 1px solid #eee;">₹{amount}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Mode</td><td style="padding: 8px; border-bottom: 1px solid #eee;">{payment_mode}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Event</td><td style="padding: 8px; border-bottom: 1px solid #eee;">{event_name}</td></tr>
                </table>
            </div>
        </div>
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
