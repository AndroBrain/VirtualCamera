import numpy as np
import pygame

import matrices

FOCAL_STEP = 2.
TRANSLATION_STEP = 20.
ROTATION_STEP = np.radians(10.8)
MIN_FOCAL = 100


def handle_zoom(keys, focal):
    if keys[pygame.K_x] and focal > MIN_FOCAL:
        return focal - FOCAL_STEP
    if keys[pygame.K_z]:
        return focal + FOCAL_STEP
    return focal


move_left = matrices.translation_matrix(TRANSLATION_STEP, 0, 0)
move_right = matrices.translation_matrix(-TRANSLATION_STEP, 0, 0)
move_forward = matrices.translation_matrix(0, -TRANSLATION_STEP, 0)
move_backward = matrices.translation_matrix(0, +TRANSLATION_STEP, 0)


def handle_horizontal_movement(keys, wireframes):
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        for wireframe in wireframes:
            wireframe.transform(move_left)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        for wireframe in wireframes:
            wireframe.transform(move_right)
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        for wireframe in wireframes:
            wireframe.transform(move_forward)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        for wireframe in wireframes:
            wireframe.transform(move_backward)


move_up = matrices.translation_matrix(0, 0, -TRANSLATION_STEP)
move_down = matrices.translation_matrix(0, 0, +TRANSLATION_STEP)


def handle_vertical_movement(keys, wireframes):
    if keys[pygame.K_SPACE]:
        for wireframe in wireframes:
            wireframe.transform(move_up)
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        for wireframe in wireframes:
            wireframe.transform(move_down)


look_left = matrices.z_rotation_matrix(ROTATION_STEP)
look_right = matrices.z_rotation_matrix(-ROTATION_STEP)
look_up = matrices.x_rotation_matrix(ROTATION_STEP)
look_down = matrices.x_rotation_matrix(-ROTATION_STEP)


def handle_looking(keys, wireframes):
    if keys[pygame.K_j]:
        for wireframe in wireframes:
            wireframe.transform(look_left)
    if keys[pygame.K_l]:
        for wireframe in wireframes:
            wireframe.transform(look_right)
    if keys[pygame.K_i]:
        for wireframe in wireframes:
            wireframe.transform(look_up)
    if keys[pygame.K_k]:
        for wireframe in wireframes:
            wireframe.transform(look_down)


left_rotation = matrices.y_rotation_matrix(ROTATION_STEP * 2)
right_rotation = matrices.y_rotation_matrix(-ROTATION_STEP * 2)


def handle_bias_looking(keys, wireframes):
    if keys[pygame.K_q]:
        for wireframe in wireframes:
            wireframe.transform(left_rotation)
    if keys[pygame.K_e]:
        for wireframe in wireframes:
            wireframe.transform(right_rotation)
