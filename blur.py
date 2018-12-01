import kivy
from kivy.config import Config
Config.set('graphics', 'width', '960')
Config.set('graphics', 'height', '540')

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.graphics import *
from kivy.properties import *
from kivy.clock import Clock

from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.effectwidget import AdvancedEffectBase, EffectWidget, HorizontalBlurEffect
from kivy.uix.image import AsyncImage

from kivy.loader import LoaderBase
LoaderBase.loading_image = 'res/load_anim.gif'
LoaderBase.max_upload_per_frame = 20
LoaderBase.num_workers = 4


from kivymd.theming import ThemeManager
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem



class AvatarSampleWidget(ILeftBody, AsyncImage):
	pass

GLSL_MASK = '''
uniform sampler2D mask;
uniform vec2 mask_pos;
uniform vec2 mask_size;
// mode:
// 0: the mask pixel multiply the texture
// 1: the mask pixel substract to the texture
// addition and division don't seem to be of any use
uniform int mode;
vec4 effect(vec4 color, sampler2D texture, vec2 tex_coords, vec2 coords){
	// get the pixel lookup pos in the mask relative to our main texture
	vec2 pos = tex_coords; // - mask_pos * resolution;
	vec2 size = mask_size / resolution;
	if (
		pos.x < 0. || pos.y < 0. ||
		pos.x > 1. || pos.y > 1.
	)
		if (mode == 0)
			return vec4(0.);
		else
			return color;
	if (mode == 0)
		return color * texture2D(mask, pos);
	else
		return color - texture2D(mask, pos);
}
'''


class MaskEffect(AdvancedEffectBase):
	mask = ObjectProperty()
	glsl = StringProperty(GLSL_MASK)
	mode = OptionProperty('multiply', options=['multiply', 'substract'])

	def __init__(self, **kwargs):
		super(MaskEffect, self).__init__(**kwargs)
		assert(self.mask)
		self.mask.bind(
			pos=self.update_mask,
			size=self.update_mask,
		)
		self.bind(mode=self.update_mask)

	def on_fbo(self, *args):
		self.update_mask()

	def update_mask(self, *args):
		with self.fbo:
			BindTexture(
				texture=self.mask.fbo.texture,
				index=1)
		self.uniforms.update({
			'mask': 1,
			'mask_pos': list(self.mask.pos),
			'mask_size': list(self.mask.size),
			'mode': 0 if self.mode == 'multiply' else 1,
		})


class BlurWidget(Widget):
	texture = ObjectProperty(None, allownone=True)

	source = ObjectProperty(None)
	target = ObjectProperty(None)
	mask = ObjectProperty(None)
	mask_layout = ObjectProperty(None)

	def __init__(self, **kwargs):
		self.canvas = Canvas()
		with self.canvas:
			self.fbo = Fbo(size=self.size, with_stencilbuffer=True)
			Color(1, 1, 1, 1)
			self.fbo_rect = Rectangle()

		# wait that all the instructions are in the canvas to set texture
		self.texture = self.fbo.texture
		
		super(BlurWidget, self).__init__(**kwargs)

	def on_size(self, instance, value):
		self.fbo.size = self.parent.size
		#self.fbo_rect.size = value
		self.update_regions()

	def update_regions(self):
		#self.canvas.ask_update()
		self.fbo.clear()
		self.fbo.add(self.source.canvas)
		self.fbo_rect.size = self.size
		self.fbo_rect.texture = self.fbo.texture
		
		self.canvas.ask_update()
		#self.mask.canvas.clear()
		for child in self.mask_layout.children:
			print(child)
			with self.mask_layout.canvas.after:
				Color(1, 1, 1, 1)
				Rectangle(pos = child.pos, size = child.size)


from kivymd.theming import ThemeManager
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem

class AvatarSampleWidget(ILeftBody, AsyncImage):
	pass
		

class Root(FloatLayout):
	pass

class MainApp(App):
	title = "Test"
	time = NumericProperty()

	def build(self):
		Clock.schedule_interval(self.update_time, 0)
		return Builder.load_file('kv/blur.kv')

	def update_time(self, dt):
		self.time += dt

if __name__ == '__main__':
	MainApp().run()

