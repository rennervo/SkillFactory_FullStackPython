def add_n(txt):
    if txt[-2] != '\n':
        txt += '\n'
    return txt


class Tag:
    def __init__(self, name, klass=None, is_single=False, **kwargs):
        self.name = name
        self.is_single = is_single
        self.klass = klass
        self.text = ""
        self.attributes = {}
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            self.attributes[attr] = value

    def __add__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if attrs:
            attrs = ' ' + attrs

        if self.children:
            opening = "\t<{name} {attrs}>".format(name=self.name, attrs=attrs)
            opening = add_n(opening)
            internal = "%s" % self.text
            for child in self.children:
                internal += '\t' + str(child)
            ending = "\t</%s>" % self.name
            txt_return = opening + internal + ending
        else:
            if not self.is_single:
                txt_return = "\t<{name} {attrs}>{text}</{name}>".format(name=self.name, attrs=attrs, text=self.text)
            else:
                txt_return = "\t<{name} {attrs}/>".format(name=self.name, attrs=attrs)
        return txt_return


class TopLevelTag(Tag):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    def __str__(self):
        opening = "<{name}>".format(name=self.name)
        opening = add_n(opening)
        internal = ""
        for child in self.children:
            internal += str(child)
        ending = "</%s>" % self.name
        return add_n(opening + internal + ending)


class HTML(TopLevelTag):
    def __init__(self, output=None, **kwargs):
        self.output = output
        super().__init__('html', **kwargs)

    def __exit__(self, *args):
        if self.output is None:
            print(self)
        else:
            with open(self.output, "w", encoding="utf-8") as file:
                file.write(str(self))


if __name__ == "__main__":
    with HTML(output="test.html") as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                    div += img

                body += div

            doc += body
