from typing import Tuple

import numpy as np
import pygame

import matrices
from Controls import handle_zoom, handle_horizontal_movement, handle_vertical_movement, handle_looking, \
    handle_bias_looking
from wireframe import load_models_from_folder


# Map 3D map to 2D display
def projection(point_3d: np.array, view_width: float, view_height: float, focal: float) -> Tuple[float, float]:
    from_focal = abs(focal / point_3d[1])
    x = from_focal * point_3d[0] + view_width / 2
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

wireframes = load_models_from_folder('models')

# transformation = matrices.translation_matrix(-200, 0, -300)
# wireframes[0].transform(transformation)

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

        handle_horizontal_movement(keys, wireframes)
        handle_vertical_movement(keys, wireframes)

        handle_looking(keys, wireframes)
        handle_bias_looking(keys, wireframes)

    # Draw
    screen.fill((0, 0, 0))
    for wireframe in wireframes:
        for edge in wireframe.edges:
            a, b = wireframe.nodes[edge[0]], wireframe.nodes[edge[1]]

            if is_point_visible(a, focal) or is_point_visible(b, focal):
                a = projection(a, *screen_size, focal)
                b = projection(b, *screen_size, focal)
                pygame.draw.line(screen, edge_color, a, b, edge_width)

    pygame.display.flip()
