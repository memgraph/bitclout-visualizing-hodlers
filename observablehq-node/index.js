const neo4j = require('neo4j-driver');
const fs = require('fs');

const driver = neo4j.driver("bolt://localhost:7687");
const session = driver.session();

const relationToLink = (relation) => {
    return {
        source: relation.start.toString(),
        target: relation.end.toString()
    }
}

const nodeToUser = (node) => {
    return {
        id: node.identity.toString(),
        img: node.properties.image,
        name: node.properties.name,
        group: node.properties.community.toString(),
    }
}

const writeToFile = (data) => {
    const fileName = './data/bitclout.json';
    fs.writeFile(fileName, JSON.stringify(data), 'utf8', (err) => {
        if (err) {
            console.log(`Error writing file: ${err}`);
        } else {
            console.log(`File is written successfully!`);
        }
    });
}

const getData = async () => {
    try {
        const result = await session.writeTransaction(tx =>
            tx.run(
                'match (a)<-[r]-()\n' +
                'with a, count(r) as cnt\n' +
                'order by cnt desc\n' +
                'limit 10\n' +
                'match (a)<-[r]-(b)\n' +
                'where b.isVerified = "True"\n' +
                'return a, r, b'
            )
        )
        const links = [];
        const nodes = {};
        result.records.forEach(record => {
            const relation = relationToLink(record.get('r'));
            links.push(relation);
        });
        result.records.forEach(record => {
            const user = nodeToUser(record.get('a'));
            const user2 = nodeToUser(record.get('b'));
            const userWeight = links.filter(i => i.source === user.id || i.target === user.id).length;
            const user2Weight = links.filter(i => i.source === user2.id || i.target === user2.id).length;
            nodes[user.id] = {...user, weight: userWeight};
            nodes[user2.id] = {...user2, weight: user2Weight};
        });

        writeToFile({nodes: Object.values(nodes), links});
    } catch (e) {
        console.log(e);
    } finally {
        await session.close()
    }
}

getData().catch((e) => console.log(e));
