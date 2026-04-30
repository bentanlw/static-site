from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("all parent nodes must have a tag")
        if not self.children:
            raise ValueError("all parent nodes must have a child")
        else:
            child_string = ""
            for c in self.children:
                child_string += c.to_html()
            return f"<{self.tag}{self.props_to_html()}>{child_string}</{self.tag}>"
