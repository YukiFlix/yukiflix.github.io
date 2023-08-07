import datetime
import json
import requests
from tools import *
from flask import *
_d = "/add/serie/new/season/"
_c = "_H.webp"
_b = "_V.webp"
_a = "description_serie"
_Z = "/static/img/"
_Y = "add_new_episode3.html"
_X = "/add/serie/new/episode/"
_W = "movies"
_V = "Ce n'est pas le bon mot de passe"
_U = "password"
_T = "star"
_S = "description"
_R = "/watch/serie/"
_Q = "___"
_P = "__"
_N = "tt_episode"
_M = "episodes"
_L = "seasons"
_K = "static/img/"
_J = "root"
_I = "image_H"
_H = "image_V"
_G = "link_vostfr"
_F = "link_fr"
_E = "series"
_D = "GET"
_C = "POST"
_B = "_"
_A = "data.json"

app = Flask(__name__)
app.secret_key = "2043a6921650c67f05bfabbef3007eea08d1d8778cc9d084"
year = datetime.datetime.now().year

ROLE_ID = "1041103551751004161"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1130964248370090115/6u4N8Hz7NsYBx5cHDBdoKnETtEUqHokzBBW2Ppl8nYq6j0x8OTngidOT7DUvXofeEKjP"


@app.before_request
def define_ephemeral_variable():
    global data
    global year
    g.year = year
    try:
        data = read_json(_A)
    except:
        data = {_W: {item: []
                     for item in ["name", _F, _G, _S, _H, _I, _T, _J]},
                _E: {}}
        write_json(data, _A)


@app.route("/")
def accueil():
    logged_in = session.get('logged_in', False)
    root = _K
    data = read_json(_A)
    count()

    if logged_in:
        # Utilisateur connecté, afficher le profil
        return render_template(
            "index.html", data=data, len=len, nb_visit=read_pickle("visits.pkl"), root=root, logged_in=True
        )
    else:
        # Utilisateur non connecté, afficher la page d'accueil avec le bouton "Sign In"
        return render_template(
            "index.html", data=data, len=len, nb_visit=read_pickle("visits.pkl"), root=root, logged_in=False
        )


@app.route("/faq/")
def faq():
    logged_in = session.get('logged_in', False)
    return render_template("faq.html", logged_in=logged_in)


@app.route("/add/")
def add():
    logged_in = session.get('logged_in', False)
    return render_template("add.html", logged_in=logged_in)


@app.route("/add/movie/", methods=[_D, _C])
def add_movies():
    logged_in = session.get('logged_in', False)
    C = "/watch/movie/"
    B = ".webp"
    A = "add_movie.html"
    data = read_json(_A)
    root_img = _K
    movies = data[_W]
    if request.method == _C:
        name = get_input("name_movie")
        name_img = (
            name.replace(" ", _B).replace(
                ":", _B).replace(_P, _B).replace(_Q, _B)
        )
        if name in list(movies.keys()):
            error = "Ce film existe déjà"
            return render_template(A, error=error)
        link_fr = get_input("link_movie_fr")
        link_vostfr = get_input("link_movie_vostfr")
        star = get_input(_T)
        description = get_input("description_movie")
        password = get_input(_U)
        if password != app.secret_key:
            error = _V
            return render_template(A, error=error)
        root_html = "templates/watch/movie/"
        image_V = request.files[_H]
        image_H = request.files[_I]
        name_image_V = name_img + "_V" + B
        name_image_H = name_img + "_H" + B
        root_image_V = root_img + name_image_V
        root_image_H = root_img + name_image_H
        create_root(root_img)
        image_V.save(root_image_V)
        image_H.save(root_image_H)
        movies[name] = {}
        movies[name][_G] = link_vostfr
        movies[name][_F] = link_fr
        movies[name][_S] = description
        movies[name][_H] = name_image_V
        movies[name][_I] = name_image_H
        movies[name][_T] = star
        movies[name][_J] = C + name
        write_json(data, _A)
        create_root(root_html)
        notification_message = f"||<@&{ROLE_ID}>||\nNouveau Film : **{name}**\nLien : https://yukiflix.pythonanywhere.com/watch/movie/{name.replace(' ', '%20')}"
        embed = {
            "title": name,
            "description": description,
            "url": f"https://yukiflix.pythonanywhere.com/watch/movie/{name.replace(' ', '%20')}",
            # Green color (you can use decimal or hex color code)
            "color": 0x00FF00,
            "image": {"url": "https://yukiflix.pythonanywhere.com" + "/" + root_image_H},
        }

        data = {"embeds": [embed], "content": notification_message}

        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        return redirect(C + name)
    return render_template(A, logged_in=logged_in)


@app.route("/watch/movie/<movie>/")
def watch_movie(movie):
    logged_in = session.get('logged_in', False)
    name = movie
    data = read_json(_A)
    if movie in list(data[_W].keys()):
        return render_template("watch/movie/model.html", data=data, name=name, logged_in=logged_in)


@app.route("/add/serie/", methods=[_D, _C])
def add_series():

    logged_in = session.get('logged_in', False)
    A = "add_serie.html"
    data = read_json(_A)
    root = _K
    series = data[_E]

    if request.method == _C:
        name = get_input("name_serie")

        if name in series:
            error = "Cette série existe déjà"
            return render_template(A, error=error)
        else:
            tt_episode = get_input(_N)
            link_fr = get_input("link_serie_fr")
            link_vostfr = get_input("link_serie_vostfr")
            star = get_input(_T)
            description = get_input(_a)
            password = get_input(_U)

            if password == app.secret_key:
                image_V = request.files[_H]
                image_H = request.files[_I]
                name_image_V = (
                    name.replace(" ", _B)
                    .replace(":", "")
                    .replace(_P, _B)
                    .replace(_Q, _B)
                    + _b
                )
                name_image_H = (
                    name.replace(" ", _B)
                    .replace(":", "")
                    .replace(_P, _B)
                    .replace(_Q, _B)
                    + _c
                )
                root_image_V = root + name_image_V
                root_image_H = root + name_image_H
                image_V.save(root_image_V)
                image_H.save(root_image_H)

                series[name] = {
                    _S: description,
                    _H: name_image_V,
                    _I: name_image_H,
                    "stars": star,
                    _J: f"/watch/serie/{name}",
                    _L: {
                        "1": {
                            _M: {
                                "1": {
                                    _J: f"/watch/serie/{name}/season/1/episode/1",
                                    _G: link_vostfr,
                                    _F: link_fr,
                                    _N: tt_episode
                                }
                            }
                        }
                    }
                }
                notification_message = f"||<@&{ROLE_ID}>||\nNouvelle Série : **{name}**\nLien : https://yukiflix.pythonanywhere.com/watch/serie/{name.replace(' ', '%20')}"
                requests.post(DISCORD_WEBHOOK_URL, data={
                              "content": notification_message})

                write_json(data, _A)
                return redirect(_R + name)
            else:
                error = _V
                return render_template(A, error=error)

    return render_template(A, logged_in=logged_in)


@app.route(_X, methods=[_D, _C])
def selected_serie():
    logged_in = session.get('logged_in', False)
    data = read_json(_A)
    series = data[_E]
    name_series = []

    if request.method == _C:
        serie = request.form.get("serie")
        return redirect(_X + serie)

    for key in series:
        name_series.append(key)

    return render_template("add_new_episode.html", name_series=name_series, logged_in=logged_in)


@app.route("/add/serie/new/episode/<serie>", methods=[_D, _C])
def selected_season(serie):
    logged_in = session.get('logged_in', False)
    data = read_json(_A)
    series = data[_E]
    seasons = []
    selected_serie = serie

    if request.method == _C:
        selected_serie = serie
        season = get_input("season")
        return redirect(_X + selected_serie + "/season/" + season)

    for key in series:
        if key == selected_serie:
            selected_series = series[key]
            season = selected_series[_L]
            for key in season:
                seasons.append(key)

    return render_template("add_new_episode2.html", seasons=seasons, serie=serie, logged_in=logged_in)


@app.route("/add/serie/new/episode/<serie>/season/<season>/", methods=[_D, _C])
def add_new_episode(serie, season):
    logged_in = session.get('logged_in', False)
    data = read_json(_A)
    series = data[_E]

    if request.method == _C:
        password = get_input(_U)
        if password == app.secret_key:
            nb_episode = get_input("nb_episode")
            tt_episode = get_input(_N)
            link_fr = get_input(_F)
            link_vostfr = get_input(_G)

            series[serie][_L][season][_M][nb_episode] = {
                _J: f"/watch/serie/{serie}/season/{season}/episode/{nb_episode}",
                _G: link_vostfr,
                _F: link_fr,
                _N: tt_episode
            }

            write_json(data, _A)
            return redirect(
                f"/watch/serie/{serie}/season/{season}/episode/{nb_episode}"
            )
        else:
            error = _V
            return render_template(_Y, serie=serie, season=season, error=error)

    return render_template(_Y, serie=serie, season=season, logged_in=logged_in)


@app.route("/watch/serie/<name>")
def watch_serie(name):
    logged_in = session.get('logged_in', False)
    root = _Z
    data = read_json(_A)
    return render_template("watch/serie/model.html", name=name, data=data, root=root, logged_in=logged_in)


@app.route("/watch/serie/<name>/season/<season>/episode/<episode>")
def watch_episode(name, season, episode):
    logged_in = session.get('logged_in', False)
    root = _Z
    data = read_json(_A)
    return render_template(
        "watch/serie/watch_episode.html",
        name=name,
        data=data,
        root=root,
        season=season,
        episode=episode,
        int=int,
        len=len,
        str=str,
        logged_in=logged_in
    )


@app.route(_d, methods=[_D, _C])
def selected_serie2():
    logged_in = session.get('logged_in', False)
    data = read_json(_A)
    series = data[_E]
    name_series = []

    if request.method == _C:
        serie = request.form.get("serie")
        return redirect(_d + serie)

    for key in series:
        name_series.append(key)

    return render_template("add_new_saison1.html", name_series=name_series, logged_in=logged_in)


@app.route("/add/serie/new/season/<serie>", methods=[_D, _C])
def add_serie_saison(serie):
    logged_in = session.get('logged_in', False)
    data = read_json(_A)
    root = _K
    series = data[_E]
    if request.method == _C:
        password = get_input(_U)
        if password == app.secret_key:
            nb_saison = get_input("nb_saison")
            tt_episode = get_input(_N)
            link_fr = get_input(_F)
            link_vostfr = get_input(_G)
            series[serie][_J] = _R + serie
            series[serie][_L][nb_saison] = {}
            season = series[serie][_L][nb_saison]
            season[_M] = {}
            season[_M]["1"] = {}
            episode = season[_M]["1"]
            episode[_J] = f"/watch/serie/{serie}/season/{nb_saison}/episode/1"
            episode[_N] = tt_episode
            episode[_G] = link_vostfr
            episode[_F] = link_fr
            write_json(data, _A)
            return redirect(_R + serie)
        else:
            error = _V
            return render_template(_Y, error=error)
    return render_template("add_new_saison2.html", logged_in=logged_in)


@app.route("/get_json/")
def get_json():

    if not 'logged_in' in session:
        return redirect("/")
    else:
        allowed_users = ["Honekichi", "Jojokes"]
        current_user = session.get('username')

        if current_user in allowed_users:
            with open(_A, "r", encoding="utf-8") as f:
                data = json.load(f)
            return json.dumps(data, ensure_ascii=False)
        else:
            return "Accès refusé. Vous n'êtes pas autorisé à accéder à cette ressource."


@app.route("/catalog/")
@app.route("/catalog/<letter>")
def catalog(letter=None):
    logged_in = session.get('logged_in', False)
    data = read_json(_A)
    if not letter:
        letter = "all"
    data = search_movie_and_series_with_letter(letter)
    return render_template("catalog.html", data=data, logged_in=logged_in)


@app.route("/signin/", methods=[_D, _C])
def sign_in():
    if 'logged_in' in session:
        return redirect("/")

    if request.method == _C:
        data = read_json(_A)
        if not "accounts" in data:
            data["accounts"] = {}
        accounts = data["accounts"]
        name = get_input("username")
        password = get_input("password")
        if name in accounts and password == accounts[name]:
            session['logged_in'] = True
            session['username'] = name
            return redirect("/")
        else:
            error_signin = "Le nom d'utilisateur ou le mot de passe est incorrect. Veuillez réessayer."
            return render_template("sign_in.html", error_signin=error_signin)
    return render_template("sign_in.html")


@app.route("/signup/", methods=[_D, _C])
def sign_up():
    if 'logged_in' in session:
        return redirect("/")

    if request.method == _C:
        data = read_json(_A)
        if "accounts" not in data:
            data["accounts"] = {}
        accounts = data["accounts"]
        name = request.form.get("username")
        password = request.form.get("password")

        if name in accounts:
            error_signup = "Le nom d'utilisateur est déjà pris. Veuillez en choisir un autre."
            return render_template("sign_up.html", error_signup=error_signup)

        accounts[name] = password
        write_json(data, _A)

        session['logged_in'] = True
        session['username'] = name

        return redirect("/")

    return render_template("sign_up.html")


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect('/')


@app.route('/profile')
def profile():
    if not session.get('logged_in'):
        return redirect('/signin')

    return render_template('profile.html', logged_in=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
