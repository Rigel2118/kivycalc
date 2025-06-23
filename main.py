from kivy.app import App
from kivy.metrics import dp, sp
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.properties import StringProperty
from arithmetic import arithmetic
from trailing import format_number
from kivy.clock import Clock
import time
'''ratio=16/9
width=350
Window.size = (width,width*ratio)'''
#Window.fullscreen = "auto"

class calcApp(App):
	pass
class MainGrid(GridLayout):
	def write(self,char):
		self.ids.text_input.text=self.ids.text_input.text[:-1]+char+"█"

	def on_button1_click(self):
		self.write("1")
	def on_button2_click(self):
		self.write("2")
	def on_button3_click(self):
		self.write("3")
	def on_button4_click(self):
		self.write("4")
	def on_button5_click(self):
		self.write("5")
	def on_button6_click(self):
		self.write("6")
	def on_button7_click(self):
		self.write("7")
	def on_button8_click(self):
		self.write("8")
	def on_button9_click(self):
		self.write("9")
	def on_button0_click(self):
		self.write("0")
	def on_buttonp_click(self):
		self.write(".")
	def on_button_DEL_click(self):
		text=self.ids.text_input.text
		if text:
			self.ids.text_input.text=text[:-2]+"█"
	def on_button_plus_click(self):
		self.write("+")
	def on_button_minus_click(self):
		self.write("-")
	def on_button_prod_click(self):
		self.write("*")
	def on_button_quot_click(self):
		self.write("/")
	def on_button_power_click(self):
		self.write("^")
	def on_button_open_click(self):
		self.write("(")
	def on_button_close_click(self):
		self.write(")")
	def on_button_CLR_click(self):
		self.ids.text_input.text="█"
	def on_button_equals_click(self):
		try:
			current_text=self.ids.text_output.text
			ans=format_number(arithmetic(self.ids.text_input.text[:-1]))
			self.ids.text_output.text=current_text+"\n"+self.ids.text_input.text[:-1]+" = "+ans
		except ValueError:
			self.ids.text_output.text=current_text+"\n"+"wrong expression"



calcApp().run()
cursor_blink()
