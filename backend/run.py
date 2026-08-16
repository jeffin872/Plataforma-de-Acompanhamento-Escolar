"""
Ponto de entrada da API.

Uso em desenvolvimento:
    flask run
ou
    python run.py
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
