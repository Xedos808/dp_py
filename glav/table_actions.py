from db_utils import select_from_reference, get_display_column, show_table_data


def add_record(cursor, conn, table_name, columns):
    print("\nВведите данные для новой записи:")
    values = []
    for col in columns:
        if col.lower().startswith("id") and col != columns[0]:
            ref_table = col[2:]
            val = select_from_reference(cursor, ref_table, col)
        elif col.lower() == columns[0].lower():
            continue  # Пропустить ID
        else:
            val = input(f"{col}: ")
        values.append(val)

    col_names = [col for col in columns if col.lower() != columns[0].lower()]
    placeholders = ", ".join(["?"] * len(values))
    query = f"INSERT INTO {table_name} ({', '.join(col_names)}) VALUES ({placeholders})"
    cursor.execute(query, values)
    conn.commit()
    print("Запись добавлена.\n")


def delete_record(cursor, conn, table_name, columns):
    print("\nТекущие записи в таблице:")
    show_table_data(cursor, table_name, columns)
    record_id = input(f"Введите ID записи для удаления ({columns[0]}): ")
    cursor.execute(f"DELETE FROM {table_name} WHERE {columns[0]}=?", (record_id,))
    conn.commit()
    print("Запись удалена.\n")


def show_table(cursor, table_name, columns):
    print(f"\nСодержимое таблицы {table_name}:")
    show_table_data(cursor, table_name, columns)


def table_menu(cursor, conn, table_name, get_columns):
    columns = get_columns(cursor, table_name)
    while True:
        print(f"\n--- Меню таблицы {table_name} ---")
        print("1. Показать все записи")
        print("2. Добавить запись")
        print("3. Удалить запись")
        print("4. Назад")
        choice = input("Выберите действие: ")

        if choice == "1":
            show_table(cursor, table_name, columns)
        elif choice == "2":
            add_record(cursor, conn, table_name, columns)
        elif choice == "3":
            delete_record(cursor, conn, table_name, columns)
        elif choice == "4":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")
