class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props != None:
            list = []
            for prop in self.props:
                list.append(f' {prop}="{self.props[prop]}"')
            string = "".join(list)
            return string
        else:
            return ""

    def __repr__(self):
        return f"HTMLNode: (tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf node must have a value")
        if self.tag == None:
            return self.value

        props_str = self.props_to_html() if self.props else ""
        return f'<{self.tag}{props_str}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props, value=None)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent Node must have a tag")
        if self.children == None or len(self.children) == 0:
            raise ValueError("Parent Node must have children")
        node_list = []
        for child in self.children:
            node_list.append(child.to_html())
        node_string = "".join(node_list)
        
        props_str = self.props_to_html() if self.props else ""
        return f"<{self.tag}{props_str}>{node_string}</{self.tag}>"

 


