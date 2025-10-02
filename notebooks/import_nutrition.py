import csv
import sqlite3
import os

def load_csv(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            return None, None
        rows = [row for row in reader]
        return headers, rows


def normalize_headers(headers):
    # Replace any header containing "µg" with "mcg"
    return [h.replace('µg','mcg') for h in headers]


def ensure_table(conn, table_name, headers):
    # headers are already normalized (e.g., "mcg" instead of "µg")
    quoted_cols = [f'"{h}"' for h in headers]
    create_sql = (
        f'CREATE TABLE IF NOT EXISTS "{table_name}" (\n'
        + ',\n'.join([f' {col} TEXT' for col in quoted_cols])
        + "\n);"
    )
    conn.execute(create_sql)

def import_csv_to_sqlite_idempotent(csv_path, db_path, table_name):
    headers, rows = load_csv(csv_path)
    if headers is None or rows is None:
        print(f"CSV not found or empty: {csv_path}")
        return 0
    db_dir = os.path.dirname(db_path)
    os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Normalize headers for DB usage
    db_headers = normalize_headers(headers)
    ensure_table(cur, table_name, db_headers)

    # determine date column value set
    date_col = headers[0]
    date_col_quoted = f'"{db_headers[0]}"'

    # collect unique dates from rows
    dates = []
    for r in rows:
        if len(r) > 0:
            dates.append(r[0])
    unique_dates = list(dict.fromkeys(dates))  # preserve order, unique
    if unique_dates:
        placeholders = ",".join(["?"] * len(unique_dates))
        delete_sql = f'DELETE FROM "{table_name}" WHERE {date_col_quoted} IN ({placeholders})'
        cur.execute(delete_sql, unique_dates)
        conn.commit()

    # Insert all rows
    col_list = ", ".join([f'"{h}"' for h in db_headers])
    placeholders = ", ".join(["?"] * len(headers))
    insert_sql = f'INSERT INTO "{table_name}" ({col_list}) VALUES ({placeholders})'
    row_count = 0
    for row in rows:
        if len(row) < len(headers):
            row = row + [''] * (len(headers) - len(row))
        elif len(row) > len(headers):
            row = row[:len(headers)]
        row_values = [None if v == '' else v for v in row]
        cur.execute(insert_sql, row_values)
        row_count += 1
        if row_count % 1000 == 0:
            conn.commit()
    conn.commit()
    cur.close()
    conn.close()
    print(f"Idempotently imported {row_count} rows into {table_name} table at {db_path}")
    return row_count

if __name__ == '__main__':
    # Daily summary: idempotent import
    csv_daily = os.path.join(os.path.dirname(__file__), 'data', 'dailysummary.csv')
    db_path = os.path.expanduser('~/HealthData/DBs/nutrition.db')
    import_csv_to_sqlite_idempotent(csv_daily, db_path, "daily_summary")
    # Servings: idempotent import
    csv_servings = os.path.join(os.path.dirname(__file__), 'data', 'servings.csv')
    import_csv_to_sqlite_idempotent(csv_servings, db_path, "servings")
