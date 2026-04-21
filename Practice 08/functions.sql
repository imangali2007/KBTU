CREATE OR REPLACE FUNCTION search_contacts(pattern VARCHAR)
RETURNS TABLE(contact_id INT, first_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT p.contact_id, p.first_name, p.phone FROM phonebook p
                 WHERE p.first_name ILIKE '%' || pattern || '%'
                    OR p.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paginated(l INT, o INT)
RETURNS TABLE(contact_id INT, first_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT p.contact_id, p.first_name, p.phone FROM phonebook p
                 ORDER BY p.contact_id
                 LIMIT l OFFSET o;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION insert_many_contacts(names VARCHAR[], phones VARCHAR[])
RETURNS TABLE(failed_name VARCHAR, failed_phone VARCHAR) AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_length(names, 1) LOOP
        IF phones[i] ~ '^[0-9]+$' AND length(phones[i]) >= 5 THEN
            IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = names[i]) THEN
                UPDATE phonebook SET phone = phones[i] WHERE first_name = names[i];
            ELSE
                INSERT INTO phonebook(first_name, phone) VALUES(names[i], phones[i]);
            END IF;
        ELSE
            failed_name := names[i];
            failed_phone := phones[i];
            RETURN NEXT;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
