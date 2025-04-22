
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        return "".join(f" {key}=\"{value}\"" for key, value in self.props.items())
    
    def __repr__(self):
        return f"tag: {self.tag}, value: {self.value}, children: {self.children}, properties: {self.props}" 
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return vars(self) == vars(other)
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        self.tag = tag
        self.value = value
        self.props = props
        self.children = None

    def __setattr__(self, name, value):
        if name == "children" and value is not None:
            raise AttributeError("LeafNode cannot have children")
        super().__setattr__(name, value)

    def to_html(self):
        if not self.value and self.tag != "img":
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return str(self.value)
        props_html = self.props_to_html() if self.props else ""
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"  

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        self.tag = tag
        self.value = None
        self.props = props
        self.children = children

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        props_html = self.props_to_html() if self.props else ""        
        children_html = ""
        
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"

# node = ParentNode("p", [
#             LeafNode("b", "Bold text"),
#             LeafNode(None, "Normal text"),
#             LeafNode("i", "italic text"),
#             LeafNode(None, "Normal text"),
#         ],)