from typing import Tuple
import functools
import numpy
import numpy as np
import pygame

from Controls import handle_zoom, handle_horizontal_movement, handle_vertical_movement, handle_looking, \
    handle_bias_looking
from worldMap import load_figures_from_path


# Map 3D map to 2D display
def projection(point_3d: np.array, view_width: float, view_height: float, focal: float) -> Tuple[float, float]:
    # f / z
    if point_3d[1] == 0:
        div = 0.0001
    else:
        div = point_3d[1]

    from_focal = abs(focal / div)

    # We need to move to the middle of the camera
    # x' = x * (f / z)
    x = from_focal * point_3d[0] + view_width / 2
    # y' = y * (f / z)
    y = view_height / 2 - from_focal * point_3d[2]

    return x, y


def is_point_visible(point_3d: np.array, focal: float) -> bool:
    return point_3d[1] > focal / 2


def is_triangle_visible(a, b, c) -> bool:
    return numpy.dot(c[:3], calc_vector(a, b, c)) > 0


def calc_vector(a, b, c):
    A = a - c
    A = A[:3]
    B = b - c
    B = B[:3]
    N = numpy.cross(A, B)
    return N


def calc_d(N, c):
    return -(N[0] * c[0] + N[1] * c[1] + N[2] * c[2])


def calc_t(N, P, D):
    P = P[:3]
    return -(numpy.dot(N, P) + D)


def compare_triangles(triangle1, triangle2):
    N = calc_vector(triangle1[0], triangle1[1], triangle1[2])
    D = calc_d(N, triangle1[2])

    if calc_t(N, triangle2[0], D) > 0:
        return -1
    if calc_t(N, triangle2[1], D) > 0:
        return -1
    if calc_t(N, triangle2[2], D) > 0:
        return -1
    return 1


screen_size = (1000, 1000)
focal = 300
edge_color = (255, 255, 255)
edge_width = 2

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Virtual Camera')

world_map = load_figures_from_path('models')

FOCAL_LIMITS = 20., 500.
FOCAL_STEP = 2.
TRANSLATION_STEP = 40.
ROTATION_STEP = np.radians(0.8)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()

        focal = handle_zoom(keys, focal)

        handle_horizontal_movement(keys, world_map)
        handle_vertical_movement(keys, world_map)

        handle_looking(keys, world_map)
        handle_bias_looking(keys, world_map)

    # Draw
    screen.fill((0, 0, 0))
    sorted_world = sorted(world_map, key=functools.cmp_to_key(
        lambda wireframe1, wireframe2: compare_triangles(
            (wireframe1.nodes[0], wireframe1.nodes[1], wireframe1.nodes[2]),
            (wireframe2.nodes[0], wireframe2.nodes[1], wireframe2.nodes[2])
        )
    ))

    for wireframe in sorted_world:
        for triangle, color in zip(wireframe.triangles, wireframe.colors):
            a, b, c = wireframe.nodes[triangle[0]], wireframe.nodes[triangle[1]], wireframe.nodes[triangle[2]]

            if is_triangle_visible(a, b, c):
                a = projection(a, *screen_size, focal)
                b = projection(b, *screen_size, focal)
                c = projection(c, *screen_size, focal)
                pygame.draw.polygon(screen, color, [a, b, c])

    pygame.display.flip()
