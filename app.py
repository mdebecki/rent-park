from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock current user (przykład)
current_user = {'is_authenticated': False}

# Strona główna
@app.route('/')
def home():
    return render_template('home.html', title="Home", current_user=current_user)

# Logowanie
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Przykład logiki logowania (do rozszerzenia)
        email = request.form['email']
        password = request.form['password']
        return redirect(url_for('home'))
    return render_template('login.html', title="Login", current_user=current_user)

# Rejestracja
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Przykład logiki rejestracji (do rozszerzenia)
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", current_user=current_user)

# FAQ
@app.route('/faq')
def faq():
    return render_template('faq.html', title="FAQ", current_user=current_user)

# Kontakt
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Przykład logiki obsługi formularza kontaktowego
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        return redirect(url_for('home'))
    return render_template('contact.html', title="Contact", current_user=current_user)

# Rezerwacja
@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        # Przykład logiki rezerwacji (do rozszerzenia)
        date = request.form['date']
        time = request.form['time']
        spot = request.form['spot']
        return redirect(url_for('home'))
    return render_template('reservation.html', title="Reservation", current_user=current_user)

# Uruchomienie aplikacji
if __name__ == '__main__':
    app.run(debug=True)
