Graph
=====

An easy-to-use graph implementation. Here's the class interface:

    template <typename NodeId = int, typename NodeData = int,
              typename EdgeData = int, bool Directed = false>
    class Graph {
      public:
        using NodeIdType    = NodeId;
        using NodeDataType  = NodeData;
        using NodeType      = Node<NodeId, NodeData, EdgeData>;

        using EdgeDataType  = EdgeData;
        using EdgeType      = Edge<NodeId, NodeData, EdgeData>;

        Graph()             = default;
        Graph(Graph&&)      = default;
        Graph(const Graph&) = delete;

        Graph& operator=(Graph&&)      = default;
        Graph& operator=(const Graph&) = delete;

        bool directed() const;

        // unspecified-order node iterators
        auto nodesSize();
        auto nodesBegin();
        auto nodesEnd();

        // unspecified-order edge iterators
        auto edgesSize();
        auto edgesBegin();
        auto edgesEnd();

        // breadth-first node iterators (movable but non-copyable)
        auto breadthBegin(NodeId start);
        auto breadthEnd();

        // depth-first node iterators (movable but non-copyable)
        auto depthBegin(NodeId start, bool postorder = false);
        auto depthEnd(bool postorder = false);

        bool hasNode(NodeId id) const;
        NodeType* getNode(NodeId id) const;
        NodeType* addNode(NodeId id, const NodeData& data = NodeData());

        bool hasEdge(NodeId startNodeId, NodeId endNodeId) const;
        EdgeType* getEdge(NodeId startNodeId, NodeId endNodeId) const;
        EdgeType* addEdge(NodeId startNodeId, NodeId endNodeId,
                          const EdgeData& edgeData = EdgeData(),
                          const NodeData& startNodeData = NodeData(),
                          const NodeData& endNodeData = NodeData());
    };

Where `Node` and `Edge` have the following interfaces:

    template <typename NodeId, typename NodeData, typename EdgeData>
    class Node {
      public:
        using NodeType = Node<NodeId, NodeData, EdgeData>;
        using EdgeType = Edge<NodeId, NodeData, EdgeData>;

        NodeId    id()   const;
        NodeData& data() const;

        // adjacent edges
        auto edgesSize() const;
        auto edgesBegin();
        auto edgesEnd();

        // adjacent nodes
        auto nodesSize() const;
        auto nodesBegin();
        auto nodesEnd();

        size_t indegree()  const;
        size_t outdegree() const;
    };

    template <typename NodeId, typename NodeData, typename EdgeData>
    class Edge {
      public:
        using NodeType = Node<NodeId, NodeData, EdgeData>;
        using EdgeType = Edge<NodeId, NodeData, EdgeData>;

        bool hasNode(const NodeType* n) const;

        NodeType* startNode() const;
        NodeType* endNode() const;
        EdgeData& data();

        // given a node on the edge, returns the other node.
        // the given node must be on the edge.
        NodeType* otherNode(const NodeType* n) const;
    };

Finally, the breadth-first iterator and depth-first iterators have the regular
forward-iterator interface except that they're non-copyable. Moreover, the
breadth-first iterator has a `parent()` method that returns the parent node of
the current node.

Following is a dynamic-programming implementation of breadth-first
shortest-distance algorithm using this class (HackerRank's first graph problem):

    #include <iostream>
    #include "graph.hpp"

    using namespace artifacts;
    using namespace std;

    template <typename NodeId>
    struct NodePairHasher {
      size_t operator()(const std::pair<NodeId, NodeId>& nodePair) const {
        size_t seed = 0;
        hash_combine(seed, nodePair.first);
        hash_combine(seed, nodePair.second);

        return seed;
      }
    };

    template <typename NodeId = int, typename NodeData = int, typename EdgeData = int,
              bool Directed = false>
    class ShortestDistCalc {
      public:
        using GraphType = Graph<NodeId, NodeData, EdgeData, Directed>;
        using NodePair  = std::pair<NodeId, NodeId>;

        ShortestDistCalc(GraphType& g):
          _g(g)
        {}

        bool hasDistance(NodeId s, NodeId e) const {
          if (s == e) {
            return true;
          }

          if (!_g.directed() && e < s) {
            std::swap(s, e);
          }

          return _distances.find(NodePair(s, e)) != _distances.end();
        }

        int distance(NodeId s, NodeId e) const {
          if (s == e) {
            return 0;
          }

          if (!_g.directed() && e < s) {
            std::swap(s, e);
          }

          return _distances.at(NodePair(s, e));
        }

        void addDistance(NodeId s, NodeId e, int dist) {
          if (s == e) {
            return;
          }

          if (!_g.directed() && e < s) {
            std::swap(s, e);
          }

          _distances[NodePair(s, e)] = dist;
        }

        int exec(NodeId s, NodeId e) {
          if (!_g.directed() && e < s) {
            std::swap(s, e);
          }

          if (hasDistance(s, e)) {
            return distance(s, e);
          }

          auto sIt  = _g.breadthBegin(s), eIt = _g.breadthBegin(e),
              last = _g.breadthEnd();

          ++sIt;
          ++eIt;

          for (; sIt != last && eIt != last; ++sIt, ++eIt) {
            auto sId = (*sIt)->id();
            auto sParentId = sIt.parent()->id();

            auto eId = (*eIt)->id();
            auto eParentId = eIt.parent()->id();

            addDistance(sId, sParentId, _g.getEdge(sId, sParentId)->data());
            addDistance(eId, eParentId, _g.getEdge(eId, eParentId)->data());

            addDistance(s, sId, distance(s, sParentId) + distance(sParentId, sId));
            addDistance(e, eId, distance(e, eParentId) + distance(eParentId, eId));

            if (hasDistance(s, e)) {
              return distance(s, e);
            }
          }

          addDistance(s, e, -1);
          return -1;
        }

      private:
        GraphType& _g;
        std::unordered_map<NodePair, int, NodePairHasher<NodeId>> _distances;
    };

    void printShortestDists(Graph<>& g, int s, int n) {
      ShortestDistCalc<> calc(g);
      for (int i = 1; i <= n; ++i) {
        if (i != s) {
          cout << calc.exec(s, i) << ' ';
        }
      }

      cout << '\n';
    }

    int main() {
      int t, n, m, b, e, s;
      cin >> t;
      for (int i = 0; i < t; ++i) {
        Graph<> g;

        cin >> n >> m;
        for (int j = 1; j <= n; ++j) {
          g.addNode(j);
        }

        for (int j = 0; j < m; ++j) {
          cin >> b >> e;
          g.addEdge(b, e, 6);
        }

        cin >> s;

        printShortestDists(g, s, n);
      }
    }

