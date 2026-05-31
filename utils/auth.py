from functools import wraps
from flask import session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password):
    """Hash a password for storing."""
    return generate_password_hash(password)


def verify_password(stored_hash, password):
    """Verify a password against a hash."""
    return check_password_hash(stored_hash, password)


def login_required(f):
    """Decorator for customer login required routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'customer_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator for admin login required routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Admin access required.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
