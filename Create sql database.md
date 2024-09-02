Steps to be executed in the terminal:<br>

1.Install sqlite3 <br>

2.Create a database:
<pre>sqlite3 data/sqldb.db</pre>
Note:this ones ins created in the folder data

3.Copy database from your sql database:
<pre>.read data/sql/<name of your sql database>.sql</pre>

4.To test the database, run a command. For example:
<pre>SELECT * FROM <any Table name in your sql database> LIMIT 10;</pre>