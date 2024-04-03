# Import des modules nécessaire
from flask import Flask, request, render_template, redirect, url_for, jsonify
import pymysql
from flask_cors import CORS
import json

# Initialisation de Flask app
app = Flask(__name__)
CORS(app)

# Configuration du connection MySQL
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='nomenjanaharyLALA10@',
    db='db_etudiant',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# Model - operations dans la base de données
class Etudiant: 
	@staticmethod
	def get_all_student():
		with conn.cursor() as cursor:
			cursor.execute('SELECT * FROM etudiant')
			student = cursor.fetchall()
		return student

	@staticmethod
	def get_student(numeroMatricule):
		with conn.cursor() as cursor:
			cursor.execute('SELECT * FROM etudiant WHERE numeroMatricule = %s', (numeroMatricule,))
			student = cursor.fetchone()
		return student

	@staticmethod
	def update(numeroMatricule, nom, prenom, date_naiss, adresse, mention, parcours, niveau, domaine, sexe):
		with conn.cursor() as cursor:
			cursor.execute(
				'UPDATE etudiant SET nom = %s, prenom = %s, date_naiss = %s, adresse = %s, mention = %s, parcours = %s, niveau = %s, domaine = %s, sexe = %s WHERE numeroMatricule = %s',
				(nom, prenom, date_naiss, adresse, mention, parcours, niveau, domaine, sexe, numeroMatricule)
			)
			conn.commit()
   
	@staticmethod
	def delete(numeroMatricule):
		with conn.cursor() as cursor:
			cursor.execute('DELETE FROM etudiant WHERE numeroMatricule = %s', (numeroMatricule))
			conn.commit()
	
@app.route('/')
def index():
	students = Etudiant.get_all_student()
	return render_template('index.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
	donnees = request.get_json()
	print(donnees)
	value = donnees.get('data')
	#print(value)
 
	json_dom = value.get('caseCochee')
	print(json_dom)
	dom = json.loads(json.dumps(json_dom))
	#value_dom = dom.get('data')
	domaine = dom.get("caseCochee")
  
	print(domaine)
	numeroMatricule = value.get('numeroMatricule')
 
	nom = value.get('nom')
	print(nom)
 
	prenom = value.get('prenom')
	print(prenom)
 
	date_naiss = value.get('date_naiss')
	print(date_naiss)
 
	adresse = value.get('adresse')
	print(adresse)
 
	json_ment = value.get('mentionbtn')
	adrs = json.loads(json.dumps(json_ment))
	mention = adrs.get("mentionbtn")
	print(mention)
 
	json_par = value.get('parcoursbtn')
	par = json.loads(json.dumps(json_par))
	parcours = par.get("parcoursbtn")
	print(parcours)
 
	json_sexe = value.get('sexe')
	sx = json.loads(json.dumps(json_sexe))
	sexe = sx.get("sexe")
	print(sexe)
 
	json_nv = value.get('niveau')
	print(json_nv)
	nv = json.loads(json.dumps(json_nv))
	niveau = nv.get("select")
	print(niveau)
	with conn.cursor() as cursor:
		cursor.execute(
		"INSERT INTO etudiant (numeroMatricule, nom, prenom, date_naiss, adresse, mention, parcours, niveau, domaine, sexe) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
		(numeroMatricule, nom, prenom, date_naiss, adresse, mention, parcours, niveau, domaine, sexe)
		)
		conn.commit()
	# return redirect(url_for('index'))
	st = Etudiant.get_all_student()
	students = jsonify(st)
	return students

@app.route('/edit', methods=['POST'])
def edit():
	data = request.get_json()
	#val = data.get('data')
 
	numeroMatricule = data.get('mat')
	# print(numeroMatricule)
	student = Etudiant.get_student(numeroMatricule)

	# Etudiant.update_student(student_id, ...)
	# return redirect(url_for('index'))
	print(student)
	return student

@app.route('/stat', methods=['POST'])
def stat():
	donnees = request.get_json()
	#val = data.get('data')
	value = donnees.get('data')
	#print(value)
 
	json_dom = value.get('caseCochee')
	print(json_dom)
	dom = json.loads(json.dumps(json_dom))
	#value_dom = dom.get('data')
	domaine = dom.get("caseCochee")
  
	print(domaine)
 
	json_ment = value.get('mentionbtn')
	adrs = json.loads(json.dumps(json_ment))
	mention = adrs.get("mentionbtn")
	print(mention)
 
	json_par = value.get('parcoursbtn')
	par = json.loads(json.dumps(json_par))
	parcours = par.get("parcoursbtn")
	print(parcours)
 
	json_sexe = value.get('sexe')
	sx = json.loads(json.dumps(json_sexe))
	sexe = sx.get("sexe")
	print(sexe)
 
	json_nv = value.get('niveau')
	print(json_nv)
	nv = json.loads(json.dumps(json_nv))
	niveau = nv.get("select")
	print(niveau)
	nb = 0
	with conn.cursor() as cursor:
			cursor.execute('SELECT count(*) FROM etudiant WHERE sexe = %s and mention = %s and parcours = %s and niveau = %s and domaine = %s', (sexe, mention, parcours, niveau, domaine))
			nb = cursor.fetchone()
	return nb

@app.route("/upd_student", methods=['POST'])
def upd_student():
    donnees = request.get_json()
    print(donnees)
    value = donnees.get('data') 
    numeroMatricule = value.get('numeroMatricule')
    print(numeroMatricule)
    nom = value.get('nom')
    print(nom)
    prenom = value.get('prenom')
    print(prenom)
    date_naiss = value.get('datenaiss')
    print(date_naiss)
    adresse = value.get('adresse')
    print(adresse)
    mention = value.get('mention')
    print(mention)
    parcours = value.get('parcours')
    print(parcours)
    niveau = value.get('niveau')
    print(niveau)
    domaine = value.get('domaine')
    print(domaine)
    sexe = value.get('sexe')
    print(sexe)
    Etudiant.update(numeroMatricule, nom, prenom, date_naiss, adresse, mention, parcours, niveau, domaine, sexe)
    st = Etudiant.get_all_student()
    students = jsonify(st)
    return students
    
@staticmethod
def create_student(numeroMatricule, nom, prenoms, date_naiss, adresse):
	with conn.cursor() as cursor:
		cursor.execute(
		'INSERT INTO etudiant (numeroMatricule, nom, prenoms, date_naiss, adresse) VALUES (%s, %s, %s, %s, %s)',
		(numeroMatricule, nom, prenoms, date_naiss, adresse)
		)
		conn.commit()
  

@app.route('/delete_student', methods=['POST'])
def delete_student():
    donnees = request.get_json()
    value = donnees.get('data') 
    numeroMatricule = value.get('numeroMatricule')
    delete = Etudiant.delete(numeroMatricule)
    st = Etudiant.get_all_student()
    students = jsonify(st)
    return students

# Lancer l'application flask
if __name__ == '__main__':
    app.run(debug=True ,port=5000,use_reloader=False)
