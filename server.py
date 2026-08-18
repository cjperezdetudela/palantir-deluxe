import os
import sys
import json
import sqlite3
import urllib.parse
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

# Initialize Kodi Shim environment
addon_dir = os.path.abspath(os.path.join("extracted_plugin.video.palantir3", "plugin.video.palantir3"))
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)

import kodi_shim
kodi_shim.install_kodi_shims()
import context
import libs.ioI1I1ii1 as resolver_mod

import zipfile
db_dir = getattr(kodi_shim, "DB_DIR", os.path.abspath(os.path.join("kodi_data", "profile", "addon_data", "script.module")))
db_path = os.path.join(db_dir, "settings.xml")
zip_path = os.path.join(db_dir, "settings.zip")
if not os.path.exists(db_path) and os.path.exists(zip_path):
    print("[SERVER STARTUP] Descomprimiendo base de datos settings.zip...")
    os.makedirs(db_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(db_dir)
    print("[SERVER STARTUP] Base de datos descompactada correctamente.")

app = FastAPI(title="Palantir Deluxe API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.abspath(os.path.join("kodi_data", "profile", "addon_data", "script.module", "settings.xml"))

def get_db_connection():
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=500, detail="Palantir database (settings.xml) not found.")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def format_poster(path, title="Palantir"):
    if not path:
        return f"/api/placeholder?text={urllib.parse.quote(str(title))}&type=poster"
    if path.startswith("http"):
        return path.replace("image.tmdb.org/t5/p/", "media.themoviedb.org/t/p/")
    return f"https://media.themoviedb.org/t/p/w500{path}"

def format_fanart(path, title="Palantir"):
    if not path:
        return f"/api/placeholder?text={urllib.parse.quote(str(title))}&type=fanart"
    if path.startswith("http"):
        return path.replace("image.tmdb.org/t5/p/", "media.themoviedb.org/t/p/")
    return f"https://media.themoviedb.org/t/p/original{path}"

from fastapi.responses import Response

@app.get("/api/placeholder")
def get_placeholder(text: str = "Palantir", type: str = "poster"):
    width = 300 if type == "poster" else 1280
    height = 450 if type == "poster" else 720
    
    title_escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
        <defs>
            <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#141824"/>
                <stop offset="50%" stop-color="#1e293b"/>
                <stop offset="100%" stop-color="#0f172a"/>
            </linearGradient>
            <radialGradient id="glow" cx="50%" cy="30%" r="50%">
                <stop offset="0%" stop-color="#6366f1" stop-opacity="0.3"/>
                <stop offset="100%" stop-color="#6366f1" stop-opacity="0"/>
            </radialGradient>
        </defs>
        <rect width="100%" height="100%" fill="url(#bg)"/>
        <rect width="100%" height="100%" fill="url(#glow)"/>
        <g transform="translate({width/2 - 24}, {height/2 - 40})" fill="none" stroke="#6366f1" stroke-width="2">
            <rect x="2" y="2" width="44" height="44" rx="6" stroke="#818cf8" stroke-width="2"/>
            <path d="M18 15v18l14-9z" fill="#6366f1"/>
        </g>
        <text x="50%" y="{height/2 + 30}" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#f8fafc" text-anchor="middle">{title_escaped}</text>
        <text x="50%" y="{height/2 + 55}" font-family="system-ui, sans-serif" font-size="11" fill="#64748b" text-anchor="middle">PALANTIR DELUXE</text>
    </svg>'''
    return Response(content=svg, media_type="image/svg+xml")


@app.get("/api/categories")
def get_categories():
    return [
        {"id": "pelis", "title": "Películas", "icon": "film"},
        {"id": "series", "title": "Series de TV", "icon": "tv"},
        {"id": "colecciones", "title": "Sagas y Colecciones", "icon": "library"},
        {"id": "search", "title": "Buscador Global", "icon": "search"}
    ]

@app.get("/api/movies")
def get_movies(
    page: int = 1,
    limit: int = 36,
    query: str = None,
    genre: str = None,
    order_by: str = "recent"
):
    conn = get_db_connection()
    cursor = conn.cursor()
    offset = (page - 1) * limit
    
    where_clauses = []
    params = []
    
    if query and query.strip():
        where_clauses.append("titulo LIKE ?")
        params.append(f"%{query.strip()}%")
        
    if genre and genre.strip():
        where_clauses.append("genero LIKE ?")
        params.append(f"%{genre.strip()}%")
        
    where_sql = (" WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
    
    order_sql = " ORDER BY tmdb DESC"
    if order_by == "title":
        order_sql = " ORDER BY titulo ASC"
    elif order_by == "recent":
        order_sql = " ORDER BY tmdb DESC"
        
    count_query = f"SELECT COUNT(*) FROM pelis{where_sql}"
    cursor.execute(count_query, params)
    total_count = cursor.fetchone()[0]
    
    query_sql = f"""
        SELECT tmdb, titulo, plot, poster, fondo, fecha, rating, duration
        FROM pelis
        {where_sql}
        {order_sql}
        LIMIT ? OFFSET ?
    """
    params.extend([limit, offset])
    cursor.execute(query_sql, params)
    rows = cursor.fetchall()
    
    items = []
    for r in rows:
        items.append({
            "tmdb": r["tmdb"],
            "title": r["titulo"],
            "plot": r["plot"] or "",
            "poster": format_poster(r["poster"], r["titulo"]),
            "fanart": format_fanart(r["fondo"], r["titulo"]),
            "year": r["fecha"][:4] if r["fecha"] else "",
            "quality": "HD 1080p",
            "rating": r["rating"] or "",
            "duration": r["duration"] or "",
            "type": "movie"
        })
        
    conn.close()
    return {
        "page": page,
        "limit": limit,
        "total": total_count,
        "pages": (total_count + limit - 1) // limit,
        "items": items
    }

@app.get("/api/movie/{tmdb_id}")
def get_movie_details(tmdb_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM pelis WHERE tmdb = ?", (tmdb_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")
        
    movie = {
        "tmdb": row["tmdb"],
        "title": row["titulo"],
        "plot": row["plot"] or "",
        "poster": format_poster(row["poster"], row["titulo"]),
        "fanart": format_fanart(row["fondo"], row["titulo"]),
        "year": row["fecha"][:4] if row["fecha"] else "",
        "quality": "HD 1080p",
        "rating": row["rating"] or "",
        "duration": row["duration"] or "",
        "genre": row["genero"] if "genero" in row.keys() else "",
        "type": "movie"
    }
    
    cursor.execute("""
        SELECT link, calidad, audio, info, updated
        FROM enlaces_pelis
        WHERE tmdb = ?
    """, (tmdb_id,))
    links = []
    for l in cursor.fetchall():
        links.append({
            "link": l["link"],
            "quality": l["calidad"] or "HD",
            "audio": l["audio"] or "Español",
            "info": l["info"] or "",
            "updated": l["updated"] or ""
        })

    def audio_sort_key(item):
        aud = (item.get("audio") or "").lower()
        if aud == "esp" or aud.startswith("esp,") or aud.startswith("spa"):
            return 0
        elif "esp" in aud or "spa" in aud:
            return 1
        elif "lat" in aud:
            return 2
        else:
            return 3

    links.sort(key=audio_sort_key)
        
    conn.close()
    movie["links"] = links
    return movie

@app.get("/api/series")
def get_series(
    page: int = 1,
    limit: int = 36,
    query: str = None,
    genre: str = None
):
    conn = get_db_connection()
    cursor = conn.cursor()
    offset = (page - 1) * limit
    
    where_clauses = []
    params = []
    
    if query and query.strip():
        where_clauses.append("titulo LIKE ?")
        params.append(f"%{query.strip()}%")
        
    if genre and genre.strip():
        where_clauses.append("genero LIKE ?")
        params.append(f"%{genre.strip()}%")
        
    where_sql = (" WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
    
    count_query = f"SELECT COUNT(*) FROM series{where_sql}"
    cursor.execute(count_query, params)
    total_count = cursor.fetchone()[0]
    
    query_sql = f"""
        SELECT tmdb, titulo, plot, poster, fondo, fecha, rating
        FROM series
        {where_sql}
        ORDER BY tmdb DESC
        LIMIT ? OFFSET ?
    """
    params.extend([limit, offset])
    cursor.execute(query_sql, params)
    rows = cursor.fetchall()
    
    items = []
    for r in rows:
        items.append({
            "tmdb": r["tmdb"],
            "title": r["titulo"],
            "plot": r["plot"] or "",
            "poster": format_poster(r["poster"], r["titulo"]),
            "fanart": format_fanart(r["fondo"], r["titulo"]),
            "year": r["fecha"][:4] if r["fecha"] else "",
            "rating": r["rating"] or "",
            "type": "series"
        })
        
    conn.close()
    return {
        "page": page,
        "limit": limit,
        "total": total_count,
        "pages": (total_count + limit - 1) // limit,
        "items": items
    }

@app.get("/api/series/{tmdb_id}")
def get_series_details(tmdb_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM series WHERE tmdb = ?", (tmdb_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Serie no encontrada")
        
    show = {
        "tmdb": row["tmdb"],
        "title": row["titulo"],
        "plot": row["plot"] or "",
        "poster": format_poster(row["poster"], row["titulo"]),
        "fanart": format_fanart(row["fondo"], row["titulo"]),
        "year": row["fecha"][:4] if row["fecha"] else "",
        "rating": row["rating"] or "",
        "genre": row["genero"] if "genero" in row.keys() else ""
    }
    
    cursor.execute("""
        SELECT DISTINCT temporada, episodio, calidad, audio, info, link
        FROM enlaces_series
        WHERE tmdb = ?
        ORDER BY temporada ASC, episodio ASC
    """, (tmdb_id,))
    
    episodes_by_season = {}
    for ep in cursor.fetchall():
        season_num = ep["temporada"]
        if season_num not in episodes_by_season:
            episodes_by_season[season_num] = []
            
        episodes_by_season[season_num].append({
            "episode": ep["episodio"],
            "quality": ep["calidad"] or "HD",
            "audio": ep["audio"] or "Español",
            "info": ep["info"] or "",
            "link": ep["link"]
        })

    def audio_sort_key(item):
        aud = (item.get("audio") or "").lower()
        if aud == "esp" or aud.startswith("esp,") or aud.startswith("spa"):
            return 0
        elif "esp" in aud or "spa" in aud:
            return 1
        elif "lat" in aud:
            return 2
        else:
            return 3

    for s_num in episodes_by_season:
        episodes_by_season[s_num].sort(key=audio_sort_key)
        
    conn.close()
    show["seasons"] = episodes_by_season
    return show

@app.get("/api/collections")
def get_collections(
    page: int = 1,
    limit: int = 36,
    query: str = None
):
    conn = get_db_connection()
    cursor = conn.cursor()
    offset = (page - 1) * limit

    where_clauses = []
    params = []

    if query and query.strip():
        where_clauses.append("titulo LIKE ?")
        params.append(f"%{query.strip()}%")

    where_sql = (" WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    count_query = f"SELECT COUNT(*) FROM colecciones_pelis{where_sql}"
    cursor.execute(count_query, params)
    total_count = cursor.fetchone()[0]

    query_sql = f"""
        SELECT id, titulo, plot, poster, fondo
        FROM colecciones_pelis
        {where_sql}
        ORDER BY titulo ASC
        LIMIT ? OFFSET ?
    """
    params.extend([limit, offset])
    cursor.execute(query_sql, params)
    rows = cursor.fetchall()

    items = []
    for r in rows:
        items.append({
            "id": r["id"],
            "title": r["titulo"],
            "plot": r["plot"] or "",
            "poster": format_poster(r["poster"], r["titulo"]),
            "fanart": format_fanart(r["fondo"], r["titulo"]),
            "type": "collection"
        })

    conn.close()
    return {
        "page": page,
        "limit": limit,
        "total": total_count,
        "pages": (total_count + limit - 1) // limit,
        "items": items
    }

@app.get("/api/top10")
def get_top10():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.tmdb, p.titulo, p.plot, p.poster, p.fondo, p.fecha, p.rating, COUNT(l.link) as num_links
        FROM pelis p
        JOIN enlaces_pelis l ON p.tmdb = l.tmdb
        WHERE p.poster IS NOT NULL AND p.poster != ''
        GROUP BY p.tmdb
        ORDER BY num_links DESC, p.fecha DESC
        LIMIT 10
    """)
    top_movies = []
    for idx, r in enumerate(cursor.fetchall(), start=1):
        top_movies.append({
            "rank": idx,
            "tmdb": r["tmdb"],
            "title": r["titulo"],
            "plot": r["plot"] or "",
            "poster": format_poster(r["poster"], r["titulo"]),
            "fanart": format_fanart(r["fondo"], r["titulo"]),
            "year": r["fecha"][:4] if r["fecha"] else "",
            "rating": r["rating"] or "",
            "type": "movie"
        })

    cursor.execute("""
        SELECT s.tmdb, s.titulo, s.plot, s.poster, s.fondo, s.fecha, s.rating, COUNT(l.link) as num_links
        FROM series s
        JOIN enlaces_series l ON s.tmdb = l.tmdb
        WHERE s.poster IS NOT NULL AND s.poster != ''
        GROUP BY s.tmdb
        ORDER BY num_links DESC, s.fecha DESC
        LIMIT 10
    """)
    top_series = []
    for idx, r in enumerate(cursor.fetchall(), start=1):
        top_series.append({
            "rank": idx,
            "tmdb": r["tmdb"],
            "title": r["titulo"],
            "plot": r["plot"] or "",
            "poster": format_poster(r["poster"], r["titulo"]),
            "fanart": format_fanart(r["fondo"], r["titulo"]),
            "year": r["fecha"][:4] if r["fecha"] else "",
            "rating": r["rating"] or "",
            "type": "series"
        })

    conn.close()
    return {
        "movies": top_movies,
        "series": top_series
    }

@app.get("/api/novedades")
def get_novedades(
    page: int = 1,
    limit: int = 36,
    filter_type: str = "all",
    query: str = None
):
    conn = get_db_connection()
    cursor = conn.cursor()
    offset = (page - 1) * limit

    if filter_type == "pelis":
        where_clauses = ["fecha IS NOT NULL AND fecha != ''"]
        params = []
        if query and query.strip():
            where_clauses.append("titulo LIKE ?")
            params.append(f"%{query.strip()}%")
        where_sql = " WHERE " + " AND ".join(where_clauses)

        cursor.execute(f"SELECT COUNT(*) FROM pelis{where_sql}", params)
        total_count = cursor.fetchone()[0]

        cursor.execute(f"""
            SELECT tmdb, titulo, plot, poster, fondo, fecha, rating, duration
            FROM pelis{where_sql}
            ORDER BY fecha DESC, updated DESC, tmdb DESC
            LIMIT ? OFFSET ?
        """, params + [limit, offset])

        items = []
        for r in cursor.fetchall():
            items.append({
                "tmdb": r["tmdb"],
                "title": r["titulo"],
                "plot": r["plot"] or "",
                "poster": format_poster(r["poster"], r["titulo"]),
                "fanart": format_fanart(r["fondo"], r["titulo"]),
                "year": r["fecha"][:4] if r["fecha"] else "",
                "fecha": r["fecha"] or "",
                "rating": r["rating"] or "",
                "type": "movie"
            })
    elif filter_type == "series":
        where_clauses = ["fecha IS NOT NULL AND fecha != ''"]
        params = []
        if query and query.strip():
            where_clauses.append("titulo LIKE ?")
            params.append(f"%{query.strip()}%")
        where_sql = " WHERE " + " AND ".join(where_clauses)

        cursor.execute(f"SELECT COUNT(*) FROM series{where_sql}", params)
        total_count = cursor.fetchone()[0]

        cursor.execute(f"""
            SELECT tmdb, titulo, plot, poster, fondo, fecha, rating
            FROM series{where_sql}
            ORDER BY fecha DESC, updated DESC, tmdb DESC
            LIMIT ? OFFSET ?
        """, params + [limit, offset])

        items = []
        for r in cursor.fetchall():
            items.append({
                "tmdb": r["tmdb"],
                "title": r["titulo"],
                "plot": r["plot"] or "",
                "poster": format_poster(r["poster"], r["titulo"]),
                "fanart": format_fanart(r["fondo"], r["titulo"]),
                "year": r["fecha"][:4] if r["fecha"] else "",
                "fecha": r["fecha"] or "",
                "rating": r["rating"] or "",
                "type": "series"
            })
    else:
        where_p = ["fecha IS NOT NULL AND fecha != ''"]
        where_s = ["fecha IS NOT NULL AND fecha != ''"]
        params_p = []
        params_s = []

        if query and query.strip():
            where_p.append("titulo LIKE ?")
            where_s.append("titulo LIKE ?")
            params_p.append(f"%{query.strip()}%")
            params_s.append(f"%{query.strip()}%")

        where_sql_p = " WHERE " + " AND ".join(where_p)
        where_sql_s = " WHERE " + " AND ".join(where_s)

        cursor.execute(f"""
            SELECT COUNT(*) FROM (
                SELECT tmdb FROM pelis{where_sql_p}
                UNION ALL
                SELECT tmdb FROM series{where_sql_s}
            )
        """, params_p + params_s)
        total_count = cursor.fetchone()[0]

        union_sql = f"""
            SELECT tmdb, titulo, plot, poster, fondo, fecha, rating, 'movie' as type
            FROM pelis{where_sql_p}
            UNION ALL
            SELECT tmdb, titulo, plot, poster, fondo, fecha, rating, 'series' as type
            FROM series{where_sql_s}
            ORDER BY fecha DESC, tmdb DESC
            LIMIT ? OFFSET ?
        """
        cursor.execute(union_sql, params_p + params_s + [limit, offset])

        items = []
        for r in cursor.fetchall():
            items.append({
                "tmdb": r["tmdb"],
                "title": r["titulo"],
                "plot": r["plot"] or "",
                "poster": format_poster(r["poster"], r["titulo"]),
                "fanart": format_fanart(r["fondo"], r["titulo"]),
                "year": r["fecha"][:4] if r["fecha"] else "",
                "fecha": r["fecha"] or "",
                "rating": r["rating"] or "",
                "type": r["type"]
            })

    conn.close()
    return {
        "page": page,
        "limit": limit,
        "total": total_count,
        "pages": (total_count + limit - 1) // limit,
        "items": items
    }

import hashlib
import secrets

APP_USERNAME = os.environ.get("APP_USERNAME", "yinfu1984")
APP_PASSWORD = os.environ.get("APP_PASSWORD", "Antonioo1838*")
AUTH_SECRET = "palantir_deluxe_secret_key_2026"

def generate_user_token(username: str) -> str:
    return hashlib.sha256(f"{username}:{AUTH_SECRET}".encode('utf-8')).hexdigest()

from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class AllDebridSaveRequest(BaseModel):
    enabled: bool = True
    apikey: str = ""

class AllDebridCheckPinRequest(BaseModel):
    pin: str
    check: str

@app.post("/api/auth/login")
def login(req: LoginRequest):
    user_clean = req.username.strip()
    pass_clean = req.password.strip()
    
    if user_clean == APP_USERNAME and pass_clean == APP_PASSWORD:
        token = generate_user_token(user_clean)
        return {
            "status": "success",
            "message": "Sesión iniciada correctamente",
            "token": token,
            "username": user_clean
        }
    else:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

@app.get("/api/auth/check")
def check_auth(token: str = Query(None)):
    expected_token = generate_user_token(APP_USERNAME)
    if token and token == expected_token:
        return {"authenticated": True, "username": APP_USERNAME}
    return {"authenticated": False}

@app.post("/api/auth/logout")
def logout():
    return {"status": "success", "message": "Sesión cerrada"}

@app.get("/api/settings/alldebrid")
def get_alldebrid_settings():
    st = kodi_shim.load_addon_settings()
    apikey = st.get("Alldebrid_apikey", "") or os.environ.get("ALLDEBRID_APIKEY", "")
    enabled = str(st.get("Alldebrid_enabled", "false")).lower() in ["true", "1", "yes"] or bool(os.environ.get("ALLDEBRID_APIKEY"))
    masked = (apikey[:4] + "..." + apikey[-4:]) if len(apikey) >= 8 else ("***" if apikey else "")
    return {
        "enabled": enabled,
        "has_key": bool(apikey),
        "apikey_masked": masked
    }

@app.post("/api/settings/alldebrid")
def save_alldebrid_settings(req: AllDebridSaveRequest):
    st = kodi_shim.load_addon_settings()
    key_to_save = (req.apikey or "").strip()
    
    if key_to_save:
        val_url = f"https://api.alldebrid.com/v4/user?agent=Palantir&apikey={urllib.parse.quote(key_to_save)}"
        try:
            val_req = urllib.request.Request(val_url, headers={'User-Agent': 'Palantir/3.0'})
            with urllib.request.urlopen(val_req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if data.get("status") != "success":
                    err_msg = data.get("error", {}).get("message", "API Key no válida en AllDebrid")
                    raise HTTPException(status_code=400, detail=f"API Key no válida: {err_msg}")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al validar API Key con AllDebrid: {str(e)}")

        st["Alldebrid_apikey"] = key_to_save
        st["Alldebrid_enabled"] = req.enabled
    else:
        st["Alldebrid_enabled"] = req.enabled
        if not req.enabled:
            st["Alldebrid_apikey"] = ""

    kodi_shim.save_addon_settings(st)
    return {"status": "success", "message": "Configuración de AllDebrid guardada correctamente"}

@app.delete("/api/settings/alldebrid")
def delete_alldebrid_settings():
    st = kodi_shim.load_addon_settings()
    st["Alldebrid_enabled"] = False
    st["Alldebrid_apikey"] = ""
    kodi_shim.save_addon_settings(st)
    return {"status": "success", "message": "Cuenta de AllDebrid desconectada"}

@app.post("/api/alldebrid/pin/start")
def start_alldebrid_pin():
    url = "https://api.alldebrid.com/v4/pin/get?agent=Palantir"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Palantir/3.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get("status") == "success":
                return data.get("data")
            else:
                raise HTTPException(status_code=400, detail=data.get("error", {}).get("message", "Error al obtener PIN"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error conectando con AllDebrid: {str(e)}")

@app.post("/api/alldebrid/pin/check")
def check_alldebrid_pin(req_data: AllDebridCheckPinRequest):
    check_enc = urllib.parse.quote(req_data.check)
    pin_enc = urllib.parse.quote(req_data.pin)
    url = f"https://api.alldebrid.com/v4/pin/check?agent=Palantir&check={check_enc}&pin={pin_enc}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Palantir/3.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get("status") == "success":
                pin_data = data.get("data", {})
                apikey = pin_data.get("apikey")
                if apikey:
                    st = kodi_shim.load_addon_settings()
                    st["Alldebrid_enabled"] = True
                    st["Alldebrid_apikey"] = apikey
                    kodi_shim.save_addon_settings(st)
                    return {"status": "success", "apikey": apikey, "activated": True}
                return {"status": "pending", "activated": False}
            else:
                return {"status": "error", "message": data.get("error", {}).get("message", "PIN no válido o expirado")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comprobando PIN: {str(e)}")

@app.get("/api/alldebrid/user")
def get_alldebrid_user_info(apikey: str = Query(None)):
    if not apikey or apikey.lower() in ["null", "undefined"]:
        st = kodi_shim.load_addon_settings()
        apikey = st.get("Alldebrid_apikey", "") or os.environ.get("ALLDEBRID_APIKEY", "")
    if not apikey:
        raise HTTPException(status_code=400, detail="No hay API Key guardada de AllDebrid")
    
    url = f"https://api.alldebrid.com/v4/user?agent=Palantir&apikey={urllib.parse.quote(apikey)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Palantir/3.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get("status") == "success":
                user_data = data.get("data", {}).get("user", {})
                return {
                    "status": "success",
                    "username": user_data.get("username"),
                    "isPremium": user_data.get("isPremium"),
                    "premiumUntil": user_data.get("premiumUntil"),
                    "email": user_data.get("email")
                }
            else:
                raise HTTPException(status_code=400, detail=data.get("error", {}).get("message", "API Key no válida"))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando usuario en AllDebrid: {str(e)}")

def unlock_with_alldebrid(target_url: str, apikey: str):
    try:
        encoded_link = urllib.parse.quote(target_url, safe='')
        req_url = f"https://api.alldebrid.com/v4/link/unlock?agent=Palantir&apikey={apikey}&link={encoded_link}"
        req = urllib.request.Request(req_url, headers={'User-Agent': 'Palantir/3.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            if res.get("status") == "success":
                data_obj = res.get("data", {})
                dl = data_obj.get("link") or data_obj.get("download")
                print(f"[ALLDEBRID UNLOCK SUCCESS] {target_url} -> {dl}")
                return dl
            else:
                print(f"[ALLDEBRID UNLOCK FAIL] {res}")
    except Exception as e:
        print(f"[ALLDEBRID UNLOCK ERROR] {e}")
    return None

@app.get("/api/resolve")
def resolve_stream(link: str):
    if not link:
        raise HTTPException(status_code=400, detail="Missing link parameter")
        
    try:
        resolver = resolver_mod.Resolver({"link": link, "url": link})
        resolved_url = getattr(resolver, "url", None)
        if not resolved_url:
            resolved_url = resolver.resolve_url()
            
        st = kodi_shim.load_addon_settings()
        apikey = st.get("Alldebrid_apikey", "") or os.environ.get("ALLDEBRID_APIKEY", "")
        enabled = str(st.get("Alldebrid_enabled", "false")).lower() in ["true", "1", "yes"] or bool(apikey)
        
        debrid_unlocked_flag = False
        if enabled and apikey and resolved_url:
            unlocked = unlock_with_alldebrid(resolved_url, apikey)
            if unlocked:
                print(f"[ALLDEBRID] Unlocked stream successfully: {unlocked}")
                resolved_url = unlocked
                debrid_unlocked_flag = True
            
        return {
            "link": link,
            "stream_url": resolved_url,
            "label": getattr(resolver, "enlace_label", "Palantir Stream"),
            "debrid_unlocked": debrid_unlocked_flag
        }
    except Exception as e:
        print(f"[RESOLVE ERROR] {e}")
        raise HTTPException(status_code=500, detail=f"Error resolviendo enlace: {str(e)}")

import subprocess

class PlayVlcRequest(BaseModel):
    link: str = ""
    stream_url: str = ""

@app.post("/api/play/vlc")
def play_in_vlc(req: PlayVlcRequest):
    target_url = req.stream_url
    unlocked = False
    if not target_url and req.link:
        res = resolve_stream(req.link)
        target_url = res.get("stream_url")
        unlocked = res.get("debrid_unlocked", False)
        
    if not target_url:
        raise HTTPException(status_code=400, detail="No se pudo obtener la URL de streaming para VLC")
        
    vlc_paths = [
        r"C:\Program Files\VideoLAN\VLC\vlc.exe",
        r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",
        "vlc"
    ]
    
    launched = False
    for p in vlc_paths:
        if os.path.exists(p) or p == "vlc":
            try:
                subprocess.Popen([p, target_url])
                launched = True
                print(f"[VLC LAUNCH SUCCESS] {p} -> {target_url}")
                break
            except Exception as e:
                print(f"[VLC LAUNCH ERROR] {p}: {e}")
                
    if not launched:
        try:
            os.system(f'start vlc "{target_url}"')
            launched = True
        except Exception:
            pass
            
    if launched:
        return {
            "status": "success",
            "stream_url": target_url,
            "debrid_unlocked": unlocked,
            "message": "VLC iniciado correctamente"
        }
    else:
        raise HTTPException(status_code=500, detail="No se encontró ejecutable de VLC en el sistema")

import shutil

@app.get("/api/transcode")
def transcode_stream(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="Missing url parameter")

    target_url = urllib.parse.unquote(url)
    while "%" in target_url:
        target_url = urllib.parse.unquote(target_url)
        
    target_url = urllib.parse.quote(target_url, safe=':/?&=#')
    print(f"[TRANSCODE TARGET URL FIXED] {target_url}")

    ffmpeg_paths = [
        "ffmpeg",
        r"C:\Program Files\DownloadHelper CoApp\ffmpeg.exe"
    ]
    ffmpeg_bin = None
    for p in ffmpeg_paths:
        if shutil.which(p) or os.path.exists(p):
            ffmpeg_bin = p
            break
    if not ffmpeg_bin:
        ffmpeg_bin = "ffmpeg"

    cmd = [
        ffmpeg_bin,
        "-headers", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n",
        "-analyzeduration", "5000000",
        "-probesize", "5000000",
        "-i", target_url,
        "-c:v", "copy",
        "-c:a", "aac",
        "-ac", "2",
        "-b:a", "192k",
        "-movflags", "frag_keyframe+empty_moov+default_base_moof",
        "-f", "mp4",
        "pipe:1"
    ]

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            bufsize=1024 * 1024
        )

        def iterfile():
            try:
                while True:
                    data = proc.stdout.read(64 * 1024)
                    if not data:
                        break
                    yield data
            finally:
                proc.kill()

        return StreamingResponse(
            iterfile(),
            media_type="video/mp4",
            headers={
                "Accept-Ranges": "bytes",
                "Content-Type": "video/mp4"
            }
        )
    except Exception as e:
        import traceback
        print(f"[TRANSCODE ERROR] {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error transcodificando audio: {str(e)}")

public_dir = os.path.abspath("public")
os.makedirs(public_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=public_dir), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(public_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Palantir Deluxe API is running!"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
