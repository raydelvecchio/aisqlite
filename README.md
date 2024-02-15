# AISQLite
AI enhanced wrapper around sqlite. Can still execute your queries in sqlite fashion, but can also retrieve data via natural language queries powered by OpenAI.

# Documentation
## Class `AISQLite`
* `__init__`: constructor for AISQLite
    * **dbname (str)**: the database name you want to use with AISQLite. Can pass in either an existing database or name one yourself, but must end in *.db*. Will save
    this to disk.
    * **autoconnect (bool)**: if we want to connect the connection and cursor objects upon initialization. If true, will connect and initialize cursor without
    having to do it manually.
    * **openai_api_key (str)**: the openai API key you want to use when generating SQL. If you don't pass in an API key, you can't use the generative features.
* `connect`: connects the connection object and initializes cursor object as internal variables.
* `close`: close connection and cursor objects.
* `execute`: executes the given query and parameters. Simply executes with the cursor, but does not return any results.
    * **sql_query (str)**: string of sql query you want to execute. 
    * **params (tuple)**: parameters we want to pass to the cursor, just like regular sqlite.
* `fetchall`: fetches all results from the last executed query from the cursor. Returns a list of tuples of results.
* `fetchone`: fetches one result from the last executed query from the cursor.
* `fetchmany`: fetches a defined number of results from the last executed query.
    * **num (int)**: number of results we want to get. If this is > len(results), it returns all results. Returns nothing if = 0, defaults to all if -1.
* `execute_and_fetch`: executes a query and returns all results from it in one command.
    * **sql_query (str)**: string of sql query you want to execute. 
    * **params (tuple)**: parameters we want to pass to the cursor, just like regular sqlite.
    * **num (int)**: number of results we want to get. If this is > len(results), it returns all results. Returns nothing if = 0, defaults to all if -1.
* `schema`: gets the schema of the database (tables and columns) in a readable format (as a dictionary). 
    * **include_dtype (bool)**: if we want to include the data type in the schema or not.
* `generate_sql`: given a natural language query, generate sql to complete the query. Returns the SQL, but does not execute it.
    * **language_query (str)**: the natural language query we want to use to generate SQL from.
    * **model (str)**: the OpenAI model we want to use to generate sql. Default to latest GPT4 turbo model.
* `generated_execute_and_fetch`: given a natural language query, generate SQL to complete it and return the results.
    * **language_query (str)**: the natural language query we want to use to generate SQL from.
    * **model (str)**: the OpenAI model we want to use to generate sql. Default to latest GPT4 turbo model.
    * **num (int)**: number of results we want to get. If this is > len(results), it returns all results. Returns nothing if = 0, defaults to all if -1.
    * **allow_modify (bool)**: if we want the query to modify the database or not. Good control access for the LLM. If True, we allow the query to execute even if
    it will modify the LLM. If False, it will block all modification queries and display a warning message.

# Pip Deploy
1. Delete existing `dist` and `build`.
2. `python3 setup.py sdist bdist_wheel`
3. `twine upload dist/*`
