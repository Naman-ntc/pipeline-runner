"""Dependency graph for tracking relationships between pipeline steps."""

from typing import Dict, Set


class DependencyGraph:
    """Directed graph for managing dependencies between steps."""

    def __init__(self) -> None:
        self._nodes: Set[str] = set()
        self._edges: Dict[str, Set[str]] = {}

    def add_node(self, name: str) -> None:
        """Add a node to the graph."""
        if name in self._nodes:
            raise ValueError(f"Node '{name}' already exists")
        self._nodes.add(name)
        self._edges[name] = set()

    def add_edge(self, from_node: str, to_node: str) -> None:
        """Add a directed edge indicating from_node depends on to_node."""
        if from_node not in self._nodes:
            raise ValueError(f"Node '{from_node}' not in graph")
        if to_node not in self._nodes:
            raise ValueError(f"Node '{to_node}' not in graph")
        if to_node in self._edges[from_node]:
            raise ValueError(
                f"Edge '{from_node}' -> '{to_node}' already exists"
            )
        self._edges[from_node].add(to_node)

    def remove_node(self, name: str) -> None:
        """Remove a node and all associated edges."""
        if name not in self._nodes:
            raise ValueError(f"Node '{name}' not in graph")
        self._nodes.discard(name)
        del self._edges[name]
        for node in self._edges:
            self._edges[node].discard(name)

    @property
    def nodes(self) -> Set[str]:
        """Return a copy of the node set."""
        return set(self._nodes)

    @property
    def edges(self) -> Dict[str, Set[str]]:
        """Return a deep copy of the edge mapping."""
        return {k: set(v) for k, v in self._edges.items()}
