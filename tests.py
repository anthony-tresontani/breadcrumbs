from unittest import TestCase
from breadcrumbs import node, Breadcrumbs

class BreadCrumbsTest(TestCase):
    def test_empty_breadcrumbs(self):
        bc = Breadcrumbs("").create()
        self.assertEquals(bc("/"), [])

    def test_constante_breadcrumbs(self):
        cfg = [node('', r'path', 'BC'),]
        bc = Breadcrumbs(cfg).create()
        self.assertEquals(bc("/path"), ["BC"])

    def test_same_level_different_pattern(self):
        cfg = [
               node('', r'A', 'AAA'),
               node('', r'B', 'BBB'),
              ]
        bc = Breadcrumbs(cfg).create()
        self.assertEquals(bc("/A/B"), ["AAA"])
        self.assertEquals(bc("/B/A"), ["BBB"])

    def test_embed_pattern(self):
        nodes = [
               node('', r'A', 'AAA'),
               node('-->', r'B', 'BBB'),
              ]
        bc = Breadcrumbs(nodes).create()
        self.assertEquals(bc("/A/B"), ["AAA", "BBB"])


