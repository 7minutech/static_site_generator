
class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None or self.props == {}:
            return ""
        attrs = [f"{key}=\"{value}\"" for key, value in self.props.items()]
        html = " ".join(attrs)
        return f" {html}"
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"