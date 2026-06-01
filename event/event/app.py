"""
Event Management System - Main Flask Application
"""
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from config import Config
from utils.db import execute_query
from utils.auth import hash_password, verify_password, login_required, admin_required
from utils.qr_generator import generate_booking_qr
from utils.email_service import init_mail, send_booking_confirmation, send_payment_receipt
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY
init_mail(app)


# ============================================
#  PUBLIC ROUTES
# ============================================

@app.route('/')
def home():
    upcoming_events = execute_query(
        "SELECT * FROM Event WHERE Date >= CURDATE() ORDER BY Date ASC LIMIT 6"
    ) or []
    total_events = (execute_query("SELECT COUNT(*) as c FROM Event") or [{'c': 0}])[0]['c']
    total_customers = (execute_query("SELECT COUNT(*) as c FROM Customer") or [{'c': 0}])[0]['c']
    total_bookings = (execute_query("SELECT COUNT(*) as c FROM Booking") or [{'c': 0}])[0]['c']
    total_venues = (execute_query("SELECT COUNT(*) as c FROM Venue") or [{'c': 0}])[0]['c']
    return render_template('home.html',
                           upcoming_events=upcoming_events,
                           total_events=total_events,
                           total_customers=total_customers,
                           total_bookings=total_bookings,
                           total_venues=total_venues)


@app.route('/events')
def events():
    query = "SELECT * FROM Event WHERE 1=1"
    params = []
    search = request.args.get('search', '')
    etype = request.args.get('type', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    if search:
        query += " AND (Event_Name LIKE %s OR Location LIKE %s)"
        params.extend([f'%{search}%', f'%{search}%'])
    if etype:
        query += " AND Type = %s"
        params.append(etype)
    if date_from:
        query += " AND Date >= %s"
        params.append(date_from)
    if date_to:
        query += " AND Date <= %s"
        params.append(date_to)
    query += " ORDER BY Date ASC"
    all_events = execute_query(query, params) or []
    return render_template('customer/events.html', events=all_events)


@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = execute_query("SELECT * FROM Event WHERE E_ID = %s", (event_id,))
    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('events'))
    event = event[0]
    organizer = execute_query("SELECT * FROM Organizer WHERE O_ID = %s", (event.get('O_ID'),))
    organizer = organizer[0] if organizer else None
    venue = execute_query("SELECT * FROM Venue WHERE V_ID = %s", (event.get('V_ID'),))
    venue = venue[0] if venue else None
    return render_template('customer/event_detail.html', event=event, organizer=organizer, venue=venue)


@app.route('/contact')
def contact():
    return render_template('contact.html')


# ============================================
#  AUTHENTICATION
# ============================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'customer')

        if role == 'admin':
            admin = execute_query("SELECT * FROM Admin WHERE Username = %s", (email,))
            if admin and verify_password(admin[0]['Password'], password):
                session['admin_id'] = admin[0]['A_ID']
                session['admin_name'] = admin[0]['Username']
                flash('Welcome back, Admin!', 'success')
                return redirect(url_for('admin_dashboard'))
            flash('Invalid admin credentials.', 'danger')
        else:
            customer = execute_query("SELECT * FROM Customer WHERE Email = %s", (email,))
            if customer and verify_password(customer[0]['Password'], password):
                session['customer_id'] = customer[0]['C_ID']
                session['customer_name'] = customer[0]['Name']
                session['customer_email'] = customer[0]['Email']
                flash(f'Welcome back, {customer[0]["Name"]}!', 'success')
                return redirect(url_for('customer_dashboard'))
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))

        existing = execute_query("SELECT C_ID FROM Customer WHERE Email = %s", (email,))
        if existing:
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))

        hashed = hash_password(password)
        execute_query(
            "INSERT INTO Customer (Name, Phone, Email, Address, Password) VALUES (%s, %s, %s, %s, %s)",
            (name, phone, email, address, hashed), fetch=False
        )
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))


# ============================================
#  CUSTOMER ROUTES
# ============================================

@app.route('/customer/dashboard')
@login_required
def customer_dashboard():
    cid = session['customer_id']
    total = (execute_query("SELECT COUNT(*) as c FROM Booking WHERE C_ID=%s", (cid,)) or [{'c': 0}])[0]['c']
    confirmed = (execute_query("SELECT COUNT(*) as c FROM Booking WHERE C_ID=%s AND Status='Confirmed'", (cid,)) or [{'c': 0}])[0]['c']
    spent = (execute_query("SELECT COALESCE(SUM(Amount),0) as s FROM Payment p JOIN Booking b ON p.B_ID=b.B_ID WHERE b.C_ID=%s", (cid,)) or [{'s': 0}])[0]['s']
    recent = execute_query(
        "SELECT b.*, e.Event_Name FROM Booking b JOIN Event e ON b.E_ID=e.E_ID WHERE b.C_ID=%s ORDER BY b.Date DESC LIMIT 5",
        (cid,)
    ) or []
    stats = {'total_bookings': total, 'confirmed': confirmed, 'total_spent': float(spent)}
    return render_template('customer/dashboard.html', stats=stats, recent_bookings=recent)


@app.route('/customer/book/<int:event_id>', methods=['GET', 'POST'])
@login_required
def book_event(event_id):
    event = execute_query("SELECT * FROM Event WHERE E_ID = %s", (event_id,))
    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('events'))
    event = event[0]

    if request.method == 'POST':
        bid = execute_query(
            "INSERT INTO Booking (C_ID, E_ID, Amount, Status) VALUES (%s, %s, %s, 'Pending')",
            (session['customer_id'], event_id, event['Price']), fetch=False
        )
        if bid:
            # Try sending email (won't fail if SMTP not configured)
            try:
                send_booking_confirmation(
                    session.get('customer_email', ''),
                    session.get('customer_name', ''),
                    event['Event_Name'], bid,
                    str(event['Date'])
                )
            except Exception:
                pass
            flash('Event booked successfully! Please complete payment.', 'success')
            return redirect(url_for('payment', booking_id=bid))
        flash('Booking failed. Try again.', 'danger')
    return redirect(url_for('event_detail', event_id=event_id))


@app.route('/customer/bookings')
@login_required
def my_bookings():
    bookings = execute_query(
        "SELECT b.*, e.Event_Name FROM Booking b JOIN Event e ON b.E_ID=e.E_ID WHERE b.C_ID=%s ORDER BY b.Date DESC",
        (session['customer_id'],)
    ) or []
    return render_template('customer/my_bookings.html', bookings=bookings)


@app.route('/customer/payment/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def payment(booking_id):
    booking = execute_query(
        "SELECT b.*, e.Event_Name FROM Booking b JOIN Event e ON b.E_ID=e.E_ID WHERE b.B_ID=%s AND b.C_ID=%s",
        (booking_id, session['customer_id'])
    )
    if not booking:
        flash('Booking not found.', 'danger')
        return redirect(url_for('my_bookings'))
    booking = booking[0]

    if request.method == 'POST':
        mode = request.form.get('mode', 'Cash')
        execute_query(
            "INSERT INTO Payment (B_ID, Amount, Mode) VALUES (%s, %s, %s)",
            (booking_id, booking['Amount'], mode), fetch=False
        )
        execute_query("UPDATE Booking SET Status='Confirmed' WHERE B_ID=%s", (booking_id,), fetch=False)
        try:
            send_payment_receipt(
                session.get('customer_email', ''),
                session.get('customer_name', ''),
                str(booking['Amount']), mode, booking['Event_Name']
            )
        except Exception:
            pass
        flash('Payment successful! Booking confirmed.', 'success')
        return redirect(url_for('my_bookings'))
    return render_template('customer/payment.html', booking=booking)


@app.route('/customer/payments')
@login_required
def payment_history():
    payments = execute_query(
        """SELECT p.*, e.Event_Name FROM Payment p
           JOIN Booking b ON p.B_ID=b.B_ID
           JOIN Event e ON b.E_ID=e.E_ID
           WHERE b.C_ID=%s ORDER BY p.Date DESC""",
        (session['customer_id'],)
    ) or []
    return render_template('customer/payment_history.html', payments=payments)


@app.route('/customer/booking/qr/<int:booking_id>')
@login_required
def booking_qr(booking_id):
    booking = execute_query(
        "SELECT b.*, e.Event_Name FROM Booking b JOIN Event e ON b.E_ID=e.E_ID WHERE b.B_ID=%s AND b.C_ID=%s",
        (booking_id, session['customer_id'])
    )
    if not booking:
        flash('Booking not found.', 'danger')
        return redirect(url_for('my_bookings'))
    booking = booking[0]
    qr_base64 = generate_booking_qr(
        booking_id, booking['Event_Name'],
        session.get('customer_name', ''), str(booking.get('Date', ''))
    )
    return f'''<html><body style="display:flex;justify-content:center;align-items:center;min-height:100vh;background:#f8fafc;flex-direction:column;font-family:Inter,sans-serif;">
    <h2>Booking #{booking_id} - {booking["Event_Name"]}</h2>
    <img src="data:image/png;base64,{qr_base64}" style="margin:20px;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,0.1);">
    <p>Scan this QR code at the event entrance</p>
    <a href="{url_for("my_bookings")}" style="color:#4F46E5;">← Back to Bookings</a>
    </body></html>'''


# ============================================
#  ADMIN ROUTES
# ============================================

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    stats = {
        'total_events': (execute_query("SELECT COUNT(*) as c FROM Event") or [{'c': 0}])[0]['c'],
        'total_customers': (execute_query("SELECT COUNT(*) as c FROM Customer") or [{'c': 0}])[0]['c'],
        'total_bookings': (execute_query("SELECT COUNT(*) as c FROM Booking") or [{'c': 0}])[0]['c'],
        'total_revenue': float((execute_query("SELECT COALESCE(SUM(Amount),0) as s FROM Payment") or [{'s': 0}])[0]['s']),
    }
    recent_bookings = execute_query(
        """SELECT b.*, e.Event_Name, c.Name as Customer_Name
           FROM Booking b JOIN Event e ON b.E_ID=e.E_ID JOIN Customer c ON b.C_ID=c.C_ID
           ORDER BY b.Date DESC LIMIT 10"""
    ) or []

    # Revenue data by month
    rev = execute_query(
        "SELECT DATE_FORMAT(Date, '%%b') as month, SUM(Amount) as total FROM Payment GROUP BY DATE_FORMAT(Date, '%%Y-%%m') ORDER BY MIN(Date)"
    ) or []
    revenue_labels = [r['month'] for r in rev] or ['Jan', 'Feb', 'Mar']
    revenue_data = [float(r['total']) for r in rev] or [0, 0, 0]

    # Bookings by type
    bt = execute_query(
        "SELECT e.Type, COUNT(*) as cnt FROM Booking b JOIN Event e ON b.E_ID=e.E_ID GROUP BY e.Type"
    ) or []
    booking_labels = [b['Type'] for b in bt] or ['None']
    booking_data = [b['cnt'] for b in bt] or [0]

    return render_template('admin/dashboard.html',
                           stats=stats, recent_bookings=recent_bookings,
                           active_page='dashboard',
                           revenue_labels=revenue_labels, revenue_data=revenue_data,
                           booking_labels=booking_labels, booking_data=booking_data)


# ---- Events CRUD ----
@app.route('/admin/events', methods=['GET', 'POST'])
@admin_required
def admin_events():
    if request.method == 'POST':
        execute_query(
            """INSERT INTO Event (Event_Name, Date, Time, Location, Type, Description, Image, Price, O_ID, V_ID)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (request.form['event_name'], request.form['date'], request.form['time'],
             request.form.get('location'), request.form.get('type'), request.form.get('description'),
             request.form.get('image'), request.form.get('price', 0),
             request.form.get('o_id') or None, request.form.get('v_id') or None),
            fetch=False
        )
        flash('Event created successfully!', 'success')
        return redirect(url_for('admin_events'))

    events = execute_query(
        "SELECT e.*, v.Name as Venue_Name FROM Event e LEFT JOIN Venue v ON e.V_ID=v.V_ID ORDER BY e.Date DESC"
    ) or []
    organizers = execute_query("SELECT * FROM Organizer") or []
    venues = execute_query("SELECT * FROM Venue") or []
    return render_template('admin/events.html', events=events, organizers=organizers, venues=venues)


@app.route('/admin/events/edit/<int:eid>', methods=['POST'])
@admin_required
def admin_edit_event(eid):
    execute_query(
        """UPDATE Event SET Event_Name=%s, Date=%s, Time=%s, Location=%s, Type=%s,
           Description=%s, Price=%s, O_ID=%s, V_ID=%s WHERE E_ID=%s""",
        (request.form['event_name'], request.form['date'], request.form['time'],
         request.form.get('location'), request.form.get('type'), request.form.get('description'),
         request.form.get('price', 0),
         request.form.get('o_id') or None, request.form.get('v_id') or None, eid),
        fetch=False
    )
    flash('Event updated!', 'success')
    return redirect(url_for('admin_events'))


@app.route('/admin/events/delete/<int:eid>')
@admin_required
def admin_delete_event(eid):
    execute_query("DELETE FROM Event WHERE E_ID=%s", (eid,), fetch=False)
    flash('Event deleted.', 'success')
    return redirect(url_for('admin_events'))


# ---- Organizers CRUD ----
@app.route('/admin/organizers', methods=['GET', 'POST'])
@admin_required
def admin_organizers():
    if request.method == 'POST':
        execute_query(
            "INSERT INTO Organizer (Name, Contact, Email) VALUES (%s,%s,%s)",
            (request.form['name'], request.form.get('contact'), request.form.get('email')), fetch=False
        )
        flash('Organizer added!', 'success')
        return redirect(url_for('admin_organizers'))
    organizers = execute_query("SELECT * FROM Organizer ORDER BY O_ID DESC") or []
    return render_template('admin/organizers.html', organizers=organizers)


@app.route('/admin/organizers/edit/<int:oid>', methods=['POST'])
@admin_required
def admin_edit_organizer(oid):
    execute_query(
        "UPDATE Organizer SET Name=%s, Contact=%s, Email=%s WHERE O_ID=%s",
        (request.form['name'], request.form.get('contact'), request.form.get('email'), oid), fetch=False
    )
    flash('Organizer updated!', 'success')
    return redirect(url_for('admin_organizers'))


@app.route('/admin/organizers/delete/<int:oid>')
@admin_required
def admin_delete_organizer(oid):
    execute_query("DELETE FROM Organizer WHERE O_ID=%s", (oid,), fetch=False)
    flash('Organizer deleted.', 'success')
    return redirect(url_for('admin_organizers'))


# ---- Venues CRUD ----
@app.route('/admin/venues', methods=['GET', 'POST'])
@admin_required
def admin_venues():
    if request.method == 'POST':
        execute_query(
            "INSERT INTO Venue (Name, Address, Capacity, Availability) VALUES (%s,%s,%s,%s)",
            (request.form['name'], request.form.get('address'), request.form.get('capacity'),
             request.form.get('availability', 'Available')), fetch=False
        )
        flash('Venue added!', 'success')
        return redirect(url_for('admin_venues'))
    venues = execute_query("SELECT * FROM Venue ORDER BY V_ID DESC") or []
    return render_template('admin/venues.html', venues=venues)


@app.route('/admin/venues/edit/<int:vid>', methods=['POST'])
@admin_required
def admin_edit_venue(vid):
    execute_query(
        "UPDATE Venue SET Name=%s, Address=%s, Capacity=%s, Availability=%s WHERE V_ID=%s",
        (request.form['name'], request.form.get('address'), request.form.get('capacity'),
         request.form.get('availability'), vid), fetch=False
    )
    flash('Venue updated!', 'success')
    return redirect(url_for('admin_venues'))


@app.route('/admin/venues/delete/<int:vid>')
@admin_required
def admin_delete_venue(vid):
    execute_query("DELETE FROM Venue WHERE V_ID=%s", (vid,), fetch=False)
    flash('Venue deleted.', 'success')
    return redirect(url_for('admin_venues'))


# ---- Staff CRUD ----
@app.route('/admin/staff', methods=['GET', 'POST'])
@admin_required
def admin_staff():
    if request.method == 'POST':
        action = request.form.get('action', 'add')
        if action == 'assign':
            try:
                execute_query(
                    "INSERT INTO Event_Staff (E_ID, S_ID) VALUES (%s, %s)",
                    (request.form['e_id'], request.form['s_id']), fetch=False
                )
                flash('Staff assigned to event!', 'success')
            except Exception:
                flash('Staff already assigned to this event.', 'warning')
        else:
            execute_query(
                "INSERT INTO Staff (Name, Role, Salary, Contact) VALUES (%s,%s,%s,%s)",
                (request.form['name'], request.form.get('role'), request.form.get('salary'),
                 request.form.get('contact')), fetch=False
            )
            flash('Staff member added!', 'success')
        return redirect(url_for('admin_staff'))
    staff = execute_query("SELECT * FROM Staff ORDER BY S_ID DESC") or []
    events = execute_query("SELECT E_ID, Event_Name FROM Event ORDER BY Date DESC") or []
    return render_template('admin/staff.html', staff=staff, events=events)


@app.route('/admin/staff/edit/<int:sid>', methods=['POST'])
@admin_required
def admin_edit_staff(sid):
    execute_query(
        "UPDATE Staff SET Name=%s, Role=%s, Salary=%s, Contact=%s WHERE S_ID=%s",
        (request.form['name'], request.form.get('role'), request.form.get('salary'),
         request.form.get('contact'), sid), fetch=False
    )
    flash('Staff updated!', 'success')
    return redirect(url_for('admin_staff'))


@app.route('/admin/staff/delete/<int:sid>')
@admin_required
def admin_delete_staff(sid):
    execute_query("DELETE FROM Staff WHERE S_ID=%s", (sid,), fetch=False)
    flash('Staff deleted.', 'success')
    return redirect(url_for('admin_staff'))


# ---- Admin Bookings / Payments View ----
@app.route('/admin/bookings')
@admin_required
def admin_bookings():
    bookings = execute_query(
        """SELECT b.*, e.Event_Name, c.Name as Customer_Name
           FROM Booking b JOIN Event e ON b.E_ID=e.E_ID JOIN Customer c ON b.C_ID=c.C_ID
           ORDER BY b.Date DESC"""
    ) or []
    return render_template('admin/bookings.html', bookings=bookings)


@app.route('/admin/payments')
@admin_required
def admin_payments():
    payments = execute_query(
        """SELECT p.*, e.Event_Name, c.Name as Customer_Name
           FROM Payment p JOIN Booking b ON p.B_ID=b.B_ID
           JOIN Event e ON b.E_ID=e.E_ID JOIN Customer c ON b.C_ID=c.C_ID
           ORDER BY p.Date DESC"""
    ) or []
    return render_template('admin/payments.html', payments=payments)


# ---- Reports ----
@app.route('/admin/reports')
@admin_required
def admin_reports():
    stats = {
        'total_events': (execute_query("SELECT COUNT(*) as c FROM Event") or [{'c': 0}])[0]['c'],
        'total_revenue': float((execute_query("SELECT COALESCE(SUM(Amount),0) as s FROM Payment") or [{'s': 0}])[0]['s']),
        'total_bookings': (execute_query("SELECT COUNT(*) as c FROM Booking") or [{'c': 0}])[0]['c'],
        'total_staff': (execute_query("SELECT COUNT(*) as c FROM Staff") or [{'c': 0}])[0]['c'],
    }

    rev = execute_query(
        "SELECT DATE_FORMAT(Date, '%%b') as month, SUM(Amount) as total FROM Payment GROUP BY DATE_FORMAT(Date, '%%Y-%%m') ORDER BY MIN(Date)"
    ) or []
    revenue_labels = [r['month'] for r in rev] or ['Jan']
    revenue_data = [float(r['total']) for r in rev] or [0]

    bt = execute_query(
        "SELECT e.Type, COUNT(*) as cnt FROM Booking b JOIN Event e ON b.E_ID=e.E_ID GROUP BY e.Type"
    ) or []
    booking_labels = [b['Type'] for b in bt] or ['None']
    booking_data = [b['cnt'] for b in bt] or [0]

    mb = execute_query(
        "SELECT DATE_FORMAT(Date, '%%b') as month, COUNT(*) as cnt FROM Booking GROUP BY DATE_FORMAT(Date, '%%Y-%%m') ORDER BY MIN(Date)"
    ) or []
    monthly_labels = [m['month'] for m in mb] or ['Jan']
    monthly_data = [m['cnt'] for m in mb] or [0]

    staff_report = execute_query(
        """SELECT s.Name, s.Role, COUNT(es.E_ID) as event_count
           FROM Staff s LEFT JOIN Event_Staff es ON s.S_ID=es.S_ID
           GROUP BY s.S_ID ORDER BY event_count DESC"""
    ) or []

    return render_template('admin/reports.html',
                           stats=stats, staff_report=staff_report,
                           revenue_labels=revenue_labels, revenue_data=revenue_data,
                           booking_labels=booking_labels, booking_data=booking_data,
                           monthly_labels=monthly_labels, monthly_data=monthly_data)


# ============================================
#  SETUP ADMIN HELPER
# ============================================
@app.route('/setup-admin')
def setup_admin():
    """One-time admin account setup. Visit /setup-admin to create the default admin."""
    existing = execute_query("SELECT * FROM Admin WHERE Username='admin'")
    if existing:
        # Update password
        execute_query(
            "UPDATE Admin SET Password=%s WHERE Username='admin'",
            (hash_password('admin123'),), fetch=False
        )
        return "Admin password reset to: admin123"
    execute_query(
        "INSERT INTO Admin (Username, Password) VALUES (%s, %s)",
        ('admin', hash_password('admin123')), fetch=False
    )
    return "Admin account created! Username: admin, Password: admin123"


# ============================================
#  RUN
# ============================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)
