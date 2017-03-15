from screen import screen_setup, draw_image

class StateModule(object):
    modid = None
    always_tick = False

    def __init__(self, previous):
        self.id = self.__class__.__name__

    def draw(self):
        pass

    def navigate(self, direction):
        pass

    def tick(self):
        return

class MenuModule(StateModule):
    controller = None
    items = []
    current = 0

    def __init__(self, controller):
        self.controller = controller
        super(MenuModule, self).__init__(controller)
        print "Created MenuModule"


    def draw(self, clear=True):
        if clear:
            self.controller.screen.clear_display()
        #  draw_image(self.controller, self.items[self.current][1])
        pos = 0
        start = max(0, min(self.current - 2, len(self.items) - 5))
        while pos < min(5, len(self.items)):
            self.controller.screen.write_line(pos+2, 0,
                "  " + self.items[start+pos][1])
            self.controller.screen.write_line(pos+2, 23, " ")
            pos = pos + 1
        cursor = min(start+self.current, max(
                     min(self.current, 2),
                     self.current + 5 - len(self.items)))
        self.controller.screen.write_line(cursor+2, 23, ">")

    def add_menu_item(self, module):
        self.items.append((module.id, module.name))
        #  print "added " + module.name + " to menu"


    def try_bricklet(self, uid, device_identifier, position):
        if device_identifier == 263:
            screen_setup(self.controller, uid)
            print "Screen Initialised"
            return True
        return False


    def navigate(self, direction):
        if direction == "forward":
            self.controller.change_module(self.items[self.current][0])
        if direction == "back":
            draw_image(self.controller, "splash")
            self.controller.current_module = None
        if direction in ["down", "up"]:
            if direction == "down":
                self.current = self.current + 1
            else:
                self.current = self.current - 1
            if self.current >= len(self.items):
                self.current = 0
            elif self.current < 0:
                self.current = len(self.items)-1
            self.draw(clear=False)
            print "Menu: " + str(self.items[self.current][1])
