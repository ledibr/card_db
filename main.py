import sqlite3
import pandas as pd
import argparse
import os
from pathlib import Path
from utils import normalize, format_pandas

DATABASE = Path(__file__).parent / 'database.db'
SCHEMA = Path(__file__).parent / 'schema.sql'
SCRATCH_SCHEMA = Path(__file__).parent / 'schema_scratch.sql'
ARGS_TO_COLUMNS = {
    'year': 'Year',
    'series': 'Series',
    'set': 'Set',
    'name': 'Name',
    'team': 'Team',
    'features': 'Features',
    'min_count': 'Count',
}


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


# NOTE: needs to be completely reworked now that database has been overhauled!
def query_db(query):
    format_pandas()
    conn = sqlite3.connect(DATABASE)

    filters = {ARGS_TO_COLUMNS[k]: v for k, v in query.items() if k != 'mode' and v is not None}
    filter_list = {k: f'({k} LIKE :{k.lower()})' for k in filters.keys()}
    if 'Name' in filters:
        filter_list['Name'] = '((Name LIKE :name) OR (Normalized_Name LIKE :name))'
    parameters = {f'{k.lower()}': f'%{v}%' for k, v in filters.items() if k != 'Count'}
    if 'Count' in filters:
        filter_list['Count'] = '(Count >= :count)'
        parameters['count'] = filters['Count']
    filter_list = ' AND '.join(list(filter_list.values()))
    # print(filter_list)

    sql = "SELECT * FROM cards WHERE " + filter_list
    df = pd.read_sql_query(sql, conn, params=parameters)
    df = df.drop(columns=['index', 'Normalized_Name'])
    print(f'{len(df)} cards found for query "{filters}".')
    print(df)


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
    query_parser.add_argument(
        '--year',
        type=int,
        default=None,
    )
    query_parser.add_argument(
        '--series',
        type=str,
        default=None,
    )
    query_parser.add_argument(
        '--set',
        type=str,
        default=None,
    )
    query_parser.add_argument(
        '--name',
        type=str,
        default=None,
    )
    query_parser.add_argument(
        '--team',
        type=str,
        default=None,
    )
    query_parser.add_argument(
        '--features',
        type=str,
        default=None,
    )
    query_parser.add_argument(
        '--min_count',
        type=int,
        default=None,
    )

    args = parser.parse_args()
    if args.mode == 'upload':
        build_db(args.files, args.build)
    elif args.mode == 'search':
        # print(vars(args))
        query_db(vars(args))