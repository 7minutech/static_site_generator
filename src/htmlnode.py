
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
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a value")
        if self.children is None:
            raise ValueError("All parent nodes must have a children")
        result = ""
        for child in self.children:
            result += child.to_html()
        result = f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"

        return result        
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"