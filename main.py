
import re
import kivy
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.stacklayout import StackLayout
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.image import Image
from kivy.properties import ListProperty
from kivy.uix.scrollview import ScrollView
from copy import copy
from time import sleep
# per aprire il browser
import webbrowser
from threading import Thread
from math import *

class MainWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    # logic ----------
    display = StringProperty("0")
    first_num = NumericProperty()
    second_num = NumericProperty()
    history = ListProperty([""])
    result_preview = StringProperty("")
    prova = 0
    # colors -----------
    bg_color = StringProperty("0.23921568627450981, 0.23921568627450981, 0.23921568627450981")
    backspace_img = StringProperty("images/backspace white.png")
    text_color = StringProperty("1, 1, 1")

    def button_click(self, num):
        if num != "0" and self.display == "0":
            self.display = ""
        self.display = self.display  + str(num)
        self.result_preview = self.display
        self.result_preview = self.result_preview.replace("\u00D7", "*")
        self.result_preview = self.result_preview.replace("÷", "/")
        self.result_preview = self.result_preview.replace(",", ".")
        self.result_preview = f"={eval(self.result_preview)}"

    def disable_num_bttn(self):
        self.num_bttn_state = True

    def backspace_bttn(self):
        if self.display == "Division By Zero":
            self.cancel_bttn()
        
        if self.display[-1] == ",":
            self.point_disabled = False
        self.display = self.display[:-1]
        if len(self.display) == 0:
            self.display = "0"
            self.point_disabled = False
        try:
            self.result_preview = self.display
            self.result_preview = self.result_preview.replace("\u00D7", "*")
            self.result_preview = self.result_preview.replace("÷", "/")
            self.result_preview = self.result_preview.replace(",", ".")
            self.result_preview = f"={eval(self.result_preview)}"
            self.result_preview = self.display
            self.result_preview = self.result_preview.replace( "*" ,"\u00D7")
            self.result_preview = self.result_preview.replace("/", "÷")
            self.result_preview = self.result_preview.replace(".", ",")
        except SyntaxError:
            pass

    def cancel_bttn(self):
        self.display = "0"
        self.num_bttn_state = False
        self.point_disabled = False
        self.result_preview = "0"

    def sum_bttn(self):
        if self.display[-1] == "-" or self.display[-1] == "\u00D7" or self.display[-1] == "÷":
            self.display = self.display[:-1] + "+"
        elif self.display[-1] != "+":
            self.display = self.display + "+"
        self.point_disabled = False

    def diff_bttn(self):
        if self.display[-1] == "+" or self.display[-1] == "\u00D7" or self.display[-1] == "÷":
            self.display = self.display[:-1] + "-"
        elif self.display[-1] != "-":
            self.display = self.display + "-"
        self.point_disabled = False

    def multiply_bttn(self):
        if self.display[-1] == "-" or self.display[-1] == "+" or self.display[-1] == "÷":
            self.display = self.display[:-1] + "\u00D7"
        elif self.display[-1] != "\u00D7":
            self.display = self.display + "\u00D7"
        self.point_disabled = False

    def divide_bttn(self):
        if self.display[-1] == "\u00D7" or self.display[-1] == "+" or self.display[-1] == "-":
            self.display = self.display[:-1] + "÷"
        elif self.display[-1] != "÷":
            self.display = self.display + "÷"
        self.point_disabled = False

    def change_symbol(self):
        if "-" in self.display:
            self.display = self.display.replace("-","")
        else:
            self.display = f"-{self.display}"

    def add_point_bttn(self):
        prev_number = self.display
        num_list = re.split("\u00d7|\u00f7|\u002b|\u002d|\u0025", prev_number)
        
        if("×" in prev_number or "-" in prev_number or "+" in prev_number or"÷" in prev_number or "%" in prev_number) and "," not in num_list[-1:]:
            self.display = f"{self.display}."

        elif "," in prev_number:
            pass

        else:
            self.display = f"{self.display}."

    def equal_bttn(self):
        self.history.append(self.display)
        try:
            if self.history[-1] == self.history[-2]:
                self.history.pop()
        except IndexError:
            pass

        print(self.history)
        self.display = self.display.replace("\u00D7", "*")
        self.display = self.display.replace("÷", "/")
        self.display = self.display.replace(",", ".")
        try:
            self.display = str(eval(self.display))
            self.display = self.display.replace(".", ",")
            if "," in self.display:
                if self.display[self.display.index(",")+1:] == "0":
                    self.display = self.display[:self.display.index(",")]
        except ZeroDivisionError:
            self.display = "Division By Zero"
        except SyntaxError:
            self.display = self.display.replace( "*" ,"\u00D7")
            self.display = self.display.replace("/", "÷")
            self.display = self.display.replace(".", ",")
        if "," in self.display:
            self.point_disabled = True

        try:
            self.result_preview = self.display
            self.result_preview = self.result_preview.replace("\u00D7", "*")
            self.result_preview = self.result_preview.replace("÷", "/")
            self.result_preview = self.result_preview.replace(",", ".")
            self.result_preview = f"={eval(self.result_preview)}"
            self.result_preview = self.display
            self.result_preview = self.result_preview.replace( "*" ,"\u00D7")
            self.result_preview = self.result_preview.replace("/", "÷")
            self.result_preview = self.result_preview.replace(".", ",")
        except SyntaxError:
            pass

    def show_history(self, state):
        result_widget = copy(self.ids.Result_display)
        prova = self.width-self.ids.DisplayBoxLayout.height/5-(self.ids.DisplayBoxLayout.height/5)
        if state == "down":
            print(self.ids.History_bttn.width)
            self.ids.DisplayBoxLayout.remove_widget(self.ids.Result_display)
            History_Layout = BoxLayout(orientation="vertical", size_hint=(None, None), width=prova, pos_hint={"right":0})
            self.ids["HistoryLayout"] = History_Layout
            for i in range(0, len(self.history)):
                self.ids.HistoryLayout.add_widget(Button(text=str(self.history[i]), size_hint_y=None, width=self.width-self.ids.History_bttn.width, text_size=(self.width,History_Layout.height),  halign="right", font_size=self.ids.DisplayBoxLayout.height/4, background_color=(1,0,0,0), height=self.ids.DisplayBoxLayout.height/4, valign="middle"))

            History_Scrollview = ScrollView(width=self.width-self.ids.History_bttn.width, do_scroll_x=False, do_scroll_y=True)
            self.ids["historyscrollview"] = History_Scrollview
            print(History_Scrollview.width)
            History_Scrollview.add_widget(History_Layout)
            History_Layout.height = self.ids.DisplayBoxLayout.height/4 * i
            self.ids.DisplayBoxLayout.add_widget(History_Scrollview)
        else:
            self.ids.DisplayBoxLayout.remove_widget(self.ids.historyscrollview)
            self.ids.DisplayBoxLayout.add_widget(result_widget)

class ScientificMode(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    # logic ----------
    display = StringProperty("0")
    first_num = NumericProperty()
    second_num = NumericProperty()
    point_disabled = BooleanProperty(False)
    history = ListProperty([""])
    result_preview = StringProperty("")
    prova = 0
    is_sqrt = False
    # colors -----------r
    
    bg_color = StringProperty("0.23921568627450981, 0.23921568627450981, 0.23921568627450981")
    backspace_img = StringProperty("images/backspace white.png")
    text_color = StringProperty("1, 1, 1")

    def button_click(self, num):
        if num != "0" and self.display == "0":
            self.display = ""
        
        self.display = self.display  + str(num)
        try:
            self.result_preview = self.display
            self.result_preview = self.result_preview.replace("\u00D7", "*")
            self.result_preview = self.result_preview.replace("÷", "/")
            self.result_preview = self.result_preview.replace(",", ".")
            self.result_preview = self.result_preview.replace("^", "**")
            self.result_preview = self.result_preview.replace("√", "sqrt(")
            print(self.result_preview)
            self.result_preview = f"={eval(self.result_preview)}"
        except SyntaxError:
            pass

    def disable_num_bttn(self):
        self.num_bttn_state = True

    def backspace_bttn(self):
        if self.display == "Division By Zero":
            self.cancel_bttn()
        if self.display[-1] == "-" or self.display[-1] == "\u00D7" or self.display[-1] == "÷" or self.display[-1] == "+":
            self.point_disabled = True
        if self.display[-1] == ",":
            self.point_disabled = False
        else:
            self.display = self.display[:-1]
        if len(self.display) == 0:
            self.display = "0"
            self.point_disabled = False
        try:
            self.result_preview = self.display
            self.result_preview = self.result_preview.replace("\u00D7", "*")
            self.result_preview = self.result_preview.replace("÷", "/")
            self.result_preview = self.result_preview.replace(",", ".")
            self.result_preview = self.result_preview.replace("^", "**")
            self.result_preview = self.result_preview.replace("√", "sqrt(")
            self.result_preview = f"={eval(self.result_preview)}"
            self.result_preview = self.display
            self.result_preview = self.result_preview.replace( "*" ,"\u00D7")
            self.result_preview = self.result_preview.replace("/", "÷")
            self.result_preview = self.result_preview.replace(".", ",")
        except SyntaxError:
            pass

    # ------------------ FUNCTIONS
    def poweroftwo_bttn(self):
        self.display = f"{self.display}^2"
        print(self.display)
        prova = ""
        try:
            self.result_preview = self.display
            self.result_preview = self.result_preview.replace("\u00D7", "*")
            self.result_preview = self.result_preview.replace("÷", "/")
            self.result_preview = self.result_preview.replace(",", ".")
            self.result_preview = self.result_preview.replace("^", "**")
            prova = str(eval(self.result_preview))
            self.result_preview = prova
        except SyntaxError:
            pass
    
    def sqrt_bttn(self):
        self.display = f"{self.display}√"
        try:
            self.result_preview = self.display
            self.result_preview = self.result_preview.replace("\u00D7", "*")
            self.result_preview = self.result_preview.replace("÷", "/")
            self.result_preview = self.result_preview.replace(",", ".")
            self.result_preview = self.result_preview.replace("^", "**")
            self.result_preview = self.result_preview.replace("√", "sqrt(")
        except SyntaxError:
            pass
        self.is_sqrt = True

    # ------------------------------------

    def cancel_bttn(self):
        self.display = "0"
        self.num_bttn_state = False
        self.point_disabled = False
        self.result_preview = "0"

    def sum_bttn(self):
        try:
            self.result_preview = self.display
            self.result_preview = self.result_preview.replace("\u00D7", "*")
            self.result_preview = self.result_preview.replace("÷", "/")
            self.result_preview = self.result_preview.replace(",", ".")
            self.result_preview = self.result_preview.replace("^", "**")
            self.result_preview = self.result_preview.replace("√", "sqrt(")
        except SyntaxError:
            pass

        if self.is_sqrt:
            self.result_preview = self.result_preview + ")"
            self.is_sqrt = False
        if self.display[-1] == "-" or self.display[-1] == "\u00D7" or self.display[-1] == "÷":
            self.display = self.display[:-1] + "+"
        elif self.display[-1] != "+":
            self.display = self.display + "+"
        self.point_disabled = False

        try:
            self.result_preview = str(eval(self.result_preview))
        except SyntaxError:
            pass

    def diff_bttn(self):
        if self.display[-1] == "+" or self.display[-1] == "\u00D7" or self.display[-1] == "÷":
            self.display = self.display[:-1] + "-"
        elif self.display[-1] != "-":
            self.display = self.display + "-"
        self.point_disabled = False

    def multiply_bttn(self):
        if self.display[-1] == "-" or self.display[-1] == "+" or self.display[-1] == "÷":
            self.display = self.display[:-1] + "\u00D7"
        elif self.display[-1] != "\u00D7":
            self.display = self.display + "\u00D7"
        self.point_disabled = False

    def divide_bttn(self):
        if self.display[-1] == "\u00D7" or self.display[-1] == "+" or self.display[-1] == "-":
            self.display = self.display[:-1] + "÷"
        elif self.display[-1] != "÷":
            self.display = self.display + "÷"
        self.point_disabled = False

    def add_point_bttn(self):
        self.display = self.display + ","
        self.point_disabled = True

    def equal_bttn(self):
        self.history.append(self.display)
        try:
            if self.history[-1] == self.history[-2]:
                self.history.pop()
        except IndexError:
            pass

        print(self.history)
        self.display = self.display.replace("\u00D7", "*")
        self.display = self.display.replace("÷", "/")
        self.display = self.display.replace(",", ".")
        try:
            self.display = str(eval(self.display))
            self.display = self.display.replace(".", ",")
            if "," in self.display:
                if self.display[self.display.index(",")+1:] == "0":
                    self.display = self.display[:self.display.index(",")]
        except ZeroDivisionError:
            self.display = "Division By Zero"
        except SyntaxError:
            self.display = self.display.replace( "*" ,"\u00D7")
            self.display = self.display.replace("/", "÷")
            self.display = self.display.replace(".", ",")
        if "," in self.display:
            self.point_disabled = True

        try:
            self.result_preview = self.display
            self.result_preview = self.result_preview.replace("\u00D7", "*")
            self.result_preview = self.result_preview.replace("÷", "/")
            self.result_preview = self.result_preview.replace(",", ".")
            self.result_preview = f"={eval(self.result_preview)}"
            self.result_preview = self.display
            self.result_preview = self.result_preview.replace( "*" ,"\u00D7")
            self.result_preview = self.result_preview.replace("/", "÷")
            self.result_preview = self.result_preview.replace(".", ",")
        except SyntaxError:
            pass

    def show_history(self, state):
        result_widget = copy(self.ids.Result_display)
        prova = self.width-self.ids.DisplayBoxLayout.height/5-(self.ids.DisplayBoxLayout.height/5)
        if state == "down":
            print(self.ids.History_bttn.width)
            self.ids.DisplayBoxLayout.remove_widget(self.ids.Result_display)
            History_Layout = BoxLayout(orientation="vertical", size_hint=(None, None), width=prova, pos_hint={"right":0})
            self.ids["HistoryLayout"] = History_Layout
            for i in range(0, len(self.history)):
                self.ids.HistoryLayout.add_widget(Button(text=str(self.history[i]), size_hint_y=None, width=self.width-self.ids.History_bttn.width, text_size=(self.width,History_Layout.height),  halign="right", font_size=self.ids.DisplayBoxLayout.height/4, background_color=(1,0,0,0), height=self.ids.DisplayBoxLayout.height/4, valign="middle"))

            History_Scrollview = ScrollView(width=self.width-self.ids.History_bttn.width, do_scroll_x=False, do_scroll_y=True)
            self.ids["historyscrollview"] = History_Scrollview
            print(History_Scrollview.width)
            History_Scrollview.add_widget(History_Layout)
            History_Layout.height = self.ids.DisplayBoxLayout.height/4 * i
            self.ids.DisplayBoxLayout.add_widget(History_Scrollview)
        else:
            self.ids.DisplayBoxLayout.remove_widget(self.ids.historyscrollview)
            self.ids.DisplayBoxLayout.add_widget(result_widget)


class SecondWindow(Screen):
    def open_website(self):
        webbrowser.open("https://leonardogangalecom.wordpress.com/")



class WindowManager(ScreenManager):
    pass

class ImageButton(ButtonBehavior, Image):
    pass

class ImageToggleButton(ToggleButtonBehavior, Image):
    pass

Window.size  = (540, 1170)
kv = Builder.load_file("calc.kv")

class cps_appApp(App):
    def build(self):
        return kv

if __name__=="__main__":
    cps_appApp().run()
