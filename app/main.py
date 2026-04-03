from sanic import Sanic
from routes.auth import auth_bp
from routes.users import users_bp
from routes.accounts import accounts_bp
from routes.payments import payments_bp

app = Sanic("PaymentService")

# Регистрируем все роуты
app.blueprint(auth_bp)
app.blueprint(users_bp)
app.blueprint(accounts_bp)
app.blueprint(payments_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)