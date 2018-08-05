class Settings:
    def __init__(self):
        self.ScreenWidth = 800
        self.ScreenHeight = 600
        self.bg_color = (217, 169, 155)
        self.gridNumLine = 4
        self.gridWidth = self.ScreenHeight // self.gridNumLine
        self.gridColor = Color()
        self.grid_speed = 2


class Color:
    def __init__(self):
        self.color = (255, 255, 255)
        self.value = 0

    def update(self, value):
        self.value = value
        if self.value == 2:
            self.color = (239, 226, 216)
        elif self.value == 4:
            self.color = (240, 224, 200)
        elif self.value == 8:
            self.color = (240, 175, 120)
        elif self.value == 16:
            self.color = (245, 150, 100)
        elif self.value == 32:
            self.color = (250, 125, 90)
        elif self.value == 64:
            self.color = (245, 95, 60)
            ##################################
        elif self.value == 128:
            self.color = (245, 150, 100)

        return self.color
