import qrcode
import io
import base64


def generate_qr_code(data):
    """Generate a QR code and return as base64 encoded image."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#4F46E5", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_base64


def generate_booking_qr(booking_id, event_name, customer_name, date):
    """Generate a QR code for a booking."""
    data = f"Booking ID: {booking_id}\nEvent: {event_name}\nCustomer: {customer_name}\nDate: {date}"
    return generate_qr_code(data)
