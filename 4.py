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

@app.route('/api/animali/filtra/dimensione', methods=['GET'])
def get_animali_con_dimensione():
    dimensione_max = request.args.get('dimensione_max')  # Ad esempio, 3 per filtrare gli animali < 3m

    if not dimensione_max:
        return jsonify({"error": "Parametro 'dimensione_max' mancante"}), 400

    try:
        dimensione_max = float(dimensione_max)

        connessione = connetti_db()
        cursore = connessione.cursor(dictionary=True)

        sql = "SELECT * FROM mammiferi WHERE dimensioni < %s"
        cursore.execute(sql, (dimensione_max,))
        animali = cursore.fetchall()

        cursore.close()
        connessione.close()

        if not animali:
            return jsonify({"message": "Nessun animale trovato con dimensione inferiore a " + str(dimensione_max)}), 404

        return jsonify(animali)

    except ValueError:
        return jsonify({"error": "'dimensione_max' deve essere un numero valido"}), 400

    except mysql.connector.Error as err:
        return jsonify({"error": f"Errore del database: {err}"}), 500

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

@app.route('/api/animali/<int:id>', methods=['PUT'])
def update_mammifero(id):
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

    sql = "UPDATE mammiferi SET nome_comune = %s, ordine = %s, dimensioni = %s, habitat = %s, alimentazione = %s WHERE Id = %s"
    cursore.execute(sql, (nome, ordine, dimensioni, habitat, alimentazione, id))
    connessione.commit()

    rowcount = cursore.rowcount
    cursore.close()
    connessione.close()

    if rowcount == 0:
        return jsonify({"message": "Animale non trovato"}), 404

    return jsonify({"message": "Animale aggiornato con successo!"}), 200

@app.route('/api/animali/<int:id>', methods=['DELETE'])
def delete_mammifero(id):
    connessione = connetti_db()
    cursore = connessione.cursor()

    cursore.execute("SELECT * FROM mammiferi WHERE Id = %s", (id,))
    if not cursore.fetchone():
        cursore.close()
        connessione.close()
        return jsonify({"message": "Animale non trovato"}), 404

    cursore.execute("DELETE FROM mammiferi WHERE Id = %s", (id,))
    connessione.commit()

    cursore.close()
    connessione.close()

    return jsonify({"message": "Animale eliminato con successo!"}), 200

if __name__ == '__main__':
    app.run(debug=True)

