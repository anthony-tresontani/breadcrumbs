Breadcrumbs
===========

This library has been created to easily define breadcrumbs.
We see a breadcrumbs as a tree transforming an url in html.

/my-url/my-page --> <a> url bit for my-url</a> | my-page html

    from breadcrumbs import Breadcrumbs
    from breadcrumbs import create_node

    node =  create_node("---")

    nodes = [
        node("", r"my-url", <a>url bit for my-url</a>),
        node("---", r'(?P<name>.*)', lambda name: name)
    ]

    bc = Breadcrumbs(nodes).create()

    bc(request.path)}

You just have to create a list of node processing the url bit by bit and rendering HTML.

`node(level, regex, html)`:
    node create a breadcrumbs node.
    Take `level` as argument. Level should be many times the patterns defined in create_node. Ie if the pattern is "-->", "" is level 0, "-->" is level 1, "-->-->" is level2, etc...
    `regex` is the pattern that should be matched. Accept any python regular expression.
    `html` is a string or a callable which should render the html.

`create_node(pattern)`:
   create the node function with the custom pattern. By default, the pattern is "-->"
    
