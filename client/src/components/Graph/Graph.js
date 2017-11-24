import React from 'react';
import withStyles from 'isomorphic-style-loader/lib/withStyles';
import s from './Graph.css';
import Popup from '../../components/Popup';

class Graph extends React.Component {
  constructor(props) {
    super(props);
    this.state = {title: "shit", text: "AAAAAAAAAAAA", hidden: true, states: {}};
  }
  onPopupClose(hidden) {
    this.setState({hidden: true});
  }
  render() {
    const { title, text, hidden } = this.state;
    return(
      <div
          id="graph"
          className={s.root}
          data-link={s.link}
          data-node={s.node}
          ref={(graph) => { this.graph = graph; }}
        >
        <svg width="2000" height="2000"></svg>
        <Popup title={title} text={text} hidden={hidden} onPopupClose={this.onPopupClose.bind(this)} />
      </div>
    );
  }

  componentDidMount() {
    var svg = d3.select("svg"),
        width = +svg.attr("width"),
        radius = 10,
        height = +svg.attr("height");

   var simulation = d3.forceSimulation();

    var color = d3.scaleOrdinal(d3.schemeCategory20);
    d3.json("states.json", function(error, graph) {
      if (error) throw error;

      this.setState({states: graph});

      var groups = Array.from(new Set(graph.nodes.map((itemNode) => itemNode.url))),
          nodes = graph.nodes.map((itemNode) => { itemNode.group = (groups.indexOf(itemNode.url) + 1); return itemNode; }),
          nodeById = d3.map(nodes, function(d) { return d.id; }),
          links = graph.links,
          bilinks = [],
          k = Math.sqrt(nodes.length / (width * height));

          console.log(nodes);

          console.log(groups);

          var manyBody =
                        d3
                          .forceManyBody()
                          .strength(function () {
                            return -500 * k;
                          });

          simulation.force("link", d3.forceLink().distance(function (node) {
                // if (node.source.url === node.target.url) {
                //   return 0.05;
                // } else {
                  return 100;
                // }
              }).strength(0.9))
              .force("charge", manyBody)
              // .force("gravity", function () { return -1 * k; })
              .force("center", d3.forceCenter(width / 2, height / 2));

      links.forEach(function(link) {
        var s = link.source = nodeById.get(link.source),
            t = link.target = nodeById.get(link.target),
            i = {}; // intermediate node
        nodes.push(i);
        links.push({source: s, target: i}, {source: i, target: t});
        bilinks.push([s, i, t]);
      });

      var link = svg.selectAll(".link")
        .data(bilinks)
        .enter().append("path")
          .attr("class", this.graph.dataset.link);

      var node = svg.selectAll(".node")
        .data(nodes.filter(function(d) { return d.id; }))
        .enter().append("circle")
          .attr("class", this.graph.dataset.node)
          .attr("r", radius)
          .attr("fill", function(d) { return color(d.url); })
          .on("click", function (node) {
            this.setState({ title: node.title, text: node.url, hidden: false });
          }.bind(this))
          .call(d3.drag()
              .on("start", dragstarted)
              .on("drag", dragged)
              .on("end", dragended));

      node.append("title")
          .text(function(d) { return d.url; });

      simulation
          .nodes(nodes)
          .on("tick", ticked);

      simulation.force("link")
          .links(links);

      function ticked() {
        link.attr("d", positionLink);
        node.attr("transform", positionNode);
      }
    }.bind(this));

    function positionLink(d) {
      return "M" + d[0].x + "," + d[0].y
           + "S" + d[1].x + "," + d[1].y
           + " " + d[2].x + "," + d[2].y;
    }

    function positionNode(d) {
      return "translate(" + d.x + "," + d.y + ")";
    }

    function dragstarted(d) {
      if (!d3.event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x, d.fy = d.y;
    }

    function dragged(d) {
      d.fx = d3.event.x, d.fy = d3.event.y;
    }

    function dragended(d) {
      if (!d3.event.active) simulation.alphaTarget(0);
      d.fx = null, d.fy = null;
    }
  }
  componentDidUpdate() {
  }
}

export default withStyles(s)(Graph);
