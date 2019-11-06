class HTML:
    def __init__(self, output="default.html"):
        self.output = output
        self.children = []
        self.name = "html"

    def __exit__(self, exc_type, exc_val, exc_tb):
        file = open(self.output, "w")
        file.write("<%s>" % self.name)
        for child in self.children:
            file.write(str(child))
        file.write("\n</%s>" % self.name)
        file.close()

    def __enter__(self):
        return self


class TopLevelTag(HTML):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        if self.children:
            opening = "\n<%s>" % self.name
            internal = ""
            for child in self.children:
                internal += str(child)
            ending = "\n</%s>" % self.name
            return opening + internal + ending


class Tag(TopLevelTag):
    def __init__(self, name, klass=None, is_single=False, **kwargs):
        super().__init__(name)
        self.is_single = is_single
        self.klass = klass
        self.text = ""
        self.attributes = {}
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            self.attributes[attr] = value

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        if self.children:
            opening = "\n<{name} {attrs}>".format(name=self.name, attrs=attrs)
            internal = "%s" % self.text
            for child in self.children:
                internal += str(child)
            ending = "\n</%s>" % self.name
            return opening + internal + ending
        else:
            if not self.is_single:
                return "\n<{name} {attrs}>{text}</{name}>".format(name=self.name, attrs=attrs, text=self.text)
            else:
                return "\n<{name} {attrs}/>".format(name=self.name, attrs=attrs)


with HTML(output="test.html") as doc:
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head.children.append(title)
        doc.children.append(head)

    with TopLevelTag("body") as body:
        with Tag("h1", klass=("main-text",)) as h1:
            h1.text = "Test"
            body.children.append(h1)

        with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
            with Tag("p") as paragraph:
                paragraph.text = "another test"
                div.children.append(paragraph)

            with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                div.children.append(img)

            body.children.append(div)

        doc.children.append(body)
