from django.test import TestCase
from prophecies.core.contrib.colors import hex_to_rgb, rgb_to_hex, hex_scale_brightness


class TestColors(TestCase):

    def test_it_convert_black_hex_to_rgb(self):
        rgb = hex_to_rgb('#000000')
        self.assertEqual(rgb, (0, 0, 0,))

    def test_it_convert_red_hex_to_rgb(self):
        rgb = hex_to_rgb('#ff0000')
        self.assertEqual(rgb, (1.0, 0, 0,))

    def test_it_convert_blue_hex_to_rgb(self):
        rgb = hex_to_rgb('#0000ff')
        self.assertEqual(rgb, (0, 0, 1.0,))

    def test_it_convert_pink_hex_to_rgb(self):
        rgb = hex_to_rgb('#ff00ff')
        self.assertEqual(rgb, (1.0, 0, 1.0))

    def test_it_convert_black_rgb_to_hex(self):
        hex = rgb_to_hex((0, 0, 0,))
        self.assertEqual(hex, '#000000')

    def test_it_convert_red_rgb_to_hex(self):
        hex = rgb_to_hex((1.0, 0, 0,))
        self.assertEqual(hex, '#ff0000')

    def test_it_convert_blue_rgb_to_hex(self):
        hex = rgb_to_hex((0, 0, 1.0,))
        self.assertEqual(hex, '#0000ff')

    def test_it_convert_pink_rgb_to_hex(self):
        hex = rgb_to_hex((1.0, 0, 1.0))
        self.assertEqual(hex, '#ff00ff')

    def test_it_scale_red_lightness_by_fivety_percent(self):
        hex = hex_scale_brightness('#ff0000', 1.5)
        self.assertEqual(hex, '#ff8080')

    def test_it_scale_blue_lightness_by_fivety_percent(self):
        hex = hex_scale_brightness('#0000ff', 1.5)
        self.assertEqual(hex, '#8080ff')

    def test_it_scale_pink_lightness_by_fivety_percent(self):
        hex = hex_scale_brightness('#ff00ff', 1.5)
        self.assertEqual(hex, '#ff80ff')

    def test_it_scale_red_darkness_by_fivety_percent(self):
        hex = hex_scale_brightness('#ff0000', 0.5)
        self.assertEqual(hex, '#800000')

    def test_it_scale_blue_darkness_by_fivety_percent(self):
        hex = hex_scale_brightness('#0000ff', 0.5)
        self.assertEqual(hex, '#000080')

    def test_it_scale_pink_darkness_by_fivety_percent(self):
        hex = hex_scale_brightness('#ff00ff', 0.5)
        self.assertEqual(hex, '#80007f')
