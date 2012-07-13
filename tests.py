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
               node('', r'A', 'A'),
               node('-->', r'B', 'BB'),
               node('', r'B', 'B'),
              ]
        bc = Breadcrumbs(nodes).create()
        self.assertEquals(bc("/A/B"), ["A", "BB"])
        self.assertEquals(bc("/B/A"), ["B"])
        self.assertEquals(bc("/B/B/"), ["B"])

    def test_regex(self):
        cfg = [node('', r'.*', 'star'),]
        bc = Breadcrumbs(cfg).create()
        self.assertEquals(bc("/path"), ["star"])



class TestIter(TestCase):
    def test_flat_iter(self):
        nodeA = node('', r'A', 'AAA')
        nodeA1 = node('-->', r'A', 'AAA')
        nodeB = node('', r'B', 'BBB')
        cfg = [
               nodeA,
               nodeA1,
               nodeB,
              ]
        bc = Breadcrumbs(cfg)
        bc.cursor_level = 0
        self.assertEquals([n for n in bc], [nodeA, nodeB])

        bc.cursor_level = 1
        self.assertEquals([n for n in bc], [nodeA1])
