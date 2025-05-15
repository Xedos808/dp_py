import sqlite3
import tkinter as tk
from tkinter import filedialog
from table_actions import table_menu
from db_utils import get_table_names, get_columns


def choose_database():
    root = tk.Tk()
    root.withdraw()
    db_path = filedialog.askopenfilename(
        title="Выберите файл базы данных",
        filetypes=[("SQLite DB ", "*.db *.sqlite3"), ("All files", "*.*")]
    )
    return db_path


def main():
    db_path = choose_database()
    if not db_path:
        print("Файл не выбран.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    while True:
        tables = get_table_names(cursor)
        print("\nВыберите таблицу:")
        for i, table in enumerate(tables, start=1):
            print(f"{i}. {table}")
        print("4. Выход")

        choice = input("Введите номер таблицы: ")
        if choice == "4":
            break
        if not choice.isdigit() or not (1 <= int(choice) <= len(tables)):
            print("Неверный выбор.")
            continue

        table_name = tables[int(choice) - 1]
        table_menu(cursor, conn, table_name, get_columns)

    conn.close()


if __name__ == "__main__":
    main()
