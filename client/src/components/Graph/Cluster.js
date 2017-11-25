function Cluster(nodes) {
    var clusters = [
      /*{
        url: "string",
        title: "string"
        nodes: []
        id: 0
        group: 0,
        has_bug: false
      }*/
    ];

    function isCluster(url) {
      var index = 0;

      //if(clusters.length === undefined) return index;
      clusters.forEach( function(cluster, i) {
        if(cluster.url === url) index = i;
      });

      return index;
    }

    for (var i = 0; i < nodes.length; i++) {
      var index = isCluster(nodes[i].url);
      if(index) {
        clusters[index].nodes.push(nodes[i]);
        clusters[index].has_bug = clusters[index].has_bug || nodes[i].has_bug;
        clusters[index].group = nodes[i].group;
      } else {
        clusters.push({
          url: nodes[i].url,
          title: nodes[i].url,
          nodes: [nodes[i]],
          id: "Cluster_" + i,
          groups: nodes[i].group,
          has_bug: nodes[i].has_bug,
        })
      }
    }

    return clusters;

};
export default Cluster;
