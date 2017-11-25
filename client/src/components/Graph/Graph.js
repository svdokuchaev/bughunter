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
    const items = this.state.states.nodes && this.state.states.nodes.slice(0, 10).map(node => {
       return <div className={s.nav_box} key={node.id}>
               <h3 className={s.nav_box__title}>{node.title}</h3>
               <div className={s.nav_box__text}>{node.url}</div>
               <div><img className={s.nav_box__image} src="https://placeimg.com/1000/1000/any" /></div>
             </div>
    });
    const nodesCount = this.state.states.nodes && this.state.states.nodes.length;

    return(
      <div>
        <div className={s.header}>
          <div className={s.top}>
            <nav className={s.nav}>
             {items}
            </nav>
          </div>
          <div className={s.bottom}>
          </div>
        </div>
        <div className={s.main}>
          <section id="top" className={[s.one, s.dark, s.cover].join(' ')}>
            <div className={s.container}>
                <h2 className={s.alt}><strong>BUGHUNTER</strong></h2>
            </div>
          </section>
          <section id="portfolio" className={s.two}>
            <div className={s.container}>
              <header>
                <h2>Graph</h2>
                <h2 id="nodesCount">{nodesCount} nodes</h2>
              </header>
              <p>Vitae natoque dictum etiam semper magnis enim feugiat convallis convallis
              egestas rhoncus ridiculus in quis risus amet curabitur tempor orci penatibus.
              Tellus erat mauris ipsum fermentum etiam vivamus eget. Nunc nibh morbi quis
              fusce hendrerit lacus ridiculus.</p>
            </div>
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
          </section>
        </div>
      </div>
    );
  }

  componentDidMount() {
    var svg = d3.select("svg"),
        width = +svg.attr("width"),
        radius = 10,
        height = +svg.attr("height");

   var simulation = d3.forceSimulation();

   //SOCKET IO
   console.log("SOCKET IO is here", io);

    var color = d3.scaleOrdinal(d3.schemeCategory20);

    fetch('http://10.76.178.67:5556/network').then(function (response) {
      var contentType = response.headers.get("content-type");
      if(contentType && contentType.includes("application/json")) {
        return response.json();
      }
    }).then(function (graph) {
      //console.log(graph.nodes);
    //})

    //d3.json("states.json", function(error, graph) {
      //if (error) throw error;

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
                //if (node.source.url === node.target.url) {
                //   return 0.05;
                //} else {
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

      var getId = (id) => { return 'http://10.76.178.67:5556/state?id=' + id };

      var node = svg.selectAll(".node")
        .data(nodes.filter(function(d) { return d.id; }))
        .enter().append("circle")
          .attr("class", this.graph.dataset.node)
          .attr("r", radius)
          .attr("fill", function(d) { return color(d.url); })
          .on("click", function (node) {
            var self = this;
            fetch(getId(node.id)).then(function (response) {
              var contentType = response.headers.get("content-type");
              if(contentType && contentType.includes("application/json")) {
                return response.json();
              }
            }).then(function (a) {
              self.setState({ title: a.title, text: a.url, hidden: false });
            })
          }.bind(this))
          /*.call(d3.drag()
              .on("start", dragstarted)
              .on("drag", dragged)
              .on("end", dragended));*/

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

      d3.interval(function() {
        var node = {
          "id": nodes.length,
          "url": "Что угодно",
          "title": "TT RS",
          "has_bug": null
        };
        nodes.push(node); // Re-add c.
        links.push([nodes[nodes.length - 1], links[links.length], node]); // Re-add b-c.
        //links.push({source: c, target: a}); // Re-add c-a.
        restart();
      }, 2000, d3.now() + 1000);

      function restart() {

        node = node.data(nodes, function(d) { return d.id;});
        node.exit().remove();
        node = node.enter().append("circle").attr("fill", function(d) { return color(d.id); }).attr("r", 8).merge(node);

        link = link.data(links, function(d) {
          //console.log(d, d[0], d[0].id, d[0].url);
          //if(d[0]) debugger;
           return (d[0]) ? d[0].id + "-" + d[2].id : d.source.id + "-" + d.target.id;
         });
        link.exit().remove();
        link = link.enter().append("line").merge(link);

        simulation.nodes(nodes);
        simulation.force("link").links(links);
        simulation.alpha(1).restart();
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
