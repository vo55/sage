import unittest
from sage import banner_parser


class BannerParserTest(unittest.TestCase):
    def test_correct_banner(self):
        parser = banner_parser.BannerParser(['Host: example.com', 'X-Something: bla', 'Server: nginx/1.2.3'])
        self.assertEqual('nginx', parser.get_server())
        self.assertEqual('1.2.3', parser.get_version())


    def test_no_banner(self):
        parser = banner_parser.BannerParser(['Host: example.com', 'X-Something: bla'])
        self.assertIsNone(parser.get_server())
        self.assertIsNone(parser.get_version())

if __name__ == '__main__':
    unittest.main()