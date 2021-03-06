from faker import Faker 
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Returns configuration of database
def get_config():
    return {
        "dbname": "postgres",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": "5432"
    }

# Connecting to database -> creating table CUSTOMERS -> inserting fake data
def create_db(config):
    conn = psycopg2.connect(**config)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS customers;")
    cur.execute('''
                    CREATE TABLE customers (
                        id serial PRIMARY KEY,
                        name varchar(50),
                        address varchar(100),
                        age int,
                        review varchar(300)
                    );
                '''
    )
    
    fake = Faker()
    print("Inserting values into database...")
    for i in range(100000):
        cur.execute("INSERT INTO customers (name, address, age, review) VALUES (%s, %s, %s, %s);", (fake.name(), fake.address(), fake.pyint(18, 100), fake.pystr()))
    print("Values are succesfully inserted.")
    conn.commit()
    cur.close()
    conn.close()

# Analyze query and print result
def analyze_query(cur, query):
    cur.execute("EXPLAIN ANALYZE " + query)
    for item in cur.fetchall():
        print(item[0])

def main():
    config = get_config() 
    create_db(config)
    conn = psycopg2.connect(**config)
    cur = conn.cursor()

    query_1 = "SELECT name FROM customers WHERE age > 50 AND age < 70"
    query_2 = "SELECT name FROM customers WHERE name = 'Lucy'"
    print("BEFORE CREATING INDEXES:")
    analyze_query(cur, query_1)
    analyze_query(cur, query_2)
    print("AFTER CREATING INDEXES:")
    cur.execute("CREATE INDEX age_idx ON customers USING btree(age);")
    cur.execute("CREATE INDEX name_idx ON customers USING hash(name);")
    analyze_query(cur, query_1)
    analyze_query(cur, query_2)

if __name__ == "__main__":
    main()
