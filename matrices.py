import numpy as np


def translation_matrix(dx: float, dy: float, dz: float) -> np.array:
    matrix = np.eye(4)
    matrix[-1][:3] = dx, dy, dz

    return matrix


def x_rotation_matrix(radians: float) -> np.array:
    sin = np.sin(radians)
    cos = np.cos(radians)
    matrix = np.eye(4)
    matrix[1:3, 1:3] = np.array([cos, -sin, sin, cos]).reshape(2, 2)
    return matrix


def y_rotation_matrix(radians: float) -> np.array:
    sin = np.sin(radians)
    cos = np.cos(radians)
    matrix = np.eye(4)
    matrix[0, 0] = cos
    matrix[0, 2] = sin
    matrix[2, 0] = -sin
    matrix[2, 2] = cos
    return matrix


def z_rotation_matrix(radians: float) -> np.array:
    sin = np.sin(radians)
    cos = np.cos(radians)
    matrix = np.eye(4)
    matrix[0:2, 0:2] = np.array([cos, -sin, sin, cos]).reshape(2, 2)
    return matrix
