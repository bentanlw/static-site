from textnode import TextNode, TextType

def main():
    t = TextNode("this is some anchor link", TextType("link"), "https://www.boot.dev")
    print(t)


if __name__ == "__main__":
    main()
