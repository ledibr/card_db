import sqlite3
import pandas as pd
import argparse
import os
import unicodedata
from pathlib import Path
# from utils import normalize, format_pandas
from gui import SearchUI

DATABASE = Path(__file__).parent / 'database.db'
SCHEMA = Path(__file__).parent / 'schema.sql'
SCRATCH_SCHEMA = Path(__file__).parent / 'schema_scratch.sql'


def normalize(text):
    text = unicodedata.normalize('NFD', text)
    result = []
    for i in range(len(text)):
        if text[i].isalpha() or text[i].isspace():
            result.append(text[i])
    result = unicodedata.normalize('NFC', ''.join(result))
    return result


def excel_to_sql(entry: os.DirEntry, conn: sqlite3.Connection):
    row_count = 0
    df_dict = pd.read_excel(io=entry.path, sheet_name=None, dtype=str, keep_default_na=False)
    for df in df_dict.values():
        df.columns = [x.lower() for x in df.columns]
        df.loc[df['count'] == '', 'count'] = 0
        df.astype({'count': 'int64'})
        # print(entry.name)
        if 'year' not in df.columns and 'series' not in df.columns:
            series_title = entry.name.strip().split('.')[0]
            series_title = series_title.split()
            year = series_title[0]
            series_name = ' '.join(series_title[1:])
            df.insert(0, 'year', year)
            df.insert(1, 'series', series_name)
        df['normalized'] = df['name'].apply(normalize)
        # print(df)
        row_count += df.to_sql('cards', conn, if_exists='append', index=False)
    print(f'{row_count} rows created in database.')


def build_db(files: str, init: bool = False):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    schema = SCHEMA
    if init:
        schema = SCRATCH_SCHEMA
    with open(schema) as f:
        cursor.executescript(f.read())
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS files (
    filename PRIMARY KEY ON CONFLICT REPLACE,
    mod_time
    )""")
    with os.scandir(files) as it:
        for entry in it:
            if entry.is_file() and entry.name.endswith('.xlsx') and entry.name[0].isalnum():
                filename = entry.name
                mod_time = entry.stat().st_mtime
                # print(filename, mod_time)
                comp_time = cursor.execute("""SELECT mod_time FROM files WHERE filename = ?""", (filename,)).fetchone()
                if not comp_time or (mod_time > comp_time[0]):
                    cursor.execute("""
                                   INSERT INTO files VALUES (?, ?)
                                   ON CONFLICT DO UPDATE SET mod_time = ?;""",
                                   (filename, mod_time, mod_time))
                    excel_to_sql(entry, conn)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='mode', required=True)

    upload_parser = subparsers.add_parser('upload')
    upload_parser.add_argument(
        '--build',
        action='store_true',
    )
    upload_parser.add_argument(
        '--files',
        type=str,
        required=True,
    )

    query_parser = subparsers.add_parser('search')

    args = parser.parse_args()
    if args.mode == 'upload':
        build_db(args.files, args.build)
    elif args.mode == 'search':
        # print(vars(args))
        # query_db(vars(args))
        connection = sqlite3.connect(DATABASE)
        gui = SearchUI(connection)
        gui.run()
        # query_db(gui)