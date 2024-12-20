from impala.dbapi import connect
import re
conn = connect(host="", 
    port = 443, 
    auth_mechanism = "LDAP",
    use_ssl = True, 
    use_http_transport = True,
    http_path = "<datahub>/cdp-proxy-api/impala",
    user = "",
    password = "")

cursor = conn.cursor()

cursor.execute("SHOW DATABASES")
databases = cursor.fetchall()

for db in databases:
    database_name = db[0]
    print(f"Processing database: {database_name}")

    cursor.execute(f"USE {database_name}")

    cursor.execute(f"SHOW TABLES IN {database_name}")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        print(f"  Processing table: {table_name}")
        
        ddl_query = f"DESCRIBE FORMATTED {database_name}.{table_name}"
        cursor.execute(ddl_query)
        ddl_output = cursor.fetchall()

        location_clause = None
        for row in ddl_output:
            if row[0] and 'Location' in row[0]:
                location_clause = row[1]
                break

        if location_clause:
            print(f"    Current LOCATION clause for {table_name}: {location_clause}")
            
            new_location = location_clause.replace('prodstorage', 'drstorage')
            print(f"    Updated LOCATION clause for {table_name}: {new_location}")
            
            alter_ddl = f"ALTER TABLE {database_name}.{table_name} SET LOCATION '{new_location}'"
            
            try:
                cursor.execute(alter_ddl)
                print(f"    Successfully updated the location of table '{table_name}' to '{new_location}'.")
            except Exception as e:
                print(f"    Error updating location for table {table_name}: {e}")
        else:
            print(f"    No LOCATION clause found for table {table_name}. Skipping...")

cursor.close()
conn.close()