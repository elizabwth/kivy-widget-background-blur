from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.image import AsyncImage

from kivymd.theming import ThemeManager
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem

class AvatarSampleWidget(ILeftBody, AsyncImage):
	pass

class MainApp(App):
	theme_cls = ThemeManager()
	previous_date = ObjectProperty()
	title = "KivyMD Kitchen Sink"

	def build(self):
		return Builder.load_file('kv/main.kv')

if __name__ == '__main__':
	MainApp().run()

