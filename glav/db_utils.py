def get_table_names(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'")
    return [row[0] for row in cursor.fetchall()]


def get_columns(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    return [row[1] for row in cursor.fetchall()]


def get_display_column(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    cols = cursor.fetchall()
    for col in cols:
        if col[1].lower() not in ("id", "id" + table_name.lower()):
            return col[1]
    return cols[1][1] if len(cols) > 1 else cols[0][1]


def select_from_reference(cursor, ref_table, id_col):
    name_col = get_display_column(cursor, ref_table)
    cursor.execute(f"SELECT {id_col}, {name_col} FROM {ref_table}")
    results = cursor.fetchall()
    print(f"\nВыберите из {ref_table}:")
    for r in results:
        print(f"{r[0]}: {r[1]}")
    while True:
        selected = input(f"Введите ID из {ref_table}: ")
        if selected.isdigit() and any(str(r[0]) == selected for r in results):
            return selected
        print("Неверный ID. Попробуйте снова.")


def show_table_data(cursor, table_name, columns):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    col_widths = [max(len(str(col)), max((len(str(row[i])) for row in rows), default=0)) for i, col in enumerate(columns)]
    header = " | ".join(col.ljust(col_widths[i]) for i, col in enumerate(columns))
    print(header)
    print("-" * len(header))
    for row in rows:
        print(" | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(columns))))
