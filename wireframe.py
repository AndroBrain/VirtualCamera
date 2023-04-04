from os import listdir
from os.path import isfile, join
from typing import List, Tuple

import numpy as np


def load_models_from_folder(foler_name: str) -> List:
    files = [f for f in listdir(foler_name) if isfile(join(foler_name, f))]
    return [Wireframe.load_from_file(join(foler_name, f)) for f in files]


class Wireframe:

    def __init__(self):
        super().__init__()
        # Nodes are stored in single row matrix to allow fast matrix operations
        self.nodes = np.zeros([0, 4])  # Format: (x, y, z, 1)
        # Edges are list of tuples that are numbers of given nodes
        self.edges = []

    def add_nodes(self, nodes: np.array) -> None:
        with_ones = np.hstack([nodes, np.ones([nodes.shape[0], 1])])
        self.nodes = np.vstack([self.nodes, with_ones])

    def add_edges(self, edge_list: List[Tuple[int, int]]) -> None:
        self.edges.extend(edge_list)

    def transform(self, transformation_matrix: np.array) -> None:
        # Matrix multiplication
        self.nodes = self.nodes @ transformation_matrix

    @staticmethod
    def load_from_file(file_name: str):
        i = 0
        loaded_points = dict()
        loaded_edges = []

        with open(file_name, 'r') as file:
            for line in file.readlines():
                points = [float(p) for p in line.split(', ')]
                start = tuple(points[:3])
                end = tuple(points[3:])

                # print(start)
                # print(end)

                for point in (start, end):
                    if point not in loaded_points:
                        loaded_points[point] = i
                        i += 1

                loaded_edges.append((loaded_points[start], loaded_points[end]))

        sorted_points = sorted(loaded_points.items(), key=lambda x: x[1])
        sorted_points = list(zip(*sorted_points))[0]

        wireframe = Wireframe()
        wireframe.add_nodes(np.array(sorted_points))
        wireframe.add_edges(loaded_edges)

        return wireframe
