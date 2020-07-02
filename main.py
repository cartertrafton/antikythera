#
# main.py
# Main python file to run project.
#

############################## file set up
import sys, time
from GUI import *
from Body import *

# global variables
global trails_active
global BLACK
global WHITE
global RED
global GREEN
global BLUE
global YELLOW
global GRAY
global WIDTH
global g

# trails
trails_active = False

# value for gravity equation
g = 0.4

# dimensions
WIDTH = 800
HEIGHT = 600

# set up colors:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

############################## set up and draw
def setup():
    # sun
    body1 = Body(1000, WIDTH/2, HEIGHT/2, 10, YELLOW, True, gui.space,trails_active)

    # planets
    body2 = Body(randint(0, 10), randint(0, WIDTH), randint(0, HEIGHT), 5, BLUE, False, gui.space, trails_active)
    body3 = Body(randint(0, 10), randint(0, WIDTH), randint(0, HEIGHT), 5, BLUE, False, gui.space, trails_active)
    body4 = Body(randint(0, 10), randint(0, WIDTH), randint(0, HEIGHT), 5, BLUE, False, gui.space, trails_active)
    body5 = Body(randint(0, 10), randint(0, WIDTH), randint(0, HEIGHT), 5, BLUE, False, gui.space, trails_active)

    # list of all bodies in universe
    global bodies
    bodies = [body1, body2, body3, body4, body5]
    return


def draw():
    # for each body: apply forces, update position, and draw
    for body in bodies:
        for other_body in bodies:
            if (body != other_body):
                global g
                force = other_body.attract(body, g)
                body.applyForce(force)
        body.update()
        body.display()
    ############################# RE-draw menu buttons
    # search objects
    pygame.draw.rect(gui.space, GRAY, gui.search_object_button)
    gui.space.blit(gui.search_object_button_surface, (40, 25))
    # search events
    pygame.draw.rect(gui.space, GRAY, gui.search_event_button)
    gui.space.blit(gui.search_event_button_surface, (330, 25))
    # calculate launch
    pygame.draw.rect(gui.space, GRAY, gui.calc_launch_button)
    gui.space.blit(gui.calc_launch_button_surface, (600, 25))
    # trails activate/deactivate
    pygame.draw.rect(gui.space, GRAY, gui.trails_button)
    gui.space.blit(gui.trails_button_surface, (35, 85))
    # exit button
    pygame.draw.rect(gui.space, GRAY, gui.exit_button)
    gui.space.blit(gui.exit_button_surface, (710, 560))
    # zoom slider
    pygame.draw.rect(gui.space, WHITE, gui.zoom_slider)
    # date display
    pygame.draw.rect(gui.space, GRAY, gui.date_button)
    gui.space.blit(gui.date_button_surface, (180, 560))
    # forward time travel
    pygame.draw.rect(gui.space, GRAY, gui.f_timetravel_button)
    gui.space.blit(gui.f_timetravel_button_surface, (420, 560))
    # backward time travel
    pygame.draw.rect(gui.space, GRAY, gui.b_timetravel_button)
    gui.space.blit(gui.b_timetravel_button_surface, (20, 560))
    pygame.display.update()
    return


############################## main loop


if __name__ == "__main__":
    # initiate pygame and clock
    pygame.init()
    pygame.display.set_caption('antikythera pre-alpha')
    clock = pygame.time.Clock()

    gui = GUI(WIDTH, HEIGHT)

    # initial set up
    setup()
    while True:
        # render screen
        draw()

        # event handler
        for event in pygame.event.get():
            # exit program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # click mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # trails button
                if gui.trails_button.collidepoint(mouse_pos):
                    print("trails button pushed")
                    for body in bodies:
                        if body.trails == True:
                            body.trails = False
                            gui.space.fill(BLACK)
                        else:
                            body.trails = True

                if gui.search_object_button.collidepoint(mouse_pos):
                    print('search1 pressed')
                # search event button
                if gui.search_event_button.collidepoint(mouse_pos):
                    print('search2 pressed')
                # calculate launch button
                if gui.calc_launch_button.collidepoint(mouse_pos):
                    print('calculate transfer pressed')

                # exit button
                if gui.exit_button.collidepoint(mouse_pos):
                    print("Exiting...")
                    pygame.quit()
                    sys.exit()

               # zoom bar
                if gui.zoom_slider.collidepoint(mouse_pos):
                    print("zoom bar click")
                # date pause/resume
                if gui.date_button.collidepoint(mouse_pos):
                    print('pause/resume time')
                # f time travel
                if gui.f_timetravel_button.collidepoint(mouse_pos):
                    print('forward time travel!')
                # b time travel
                if gui.b_timetravel_button.collidepoint(mouse_pos):
                    print('!levart emit sdrawkcab')

        # update GUI and wait
        pygame.display.update()
        time.sleep(0.05)