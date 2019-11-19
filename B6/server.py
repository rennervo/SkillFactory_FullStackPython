import album
from bottle import HTTPError
from bottle import route
from bottle import run


@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомы исполнителя {} не найдены".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Список альбомов исполнителя {}:\n".format(artist)
        result += "\n".join(album_names)
    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
