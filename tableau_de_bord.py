import mysql.connector
from tkinter import *
from tkinter import ttk

window = Tk()
window.title("Tableau de bord")
window.geometry("900x600")

# connexion à la base de données
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "sophie",
    database = "boutique")

# créer un curseur
cursor = conn.cursor()

conn.commit() # enregistrer les changements
conn.close() # fermer la connexion

# fonction pour interroger la base de données
def query_database():
    conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "sophie",
    database = "boutique")

    cursor = conn.cursor()

    requete = "SELECT * FROM produit" # requête pour afficher les données de la table produit

    cursor.execute(requete)
    produit = cursor.fetchall()

    # ajouter des données
    global count
    count = 0
    
    for produit in produit:
        if count % 2 == 0:
            my_tree.insert(parent="", index="end", iid=count, text="", values=(produit[0], produit[1], produit[2], produit[3], produit[4], produit[5]), tags=("evenrow",))
        else:
            my_tree.insert(parent="", index="end", iid=count, text="", values=(produit[0], produit[1], produit[2], produit[3], produit[4], produit[5]), tags=("oddrow",))
        count += 1

    print(produit)

    conn.commit() # enregistrer les changements
    conn.close() # fermer la connexion

# ajouter un style et un thème
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="darkseagreen")

# choisir la couleur de sélection
style.map("Treeview", background=[("selected", "lime")], foreground=[("selected", "blue")])

# créer une frame
tree_frame = Frame(window)
tree_frame.pack(pady=20)

# créer treeview
my_tree = ttk.Treeview(tree_frame)
my_tree.pack()

# définir les colonnes
my_tree["columns"] = ("ID", "Nom", "Description", "Prix", "Quantité", "Catégorie")

# formatage des colonnes
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=W, width=50)
my_tree.column("Nom", anchor=W, width=140)
my_tree.column("Description", anchor=W, width=350)
my_tree.column("Prix", anchor=CENTER, width=60)
my_tree.column("Quantité", anchor=CENTER, width=60)
my_tree.column("Catégorie", anchor=CENTER, width=65)

# créer les en-têtes
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("ID", text="ID", anchor=W)
my_tree.heading("Nom", text="Nom", anchor=W)
my_tree.heading("Description", text="Description", anchor=W)
my_tree.heading("Prix", text="Prix", anchor=CENTER)
my_tree.heading("Quantité", text="Quantité", anchor=CENTER)
my_tree.heading("Catégorie", text="Catégorie", anchor=CENTER)

# créer des lignes rayées
my_tree.tag_configure("oddrow", background="pink")
my_tree.tag_configure("evenrow", background="aquamarine")

# ajouter les labels et les entrées dans une frame
data_frame = LabelFrame(window, text="Produit")
data_frame.pack(fill="x", expand="yes", padx=20)

id_label = Label(data_frame, text="ID")
id_label.grid(row=0, column=0, padx=10, pady=10)
id_entry = Entry(data_frame)
id_entry.grid(row=0, column=1, padx=10, pady=10)

nom_label = Label(data_frame, text="Nom")
nom_label.grid(row=0, column=2, padx=10, pady=10)
nom_entry = Entry(data_frame)
nom_entry.grid(row=0, column=3, padx=10, pady=10)

prix_label = Label(data_frame, text="Prix")
prix_label.grid(row=0, column=4, padx=10, pady=10)
prix_entry = Entry(data_frame)
prix_entry.grid(row=0, column=5, padx=10, pady=10)

quant_label = Label(data_frame, text="Quantité")
quant_label.grid(row=0, column=6, padx=10, pady=10)
quant_entry = Entry(data_frame)
quant_entry.grid(row=0, column=7, padx=10, pady=10)

cat_label = Label(data_frame, text="Catégorie")
cat_label.grid(row=1, column=0, padx=10, pady=10)
cat_entry = Entry(data_frame)
cat_entry.grid(row=1, column=1, padx=10, pady=10)

desc_label = Label(data_frame, text="Description")
desc_label.grid(row=1, column=2, padx=10, pady=10)
desc_entry = Entry(data_frame)
desc_entry.grid(row=1, column=3, padx=10, pady=10)
    
# supprimer un produit
def supp_1_produit():
    x = my_tree.selection()[0] # sélectionner un produit
    my_tree.delete(x) # supprimer le produit sélectionné

# supprimer tous les produit
def supp_all():
    for produit in my_tree.get_children(): # sélectionner tous les produits
        my_tree.delete(produit) # supprimer tous les produits sélectionnés

def clear_entries():
    id_entry.delete(0, END)
    nom_entry.delete(0, END)
    desc_entry.delete(0, END)
    prix_entry.delete(0, END)
    quant_entry.delete(0, END)
    cat_entry.delete(0, END)

# choisir un produit
def select_produit(e):
    selected = my_tree.focus() # sélectionner un produit
    values = my_tree.item(selected, "values") # récupérer les valeurs du produit sélectionné
    id_entry.delete(0, END)
    id_entry.insert(0, values[0]) # insérer les valeurs dans les entrées
    nom_entry.delete(0, END)
    nom_entry.insert(0, values[1])
    desc_entry.delete(0, END)
    desc_entry.insert(0, values[2])
    prix_entry.delete(0, END)
    prix_entry.insert(0, values[3])
    quant_entry.delete(0, END)
    quant_entry.insert(0, values[4])
    cat_entry.delete(0, END)
    cat_entry.insert(0, values[5])

# mettre à jour un produit
def update_produit():
    selected = my_tree.focus() # sélectionner un produit
    my_tree.item(selected, text="", values=(id_entry.get(), nom_entry.get(), desc_entry.get(), prix_entry.get(), quant_entry.get(), cat_entry.get())) # mettre à jour les valeurs du produit sélectionné
    clear_entries()

# ajouter un produit
def ajouter_produit():
    conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "sophie",
    database = "boutique")

    cursor = conn.cursor()

    ajout = "INSERT INTO produit (nom, description, prix, quantité, id_catégorie) VALUES (id_entry.get(), nom_entry.get(), desc_entry.get(), prix_entry.get(), quant_entry.get(), cat_entry.get())"
    cursor.execute(ajout)
    conn.commit()
    conn.close()
    
    my_tree.delete(*my_tree.get_children())
    
    query_database()

# ajouter des boutons
button_frame = LabelFrame(window, text="Commandes")
button_frame.pack(fill="x", expand="yes", padx=20)

button_update = Button(button_frame, text="Update", command=update_produit)
button_update.grid(row=0, column=0, padx=10, pady=10)

button_ajouter = Button(button_frame, text="Ajouter", command=ajouter_produit)
button_ajouter.grid(row=0, column=1, padx=10, pady=10)

button_sup_all = Button(button_frame, text="Supprimer tout", command=supp_all)
button_sup_all.grid(row=0, column=2, padx=10, pady=10)

button_sup_1 = Button(button_frame, text="Supprimer un produit", command=supp_1_produit)
button_sup_1.grid(row=0, column=3, padx=10, pady=10)

button_select = Button(button_frame, text="Effacer les entrées", command=clear_entries)
button_select.grid(row=0, column=4, padx=10, pady=10)

# lier le treeview
my_tree.bind("<ButtonRelease-1>", select_produit)

# exécuter pour extraire les données de la base de données
query_database()

window.mainloop()