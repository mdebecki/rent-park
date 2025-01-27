from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import re

# Inicjalizacja aplikacji Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Inicjalizacja Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Mock bazy danych użytkowników
users_db = {
    "user@example.com": {"password": "Password@123", "id": "1"}
}

# Model użytkownika
class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email

# Funkcja do ładowania użytkownika po ID
@login_manager.user_loader
def load_user(user_id):
    for email, user_data in users_db.items():
        if user_data['id'] == user_id:
            return User(id=user_data['id'], email=email)
    return None

# Helper: sprawdzanie poprawności email
def is_valid_email(email):
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(email_regex, email)

# Helper: sprawdzanie bezpieczeństwa hasła
def is_secure_password(password):
    password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(password_regex, password)

# Strona główna
@app.route('/')
def home():
    return render_template('home.html', title="Home", current_user=current_user)

# Logowanie
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Walidacja danych logowania
        if not is_valid_email(email):
            flash('Invalid email address', 'danger')
            return render_template('login.html', title="Login")
        if not is_secure_password(password):
            flash('Password does not meet security requirements', 'danger')
            return render_template('login.html', title="Login")

        # Sprawdzenie danych logowania
        user_data = users_db.get(email)
        if user_data and user_data['password'] == password:
            user = User(id=user_data['id'], email=email)
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', title="Login")

# Rejestracja
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Walidacja email i hasła
        if not is_valid_email(email):
            flash('Invalid email address', 'danger')
            return render_template('register.html', title="Register")
        if not is_secure_password(password):
            flash('Password does not meet security requirements', 'danger')
            return render_template('register.html', title="Register")

        # Sprawdzanie, czy użytkownik już istnieje
        if email in users_db:
            flash('Email already registered', 'danger')
            return render_template('register.html', title="Register")

        # Rejestracja użytkownika
        users_db[email] = {"password": password, "id": str(len(users_db) + 1)}
        flash('Registered successfully! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title="Register")

# Rezerwacja miejsca parkingowego
@app.route('/reservation', methods=['GET', 'POST'])
@login_required
def reservation():
    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        spot = request.form.get('spot')

        # Przykład obsługi rezerwacji
        flash(f'Reservation confirmed for spot {spot} on {date} at {time}.', 'success')
        return redirect(url_for('home'))

    return render_template('reservation.html', title="Reservation", current_user=current_user)

# Strona FAQ
@app.route('/faq')
def faq():
    return render_template('faq.html', title="FAQ", current_user=current_user)

# Formularz kontaktowy
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Przykładowe zapisanie zgłoszenia
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('contact.html', title="Contact", current_user=current_user)

# Wylogowanie
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/account', methods=['GET'])
@login_required
def account():
    return render_template('account.html', title="Account", current_user=current_user)

# Uruchomienie aplikacji
if __name__ == '__main__':
    app.run(debug=True)
