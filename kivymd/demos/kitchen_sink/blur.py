from kivy.app import App
from kivy.lang import Builder

class MainApp(App):
	title = "Test"

	def build(self):
		return Builder.load_file('kv/blur_test.kv')

if __name__ == '__main__':
	MainApp().run()

