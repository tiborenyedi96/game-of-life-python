import pygame
from Board import Board
from Renderer import Renderer

SPEED = 10

EDITING = "Edit"
RUNNING = "Running"
PAUSED = "Paused"

if __name__ == "__main__":
    board = Board()
    renderer = Renderer()
    state = EDITING

    follow = False
    dragging = False
    last_mouse = (0, 0)

    step_interval = 1000 / SPEED
    last_step = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = renderer.button_at(event.pos)
                if clicked == "start":
                    state = RUNNING
                elif clicked == "pause":
                    if state == RUNNING:
                        state = PAUSED
                elif clicked == "reset":
                    board.clear()
                    state = EDITING
                elif event.button == 1 and state != RUNNING:
                    board.change_cell_liveness(*renderer.screen_to_cell(event.pos))
                elif event.button == 3:
                    dragging = True
                    last_mouse = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    dragging = False

            elif event.type == pygame.MOUSEMOTION and dragging:
                dx = event.pos[0] - last_mouse[0]
                dy = event.pos[1] - last_mouse[1]
                renderer.pan(dx, dy)
                last_mouse = event.pos

            elif event.type == pygame.MOUSEWHEEL:
                factor = 1.1 if event.y > 0 else 1 / 1.1
                renderer.zoom(factor, pygame.mouse.get_pos())

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = RUNNING if state != RUNNING else PAUSED
                elif event.key == pygame.K_f:
                    follow = not follow

        now = pygame.time.get_ticks()
        if state == RUNNING and now - last_step >= step_interval:
            board.step()
            if follow:
                renderer.center_on(*board.centroid())
            last_step = now

        renderer.draw(board, state)
        renderer.clock.tick(60)

    pygame.quit()