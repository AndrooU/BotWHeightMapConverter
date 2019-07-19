import time
from generate_map import create_image

from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 200)
Config.set('graphics', 'height', 200)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.core.window import Window
Window.clearcolor = (0.8,0.8,0.8,1)

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import *


class Map(Widget):
    def make(self):
        self.lod = 0
        self.num = 1
        self.w = 512
        self.h = 512
        self.dragstart = None
        self.topleft = None
        self.bottomright = None
        
    def set_lod(self, lod):
        self.lod = lod
        self.num = 2 ** lod
    
    def draw(self):
        self.canvas.clear()
        with self.canvas:
            if self.topleft != None and self.bottomright != None:
                x1,y1 = self.tile_to_coord(self.topleft[0], self.topleft[1])
                x2,y2 = self.tile_to_coord(self.bottomright[0]+1, self.bottomright[1]+1)
                Color(1,0,0,0.3)
                Rectangle(pos=(x1,y1),size=(x2-x1,y2-y1))
                Color(0.6, 0, 0,1)
                Line(points=[x1,y1,x1,y2,x2,y2,x2,y1,x1,y1])
    
    def on_touch_down(self, touch):
        if touch.button == 'left':
            x, y = touch.pos
            point = self.get_tile(x, y)
            if point != None:
                self.dragstart = point
                self.topleft = point
                self.bottomright = point
                self.draw()
            else:
                self.topleft = None
                self.bottomright = None
    
    
    def on_touch_move(self, touch):
        x, y = touch.pos
        point = self.get_tile(x, y)
        if point != None and self.dragstart != None:
            xi, yi = self.dragstart
            xf, yf = point
            new_topleft = (min(xi,xf), min(yi,yf))
            new_bottomright = (max(xi,xf), max(yi,yf))
            if new_topleft != self.topleft or new_bottomright != self.bottomright:
                self.topleft = new_topleft
                self.bottomright = new_bottomright
                self.draw()
                
                
    def on_touch_up(self, touch):
        self.dragstart = None
        
    def tile_to_coord(self, col, row):
        x = self.w / self.num * col
        y = self.h / self.num * row
        return (x, y)

    def get_tile(self, x, y):
        if x >= 0 and x < self.w and y >= 0 and y < self.h:
            col = int(x * self.num / self.w)
            row = int(y * self.num / self.h)
            return (col, row)
        return None
    
    def generate(self):
        if self.topleft != None and self.bottomright != None:
            x1, y1 = self.topleft
            x2, y2 = self.bottomright
            tl = (x1 / self.num, 1 - ((y2 + 1) / self.num))
            br = ((x2 + 1) / self.num, 1 - (y1 / self.num))
            create_image(tl, br, self.lod, str(int(time.time())))
            self.topleft = None
            self.bottomright = None
            self.draw()
    
    

class RegionSelector(BoxLayout):
    def set_active(self, lod):
        Window.size = (512, 600)
        self.hmap.topleft = None
        self.hmap.bottomright = None
        self.hmap.set_lod(lod)
        self.hmap.draw()
        
    def make(self):
        self.orientation = "vertical"
        Window.size = (512, 600)
        
        layout_uno = RelativeLayout(size=(512,512),size_hint=(None,None))
        img = Image(source='bg_image.png',pos=(0,0))
        layout_uno.add_widget(img)
        
        self.hmap = Map()
        self.hmap.pos = (0, 0)
        self.hmap.size = (512, 512)
        self.hmap.make()
        layout_uno.add_widget(self.hmap)
        
        self.add_widget(layout_uno)
        
        layout_dos = BoxLayout(orientation="horizontal")
        gen_button = Button(text="Generate")
        gen_button.bind(on_release=self.generate)
        self.switch_button = Button(text="Change LOD")
        layout_dos.add_widget(gen_button)
        layout_dos.add_widget(self.switch_button)
        self.add_widget(layout_dos)
    
    def generate(self, _):
        self.hmap.generate()


class LodSelector(BoxLayout):    
    def set_active(self):
        Window.size = (200, 200)
    
    def make(self):
        self.orientation = 'vertical'
        
        self.add_widget(Label(text="Select the level of detail",color=(0,0,0,1),height=40,size_hint_y=None))
        
        slider_centerer = AnchorLayout(anchor_x='center', anchor_y='bottom')
        self.slider = Slider(min=0,max=8,value=4,step=1,width=180,height=100,size_hint_x=None,size_hint_y=None)
        slider_centerer.add_widget(self.slider)
        
        label_bottomer = AnchorLayout(anchor_y='bottom')
        value_text = Label(text="4",color=(0,0,0,1))
        def UpdateValueText(instance,value):
            value_text.text = str(int(value))
        self.slider.bind(value=UpdateValueText)
        label_bottomer.add_widget(value_text)
        
        self.add_widget(label_bottomer)
        self.add_widget(slider_centerer)
        
        self.switch_button = Button(text="OK")
        self.add_widget(self.switch_button)
        

class HolderLayout(BoxLayout):
    def make(self):
        self.layouts = [LodSelector(), RegionSelector()]
        self.cur = 0
        for l in self.layouts:
            l.make()
            l.switch_button.bind(on_release=self.switch)
        self.layouts[self.cur].set_active()
        self.add_widget(self.layouts[self.cur])
        
    def switch(self, _):
        self.cur = 1 - self.cur
        if self.cur == 1:
            self.layouts[1].set_active(int(self.layouts[0].slider.value))
        else:
            self.layouts[0].set_active()
        self.clear_widgets()
        self.add_widget(self.layouts[self.cur])
        

class Main(App):
    def build(self):
        self.title = "BotW Height Map Converter"
        layout = HolderLayout()
        layout.make()
        return layout
        
    
Main().run()