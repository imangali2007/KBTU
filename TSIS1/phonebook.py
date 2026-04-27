import psycopg2
import csv
import json
from connect import connect

def run_sql_file(filename):
    conn = connect()
    if not conn: return
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            sql = f.read()
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            cur.close()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def insert_contact_initial(name, email, birthday):
    conn = connect()
    if not conn: return
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO contacts (first_name, email, birthday) VALUES (%s, %s, %s) RETURNING id", (name, email, birthday))
        conn.commit()
        print("Contact created.")
        cur.close()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def get_paginated():
    conn = connect()
    if not conn: return
    limit = 5
    offset = 0
    while True:
        try:
            cur = conn.cursor()
            cur.callproc('get_contacts_paginated', (limit, offset))
            rows = cur.fetchall()
            cur.close()
            print("\n--- Page ---")
            if not rows:
                print("[No contacts found]")
            for r in rows:
                print(f"ID: {r[0]} | Name: {r[1]} | Email: {r[2]}")
            
            nav = input("n=Next, p=Prev, q=Quit: ").strip()
            if nav == 'n': offset += limit
            elif nav == 'p' and offset >= limit: offset -= limit
            elif nav == 'q': break
        except Exception as e:
            print(e)
            break
    conn.close()

def export_json(filename):
    conn = connect()
    if not conn: return
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT c.first_name, c.email, TO_CHAR(c.birthday, 'YYYY-MM-DD'), g.name, p.phone, p.type 
            FROM contacts c 
            LEFT JOIN groups g ON c.group_id = g.id 
            LEFT JOIN phones p ON c.id = p.contact_id
        """)
        rows = cur.fetchall()
        data = {}
        for r in rows:
            name, email, bday, grp, phone, ptype = r
            if name not in data:
                data[name] = {"email": email, "birthday": bday, "group": grp, "phones": []}
            if phone:
                data[name]["phones"].append({"phone": phone, "type": ptype})
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print("Exported.")
        cur.close()
    except Exception as e:
        print(e)
    finally:
        conn.close()

if __name__ == '__main__':
    run_sql_file('schema.sql')
    run_sql_file('procedures.sql')
    
    while True:
        print("\n0. Add New Contact")
        print("1. Search")
        print("2. Add Phone to existing")
        print("3. Set Group")
        print("4. View Paginated")
        print("5. Export JSON")
        print("6. Exit")
        c = input("Choice: ")
        
        if c == '0':
            n = input("Name: ")
            e = input("Email: ")
            b = input("Birthday (YYYY-MM-DD): ")
            insert_contact_initial(n, e, b)
        elif c == '1':
            q = input("Query (name/email/phone): ")
            conn = connect()
            if conn:
                cur = conn.cursor()
                cur.callproc('search_contacts_advanced', (q,))
                for r in cur.fetchall(): print(r)
                cur.close()
                conn.close()
        elif c == '2':
            add_phone_name = input("Contact Name: ")
            phone = input("Phone: ")
            ptype = input("Type (home/work/mobile): ")
            conn = connect()
            if conn:
                cur = conn.cursor()
                cur.execute("CALL add_phone(%s, %s, %s)", (add_phone_name, phone, ptype))
                conn.commit()
                cur.close()
                conn.close()
        elif c == '3':
            n = input("Contact Name: ")
            g = input("Group Name: ")
            conn = connect()
            if conn:
                cur = conn.cursor()
                cur.execute("CALL move_to_group(%s, %s)", (n, g))
                conn.commit()
                cur.close()
                conn.close()
        elif c == '4':
            get_paginated()
        elif c == '5':
            export_json("contacts_export.json")
        elif c == '6':
            break
