from navigation import StateModule
from gpiozero import Energenie

OUTLETS = {
    1: "Laptop",
    2: "Monitor",
    3: "Monitor",
    # 4: "USB",
}


class Outlet():
    def __init__(self, outlet, controller):
        self.instance = Energenie(outlet)
        self.state = True
        if self.controller.localdb:
            unique_name = self.controller.localdb.get("outlet-" + outlet)
        if unique_name:
            self.name = unique_name
        else:
            self.name = OUTLETS[outlet]

    def on(self):
        if not self.state:
            self.instance.on()
            self.state = True

    def off(self):
        if self.state:
            self.instance.off()
            self.state = False

    def switch(self):
        if self.state:
            self.off()
        else:
            self.on()


class ACPowerModule(StateModule):
    menu_title = "Power"
    outlets = {}
    current = 1

    def __init__(self, controller):
        super(ACPowerModule, self).__init__(controller)
        controller.add_event_handler("sleep", self.on_sleep)
        controller.add_event_handler("wake", self.on_wake)
        for outlet in OUTLETS:
            self.outlets[outlet] = Outlet(outlet, controller)

    def draw(self, clear=True):
        if clear:
            self.controller.screen.device.clear_display()
        if not len(self.outlets):
            self.controller.ipcon.enumerate()
            self.controller.screen.draw("values", {})
            return
        key = self.outlets.keys()[self.current]
        outlet = self.outlets[key]
        if outlet.state:
            state = "Off"
        else:
            state = "On "
        self.controller.screen.draw(
            "values",
            {"title": outlet.name, "value": str(state), })

    def switch_relay(self):
        if self.outlets:
            key = self.outlets.keys()[self.current]
            self.outlets[key].switch()
            self.draw(False)

    def on_sleep(self, data):
        for outlet in self.outlets:
            # TODO: Less hacky!
            if outlet != 1:
                self.outlets[outlet].off()

    def on_wake(self, data):
        for outlet in self.outlets:
            self.outlets[outlet].on()

    def navigate(self, direction):
        if direction == "back":
            self.controller.prev_module()
        if direction == "forward":
            self.switch_relay()
        if direction in ["down", "up"]:
            if direction == "down":
                self.current = self.current + 1
            else:
                self.current = self.current - 1
            if self.current >= len(self.relays):
                self.current = 0
            elif self.current < 0:
                self.current = len(self.relays) - 1
            # print("Output: " + str(list(self.outputs)[self.current]))
            self.draw()

    def tick(self):
        self.draw(clear=False)
