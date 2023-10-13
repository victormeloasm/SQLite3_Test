import sqlite3
import os
import sys
import json

# Obter o diretório em que o executável está localizado
executable_dir = os.path.dirname(sys.argv[0])
database_list_file = os.path.join(executable_dir, "database_list.json")

# Inicializar a lista de bancos de dados a partir do arquivo ou criar uma lista vazia
if os.path.exists(database_list_file):
    with open(database_list_file, "r") as file:
        try:
            database_files = json.load(file)
        except json.JSONDecodeError:
            database_files = {}
else:
    database_files = {}

def save_database_list():
    # Salvar a lista de bancos de dados no arquivo
    with open(database_list_file, "w") as file:
        json.dump(database_files, file)

def create_database(database_name):
    # Caminho completo para o arquivo do banco de dados
    db_file = os.path.join(executable_dir, f"{database_name}.db")

    if not os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                email TEXT
            )
        ''')
        conn.commit()
        conn.close()

    print(f"Using database: {database_name}")

    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(db_file)
    return conn

def list_databases():
    print("\nAvailable databases:")
    for key in database_files:
        print(key)

def create_or_select_database():
    while True:
        print("\nOptions:")
        print("1. Create a New Database")
        print("2. Select an Existing Database")
        print("3. List Databases")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            new_database_name = input("Enter the name of the new database: ")
            if new_database_name:
                conn = create_database(new_database_name)
                database_files[new_database_name] = os.path.join(executable_dir, f"{new_database_name}.db")
                save_database_list()
                return conn
            else:
                print("Invalid database name. Please enter a valid name.")
        elif choice == '2':
            while True:
                print("\nAvailable databases:")
                for key in database_files:
                    print(key)

                database_name = input("Enter the name of the database you want to use: ")

                if database_name in database_files:
                    conn = create_database(database_name)
                    return conn
                else:
                    print("Database does not exist. Please select an existing database or create a new one.")
        elif choice == '3':
            list_databases()
        elif choice == '4':
            exit()
        else:
            print("Invalid choice. Please select a valid option.")

def main():
    # Inicialmente, cria ou seleciona o banco de dados
    conn = create_or_select_database()
    cursor = conn.cursor()

    while True:
        print("\nOptions:")
        print("1. Register a user")
        print("2. Remove a user")
        print("3. Search for a user")
        print("4. Update email")
        print("5. Show All Users")
        print("6. Change Database")
        print("7. List Databases")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            register_user(cursor)
        elif choice == '2':
            remove_user(cursor)
        elif choice == '3':
            search_user(cursor)
        elif choice == '4':
            update_email(cursor)
        elif choice == '5':
            show_all_users(cursor)
        elif choice == '6':
            conn.close()
            conn = create_or_select_database()
            cursor = conn.cursor()
        elif choice == '7':
            list_databases()
        elif choice == '8':
            exit()
        else:
            print("Invalid choice. Please select a valid option.")

    conn.close()

def register_user(cursor):
    username = input("Enter username: ")
    email = input("Enter email: ")
    cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
    cursor.connection.commit()
    print(f"Registered user: {username}, Email: {email}")

def remove_user(cursor):
    user_id = int(input("Enter the user ID to remove: "))
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    cursor.connection.commit()
    print(f"Removed user with ID: {user_id}")

def search_user(cursor):
    search_term = input("Enter a username or email to search: ")
    cursor.execute("SELECT * FROM users WHERE username LIKE ? OR email LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
    users = cursor.fetchall()
    if users:
        print("\nSearch results:")
        for user in users:
            print(f"User ID: {user[0]}, Username: {user[1]}, Email: {user[2]}")
    else:
        print(f"No users found matching '{search_term}'")

def update_email(cursor):
    user_id = int(input("Enter the user ID to update email: "))
    new_email = input("Enter the new email address: ")
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    cursor.connection.commit()
    print(f"Updated email for user with ID {user_id} to: {new_email}")

def show_all_users(cursor):
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    if users:
        print("\nList of all registered users:")
        for user in users:
            print(f"User ID: {user[0]}, Username: {user[1]}, Email: {user[2]}")
    else:
        print("No registered users found.")

if __name__ == "__main__":
    main()
