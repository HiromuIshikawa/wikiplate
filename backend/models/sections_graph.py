# -*- coding: utf-8 -*-
from ..lib import accessor as ac
import numpy as np

class SectionsGraph:
    """
    sections graph class for recommend sections of new template
    """

    nodes = ac.reader("_nodes")
    edges = ac.reader("_edges")
    djacency = ac.reader("_djacency")

    def __init__(self):
        self._nodes = ["_s","_e"]
        self._edges = []
        self._djacency = []

    def add_sections(self, secs):
        src = 0
        dest = 0
        for section in secs:
            try:
                dest = self._nodes.index(section)
            except ValueError:
                dest = len(self._nodes) -1
                self._nodes.insert(dest, section)

            self._edges.append((src, dest))
            src = dest

        self._edges.append((src, -1))

    def create_djacency(self):
        size = len(self._nodes)
        count_djacency = np.zeros((size, size))
        for edge in self._edges:
            count_djacency[edge[0], edge[1]] += 1

        self._djacency = count_djacency

    def dijkstra_path(self):
        size = len(self._nodes)
        V = np.array(range(size))
        prev = np.empty(size)
        d = np.zeros(size)
        d[1:] = np.inf
        u = 0
        Q = V

        while len(Q) > 0:
            du = np.inf
            for n in Q:
                if d[n] < du:
                    u = n
                    du = d[n]
            Q = Q[~(Q == u)]
            for v in np.where(self._djacency[u] != 0.0)[0]:
                if(d[v] > (d[u] + 1/self._djacency[u,v])):
                    d[v] = d[u] + 1/self._djacency[u,v]
                    prev[v] = u

        sections = []
        section_index = -1
        while section_index != 0:
            section_index = int(prev[section_index])
            if section_index == 0:
                break
            sections.insert(0, self._nodes[section_index])
        return sections
