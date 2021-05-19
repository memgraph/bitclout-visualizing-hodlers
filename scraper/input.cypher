create index on :User(id);
create index on :User(name);
create constraint on (user:User) assert user.id is unique;

load csv from '/profiles.csv' with header as row
create (sample:User {id: row.id})
set sample += {
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
};

load csv from '/hodls.csv' with header as row
match (hodler:User {id: row.from})
match (creator:User {id: row.to})
create (hodler)-[:HODLS {amount: row.nanos}]->(creator);

match (a)-[r]->(b)
with a, b, collect(r) as relationships
where size(relationships) > 1 and relationships[0]['amount'] = relationships[1]['amount']
delete relationships[0];

call louvain.get() yield community, node
with community, node.id as user_id
match (user:User {id: user_id})
set user.community = community;

match (a)<-[r]-(b)
with a, sum(case b.name when null then 0 else 1 end) as anonymousHodlers, count(r) as hodlers
set a.numberOfHodlers = hodlers
set a.numberOfAnonymousHodlers = anonymousHodlers;
