from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock
# from kivy.core.window import Window

# Window.size = 360,640


# class ringwidget(Widget):
#     pass
class container(AnchorLayout):
    def __init__(self, **kwargs):
        super(container,self).__init__(**kwargs)
        self.start = 0
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.size_hint = (1, 1)
        # self.size_hint = (None, None)
        self.sizing = (350,350)

        self.colors = [(.5,1,.5,1),(1,0,1,1),(1,1,0,1)]

        self.updater = Clock.schedule_interval(self.count, 1)
        self.updater2 = Clock.schedule_interval(self.animator,0)

    def count(self, *args):
        if self.start <= 0:
            self.updater.cancel()
            self.updater2.cancel()
        self.ids.target.text = f'{self.start}'
        self.start -= 1

    def animator(self, *args):
        velocity = 5
            
        if self.ids.ring1.angle < 360:
            self.ids.ring1.angle += velocity
        else:
            self.ids.ring1.angle = 100

        if self.ids.ring2.angle < 360:
            self.ids.ring2.angle += velocity
        else:
            self.ids.ring2.angle = 30

        if self.ids.ring3.angle < 360:
            self.ids.ring3.angle += velocity
        else:
            self.ids.ring3.angle = 50
        
        


class CountApp(App):
    pass

kiv = CountApp()
kiv.run()
