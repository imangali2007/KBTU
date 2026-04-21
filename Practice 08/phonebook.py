import psycopg2
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

def search(pattern):
    conn = connect()
    if not conn: return
    try:
        cur = conn.cursor()
        cur.callproc('search_contacts', (pattern,))
        rows = cur.fetchall()
        for r in rows:
            print(f"ID: {r[0]} | Name: {r[1]} | Phone: {r[2]}")
        cur.close()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def upsert(name, phone):
    conn = connect()
    if not conn: return
    try:
        cur = conn.cursor()
        cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
        conn.commit()
        cur.close()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def bulk_insert(names, phones):
    conn = connect()
    if not conn: return
    try:
        cur = conn.cursor()
        cur.callproc('insert_many_contacts', (names, phones))
        rows = cur.fetchall()
        print("Failed insertions:")
        for r in rows:
            print(f"Name: {r[0]}, Phone: {r[1]}")
        conn.commit()
        cur.close()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def get_page(limit, offset):
    conn = connect()
    if not conn: return
    try:
        cur = conn.cursor()
        cur.callproc('get_contacts_paginated', (limit, offset))
        rows = cur.fetchall()
        for r in rows:
            print(f"ID: {r[0]} | Name: {r[1]} | Phone: {r[2]}")
        cur.close()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def delete(dtype, val):
    conn = connect()
    if not conn: return
    try:
        cur = conn.cursor()
        cur.execute("CALL delete_contact(%s, %s)", (dtype, val))
        conn.commit()
        cur.close()
    except Exception as e:
        print(e)
    finally:
        conn.close()

if __name__ == '__main__':
    run_sql_file('functions.sql')
    run_sql_file('procedures.sql')
    
    while True:
        print("\n1. Search by pattern\n2. Upsert contact\n3. Insert many\n4. Get paginated\n5. Delete contact\n6. Exit")
        c = input("Choice: ")
        
        if c == '1':
            p = input("Pattern: ")
            search(p)
        elif c == '2':
            n = input("Name: ")
            p = input("Phone: ")
            upsert(n, p)
        elif c == '3':
            ns = input("Names (comma sep): ").replace(" ", "").split(',')
            ps = input("Phones (comma sep): ").replace(" ", "").split(',')
            bulk_insert(ns, ps)
        elif c == '4':
            l = int(input("Limit: "))
            o = int(input("Offset: "))
            get_page(l, o)
        elif c == '5':
            dt = input("Type (name/phone): ")
            v = input("Value: ")
            delete(dt, v)
        elif c == '6':
            break
