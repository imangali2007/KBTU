import psycopg2
import csv
from connect import connect

def create_table():
    command = """
    CREATE TABLE IF NOT EXISTS phonebook (
        contact_id SERIAL PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        phone VARCHAR(50) NOT NULL
    )
    """
    conn = None
    try:
        conn = connect()
        if conn is None: return
        cur = conn.cursor()
        cur.execute(command)
        conn.commit()
        cur.close()
        print("Table 'phonebook' ensured.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_contact(first_name, phone):
    sql = "INSERT INTO phonebook(first_name, phone) VALUES(%s, %s)"
    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(sql, (first_name, phone))
        conn.commit()
        cur.close()
        print(f"Contact {first_name} inserted successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def import_csv(filename):
    sql = "INSERT INTO phonebook(first_name, phone) VALUES(%s, %s)"
    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            count = 0
            for row in reader:
                if len(row) >= 2:
                    cur.execute(sql, (row[0], row[1]))
                    count += 1
        conn.commit()
        cur.close()
        print(f"{count} records imported from {filename}.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def update_contact(contact_id, new_name=None, new_phone=None):
    if new_name and new_phone:
        sql = "UPDATE phonebook SET first_name = %s, phone = %s WHERE contact_id = %s"
        params = (new_name, new_phone, contact_id)
    elif new_name:
        sql = "UPDATE phonebook SET first_name = %s WHERE contact_id = %s"
        params = (new_name, contact_id)
    elif new_phone:
        sql = "UPDATE phonebook SET phone = %s WHERE contact_id = %s"
        params = (new_phone, contact_id)
    else:
        return

    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(sql, params)
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()
        print(f"Contact updated. Rows affected: {updated_rows}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def query_contacts(filter_type=None, filter_value=None):
    if filter_type == 'name':
        sql = "SELECT * FROM phonebook WHERE first_name ILIKE %s ORDER BY contact_id"
        value = f"%{filter_value}%"
    elif filter_type == 'phone':
        sql = "SELECT * FROM phonebook WHERE phone LIKE %s ORDER BY contact_id"
        value = f"{filter_value}%"
    else:
        sql = "SELECT * FROM phonebook ORDER BY contact_id"
        value = None

    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        if value:
            cur.execute(sql, (value,))
        else:
            cur.execute(sql)
        rows = cur.fetchall()
        
        print("\n--- Contacts ---")
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
        print("----------------\n")
        
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def delete_contact(delete_by, value):
    if delete_by == 'name':
        sql = "DELETE FROM phonebook WHERE first_name = %s"
    elif delete_by == 'phone':
        sql = "DELETE FROM phonebook WHERE phone = %s"
    else:
        return

    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(sql, (value,))
        deleted_rows = cur.rowcount
        conn.commit()
        cur.close()
        print(f"Contact deleted safely. Rows affected: {deleted_rows}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_table()
    while True:
        print("\nPhoneBook Options:")
        print("1. Insert via console")
        print("2. Import via CSV")
        print("3. Update contact")
        print("4. Query contacts")
        print("5. Delete contact")
        print("6. Exit")
        choice = input("Enter choice (1-6): ")

        if choice == '1':
            name = input("Enter first name: ")
            phone = input("Enter phone number: ")
            insert_contact(name, phone)
        elif choice == '2':
            filename = input("Enter CSV filename (e.g. contacts.csv): ")
            import_csv(filename)
        elif choice == '3':
            cid = input("Enter contact ID to update: ")
            print("Leave blank if you do not want to update a field.")
            new_name = input("Enter new name: ")
            new_phone = input("Enter new phone: ")
            update_contact(int(cid), new_name if new_name else None, new_phone if new_phone else None)
        elif choice == '4':
            print("a. All contacts")
            print("b. Filter by name")
            print("c. Filter by phone prefix")
            subchoice = input("Choice (a/b/c): ")
            if subchoice == 'b':
                val = input("Enter name to search: ")
                query_contacts('name', val)
            elif subchoice == 'c':
                val = input("Enter phone prefix: ")
                query_contacts('phone', val)
            else:
                query_contacts()
        elif choice == '5':
            print("a. Delete by name")
            print("b. Delete by phone")
            subchoice = input("Choice (a/b): ")
            if subchoice == 'a':
                val = input("Enter name to delete: ")
                delete_contact('name', val)
            elif subchoice == 'b':
                val = input("Enter phone to delete: ")
                delete_contact('phone', val)
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
