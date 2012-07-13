from unittest import TestCase
from breadcrumbs import node, Breadcrumbs, create_node

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
        cfg = [
               node('', r'\d+', 'id'),
               node('', r'.*', 'star'),
              ]
        bc = Breadcrumbs(cfg).create()
        self.assertEquals(bc("/path"), ["star"])
        self.assertEquals(bc("/123"), ["id"])

    def test_callable(self):
        cfg = [
               node('', r'(?P<id>\d+)', lambda id_: int(id_) + 1),
               node('', r'\w+', lambda x: "ID"),
              ]
        bc = Breadcrumbs(cfg).create()
        self.assertEquals(bc("/path"), ["ID"])
        self.assertEquals(bc("/13"), [14])

    def test_custom_pattern(self):
        node = create_node("---")
        nodes = [
               node('', r'A', 'A'),
               node('---', r'B', 'BB'),
               node('', r'B', 'B'),
              ]
        bc = Breadcrumbs(nodes).create()
        self.assertEquals(bc("/A/B"), ["A", "BB"])
        self.assertEquals(bc("/B/A"), ["B"])
        self.assertEquals(bc("/B/B/"), ["B"])


class TestNode(TestCase):
    def test_node_raise_exception_if_invalid_level(self):
        with self.assertRaises(ValueError):
            node('-->/', r'', 'error')

    def test_node_raise_exception_if_invalid_level2(self):
        with self.assertRaises(ValueError):
            node('---', r'', 'error')



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
