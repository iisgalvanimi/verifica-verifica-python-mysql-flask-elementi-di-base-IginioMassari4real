from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Funzione per connettersi al database MySQL
def connetti_db():
    return mysql.connector.connect(
        host="localhost",      # Cambia con l'host del tuo database
        user="root",           # Cambia con il tuo username
        password="",           # Cambia con la tua password
        database="Animali"     # Cambia con il nome del tuo database
    )

# Route per ottenere i dati in formato JSON
@app.route('/api/animali', methods=['GET'])
def get_animali():
    connessione = connetti_db()
    cursore = connessione.cursor(dictionary=True)
    cursore.execute("SELECT * FROM mammiferi")
    animali = cursore.fetchall()
    cursore.close()
    connessione.close()
    return jsonify(animali)

@app.route('/api/animali', methods=['POST'])
def add_animali():
    data = request.get_json()
    if not all(key in data for key in ('nome_comune', 'ordine', 'dimensioni', 'habitat', 'alimentazione')):
        return jsonify({"error": "Dati mancanti"}), 400

    nome = data['nome_comune']
    ordine = data['ordine']
    dimensioni = data['dimensioni']
    habitat = data['habitat']
    alimentazione = data['alimentazione']

    connessione = connetti_db()
    cursore = connessione.cursor()

    sql = "INSERT INTO mammiferi (nome_comune, ordine, dimensioni, habitat, alimentazione) VALUES (%s, %s, %s, %s, %s)"
    cursore.execute(sql, (nome, ordine, dimensioni, habitat, alimentazione))
    connessione.commit()

    cursore.close()
    connessione.close()

    return jsonify({"message": "Animale inserito con successo!"}), 201

if __name__ == '__main__':
    app.run(debug=True)
