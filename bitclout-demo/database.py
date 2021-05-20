def load_data(cursor):
    cursor.execute("""MATCH (n) 
                      DETACH DELETE n;""")
    cursor.fetchall()
    cursor.execute("""CREATE INDEX ON :User(id);""")
    cursor.fetchall()
    cursor.execute("""CREATE INDEX ON :User(name);""")
    cursor.fetchall()
    cursor.execute("""CREATE CONSTRAINT ON (user:User) 
                      ASSERT user.id IS UNIQUE;""")
    cursor.fetchall()
    cursor.execute("""LOAD CSV FROM '/usr/lib/memgraph/import-data/profiles-1.csv' 
                      WITH header AS row
                      CREATE (sample:User {id: row.id})
                      SET sample += {
                        name: row.name,
                        description: row.description,
                        image: row.image,
                        isHidden: row.isHidden,
                        isReserved: row.isReserved,
                        isVerified: row.isVerified,
                        coinPrice: row.coinPrice,
                        creatorBasisPoints: row.creatorBasisPoints,
                        lockedNanos: row.lockedNanos,
                        nanosInCirculation: row.nanosInCirculation,
                        watermarkNanos: row.watermarkNanos
                      };""")
    cursor.fetchall()
    cursor.execute("""LOAD CSV FROM '/usr/lib/memgraph/import-data/profiles-2.csv' 
                      WITH header AS row
                      CREATE (sample:User {id: row.id})
                      SET sample += {
                        name: row.name,
                        description: row.description,
                        image: row.image,
                        isHidden: row.isHidden,
                        isReserved: row.isReserved,
                        isVerified: row.isVerified,
                        coinPrice: row.coinPrice,
                        creatorBasisPoints: row.creatorBasisPoints,
                        lockedNanos: row.lockedNanos,
                        nanosInCirculation: row.nanosInCirculation,
                        watermarkNanos: row.watermarkNanos
                      };""")
    cursor.fetchall()
    cursor.execute("""LOAD CSV FROM '/usr/lib/memgraph/import-data/hodls.csv' 
                      WITH header AS row
                      MATCH (hodler:User {id: row.from})
                      MATCH (creator:User {id: row.to})
                      CREATE (hodler)-[:HODLS {amount: row.nanos}]->(creator);""")
    cursor.fetchall()
