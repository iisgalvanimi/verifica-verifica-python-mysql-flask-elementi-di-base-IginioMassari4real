import mysql.connector

# Funzione per connettersi al database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Animali"
    )

# Dati degli animali da inserire
animali = [
    ('Elefante', 'Proboscidea', '3-7 m', 'Savana', 'Piante'),
    ('Balena', 'Cetacea', '20-30 m', 'Oceani', 'Plancton'),
    ('Leone', 'Carnivora', '1.5-2.5 m', 'Savana', 'Carnivori'),
    ('Giraffa', 'Artiodactyla', '4-5 m', 'Savana', 'Foglie'),
    ('Orso', 'Carnivora', '2-3 m', 'Boschi', 'Onnivori'),
    ('Cane', 'Carnivora', '0.5-1 m', 'Domestico', 'Onnivori'),
    ('Gatto', 'Carnivora', '0.3-0.6 m', 'Domestico', 'Carnivori'),
    ('Topo', 'Rodentia', '5-10 cm', 'Urbano', 'Semi, Insetti'), 
    ('Coniglio', 'Lagomorpha', '30-50 cm', 'Prati', 'Piante')
]

# Connessione al database e inserimento degli animali
mydb = connect_to_db()
mycursor = mydb.cursor()

sql = "INSERT INTO mammiferi (nome_comune, ordine, dimensioni, habitat, alimentazione) VALUES (%s, %s, %s, %s, %s)"
mycursor.executemany(sql, animali)
mydb.commit()