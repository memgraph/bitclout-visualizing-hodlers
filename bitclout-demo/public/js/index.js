const width = 800;
const height = 600;

var links;
var nodes;

var simulation;
var transform;

var canvas = d3.select("canvas");
var context = canvas.node().getContext('2d');

var xmlhttp = new XMLHttpRequest();
xmlhttp.open("GET", '/load-all', true);
xmlhttp.setRequestHeader('Content-type', 'application/json; charset=utf-8');

xmlhttp.onreadystatechange = function () {
    if (xmlhttp.readyState == 4 && xmlhttp.status == "200") {
        data = JSON.parse(xmlhttp.responseText);
        links = data.links;
        nodes = data.nodes;

        simulation = d3.forceSimulation()
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("x", d3.forceX(width / 2).strength(0.1))
            .force("y", d3.forceY(height / 2).strength(0.1))
            .force("charge", d3.forceManyBody().strength(-50))
            .force("link", d3.forceLink().strength(1).id(function (d) { return d.id; }))
            .alphaTarget(0)
            .alphaDecay(0.05);

        transform = d3.zoomIdentity;

        d3.select(context.canvas)
            .call(d3.drag().subject(dragsubject).on("start", dragstarted).on("drag", dragged).on("end", dragended))
            .call(d3.zoom().scaleExtent([1 / 10, 8]).on("zoom", zoomed));

        simulation.nodes(nodes)
            .on("tick", simulationUpdate);

        simulation.force("link")
            .links(links);
    }
}
xmlhttp.send();

function zoomed(event) {
    transform = event.transform;
    simulationUpdate();
}

var radius = 5;

function dragsubject(event) {
    var i,
        x = transform.invertX(event.x),
        y = transform.invertY(event.y),
        dx,
        dy;
    for (i = nodes.length - 1; i >= 0; --i) {
        node = nodes[i];
        dx = x - node.x;
        dy = y - node.y;

        if (dx * dx + dy * dy < radius * radius) {
            node.x = transform.applyX(node.x);
            node.y = transform.applyY(node.y);
            return node;
        }
    }
}

function simulationUpdate() {
    context.save();
    context.clearRect(0, 0, width, height);
    context.translate(transform.x, transform.y);
    context.scale(transform.k, transform.k);

    links.forEach(function (d) {
        context.beginPath();
        context.moveTo(d.source.x, d.source.y);
        context.lineTo(d.target.x, d.target.y);
        context.stroke();
    });
    nodes.forEach(function (d, i) {
        context.beginPath();
        context.arc(d.x, d.y, radius, 0, 2 * Math.PI, true);
        context.fillStyle = "#FFA500";
        context.fill();
    });
    
    context.restore();
}

function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = transform.invertX(event.x);
    event.subject.fy = transform.invertY(event.y);
}

function dragged(event) {
    event.subject.fx = transform.invertX(event.x);
    event.subject.fy = transform.invertY(event.y);
}

function dragended(event) {
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
}
