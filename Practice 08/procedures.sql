CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook(first_name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(del_type VARCHAR, val VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF del_type = 'name' THEN
        DELETE FROM phonebook WHERE first_name = val;
    ELSIF del_type = 'phone' THEN
        DELETE FROM phonebook WHERE phone = val;
    END IF;
END;
$$;
