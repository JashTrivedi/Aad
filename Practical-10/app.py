import streamlit as st
import graphviz


# Node class for Huffman Tree
class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

# Huffman Tree building function (descending order)
def build_huffman_tree(char_freq):
    nodes = [Node(char, freq) for char, freq in char_freq.items()]
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.freq, reverse=True)  # Sort by descending frequency
        left = nodes.pop()  # Remove lowest frequency (smallest element)
        right = nodes.pop()  # Remove second lowest frequency
        merged = Node(None, left.freq + right.freq, left, right)
        nodes.append(merged)
    return nodes[0]

# Generate Huffman codes
def generate_huffman_codes(root, current_code="", codes={}):
    if root is None:
        return
    if root.char is not None:
        codes[root.char] = current_code
    generate_huffman_codes(root.left, current_code + "0", codes)
    generate_huffman_codes(root.right, current_code + "1", codes)
    return codes

# Encoding function
def encode(text, codes):
    try:
        return ''.join([codes[char] for char in text])
    except KeyError:
        return "Error: Invalid character in input."

# Decoding function
def decode(encoded_text, root):
    decoded_text = ""
    current_node = root
    for bit in encoded_text:
        current_node = current_node.left if bit == '0' else current_node.right
        if current_node.char is not None:
            decoded_text += current_node.char
            current_node = root
    return decoded_text

def create_huffman_tree():
    dot = graphviz.Digraph()
    dot.attr('node', shape='circle', style='filled', color='lightblue')

    # Add nodes with labels and weights
    dot.node('root', label='2.05')
    dot.node('0.9')
    dot.node('1.15')
    dot.node('E', label='E:0.4')
    dot.node('A', label='A:0.5')
    dot.node('C', label='C:0.5')
    dot.node('0.65')
    dot.node('0.3')
    dot.node('B', label='B:0.35')
    dot.node('D', label='D:0.1')
    dot.node('-', label='-:0.2')

    # Add edges with labels
    dot.edge('root', '0.9')
    dot.edge('root', '1.15')
    dot.edge('0.9', 'E')
    dot.edge('0.9', 'A')
    dot.edge('1.15', 'C')
    dot.edge('1.15', '0.65')
    dot.edge('0.65', '0.3')
    dot.edge('0.65', 'B')
    dot.edge('0.3', 'D')
    dot.edge('0.3', '-')

    return dot

# Streamlit app
def main():
    st.title("Huffman Coding with Streamlit")

    # Input for character frequencies
    char_freq_input = st.text_input("Enter Character Frequencies (Format: A:0.5, B:0.35, C:0.1):", "A:0.5, B:0.35, C:0.1")

    # Input for encoding text
    input_text = st.text_input("Enter Text to Encode:", "CAD-BE")

    # Input for decoding text
    encoded_text_to_decode = st.text_input("Enter Encoded Text to Decode:", "110101")

    # Action button
    if st.button("Submit"):
        try:
            # Parse character frequencies
            char_freq = {pair.split(':')[0].strip().upper(): float(pair.split(':')[1].strip()) for pair in char_freq_input.split(',')}
        except Exception as e:
            st.error(f"Error parsing input: {e}")
            return

        # Build Huffman Tree
        huffman_tree = build_huffman_tree(char_freq)
        huffman_codes = generate_huffman_codes(huffman_tree)

        # Display Huffman Codes
        st.subheader("Huffman Codes")
        st.write(huffman_codes)

        # Encode text
        if input_text:
            encoded_text = encode(input_text.upper(), huffman_codes)
            st.subheader("Encoded Text")
            st.write(encoded_text)

        # Decode text
        if encoded_text_to_decode:
            decoded_text = decode(encoded_text_to_decode, huffman_tree)
            st.subheader("Decoded Text")
            st.write(decoded_text)
         
        st.title("Huffman Tree Visualization")

        huffman_tree = create_huffman_tree()
        st.graphviz_chart(huffman_tree)
 

if __name__ == '__main__':
    main()
