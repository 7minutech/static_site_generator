from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if (node.text).count(delimiter) % 2 != 0:
            raise ValueError("text is not valid markdown")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parsed_text = (node.text).split(delimiter)
            for i in range(len(parsed_text)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(parsed_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(parsed_text[i], text_type))
    return new_nodes
