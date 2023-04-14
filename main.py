from typing import Tuple

import numpy as np
import pygame

from Controls import handle_zoom, handle_horizontal_movement, handle_vertical_movement, handle_looking, \
    handle_bias_looking
from worldMap import load_figures_from_path


# Map 3D map to 2D display
def projection(point_3d: np.array, view_width: float, view_height: float, focal: float) -> Tuple[float, float]:
    # f / z
    from_focal = abs(focal / point_3d[1])

    # We need to move to the middle of the camera
    # x' = x * (f / z)
    x = from_focal * point_3d[0] + view_width / 2
    # y' = y * (f / z)
    y = view_height / 2 - from_focal * point_3d[2]

    return x, y


def is_point_visible(point_3d: np.array, focal: float) -> bool:
    return point_3d[1] > focal / 2


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
    for wireframe in world_map:
        for triangle in wireframe.triangles:
            a, b, c = wireframe.nodes[triangle[0]], wireframe.nodes[triangle[1]], wireframe.nodes[triangle[2]]

            if is_point_visible(a, focal) or is_point_visible(b, focal) or is_point_visible(c, focal):
                a = projection(a, *screen_size, focal)
                b = projection(b, *screen_size, focal)
                c = projection(c, *screen_size, focal)
                pygame.draw.polygon(screen, edge_color, [a, b, c])

    pygame.display.flip()
