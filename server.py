import tempfile
import tornado.ioloop
import tornado.web
import pandas as pd


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        print("Receive POST request")
        filename = self.request.path.split("/")[-1]
        if not filename:
            filename = tempfile.mktemp()
        with open(filename, "wb") as f:
            f.write(self.request.body)
        table = pd.read_excel(open(filename, "rb")).head()
        self.write(table.style.render().encode())


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
