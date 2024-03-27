"""Tests for the DependencyGraph component."""

import pytest

from pipeline_runner.core.dependency_graph import DependencyGraph


class TestDependencyGraph:
    def test_add_and_remove_nodes(self):
        g = DependencyGraph()
        g.add_node("a")
        g.add_node("b")
        assert g.nodes == {"a", "b"}
        g.remove_node("a")
        assert g.nodes == {"b"}

    def test_add_duplicate_node_raises(self):
        g = DependencyGraph()
        g.add_node("a")
        with pytest.raises(ValueError):
            g.add_node("a")

    def test_add_edge(self):
        g = DependencyGraph()
        g.add_node("a")
        g.add_node("b")
        g.add_edge("a", "b")
        assert "b" in g.edges["a"]

    def test_topological_sort_linear(self):
        g = DependencyGraph()
        g.add_node("a")
        g.add_node("b")
        g.add_node("c")
        g.add_edge("a", "b")
        g.add_edge("b", "c")
        order = g.topological_sort()
        assert order.index("c") < order.index("b") < order.index("a")

    def test_topological_sort_single_node(self):
        g = DependencyGraph()
        g.add_node("only")
        order = g.topological_sort()
        assert order == ["only"]

    def test_detect_cycle(self):
        g = DependencyGraph()
        g.add_node("a")
        g.add_node("b")
        g.add_edge("a", "b")
        g.add_edge("b", "a")
        cycles = g.detect_cycles()
        assert len(cycles) > 0
