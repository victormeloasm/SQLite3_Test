import sqlite3
import os

# Check if the database file exists, and create it if not
db_file = 'user_database.db'
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

# Connect to the SQLite database
conn = sqlite3.connect(db_file)

# Create a cursor object to interact with the database
cursor = conn.cursor()

def register_user():
    username = input("Enter username: ")
    email = input("Enter email: ")
    cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
    conn.commit()
    print(f"Registered user: {username}, Email: {email}")

def remove_user():
    user_id = int(input("Enter the user ID to remove: "))
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    print(f"Removed user with ID: {user_id}")

def search_user():
    search_term = input("Enter a username or email to search: ")
    cursor.execute("SELECT * FROM users WHERE username LIKE ? OR email LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
    users = cursor.fetchall()
    if users:
        print("\nSearch results:")
        for user in users:
            print(f"User ID: {user[0]}, Username: {user[1]}, Email: {user[2]}")
    else:
        print(f"No users found matching '{search_term}'.")

def update_email():
    user_id = int(input("Enter the user ID to update email: "))
    new_email = input("Enter the new email address: ")
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    conn.commit()
    print(f"Updated email for user with ID {user_id} to: {new_email}")

def show_all_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    if users:
        print("\nList of all registered users:")
        for user in users:
            print(f"User ID: {user[0]}, Username: {user[1]}, Email: {user[2]}")
    else:
        print("No registered users found.")

while True:
    print("\nOptions:")
    print("1. Register a user")
    print("2. Remove a user")
    print("3. Search for a user")
    print("4. Update email")
    print("5. Show All Users")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        register_user()
    elif choice == '2':
        remove_user()
    elif choice == '3':
        search_user()
    elif choice == '4':
        update_email()
    elif choice == '5':
        show_all_users()
    elif choice == '6':
        break
    else:
        print("Invalid choice. Please select a valid option.")

# Close the cursor and the database connection
cursor.close()
conn.close()
