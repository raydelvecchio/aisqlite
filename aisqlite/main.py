import sqlite3
import string
import re
from openai import OpenAI

class AISQLite:
    def __init__(self, dbname: str, autoconnect: bool = True, openai_api_key: str = None):
        self.dbname = dbname if dbname.endswith('.db') else f"{dbname}.db"
        self.conn = None
        self.cursor = None

        if autoconnect:
            self.connect()

        self.llm = OpenAI(api_key=self.openai_api_key) if openai_api_key else None

    def connect(self):
        """
        Connect to the SQLite3 database with the given name.
        """
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()
    
    def close(self):
        """
        Close the SQLite3 database connection.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    def execute(self, sql_query: str, params: tuple = ()):
        """
        Given a query and parameters, execute the query.
        """
        self.cursor.execute(sql_query, params)
    
    def fetchall(self) -> list[tuple]:
        """
        Fetch all results from the latest query via the cursor.
        """
        return self.cursor.fetchall()

    def fetchone(self) -> list[tuple]:
        """
        Fetch one result from the latest query via the cursor.
        """
        return [self.cursor.fetchone()]

    def fetchmany(self, num: int) -> list[tuple]:
        """
        Fetch many results from the latest query via the cursor. If num > results, it cuts off to the maximum amount.
        """
        return self.cursor.fetchmany(size=num)
    
    def execute_and_fetch(self, sql_query: str, params: tuple = (), num: int = -1) -> list[tuple]:
        """
        Execute the query and return the results. By default, return all results. However, can change this.
        """
        self.cursor.execute(sql_query, params)
        if num == -1:
            return self.fetchall()
        if num == 0:
            return [()]
        if num == 1:
            return self.fetchone()
        else:
            return self.fetchmany(num=num)
        
    def schema(self, include_dtype: bool = False) -> dict:
        """
        Gets the table schema of the database in a readable format.
        """
        tables = self.execute_and_fetch("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")  # exclude sqlite_sequence table

        schema = {}
        for table_name in tables:
            table_name = table_name[0]
            schema[table_name] = []
            columns = self.execute_and_fetch(f"PRAGMA table_info({table_name})")
            if include_dtype:
                schema[table_name] = [{'column_name': column[1], 'data_type': column[2]} for column in columns]
            else:
                schema[table_name].extend([column[1] for column in columns])
        
        return schema
    
    def generate_sql(self, language_query: str, model: str = 'gpt-4-0125-preview') -> dict:
        """
        Given natural language query, generate SQL to operate over this database.
        """
        if not self.llm:
            raise Exception("No OpenAI API key passed in; cannot generate SQL.")

        common_suffixes = ['ing', 'ly', 'ed', 'ious', 'es', 's', 'ment', 'tion', 'ness']
        query = language_query.translate(str.maketrans('', '', string.punctuation))
        query_words = query.split()
        for i, word in enumerate(query_words):
            for suffix in common_suffixes:
                if word.endswith(suffix):
                    query_words[i] = word[:-len(suffix)]
        query = ' '.join(query_words)
        
        system_prompt = "You are a SQL generating service. You will receive a sqlite3 database schema in the form [{table_name: list_of_column_names},]. You will also receive a natural language query about the data. Your job is to turn that natural language query into a SQL query to get the relevant data. Do not respond to this prompt, and only output the SQL you generate. When checking fields, always use the 'like' keyword. Only output one query, as you can only execute one at once. The schema and query are as follows:"
        query = f"Schema: {self.schema()}\n\nQuery: {query}"

        messages = [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': query}]
        completion = self.llm.chat.completions.create(model=model, messages=messages)
        sql = completion.choices[0].message.content
        sql = re.sub(r"```.*?\n|```", "", sql)
        return sql.lower()
    
    def generated_execute_and_fetch(self, language_query: str, model: str = 'gpt-4-0125-preview', num: int = -1, allow_modify: bool = False) -> [()]:
        """
        Generate SQL from natural language and return the results. If allow_modify is True, we allow the model to modify the database.
        """
        sql = self.generate_sql(language_query=language_query, model=model)
        modify_keywords = ['insert', 'update', 'delete', 'drop', 'create', 'add', 'truncate']  # keywords that modify data
        if not allow_modify and any(keyword in sql for keyword in modify_keywords):
            print(f"Query BLOCKED: will modify the database. Pass allow_modify=True if this is your intention. Query: '''{sql}'''")
            return [()]
        
        return self.execute_and_fetch(sql, num=num)
