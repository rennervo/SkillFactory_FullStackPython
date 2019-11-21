from bottle import HTTPError
from bottle import request
from bottle import route
from bottle import run

from B6 import album


@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомы исполнителя {} не найдены".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Найдено {} альбомов исполнителя {}:\n".format(len(album_names), artist)
        result += "\n".join(album_names)
    return result


@route("/albums", method="POST")
def add_item():
    album_data = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album"),
    }
    if album.find_album(album_data["artist"], album_data["album"]):
        session = album.connect_db()
        session.add(album_data)
        session.commit()
        result = "Альбом успешно добавлен в БД. ID добавленного альбома {}".format(album_data["id"])
    else:
        message = "Запись с альбомом {} у исполнителя {} уже есть в БД".format(album_data["album"],
                                                                               album_data["artist"])
        result = HTTPError(409, message)
    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
