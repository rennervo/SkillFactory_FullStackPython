from bottle import HTTPError
from bottle import request
from bottle import route
from bottle import run

from B6.album import *


@route("/albums/<artist>")
def albums(artist):
    albums_list = find(artist)
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
    try:
        album = Album(
            year=request.forms.get("year"),
            artist=request.forms.get("artist"),
            genre=request.forms.get("genre"),
            album=request.forms.get("album")
        )
        if not verify_year(album.year):
            raise ValueError("Указанный год не соответствует формату 'YYYY'")
        if find_album(album.artist, album.album):
            session = connect_db()
            session.add(album)
            session.commit()
            result = "Альбом успешно добавлен в БД. ID добавленного альбома {}".format(album.id)
        else:
            message = "Запись с альбомом {} у исполнителя {} уже есть в БД".format(album.album,
                                                                                   album.artist)
            result = HTTPError(409, message)
        return result
    except ValueError as err:
        return HTTPError(409, err)


def verify_year(year):
    if len(year) == 4 & str(year).isdigit():
        return True
    else:
        return False


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
