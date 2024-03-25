"""Dependency graph for tracking relationships between pipeline steps."""

from collections import deque
from typing import Dict, List, Set


class DependencyGraph:
    """Directed graph for managing dependencies between steps."""

    def __init__(self) -> None:
        self._nodes: Set[str] = set()
        self._edges: Dict[str, Set[str]] = {}

    def add_node(self, name: str) -> None:
        if name in self._nodes:
            raise ValueError(f"Node '{name}' already exists")
        self._nodes.add(name)
        self._edges[name] = set()

    def add_edge(self, from_node: str, to_node: str) -> None:
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
        if name not in self._nodes:
            raise ValueError(f"Node '{name}' not in graph")
        self._nodes.discard(name)
        del self._edges[name]
        for node in self._edges:
            self._edges[node].discard(name)

    def topological_sort(self) -> List[str]:
        """Return nodes in topological order using Kahn's algorithm.

        Raises ValueError if the graph contains a cycle.
        """
        in_degree: Dict[str, int] = {}
        for node in self._nodes:
            for dep in self._edges[node]:
                in_degree[dep] = in_degree.get(dep, 0) + 1

        # FIX: use .get(node, 0) so nodes absent from in_degree (zero
        # incoming edges) are correctly seeded into the queue.
        queue = deque(
            node for node in self._nodes
            if in_degree.get(node, 0) == 0
        )
        result: List[str] = []
        while queue:
            current = queue.popleft()
            result.append(current)
            for neighbor in self._edges.get(current, set()):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(result) != len(self._nodes):
            raise ValueError("Graph contains a cycle")
        return result

    def detect_cycles(self) -> List[List[str]]:
        """Detect cycles in the graph using DFS."""
        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        cycles: List[List[str]] = []
        path: List[str] = []

        def _dfs(node: str) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            for neighbor in self._edges.get(node, set()):
                if neighbor not in visited:
                    _dfs(neighbor)
                elif neighbor in rec_stack:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            path.pop()
            rec_stack.discard(node)

        for node in self._nodes:
            if node not in visited:
                _dfs(node)
        return cycles

    @property
    def nodes(self) -> Set[str]:
        return set(self._nodes)

    @property
    def edges(self) -> Dict[str, Set[str]]:
        return {k: set(v) for k, v in self._edges.items()}
