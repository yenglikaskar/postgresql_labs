-- phonebook.sql

-- 1. Создать 
CREATE TABLE IF NOT EXISTS phonebook (
    id     SERIAL PRIMARY KEY,
    name   VARCHAR(50) NOT NULL UNIQUE,
    phone  VARCHAR(20)
);

-- 2. Функция: поиск по шаблону
CREATE OR REPLACE FUNCTION fn_search_phonebook(pattern TEXT)
RETURNS TABLE (id INT, name VARCHAR, phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.name, pb.phone
      FROM phonebook AS pb
     WHERE pb.name  ILIKE '%' || pattern || '%'
        OR pb.phone ILIKE '%' || pattern || '%';
END;
$$;


-- 3. Процедура: вставка или обновление одного пользователя
CREATE OR REPLACE PROCEDURE sp_upsert_user(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$;

-- 4. Процедура: удаление по имени или телефону
CREATE OR REPLACE PROCEDURE sp_delete_phonebook(
    p_name  VARCHAR DEFAULT NULL,
    p_phone VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_name IS NULL AND p_phone IS NULL THEN
        RAISE EXCEPTION 'Provide name or phone to delete.';
    ELSIF p_name IS NOT NULL AND p_phone IS NOT NULL THEN
        DELETE FROM phonebook WHERE name = p_name AND phone = p_phone;
    ELSIF p_name IS NOT NULL THEN
        DELETE FROM phonebook WHERE name = p_name;
    ELSE
        DELETE FROM phonebook WHERE phone = p_phone;
    END IF;
END;
$$;
