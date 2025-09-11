# kivycalc v0.5.0-beta

# Python modules
import os, time, json, webbrowser
from parse import parse
from trailing import format_number
from arithmetic import arithmetic

# Kivy modules
from kivy.clock import Clock
from kivy.utils import platform
from kivy.metrics import sp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget

# Material design (kivymd 2.0)
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.utils.set_bars_colors import set_bars_colors
from kivymd.uix.list import MDListItem
from kivymd.uix.recycleboxlayout import MDRecycleBoxLayout
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.dialog import (
	MDDialog,
	MDDialogIcon,
	MDDialogHeadlineText,
	MDDialogSupportingText,
	MDDialogButtonContainer,
	MDDialogContentContainer,
)
from kivymd.uix.divider import MDDivider
from kivymd.uix.list import (
	MDListItem,
	MDListItemLeadingIcon,
	MDListItemSupportingText,
	MDListItemTrailingCheckbox,
)

# Load classes
def load_kv_files():

	# Load widget KV files
	widgets_path = os.path.join('widgets')
	for file in os.listdir(widgets_path):
		if file.endswith('.kv'):
			Builder.load_file(os.path.join(widgets_path, file))
			print("Loaded", os.path.join(widgets_path, file))
			
	# Load tab KV files
	tabs_path = os.path.join('tabs')
	for file in os.listdir(tabs_path):
		if file.endswith('.kv'):
			Builder.load_file(os.path.join(tabs_path, file))
			print("Loaded", os.path.join(tabs_path, file))

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # App working directory
data_input = os.path.join(BASE_DIR, 'data', 'input.dat') # Used to store inputs
data_output = os.path.join(BASE_DIR, 'data', 'output.dat') # Used to store results
data_info = os.path.join(BASE_DIR, 'data', 'info.txt') # Not used yet
data_conf = os.path.join(BASE_DIR, 'config', 'config.json') # Used to store app settings
	
# Create files
def create_io_files(*args): 
	try:
		with open(data_input, 'w') as f: 
			pass
		with open(data_output, 'w') as f:
			pass
		print("Data files created successfully")
	except Exception as e:
		print(f"Error creating files: {e}")
		
# Count lines
def count_lines(file_path):
	try:
		with open(file_path, 'r', encoding='utf-8') as file:
			line_count = 0
			for line in file:
				line_count += 1
		return line_count
	except FileNotFoundError:
		print(f"File '{file_path}' not found")
		return None
	except IOError as e:
		print(f"Error reading file '{file_path}': {e}")
		return None

# Read lines from file
def read_line(file_path, line_number): 
	try:
		with open(file_path, 'r') as file:
			for i in range(line_number - 1):
				if not file.readline():  # End of file reached
					return None
			return file.readline().rstrip('\n')
	except Exception as e:
		print(f"Error reading file: {e}")
		return None
		
# Protocol for navigationbar
class BaseMDNavigationItem(MDNavigationItem):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.ripple_effect = False
	
	icon = StringProperty()
	text = StringProperty()
		
class calcApp(MDApp):
	
	# Startup settings
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		# Window resizing
		if platform == "win" or platform == "linux" or platform == "macosx":
			Window.size = (400, 800)  # set window size for PC
		
		# Configuration attributes 
		self.preserve_history = ""
		self.precision = ""
		
	# Load config 
	# Usage: no args -> load everything, request -> ask for existing setting
	def load_config_file(self, request=None):
		with open(data_conf, "r") as file:
			data = json.load(file)
		if request == None:
			self.theme_cls.theme_style = data["theme"]
			self.theme_cls.primary_palette = data["palette"]
			self.preserve_history = data["preserve-history"]
			self.precision = data["precision"]
		else:
			return data[request]
		
	# Save configuration to file
	def save_config_file(self, config):
		if config != None:
			with open(data_conf, "r") as file:
				data = json.load(file)
			
				for i, j in config.items():
					match i:
						case "theme": data["theme"] = j
						case "palette": data["palette"] = j
						case "preserve-history": data["preserve-history"] = j
						case "memory": data["memory"] = j
						case "sci": data["sci"] = j
						case "precision": data["precision"] = j
						
			with open(data_conf, "w") as file:
				json.dump(data, file, indent=4)
	
	# Initalize settings
	def generate_config_file(self):
	
		# Default settings
		config = {
			"theme": "Light",
			"palette": "Blue",
			"preserve-history": "Off",
			"memory": "0",
			"sci": "Off",
			"precision": "5 digits"
		}
		
		# Write to json file
		with open(data_conf, "w") as file:
			json.dump(config, file, indent=4)
		
	# Navigation bar stuff
	def on_switch_tabs(
		self,
		bar: MDNavigationBar,
		item: MDNavigationItem,
		item_icon: str,
		item_text: str,
	):
		
		# Shortcuts
		sm = self.root.ids.screen_manager
		app = MDApp.get_running_app()
		
		# Determine slide direction
		order = {"home": 1, "history": 2, "settings": 3, "empty": 2}
		
		if order[item_text] > order[sm.current]:
			sm.transition = SlideTransition(direction="left", duration=0.2)
		else:
			sm.transition = SlideTransition(direction="right", duration=0.2)
		
		# y to bottom in history when switching to that tab
		if item_text == "history":
			history = sm.get_screen("history")
			if len(history.ids.history_stand.children) == 0:
				sm.current = "empty"
			else:
				sm.current = "history"
		else:
			sm.current = item_text
	
	# Procedure to build the kivy interface
	def build(self):
		
		# Avoid android keyboard popping up
		MDTextField.keyboard_mode = "managed"
		
		# Check data files existance
		if not (os.path.exists(data_input) 
		and os.path.exists(data_output)):
			create_io_files()
		
		# Generate default settings
		if not os.path.exists(data_conf):
			self.generate_config_file()
			
		# Load config at startup
		try:
			self.load_config_file()
		except Exception as e:
			print(f"Error when loading settings: {e}\n Creating new config file")
			self.generate_config_file()
		
		# Load design
		load_kv_files()
		
		# Return the root widget (main UI)
		return Builder.load_file("main.kv")
	
	# Stuff to do after the build
	def on_start(self):
	
		# Synchronize system bar colors with the app's primary color
		self.set_bars_colors()
	
	def set_bars_colors(self):
		theme = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
		set_bars_colors(
			self.theme_cls.backgroundColor,  # status bar color
			self.theme_cls.surfaceContainerColor,  # navigation bar color
			theme
		)
	
	# ------------- Settings dialogs --------------- #
	
	# Theme dialog
	def show_theme_dialog(self):
			
		# Menu options
		theme_names = [
			"Light",
			"Dark"
		]
		
		# Create one checkbox for each theme
		self.boxes = [
			MDListItemTrailingCheckbox(
				group="Theme",
				active=False,
				focus_behavior=False,
			)
			for i in range(len(theme_names))
		]

		# Assign names to checkboxes
		for i, j in enumerate(theme_names):
			self.boxes[i].name = j
		
		# Pre-check 
		for i in self.boxes:
			if i.name == self.theme_cls.theme_style:
				i.active = True
				break
		
		# Create list items for the dialog
		list_items = [
			
			MDListItem(
				MDListItemSupportingText(text=j),
				self.boxes[i],
				theme_bg_color="Custom",
				md_bg_color=self.theme_cls.transparentColor,
				focus_behavior=False,
			)
			
			for i, j in enumerate(theme_names)
		]
		
		# Get height of stacked items
		total_height = sum(i.height for i in list_items)
		
		# Get optimal scrollview height
		scrollview_height = min(sp(300), total_height)
		
		self.dialog = MDDialog(
			# ----------------------------Icon-----------------------------
			MDDialogIcon(
				icon="theme-light-dark",
			),
			# -----------------------Headline text-------------------------
			MDDialogHeadlineText(
				text="Choose your theme",
			),
			# -----------------------Custom content------------------------
			MDDialogContentContainer(
				MDScrollView(
					MDBoxLayout(
						
						*list_items,  # Unpack all list items
						
						orientation="vertical",
						adaptive_height=True,
					),
					do_scroll_x=False,
					size_hint_y=None,
					height=scrollview_height,
				),
				orientation="vertical",
			),
			# ---------------------Button container------------------------
			MDDialogButtonContainer(
				Widget(),
				MDButton(
					MDButtonText(text="Accept"),
					style="text",
					on_release=lambda x: self.close_and_save_theme(),
				),
				spacing="8sp",
			),
			# -------------------------------------------------------------
		)
		self.dialog.open()

	def close_and_save_theme(self):
		active_option = None
		# Get active box
		for i in self.boxes:
			if i.active:
				active_option = i
				break
		
		if active_option:
			# Set the primary palette to the selected color
			self.theme_cls.theme_style = active_option.name
			self.set_bars_colors()
			
			# Update text
			app = MDApp.get_running_app()
			settings = app.root.ids.screen_manager.get_screen("settings")
			settings.ids.theme_text.text = active_option.name
			
			# Save to file
			self.save_config_file({"theme":active_option.name})
			self.dialog.dismiss()

	# Palette dialog
	def show_palette_dialog(self):
	
		# Menu options
		color_names = [
			"Red",
			"Green",
			"Blue",
			"Yellow",
			"Orange",
			"Purple",
			"Pink",
			"Cyan"
		]
		
		# Create one checkbox for each color
		self.boxes = [
			MDListItemTrailingCheckbox(
				group="Palette",
				active=False,
				focus_behavior=False,
			)
			for i in range(len(color_names))
		]
		
		# Assign names to checkboxes
		for i, color_name in enumerate(color_names):
			self.boxes[i].name = color_name
		
		# Pre-check based on current palette
		for i in self.boxes:
			if i.name == self.theme_cls.primary_palette:
				i.active = True
				break
		
		# Create list items for the dialog
		list_items = [
			
			MDListItem(
				MDListItemSupportingText(text=j),
				self.boxes[i],
				theme_bg_color="Custom",
				md_bg_color=self.theme_cls.transparentColor,
				focus_behavior=False,
				
			)
			
			for i, j in enumerate(color_names)
		]
		
		# Get height of stacked items
		total_height = sum(i.height for i in list_items)
		
		# Get optimal scrollview height
		scrollview_height = min(sp(300), total_height)
		
		self.dialog = MDDialog(
			# ----------------------------Icon-----------------------------
			MDDialogIcon(icon="palette"),
			# -----------------------Headline text-------------------------
			MDDialogHeadlineText(text="Choose your accent color"),
			# -----------------------Custom content------------------------
			MDDialogContentContainer(
				MDScrollView(
					MDBoxLayout(
						
						*list_items,  # Unpack all list items
						
						orientation="vertical",
						adaptive_height=True,
					),
					do_scroll_x=False,
					size_hint_y=None,
					height=scrollview_height, 
				),
				orientation="vertical",
			),
			# ---------------------Button container------------------------
			MDDialogButtonContainer(
				Widget(),
				MDButton(
					MDButtonText(text="Accept"),
					style="text",
					on_release=lambda x: self.close_and_save_palette(),
				),
				spacing="8sp",
			),
			# -------------------------------------------------------------
		)
		self.dialog.open()

	def close_and_save_palette(self):
		
		# Get active box
		active_option = None
		for i in self.boxes:
			if i.active:
				active_option = i
				break
		
		if active_option:
			# Set the primary palette to the selected color
			self.theme_cls.primary_palette = active_option.name
			self.set_bars_colors()
			
			# Update text
			app = MDApp.get_running_app()
			settings = app.root.ids.screen_manager.get_screen("settings")
			settings.ids.palette_text.text = active_option.name
			
			# Save to file
			self.save_config_file({"palette":active_option.name})
			
			self.dialog.dismiss()
	
	# Precision
	def show_precision_dialog(self):
	
		# Menu options
		options = [
			"1 digit",
			"2 digits",
			"3 digits",
			"4 digits",
			"5 digits",
			"6 digits",
			"7 digits",
			"8 digits",
			"9 digits"
		]
		
		# Create one checkbox for each color
		self.boxes = [
			MDListItemTrailingCheckbox(
				group="Precision",
				active=False,
				focus_behavior=False,
			)
			for i in range(len(options))
		]
		
		# Assign names to checkboxes
		for i, j in enumerate(options):
			self.boxes[i].name = j
		
		# Pre-check based on current palette
		for i in self.boxes:
			if i.name == self.precision:
				i.active = True
				break
		
		# Create list items for the dialog
		list_items = [
			
			MDListItem(
				MDListItemSupportingText(text=j),
				self.boxes[i],
				theme_bg_color="Custom",
				md_bg_color=self.theme_cls.transparentColor,
				focus_behavior=False,
			)
			
			for i, j in enumerate(options)
		]
		
		# Get height of stacked items
		total_height = sum(i.height for i in list_items)
		
		# Get optimal scrollview height
		scrollview_height = min(sp(300), total_height)
		
		self.dialog = MDDialog(
			# ----------------------------Icon-----------------------------
			MDDialogIcon(icon="numeric"),
			# -----------------------Headline text-------------------------
			MDDialogHeadlineText(text="Precision when working with scientific mode"),
			# -----------------------Custom content------------------------
			MDDialogContentContainer(
				MDScrollView(
					MDBoxLayout(
						
						*list_items,  # Unpack all list items
						
						orientation="vertical",
						adaptive_height=True,
					),
					do_scroll_x=False,
					size_hint_y=None,
					height=scrollview_height, 
				),
				orientation="vertical",
			),
			# ---------------------Button container------------------------
			MDDialogButtonContainer(
				Widget(),
				MDButton(
					MDButtonText(text="Accept"),
					style="text",
					on_release=lambda x: self.close_and_save_precision(),
				),
				spacing="8sp",
			),
			# -------------------------------------------------------------
		)
		self.dialog.open()

	def close_and_save_precision(self):
		
		# Get active box
		active_option = None
		for i in self.boxes:
			if i.active:
				active_option = i
				break
		
		if active_option:
			# Set the global config
			self.precision = active_option.name
			
			# Update text
			app = MDApp.get_running_app()
			settings = app.root.ids.screen_manager.get_screen("settings")
			settings.ids.precision_text.text = active_option.name
			
			# Save to file
			self.save_config_file({"precision": active_option.name})
			
			self.dialog.dismiss()
	
	# Preserve-history dialog
	def show_history_dialog(self):
	
		# Menu options
		switch = [
			"On",
			"Off"
		]
		
		# Create one checkbox for each color
		self.boxes = [
			MDListItemTrailingCheckbox(
				group="preserve-history",
				active=False,
				focus_behavior=False,
			)
			for i in range(len(switch))
		]
		
		# Assign names to checkboxes
		for i, j in enumerate(switch):
			self.boxes[i].name = j
		
		# Pre-check based on current palette
		for i in self.boxes:
			if i.name == self.preserve_history:
				i.active = True
				break
		
		# Create list items for the dialog
		list_items = [
			
			MDListItem(
				MDListItemSupportingText(text=j),
				self.boxes[i],
				theme_bg_color="Custom",
				md_bg_color=self.theme_cls.transparentColor,
				focus_behavior=False,
			)
			
			for i, j in enumerate(switch)
		]
		
		# Get height of stacked items
		total_height = sum(i.height for i in list_items)
		
		# Get optimal scrollview height
		scrollview_height = min(sp(300), total_height)
		
		self.dialog = MDDialog(
			# ----------------------------Icon-----------------------------
			MDDialogIcon(icon="content-save"),
			# -----------------------Headline text-------------------------
			MDDialogHeadlineText(text="Across-reboot persistent history"),
			# -----------------------Custom content------------------------
			MDDialogContentContainer(
				MDScrollView(
					MDBoxLayout(
						
						*list_items,  # Unpack all list items
						
						orientation="vertical",
						adaptive_height=True,
					),
					do_scroll_x=False,
					size_hint_y=None,
					height=scrollview_height, 
				),
				orientation="vertical",
			),
			# ---------------------Button container------------------------
			MDDialogButtonContainer(
				Widget(),
				MDButton(
					MDButtonText(text="Accept"),
					style="text",
					on_release=lambda x: self.close_and_save_ph(),
				),
				spacing="8sp",
			),
			# -------------------------------------------------------------
		)
		self.dialog.open()
	
	# Save preserve-history configuration
	def close_and_save_ph(self):
		
		# Get active box
		active_option = None
		for i in self.boxes:
			if i.active:
				active_option = i
				break
		
		# Save config
		self.save_config_file({"preserve-history":active_option.name})
		
		# Update text
		app = MDApp.get_running_app()
		settings = app.root.ids.screen_manager.get_screen("settings")
		settings.ids.history_text.text = active_option.name
		
		self.dialog.dismiss()

	# Info dialog
	def show_info_dialog(self):
		
		self.dialog = MDDialog(
			# ----------------------------Icon-----------------------------
			MDDialogIcon(icon="information"),
			# -----------------------Headline text-------------------------
			MDDialogHeadlineText(text="About"),
			# -----------------------Custom content------------------------
			MDDialogContentContainer(
				MDLabel(
					text=(
						"kivycalc v0.5.0-beta\n\n"
						"Created by Rigel. Thank you for using!\n\n"
						"Visit the git at: https://github.com/Rigel2118/kivycalc"
						),
					size_hint_y = None,
					size_hint_x = 1,
					halign = "center",
					valign = "center",
					height = sp(120),
				)
			),
			# ---------------------Button container------------------------
			MDDialogButtonContainer(
				Widget(),
				MDButton(
					MDButtonText(text="Visit git"),
					style="text",
					on_release=lambda x: webbrowser.open("https://github.com/Rigel2118/kivycalc"),
				),
				MDButton(
					MDButtonText(text="Accept"),
					style="text",
					on_release=lambda x: self.dialog.dismiss(),
				),
				spacing="8sp",
			),
			# -------------------------------------------------------------
		)
		self.dialog.open()
	
# -------------- Tabs -------------- #

class HomeTab(MDScreen):
	
	# Initialize stuff when the app starts
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		# Counter
		self.n_lines = 0
		
		# Current line
		self.cur_line = 0
		
		# Make the function an instance attribute for convenience later
		self.create_io_files = create_io_files
		
		# Toggle C-AC button function
		self.l1 = lambda x: self.reset_helper()
		
		# Memory functions
		self.l2 = lambda x: self.memory_recall()
		self.l3 = lambda x: self.memory_store()
		self.l4 = lambda x: self.memory_add()
		self.l5 = lambda x: self.memory_substract()
		
		# Monitor 2ND button state
		self.is_second = False
		
		# Monitor SCI mode
		app = MDApp.get_running_app()
		if app.load_config_file("sci") == "On":
			self.is_sci = True
		else:
			self.is_sci = False
		
		# Initialize widgets
		Clock.schedule_once(lambda dt: self.initialize_helper_text(), 0)
		Clock.schedule_once(lambda dt: self.ids.memr.bind(on_release = self.l2), 0)
		Clock.schedule_once(lambda dt: self.ids.mem.bind(on_release = self.l4), 0)
	
	# Update helper text
	def update_helper(self, new=None):
	
		# Assume we want to update cur_line to the latest possible
		if new is None:
			new = self.n_lines
		
		# History lookup mode
		if new < self.n_lines:
			self.ids.helper_line.text = f"Line {new} (history lookup)"
		
		# New line mode
		else:
			self.ids.helper_line.text = f"Line {new} (new line)"
		
		# Update current line
		self.cur_line = new
	
	# Update the counter
	def initialize_helper_text(self):
	
		# Get total lines from the file
		self.n_lines = count_lines(data_output)+1
		
		# Call the updater
		self.update_helper()
	
	# Insert
	def insert_text(self, text):
		
		# Call the widget method for inserting text
		self.ids.input_field.insert_text(text)
		
		# Focus the input immediately
		self.ids.input_field.focus = True
		
		# Call the updater
		self.update_helper()
		
		# Delete output contents
		self.ids.output_field.text = ""
	
	# Toggle ON-OFF 2ND
	def toggle_2nd(self, mode=None):
		
		# Toggles to the opposite
		if mode == None:
			if self.is_second:
				self.toggle_off_2nd()
			else:
				self.toggle_on_2nd()
			self.is_second = not self.is_second
		
		# Toggles to a specific state
		else:
			match mode:
				case "on": 
					self.toggle_on_2nd()
					self.is_second = True
				case "off": 
					self.toggle_off_2nd()
					self.is_second = False
					
	# Toggle ON 2ND (what changes)
	def toggle_on_2nd(self):
	
		# Clear
		self.ids.clear_button.text = "AC"
		self.ids.clear_button.bind(on_release = self.l1)
		
		# M-
		self.ids.mem.text = "M-"
		self.ids.mem.unbind(on_release = self.l4)
		self.ids.mem.bind(on_release = self.l5)
		
		# MS
		self.ids.memr.text = "MS"
		self.ids.memr.unbind(on_release = self.l2)
		self.ids.memr.bind(on_release = self.l3)
		
		# Toggle appearance
		self.ids.secondf.style = "filled"
	
	# Toggle OFF 2ND (what changes)
	def toggle_off_2nd(self):
	
		# Clear
		self.ids.clear_button.text = "C"
		self.ids.clear_button.unbind(on_release = self.l1)
		
		# M+
		self.ids.mem.text = "M+"
		self.ids.mem.unbind(on_release = self.l5)
		self.ids.mem.bind(on_release = self.l4)
		
		# MR
		self.ids.memr.text = "MR"
		self.ids.memr.unbind(on_release = self.l3)
		self.ids.memr.bind(on_release = self.l2)
		
		# Toggle appearance
		self.ids.secondf.style = "outlined"
	
	# Toggle SCI mode
	def toggle_sci(self):
		if self.is_sci:
			self.ids.sci.style = "outlined"
		else:
			self.ids.sci.style = "filled"
		self.is_sci = not self.is_sci
		
	# C -> AC
	def clear_toggle_AC(self):
		self.ids.clear_button.text = "AC"
		self.ids.clear_button.bind(on_release=self.l1)

	# Helper
	def reset_helper(self):
		
		# Delete file contents
		self.create_io_files()
		
		# Reset counter
		self.n_lines = 1
		
		# Call updater
		self.update_helper()
		
		# Clear history
		app = MDApp.get_running_app()
		history = app.root.ids.screen_manager.get_screen("history")
		history.clear_history()
		
	# AC -> C
	def clear_toggle_C(self):
		self.ids.clear_button.text = "C"
		self.ids.clear_button.unbind(on_release=self.l1)
	
	# Memory Store
	def memory_store(self):
		if self.ids.output_field.text:
			app = MDApp.get_running_app()
			res = self.ids.output_field.text[2:]
			app.save_config_file({"memory": res})
		
	# Memory Recall
	def memory_recall(self):
		app = MDApp.get_running_app()
		res = app.load_config_file("memory")
		self.insert_text(res)
	
	# Memory add
	def memory_add(self):
		if self.ids.output_field.text:
			app = MDApp.get_running_app()
			prev = float(app.load_config_file("memory"))
			res = float(self.ids.output_field.text[2:])
			new = str(format_number(prev+res))
			app.save_config_file({"memory": new})
		
	# Memory substract
	def memory_substract(self):
		if self.ids.output_field.text:
			app = MDApp.get_running_app()
			prev = float(app.load_config_file("memory"))
			res = float(self.ids.output_field.text[2:])
			new = str(format_number(prev-res))
			app.save_config_file({"memory": new})
		
	# Backspace
	def backspace(self):
		if self.ids.input_field.cursor_index() > 0:
			self.ids.input_field.do_backspace()
			self.ids.input_field.focus = True
			self.update_helper()
			self.ids.output_field.text = ""
			
	# Clear input
	def clear(self):
		if self.ids.input_field.cursor_index() > 0:
			self.ids.input_field.text = ""
			self.ids.input_field.focus = True
			self.update_helper()
			self.ids.output_field.text = ""
			
	
	# Move backwards
	def move_left(self):
		self.ids.input_field.do_cursor_movement('cursor_left')
		self.ids.input_field.focus = True
		
	# Move forward
	def move_right(self):
		self.ids.input_field.do_cursor_movement('cursor_right')
		self.ids.input_field.focus = True
	
	# Move home
	def move_home(self):
		self.ids.input_field.do_cursor_movement('cursor_home')
		self.ids.input_field.focus = True
		
	# Move end
	def move_end(self):
		self.ids.input_field.do_cursor_movement('cursor_end')
		self.ids.input_field.focus = True
		
	# Solve
	def solve(self):
		
		# Make sure there is text
		if self.ids.input_field.text != "":
			try:
				# Compute
				result=format_number(arithmetic(self.ids.input_field.text))
				
				# Show result in output (SCI on)
				if self.is_sci:
					app = MDApp.get_running_app()
					sci_num = float("{:e}".format(float(result)))
					precision = int(app.precision[0])-1
					result = f"{sci_num:.{precision}e}"
					
					self.ids.output_field.text = "= "+result
					
				# SCI off
				else:
					self.ids.output_field.text = "= "+result
				
				# Write result to data files
				with open(data_input, 'a+') as file:
					file.write(self.ids.input_field.text + '\n')
				with open(data_output, 'a+') as file:
					file.write(result + '\n')
				
				# Add card in history
				app = MDApp.get_running_app()
				app.history_tab.add_card(self.ids.input_field.text, result, self.cur_line)
				
				# Account for counter
				self.n_lines+=1
				self.update_helper()
				
			except Exception as e:
			
				# Write error message to output
				self.ids.output_field.text=f"Error: {str(e)}"
	
	# Load previous line
	def get_prev_line(self):
		if self.cur_line > 1:

			self.update_helper(self.cur_line-1)
			
			# Get previous line from file
			self.ids.input_field.text = f"{read_line(data_input, self.cur_line)}"
			self.ids.input_field.focus = True
			self.ids.output_field.text = f"= {read_line(data_output, self.cur_line)}"
			
	
	# Load next line
	def get_next_line(self):
		if self.cur_line < self.n_lines:
			self.update_helper(self.cur_line+1)
			self.ids.input_field.text = f"{read_line(data_input, self.cur_line)}"
			self.ids.input_field.focus = True
			
			if self.cur_line < self.n_lines:
				self.ids.output_field.text = f"= {read_line(data_output, self.cur_line)}"
				
			# New line is always blank
			else:
				self.ids.output_field.text = ""
		
# History tab
class HistoryTab(MDScreen):
	
	# When tab is accessed
	def on_enter(self, *args):
		Clock.schedule_once(lambda dt: self.bottom_scroll(), 0)
			
	# Run at creation of tab	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		# Helper
		app = MDApp.get_running_app()
		app.history_tab = self
		
		# Load stand with cards
		match app.preserve_history:
			case "On": Clock.schedule_once(self.fill_stand, 0)
			case "Off": create_io_files()
		
	# Go to the bottom of history stand
	def bottom_scroll(self, *args):
	
		stand = self.ids.history_stand
		stand.height = stand.minimum_height
		
		# Only when needed
		if stand.minimum_height > Window.height:
			self.ids.history_scroll.scroll_y = 0
		
		
	
	# Load cards
	def fill_stand(self, dt):
		
		# Get total lines
		n_lines = count_lines(data_output)
		
		# For each line in file
		for i in range(1, n_lines+1):
			
			# Extract information
			exp = read_line(data_input, i)
			res = read_line(data_output, i)
			
			# Add to stand
			self.ids.history_scroll.data.append({"text": f"{exp}\n= {res}", "line": i})

	
	# Add card to stand
	def add_card(self, exp, res, l):
		self.ids.history_scroll.data.append({"text": f"{exp}\n= {res}", "line": l})
	
	# Clear history
	def clear_history(self):
		self.ids.history_scroll.data = []
		self.ids.history_scroll.refresh_from_data()
	
# Settings tab
class SettingsTab(MDScreen):
	
	# At creation
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		Clock.schedule_once(self.load_settings, 0)
	
	# Load text that shows current settings
	def load_settings(self, dt):
		app = MDApp.get_running_app()
		self.ids.theme_text.text = self.theme_cls.theme_style
		self.ids.palette_text.text = self.theme_cls.primary_palette
		self.ids.history_text.text = app.preserve_history
		self.ids.precision_text.text = app.precision
		
# ------------- Widgets ------------- #

# Cards
class HistoryCard(MDCard):

	# Make bindable
	text = StringProperty("")
	line = NumericProperty()
	
	# Nothing to do at creation lol
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
	
	# Write to io fields
	def write_io(self):
		app = MDApp.get_running_app()
		home = app.root.ids.screen_manager.get_screen("home")
		
		# Grab from file and place into input
		home.ids.input_field.text = f"{read_line(data_input, self.line)}"
		home.ids.input_field.focus = True
		
		# Grab from file and place into output
		home.ids.output_field.text = f"= {read_line(data_output, self.line)}"
		
		home.update_helper(self.line)
	
	# Change screen when a card is clicked
	def go_home(self):
		app = MDApp.get_running_app()
		navbar = app.root.ids.navbar
		self.match(navbar, "home")
		
	# Match item by text
	def match(self, widget, text):
		for item in widget.children:
			if item.text == text:
				widget.set_active_item(item)
				break
			
# Run app
if __name__ == '__main__':	
	calcApp().run()
