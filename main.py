from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.list import OneLineListItem
import pandas as pd
import geopandas as gpd
from shapely.geometry import point
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from numpy import arange, sin, pi
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.boxlayout import BoxLayout
import os
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Rectangle, Line
import plotly.express as px
from kivy.properties import StringProperty
import asyncio
from kivy.uix.button import Button
import asyncio
from kivy.graphics.transformation import Matrix
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scatter import Scatter
from kivy.uix.scatter import ScatterPlane
from kivy.uix.stencilview import StencilView

states = gpd.read_file("World_Countries.shx")

Buil_strng = '''
ScreenManager:
    First:
    Second:
<First>:
    name:'first'
    BoxLayout:
        orientation : "vertical"
        padding: dp(12)
        spacing: dp(12)
        MDLabel:
            text:'Atlas'
            halign: 'center'
            font_style: 'H2'
            pos_hint:{'center_y':0.8}
        MDTextField:
            id : task_text

            pos_hint: {'center_x':0.5, 'center_y':0.5}
            width:300
            hint_text:'Write a country. For example: India '
        MDTextField:
            id : task_text_2
            hint_text : "Country 2"
            pos_hint: {'center_x':0.5, 'center_y':0.4}
            width:300


        MDRaisedButton:
            text:'Show on the map'
            pos_hint: {'center_x':0.5,'center_y':0.35}
            on_press:
                app.addCountry()
<Second>:
    name: 'second' 
    StencilBox:
        id:stb
        Zoom:
            id:task_items
            on_touch_down: app.touch_event(args[1])
            on_touch_move: None
            size_hint_x: 1
            size_hint_y: 1
            Map:
                id:map


    MDToolbar :
        pos_hint: {"top": 1}
        title : "Toolbar" 


        MDRaisedButton:
            text: 'Back'
            pos_hint: {'center_x':0.3,'center_y':0.2}
            on_press:
                root.manager.current = 'first'
        MDRaisedButton:
            text: 'Clear'
            pos_hint: {'center_x':0.4,'center_y':0.2}
            on_press:
                app.clear_plot()
        MDRaisedButton:
            text: '+'
            pos_hint: {'center_x':0.4,'center_y':0.2}
            on_press:
                app.zoom_in()
        MDRaisedButton:
            text: '-'
            pos_hint: {'center_x':0.4,'center_y':0.2}
            on_press:
                app.zoom_out()
        MDRaisedButton:
            text: 'Click to draw on the map'
            pos_hint: {'center_x':0.4,'center_y':0.2}
            on_press:
                app.chtev()
        MDRaisedButton:
            text: 'Clear Canvas'
            pos_hint: {'center_x':0.4,'center_y':0.2}
            on_press:
                app.clear_canvas()

'''


class Map(StencilView, BoxLayout):
    pass


class StencilBox(StencilView, BoxLayout):
    pass


class Zoom(ScatterLayout):
    pass


class First(Screen):
    pass


class Second(Screen):
    pass


sm = ScreenManager()
sm.add_widget(First(name='first'))
sm.add_widget(Second(name='second'))


class NewApp(MDApp):
    def build(self):
        self.strng = Builder.load_string(Buil_strng)
        self.screen_2 = self.strng.get_screen('second').ids.task_items
        return self.strng

    def change_screen(self):
        self.strng.get_screen('second').manager.current = 'first'

    def change_screen2(self):
        self.strng.get_screen('second').manager.current = 'second'

    def clear_plot(self):
        self.strng.get_screen('second').ids.map.clear_widgets()

    def clear_canvas(self):
        self.strng.get_screen('second').ids.map.canvas.clear()

    def zoom_in(self, **kwargs):
        self.strng.get_screen('second').ids.task_items.size_hint_x += 0.1
        self.strng.get_screen('second').ids.task_items.size_hint_y += 0.1

    def zoom_out(self, **kwargs):
        self.strng.get_screen('second').ids.task_items.size_hint_x -= 0.1
        self.strng.get_screen('second').ids.task_items.size_hint_y -= 0.1

    def touch_event(self, touch):
        # Override Scatter's `on_touch_down` behavior for mouse scroll
        scatter_ = self.strng.get_screen('second').ids.task_items
        if touch.is_mouse_scrolling:
            if touch.button == 'scrolldown':
                if scatter_.scale < 20:
                    scatter_.scale = scatter_.scale * 1.1
            elif touch.button == 'scrollup':
                if scatter_.scale > 1:
                    scatter_.scale = scatter_.scale * 0.8
        # If some other kind of "touch": Fall back on Scatter's behavior
        else:
            print("nothing happen")

    def chtev(self):
        self.strng.get_screen('second').ids.task_items.on_touch_down = self.on_touch_down
        self.strng.get_screen('second').ids.task_items.on_touch_move = self.on_touch_move

    def on_touch_down(self, touch):
        with self.strng.get_screen('second').ids.map.canvas:
            Color(1., 0, 0)
            self.strng.get_screen('second').ids.map.rect = Rectangle(pos=touch.pos, size=(5, 5))
            # d = 30
            # touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        with self.strng.get_screen('second').ids.map.canvas:
            Color(1., 0, 0)
            self.strng.get_screen('second').ids.map.rect = Rectangle(pos=touch.pos, size=(5, 5))

    def addCountry(self):
        self.task_text = self.strng.get_screen('first').ids.task_text.text
        self.task_text_2 = self.strng.get_screen('first').ids.task_text_2.text

        if self.task_text.split() != []:
            country = states[states.COUNTRY == self.task_text]
            country2 = states[states.COUNTRY == self.task_text_2]
            country.plot(ax=country2.plot(color='blue', edgecolor='black', linewidth=3))
            fig = FigureCanvasKivyAgg(plt.gcf())
            self.change_screen2()
            self.strng.get_screen('second').ids.map.add_widget(fig)



        else:
            self.strng.get_screen('second').manager.current = 'second'

            # Snackbar(text='Task is Empty').show()


NewApp().run()