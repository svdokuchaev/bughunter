import React from 'react';
import withStyles from 'isomorphic-style-loader/lib/withStyles';
import s from './Graph.css';
import Popup from '../../components/Popup';

class Graph extends React.Component {
  constructor(props) {
    super(props);
    this.state = {title: "shit", text: "AAAAAAAAAAAA", screenshot: "", hidden: true, states: {}, stat: {}};
  }
  onPopupClose(hidden) {
    this.setState({hidden: true});
  }
  render() {
    const { title, text, screenshot, hidden } = this.state;
    const items = this.state.states.nodes && this.state.states.nodes.filter(node => node.has_bug/* || node.id % 147 == 0*/)
      .map(node => {
       return <div className={s.nav_box} key={node.id}>
               <h3 className={s.nav_box__title}>{node.title}</h3>
               <div className={s.nav_box__text}>{node.url}</div>
               <div><img className={s.nav_box__image} src={"data:image/png;base64," + node.screenshot} /></div>
             </div>
    });
    const nodesCount = this.state.states.nodes ? this.state.states.nodes.length : 0;

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
                <h2>Statistics</h2>
                <div className={s.stat}>
                  <h2 id="botsCount">Bots: {this.state.stat.bots}</h2>
                  <h2 id="statesCount">States: {this.state.stat.states}</h2>
                  <h2 id="edgesCount">Edges: {this.state.stat.edges}</h2>
                  <h2 id="bugsCount">Bugs: {this.state.stat.bugs}</h2>
                </div>
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
              <div className={s.graphView}>
                <svg width="2000" height="2000"></svg>
              </div>
              <Popup title={title} text={text} hidden={hidden} screenshot={screenshot} onPopupClose={this.onPopupClose.bind(this)} />
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


    fetch('http://10.76.178.67:5556/stats').then(function(response) {
      var contentType = response.headers.get("content-type");
      if(contentType && contentType.includes("application/json")) {
        return response.json();
      }
    }).then(function(a) {
      this.setState({stat: a})
    }.bind(this));

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
      var promises = [];
      graph.nodes.filter(node => node.has_bug).forEach(function(node) {
        promises.push(new Promise(function(resolve, reject) {
          fetch('http://10.76.178.67:5556/state?id=' + node.id).then(function(response) {
            var contentType = response.headers.get("content-type");
            if(contentType && contentType.includes("application/json")) {
              return response.json();
            }
          }).then(function(a) {
            node.screenshot = a.screenshot;
            resolve();
          })
        }))
      });
      Promise.all(promises).then(function() {
        this.setState({states: graph});
      }.bind(this));

      var groups = Array.from(new Set(graph.nodes.map((itemNode) => itemNode.url))),
          nodes = graph.nodes.map((itemNode) => { itemNode.group = (groups.indexOf(itemNode.url) + 1); return itemNode; }),
          nodeById = d3.map(nodes, function(d) { return d.id; }),
          links = graph.links,
          bilinks = [],
          k = Math.sqrt(nodes.length / (width * height));

          //console.log(nodes);

          //console.log(groups);

          var manyBody =
                        d3
                          .forceManyBody()
                          .strength(function () {
                            return -300 * k;
                          });

          simulation.force("link", d3.forceLink()
          .id(function (d) {return d.id;})
          .distance(function (node) {
                //if (node.source.url === node.target.url) {
                //   return 0.05;
                //} else {
                  return 50;
                // }
              }).strength(0.9))
              .force("charge", manyBody)
              // .force("gravity", function () { return -1 * k; })
              .force("center", d3.forceCenter(width / 2, height / 2));

      // links.forEach(function(link) {
      //   var s = link.source = nodeById.get(link.source),
      //       t = link.target = nodeById.get(link.target),
      //       i = {}; // intermediate node
      //   nodes.push(i);
      //   links.push({source: s, target: i}, {source: i, target: t});
      // });

      var link = svg.selectAll(".link")
        .data(links)
        .enter().append("line")
        .attr("class", this.graph.dataset.link)
        .attr("stroke-width", function(d) { return 3; });


      var getId = (id) => { return 'http://10.76.178.67:5556/state?id=' + id };

      var node = svg.selectAll(".node")
        .data(nodes.filter(function(d) { return d.id; }))
        .enter().append("circle")
          .attr("class", this.graph.dataset.node)
          .attr("r", radius)
          .attr("fill", function(d) { return color(d.url); })
          .on("click", function (node) {
            var self = this;
            var promises = [];
            var newState = {};
            promises.push(new Promise(function(resolve, reject) {
              fetch(getId(node.id)).then(function (response) {
                var contentType = response.headers.get("content-type");
                if(contentType && contentType.includes("application/json")) {
                  return response.json();
                }
              }).then(function (a) {
                newState.title = a.title;
                newState.text = a.url;
                newState.hidden = false;
                resolve();
              })
            }));
            promises.push(new Promise(function(resolve, reject) {
              fetch('http://10.76.178.67:5556/state?id=' + node.id).then(function(response) {
                var contentType = response.headers.get("content-type");
                if(contentType && contentType.includes("application/json")) {
                  return response.json();
                }
              }).then(function(a) {
                newState.screenshot = a.screenshot;
                resolve();
              })
            }));
            Promise.all(promises).then(function() {
              //console.log(newState);
              self.setState(newState);
            }.bind(this));
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




    /*d3.interval(function() {

      var node = {
        id: nodes.length + 1,
        title: 'Some random',
        url: 'http://dumbfuck.com',
        group: 1,
        has_bug: false
      };


      nodes.push(node); // Re-add c.
      links.push({source: nodes[nodes.length - 2].id, target: node.id, key: 0}); // Re-add b-c.
      restart();
    }.bind(this), 2000);*/


    function restart() {

      // Apply the general update pattern to the nodes.
      node = node.data(nodes, function(d) { return d.id;});
      node.exit().remove();
      node = node.enter().append("circle").attr("fill", function(d) { return color(d.id); }).attr("r", 8).merge(node);

      // Apply the general update pattern to the links.
      link = link.data(links, function(d) { return d.source.id + "-" + d.target.id; });
      link.exit().remove();
      link = link.enter().append("line").merge(link);

      // Update and restart the simulation.
      simulation.nodes(nodes);
      simulation.force("link").links(links);
      simulation.alpha(0.3).restart();
    }


      function ticked() {
        link
              .attr("x1", function(d) { return d.source.x; })
              .attr("y1", function(d) { return d.source.y; })
              .attr("x2", function(d) { return d.target.x; })
              .attr("y2", function(d) { return d.target.y; });

          node
              .attr("cx", function(d) { return d.x; })
              .attr("cy", function(d) { return d.y; });
        // link.attr("d", positionLink);
        // node.attr("transform", positionNode);
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
