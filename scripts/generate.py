import json, os, re, sys, datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "templates"))
from icons import ICONS
from jinja2 import Environment, FileSystemLoader

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATES = os.path.join(ROOT, "templates")
DATA = os.path.join(ROOT, "data", "estudios.json")
SITE_URL = "https://www.pilatesmediterraneo.com"

env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=False)

with open(DATA, encoding="utf-8") as f:
    studios = json.load(f)

def resenas_num(s):
    if not s.get("resenas"):
        return None
    m = re.search(r"\d+", str(s["resenas"]))
    return int(m.group()) if m else None

for s in studios:
    s["resenas_num"] = resenas_num(s)

municipios = sorted(set(s["municipio"] for s in studios))

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

year = datetime.date.today().year

# Links de barrios de Valencia (para nav chips)
BARRIO_LINKS = [
    {"nombre": "Eixample / Ensanche", "slug": "eixample-valencia"},
    {"nombre": "Ruzafa",              "slug": "ruzafa-valencia"},
    {"nombre": "Ciutat Vella",        "slug": "ciutat-vella-valencia"},
    {"nombre": "Patraix",             "slug": "patraix-valencia"},
    {"nombre": "Extramurs",           "slug": "extramurs-valencia"},
]

# FAQs para la pagina de inicio
INDEX_FAQS = [
    {"q": "¿Cuántos estudios de pilates hay en Valencia?", "a": "El directorio recoge 38 estudios de pilates en Valencia ciudad y el área metropolitana, incluyendo municipios como Paterna, Torrent, L'Eliana y Aldaia."},
    {"q": "¿Cuánto cuesta el pilates en Valencia?", "a": "Las clases sueltas van de 10€ a 49€ por sesión. Las mensualidades para 2 sesiones semanales cuestan entre 78€ y 155€ según el estudio y la modalidad (reformer o suelo)."},
    {"q": "¿Qué diferencia hay entre el pilates reformer y el pilates de suelo?", "a": "El pilates reformer usa una máquina con muelles que permite ajustar la resistencia y trabaja en múltiples planos de movimiento. El pilates de suelo (mat) usa solo el peso corporal. El reformer suele costar entre un 30% y un 60% más que el suelo."},
    {"q": "¿Hay estudios de pilates con fisioterapia en Valencia?", "a": "Sí, varios centros del directorio combinan pilates con fisioterapia clínica. Son ideales para rehabilitación, lesiones, dolor crónico o suelo pélvico. Podés filtrarlos en la sección de pilates con fisioterapia."},
    {"q": "¿Puedo hacer pilates si soy principiante?", "a": "Sí. La mayoría de los estudios del directorio ofrecen clases para todos los niveles, incluyendo principiantes absolutos. Muchos centros realizan una evaluación inicial para adaptar los ejercicios a tu nivel y necesidades."},
]

# Index
tpl = env.get_template("index.html")
html = tpl.render(
    title="Clases de Pilates en Valencia · 38 Estudios con Precios y Horarios",
    description="Compara 38 estudios de clases de pilates en Valencia: reformer, mat, suelo y fisioterapia. Precios, horarios y valoraciones actualizados. Valencia ciudad, Paterna, Torrent y L'Eliana.",
    canonical=f"{SITE_URL}/",
    root="", active="home", icons=ICONS, studios=studios, municipios=municipios,
    year=year, index_faqs=INDEX_FAQS, barrio_links=BARRIO_LINKS,
    en_url="../en/index.html",
)
write("index.html", html)

# Fichas de estudio
tpl = env.get_template("estudio.html")
for s in studios:
    desc_bits = [s["equipamiento_label"]]
    if s["fisioterapia"]: desc_bits.append("fisioterapia")
    if s["zona"]: desc_bits.append(f"en {s['zona']}, {s['municipio']}")
    else: desc_bits.append(f"en {s['municipio']}")
    description = f"{s['nombre']}: pilates {', '.join(desc_bits)}. Precios, horarios, niveles y contacto."
    html = tpl.render(
        title=f"{s['nombre']} | Pilates en {s['municipio']} - Directorio Pilates Valencia",
        description=description, canonical=f"{SITE_URL}/estudios/{s['slug']}.html",
        root="../", active="estudio", icons=ICONS, s=s, year=year,
        en_url="",
    )
    write(f"estudios/{s['slug']}.html", html)

# Paginas de zona (municipios)
zona_config = [
    ("Valencia",  "valencia",   "Mas de 30 estudios de pilates en Valencia ciudad: reformer, mat, fisioterapia y clases en ingles. Busca por barrio — Eixample, Ruzafa, Extramurs, Ciutat Vella, Patraix y mas.", "Valencia ciudad tiene la mayor concentracion de estudios de pilates de la Comunitat Valenciana: mas de 30 centros distribuidos por barrios. El Eixample y Ensanche concentran los estudios boutique de reformer. Ruzafa combina grupos reducidos con precios mas accesibles. Extramurs y Ciutat Vella tienen buena oferta de pilates con fisioterapia clinica. Patraix destaca por pilates terapeutico y suelo pelvico. Muchos centros ofrecen clases en ingles, ideal para expatriados y turistas de larga estancia.",
     [
        {"q": "¿Cuántos estudios de pilates hay en Valencia ciudad?", "a": "El directorio recoge más de 30 estudios de pilates en Valencia ciudad, distribuidos por barrios como Eixample, Ensanche, Ruzafa, Ciutat Vella, Patraix y Extramurs. Es la ciudad con mayor oferta de pilates de la Comunitat Valenciana."},
        {"q": "¿Qué barrios de Valencia tienen más estudios de pilates?", "a": "El Eixample-Ensanche concentra la mayor oferta de estudios boutique de reformer. Ruzafa tiene opciones más accesibles. Ciutat Vella y Extramurs destacan por pilates con fisioterapia. Patraix es el barrio de referencia para pilates terapéutico y suelo pélvico."},
        {"q": "¿Cuánto cuesta el pilates en Valencia ciudad?", "a": "Las clases sueltas van de 10€ a 49€ por sesión. Las mensualidades para 2 sesiones semanales están entre 78€ y 155€ según el estudio y modalidad. El reformer es entre un 30 y 60% más caro que el mat por el equipamiento y el tamaño reducido de los grupos."},
        {"q": "¿Hay pilates en inglés en Valencia?", "a": "Sí, varios estudios del directorio ofrecen clases en inglés, especialmente en el Eixample, Ruzafa y Extramurs. Es una opción muy buscada por expatriados y turistas de larga estancia en Valencia."},
        {"q": "¿Dónde hacer pilates reformer en Valencia ciudad?", "a": "Los estudios de reformer están concentrados sobre todo en el Eixample-Ensanche, Extramurs y Ruzafa. Podés filtrar por equipamiento en el directorio para ver solo los centros con reformer en Valencia ciudad."},
    ]),
    ("Paterna",   "paterna",    "Estudios de pilates en Paterna: compara precios, equipamiento y servicios de los centros disponibles en el municipio.", "Paterna es uno de los municipios del area metropolitana de Valencia con oferta creciente de pilates. Los estudios suelen ofrecer grupos reducidos y atencion personalizada con precios competitivos.",
     [
        {"q": "¿Cuántos estudios de pilates hay en Paterna?", "a": "El directorio recoge varios estudios de pilates en Paterna, con grupos reducidos, atención personalizada y precios competitivos respecto a la ciudad."},
        {"q": "¿Es más barato el pilates en Paterna?", "a": "En general sí, los estudios de Paterna ofrecen precios más competitivos que los centros del centro de Valencia, con una calidad de servicio similar."},
    ]),
    ("Torrent",   "torrent",    "Estudios de pilates en Torrent: encuentra centros cerca de ti con informacion de precios, horarios y tipo de clases.", "Torrent, el municipio mas poblado del area metropolitana sur de Valencia, cuenta con estudios de pilates para todos los niveles. Una buena alternativa a desplazarse a la ciudad.",
     [
        {"q": "¿Dónde hacer pilates en Torrent?", "a": "Torrent, el municipio más poblado del área metropolitana sur de Valencia, cuenta con estudios de pilates para todos los niveles, sin necesidad de desplazarse a Valencia ciudad."},
    ]),
    ("L'Eliana",  "l-eliana",   "Estudios de pilates en L'Eliana: compara los centros disponibles en este municipio del area metropolitana norte de Valencia.", "L'Eliana es un municipio residencial del area metropolitana norte de Valencia con oferta de pilates en crecimiento, desde clases de suelo hasta pilates con maquinas.",
     [
        {"q": "¿Hay pilates en L'Eliana?", "a": "Sí, L'Eliana cuenta con estudios de pilates en crecimiento, con clases de suelo y máquinas para todos los niveles, como alternativa a desplazarse a Valencia."},
    ]),
    ("Aldaia",    "aldaia",     "Estudios de pilates en Aldaia: encuentra opciones de calidad cerca de ti sin ir hasta Valencia ciudad.", "Aldaia, en el area metropolitana oeste de Valencia, dispone de centros de pilates con clases personalizadas y servicios complementarios como entrenamiento personal.",
     [
        {"q": "¿Dónde hacer pilates en Aldaia?", "a": "Aldaia dispone de centros de pilates con clases personalizadas y servicios complementarios, como alternativa a desplazarse a Valencia ciudad."},
    ]),
]

tpl_zona = env.get_template("zona.html")
zonas_generadas = 0
for municipio, slug, desc_larga, texto_info, faqs in zona_config:
    studios_zona = [s for s in studios if s["municipio"] == municipio]
    if not studios_zona:
        continue
    n = len(studios_zona)
    html = tpl_zona.render(
        title=f"Pilates en {municipio} | Estudios, Precios y Horarios",
        description=desc_larga,
        canonical=f"{SITE_URL}/zona/{slug}.html",
        root="../", active="zona", icons=ICONS,
        municipio=municipio, studios=studios_zona,
        descripcion_larga=desc_larga, texto_informativo=texto_info,
        faqs=faqs, year=year,
        barrio_links=BARRIO_LINKS if municipio == "Valencia" else [],
        en_url=f"../../en/zona/{slug}.html",
    )
    write(f"zona/{slug}.html", html)
    zonas_generadas += 1

# Paginas de barrio (Valencia ciudad)
barrio_config = [
    {
        "barrio": "el Eixample",
        "slug": "eixample-valencia",
        "filtro": lambda s: s["municipio"] == "Valencia" and any(
            k in (s.get("zona") or "") for k in ["Eixample", "eixample", "Ensanche", "L'Eixample"]
        ),
        "desc_larga": "Guia de los estudios de pilates en el Eixample y Ensanche de Valencia. La zona con mayor concentracion de centros boutique, reformer y pilates terapeutico de la ciudad.",
        "texto_info": "El Eixample y el Ensanche de Valencia concentran la mayor densidad de estudios de pilates de la ciudad. Encontraras desde estudios boutique especializados en reformer hasta centros que combinan pilates con fisioterapia clinica. Es la zona de referencia para pilates de alta calidad en Valencia.",
        "faqs": [
            {"q": "¿Cuántos estudios de pilates hay en el Eixample de Valencia?", "a": "El directorio recoge más de 10 estudios de pilates en el Eixample y Ensanche de Valencia, incluyendo centros boutique de reformer, estudios con fisioterapia y centros con máquinas completas."},
            {"q": "¿Cuánto cuesta el pilates en el Eixample?", "a": "Los estudios del Eixample y Ensanche tienen precios variados: desde clases de grupo a 15-20€ hasta clases privadas por encima de 40€. Las mensualidades van de 90€ a 155€ para 2 sesiones semanales."},
            {"q": "¿Hay pilates con fisioterapia en el Eixample de Valencia?", "a": "Sí, varios estudios del Eixample y Ensanche combinan pilates con fisioterapia clínica, ideal para rehabilitación o pilates terapéutico supervisado."},
        ],
    },
    {
        "barrio": "Ruzafa",
        "slug": "ruzafa-valencia",
        "filtro": lambda s: s["municipio"] == "Valencia" and "Ruzafa" in (s.get("zona") or ""),
        "desc_larga": "Estudios de pilates en Ruzafa, Valencia. Clases de reformer y mat en uno de los barrios mas activos y con mas personalidad de la ciudad.",
        "texto_info": "Ruzafa es uno de los barrios con mas personalidad de Valencia, y su oferta de pilates refleja esa identidad: estudios modernos, grupos reducidos y una propuesta de bienestar integrada en el estilo de vida del barrio.",
        "faqs": [
            {"q": "¿Dónde hacer pilates en Ruzafa, Valencia?", "a": "En Ruzafa hay varios estudios de pilates, desde clases de suelo en grupo hasta pilates reformer. Son centros accesibles con precios más competitivos que los estudios boutique del Eixample."},
            {"q": "¿Es caro el pilates en Ruzafa?", "a": "Ruzafa tiene opciones más económicas que el Eixample. Podés encontrar clases de pilates de suelo en grupo a precios muy competitivos y mensualidades accesibles."},
        ],
    },
    {
        "barrio": "Ciutat Vella",
        "slug": "ciutat-vella-valencia",
        "filtro": lambda s: s["municipio"] == "Valencia" and "Ciutat Vella" in (s.get("zona") or ""),
        "desc_larga": "Estudios de pilates en Ciutat Vella, el centro historico de Valencia. Compara los mejores centros del barrio con precios, equipamiento y servicios.",
        "texto_info": "Ciutat Vella, el casco historico de Valencia, cuenta con varios estudios de pilates que combinan una ubicacion central con una oferta variada: reformer, pilates clinico con fisioterapia y clases de diferentes niveles.",
        "faqs": [
            {"q": "¿Dónde hacer pilates en el centro histórico de Valencia?", "a": "En Ciutat Vella hay varios estudios de pilates con reformer y fisioterapia, bien comunicados y accesibles, ideales si trabajás o vivís en el centro histórico de Valencia."},
            {"q": "¿Hay pilates con fisioterapia en Ciutat Vella?", "a": "Sí, algunos centros de Ciutat Vella combinan pilates con fisioterapia clínica, convirtiéndolos en una buena opción para pilates terapéutico o rehabilitación en el centro de Valencia."},
        ],
    },
    {
        "barrio": "Patraix",
        "slug": "patraix-valencia",
        "filtro": lambda s: s["municipio"] == "Valencia" and "Patraix" in (s.get("zona") or ""),
        "desc_larga": "Estudios de pilates en Patraix, Valencia. Centros especializados en pilates terapeutico, suelo pelvico y rehabilitacion en un barrio accesible y bien comunicado.",
        "texto_info": "Patraix concentra una oferta de pilates enfocada en el aspecto clinico y terapeutico, con centros que combinan fisioterapia y pilates en un entorno de barrio cercano y accesible.",
        "faqs": [
            {"q": "¿Qué estudios de pilates hay en Patraix, Valencia?", "a": "Patraix cuenta con varios estudios especializados en pilates terapéutico, suelo pélvico y fisioterapia, además de clases generales para todos los niveles."},
            {"q": "¿Hay pilates para embarazadas en Patraix?", "a": "Sí, algunos estudios de Patraix ofrecen clases específicas para embarazadas y posparto, con profesionales especializados en suelo pélvico y pilates terapéutico."},
        ],
    },
    {
        "barrio": "Extramurs",
        "slug": "extramurs-valencia",
        "filtro": lambda s: s["municipio"] == "Valencia" and "Extramurs" in (s.get("zona") or ""),
        "desc_larga": "Estudios de pilates en Extramurs, Valencia. Un barrio central bien comunicado con oferta de pilates reformer y clases para todos los niveles.",
        "texto_info": "Extramurs es un barrio central de Valencia con buena comunicacion y una oferta de pilates que incluye reformer y diferentes modalidades de clases, con acceso rapido desde el centro y otros barrios.",
        "faqs": [
            {"q": "¿Dónde hacer pilates en Extramurs, Valencia?", "a": "En Extramurs hay estudios de pilates con reformer y clases para todos los niveles, bien ubicados y accesibles desde el centro de Valencia y barrios colindantes."},
        ],
    },
]

barrios_generados = 0
for cfg in barrio_config:
    studios_barrio = [s for s in studios if cfg["filtro"](s)]
    if not studios_barrio:
        continue
    n = len(studios_barrio)
    barrio = cfg["barrio"]
    html = tpl_zona.render(
        title=f"Pilates en {barrio}, Valencia | Estudios y Precios",
        description=f"Guia de estudios de pilates en {barrio} (Valencia): reformer, suelo, fisioterapia. Compara {n} centro{'s' if n!=1 else ''} con precios y horarios.",
        canonical=f"{SITE_URL}/zona/{cfg['slug']}.html",
        root="../", active="zona", icons=ICONS,
        municipio=f"{barrio}, Valencia", studios=studios_barrio,
        descripcion_larga=cfg["desc_larga"], texto_informativo=cfg["texto_info"],
        faqs=cfg["faqs"], year=year,
        en_url=f"../../en/zona/{cfg['slug']}.html",
    )
    write(f"zona/{cfg['slug']}.html", html)
    barrios_generados += 1

# Paginas de tipo
tipo_config = [
    {
        "slug": "reformer",
        "filtro": lambda s: s["equipamiento_tipo"] in ("reformer", "mixto"),
        "h1": "Pilates Reformer en Valencia",
        "h2_info": "Que es el pilates reformer",
        "icono": "⚙️",
        "desc_corta": "Máquina con muelles y poleas para un trabajo preciso, adaptable a cualquier nivel.",
        "desc_larga": "Directorio de estudios de pilates reformer en Valencia y alrededores. Compara precios, ubicaciones y servicios de todos los centros especializados.",
        "texto_info": "El pilates reformer es la modalidad mas buscada en Valencia. A diferencia del pilates de suelo, el reformer utiliza una maquina con muelles y poleas para trabajar resistencia, control y alineacion. Es recomendado para rehabilitacion, embarazo, deportistas y personas con lesiones. Los precios van desde sesiones sueltas hasta mensualidades, con grupos de entre 1 y 6 personas segun el estudio.",
        "que_es": [
            "El pilates reformer usa una máquina especializada compuesta por una cama deslizante, muelles de resistencia graduable, poleas y correas. Este equipo permite trabajar en múltiples planos de movimiento y ajustar la resistencia a cada persona, lo que lo hace ideal tanto para principiantes como para niveles avanzados.",
            "Las clases de reformer suelen ser en grupos pequeños de 2 a 6 personas, con atención personalizada del instructor. La máquina asiste o resiste el movimiento según la configuración, lo que permite un trabajo muy preciso sobre la musculatura profunda.",
            "En Valencia, la mayoría de los estudios boutique están especializados en reformer puro o combinan el reformer con otras máquinas del método Pilates.",
        ],
        "beneficios": [
            "Fortalecimiento profundo del core y la musculatura estabilizadora",
            "Bajo impacto articular, apto para rehabilitación y lesiones",
            "Mejora de la postura y la alineación corporal",
            "Adaptable a cualquier nivel, de principiante a avanzado",
            "Grupos pequeños con mayor atención del instructor",
        ],
        "para_quien": "Personas de cualquier nivel, especialmente indicado para rehabilitación, embarazo, deporte de alto rendimiento o quienes buscan un trabajo técnico y personalizado.",
        "en": True,
        "faqs": [
            {"q": "¿Qué es el pilates reformer?", "a": "El pilates reformer es una modalidad que utiliza una máquina con muelles y poleas que añade resistencia o asistencia a los movimientos, permitiendo un trabajo más preciso y adaptable que el pilates de suelo. Es especialmente efectivo para rehabilitación, control postural y fortalecimiento progresivo."},
            {"q": "¿Para quién es el pilates reformer?", "a": "El reformer es adecuado para cualquier nivel, desde principiantes hasta deportistas. Está especialmente recomendado para personas en rehabilitación, embarazadas, personas con lesiones de espalda o rodilla, y quienes buscan un trabajo más técnico y personalizado."},
            {"q": "¿Cuánto cuesta el pilates reformer en Valencia?", "a": "Las sesiones sueltas de reformer van de 17€ a 49€. Las mensualidades de 2 sesiones por semana están entre 95€ y 155€ según el estudio. El reformer suele costar entre un 30% y un 60% más que el pilates de suelo por el equipamiento y los grupos más reducidos."},
            {"q": "¿Cuántas personas hay por clase de pilates reformer?", "a": "Los grupos de reformer suelen ser de 2 a 6 personas, mucho más reducidos que en pilates de suelo, lo que garantiza mayor atención del instructor y una práctica más personalizada."},
        ],
    },
    {
        "slug": "con-fisioterapia",
        "filtro": lambda s: s["fisioterapia"] is True,
        "h1": "Pilates con Fisioterapia en Valencia",
        "h2_info": "Ventajas de combinar pilates y fisioterapia",
        "icono": "🩺",
        "desc_corta": "Pilates supervisado por fisioterapeutas clínicos, ideal para lesiones y rehabilitación.",
        "desc_larga": "Estudios de pilates en Valencia con servicio clinico de fisioterapia. Ideal para rehabilitacion, lesiones o pilates terapeutico supervisado.",
        "texto_info": "Combinar pilates con fisioterapia permite un trabajo mas preciso, especialmente en casos de lesion, dolor cronico, recuperacion postoperatoria o suelo pelvico. Los centros listados cuentan con fisioterapeutas titulados que adaptan los ejercicios a cada persona.",
        "que_es": [
            "El pilates con fisioterapia combina la práctica del pilates (en reformer, máquinas o suelo) con la supervisión y evaluación de un fisioterapeuta titulado. A diferencia de un estudio convencional, estos centros ofrecen una valoración clínica previa y adaptan los ejercicios a la condición específica de cada persona.",
            "Este enfoque es especialmente útil para quienes tienen una lesión activa, dolor crónico, están en recuperación postoperatoria, o trabajan el suelo pélvico (embarazo, posparto, incontinencia). La figura del fisioterapeuta garantiza que el trabajo sea seguro y terapéutico.",
            "En Valencia, los centros de pilates con fisioterapia suelen ofrecer sesiones individuales o en grupos muy reducidos, con tarifas algo superiores al pilates convencional por el nivel de especialización.",
        ],
        "beneficios": [
            "Evaluación clínica previa y ejercicios adaptados a tu condición",
            "Trabajo seguro con lesiones, dolor crónico o patologías específicas",
            "Rehabilitación postoperatoria o postelesión supervisada",
            "Trabajo de suelo pélvico (embarazo, posparto, incontinencia)",
            "Prevención de lesiones con supervisión profesional",
        ],
        "para_quien": "Personas con lesiones activas, dolor crónico, en rehabilitación postoperatoria, embarazadas, o quienes buscan un pilates terapéutico con supervisión clínica.",
        "en": True,
        "faqs": [
            {"q": "¿Qué ventaja tiene el pilates con fisioterapia?", "a": "Combinar pilates con fisioterapia permite una evaluación clínica previa, la adaptación de ejercicios a lesiones o patologías específicas, y el seguimiento por un fisioterapeuta titulado. Es especialmente útil en rehabilitación, dolor crónico y trabajo de suelo pélvico."},
            {"q": "¿Es más caro el pilates con fisioterapia clínica?", "a": "En general sí, los centros con fisioterapeutas en plantilla tienen tarifas algo más altas que los estudios convencionales, especialmente para pilates terapéutico o rehabilitación. El nivel de personalización y seguridad es mayor."},
            {"q": "¿El pilates terapéutico es solo para personas con lesiones?", "a": "No, también es recomendable como prevención para personas sedentarias, deportistas con desequilibrios musculares, adultos mayores y embarazadas o en posparto que buscan un seguimiento más clínico de su práctica."},
        ],
    },
    {
        "slug": "todas-las-maquinas",
        "filtro": lambda s: s["equipamiento_tipo"] == "mixto",
        "h1": "Pilates con Todas las Máquinas en Valencia",
        "h2_info": "Qué incluye un estudio completo de pilates",
        "icono": "🏋️",
        "desc_corta": "Estudios con equipamiento completo: reformer, cadillac, wunda chair, barrel y más.",
        "desc_larga": "Directorio de estudios de pilates con equipamiento completo en Valencia. Reformer, cadillac, wunda chair, barrel y más máquinas para un trabajo integral.",
        "texto_info": "Los estudios con todas las máquinas ofrecen la experiencia más completa del método Pilates clásico. Combinan el reformer con aparatos como el cadillac (también llamado trapecio), el wunda chair, el barrel y otros. Esta variedad permite trabajar todos los grupos musculares en distintos planos y progresiones, siguiendo el método original de Joseph Pilates.",
        "que_es": [
            "Los estudios con todas las máquinas ofrecen el equipamiento completo del método Pilates: reformer, cadillac (o trapecio), wunda chair, barrel, spine corrector y otros aparatos diseñados por Joseph Pilates. Este conjunto permite trabajar el cuerpo en todos los planos de movimiento y con progresiones muy variadas.",
            "A diferencia de los estudios solo con reformer, estos centros permiten seguir el método Pilates clásico en su totalidad, alternando máquinas según el objetivo de cada sesión. Suelen contar con instructores de formación más amplia y grupos más reducidos.",
            "En Valencia, los centros con equipamiento completo tienden a ser estudios boutique con clases muy personalizadas, ideales para quienes quieren profundizar en el método o ya llevan tiempo practicando pilates.",
        ],
        "beneficios": [
            "Trabajo integral del cuerpo con variedad de máquinas y planos de movimiento",
            "Seguimiento del método Pilates clásico en su totalidad",
            "Mayor progresión técnica y variedad en las sesiones",
            "Grupos muy reducidos con alta atención personalizada",
            "Ideal para avanzar si ya practicás pilates reformer",
        ],
        "para_quien": "Practicantes con cierta experiencia que quieren profundizar en el método, o quienes buscan la experiencia más completa del pilates clásico.",
        "en": True,
        "faqs": [
            {"q": "¿Qué máquinas incluye un estudio de pilates completo?", "a": "Un estudio completo suele tener reformer, cadillac o trapecio, wunda chair, barrel y spine corrector. Algunos centros incluyen también el pedi-pull o el ladder barrel. Esta variedad permite seguir el método Pilates clásico en su totalidad."},
            {"q": "¿Es mejor el pilates con todas las máquinas que solo reformer?", "a": "Depende del objetivo. El reformer solo es suficiente para la mayoría de personas. El equipamiento completo añade variedad y profundidad en el trabajo, y es especialmente útil para quienes llevan tiempo practicando y quieren explorar todo el método."},
            {"q": "¿Es más caro el pilates con todas las máquinas?", "a": "No necesariamente. El precio depende más del tipo de clase (privada, semiprivada o grupal) que del equipamiento disponible. Lo que sí puede variar es el número de personas por clase y el nivel de atención personalizada."},
        ],
    },
    {
        "slug": "mat-suelo",
        "filtro": lambda s: s["equipamiento_tipo"] == "suelo",
        "h1": "Pilates Mat / Suelo en Valencia",
        "h2_info": "Qué es el pilates de suelo",
        "icono": "🧘",
        "desc_corta": "La forma más accesible del pilates: colchoneta, peso corporal y grupos amplios.",
        "desc_larga": "Estudios de pilates de suelo (mat) en Valencia. La modalidad más accesible del pilates: sin máquinas, grupos más grandes y precios más económicos.",
        "texto_info": "El pilates de suelo o mat es la forma más accesible del método. No requiere máquinas: se trabaja principalmente con el peso corporal sobre una colchoneta, a veces con accesorios pequeños como bandas elásticas, pelotas o círculos. Los grupos suelen ser mayores (8-15 personas) y los precios, más económicos que el reformer.",
        "que_es": [
            "El pilates de suelo, también llamado pilates mat, es la forma más accesible y original del método Pilates. Se practica sobre una colchoneta, usando principalmente el peso corporal, aunque a veces se añaden pequeños accesorios como bandas elásticas, pelotas de pilates, magic circles o bloques.",
            "Es la modalidad con grupos más grandes (hasta 10-15 personas en algunos centros) y tarifas más económicas que el reformer, lo que la convierte en la opción ideal para quienes se inician en el pilates o buscan una práctica regular de bienestar a buen precio.",
            "A pesar de no usar máquinas, el pilates de suelo trabaja profundamente el core, la postura, la flexibilidad y el control motor. Es el punto de partida del método original de Joseph Pilates y sigue siendo una práctica muy completa para todos los niveles.",
        ],
        "beneficios": [
            "La modalidad más económica: la mejor opción para empezar",
            "Clases en grupo en un entorno social y motivador",
            "Mejora del core, la postura y la flexibilidad sin equipamiento especial",
            "Bajo impacto, apto para todas las edades y niveles",
            "Disponible en más centros y horarios en Valencia",
        ],
        "para_quien": "Personas que empiezan en el pilates, quienes buscan una práctica de bienestar a buen precio, y quienes prefieren clases en grupo sin necesidad de máquinas.",
        "en": True,
        "faqs": [
            {"q": "¿Qué diferencia hay entre pilates de suelo y pilates reformer?", "a": "El pilates de suelo usa solo el peso corporal sobre una colchoneta, con grupos más grandes y precios más accesibles. El reformer usa una máquina que añade resistencia variable, con grupos más pequeños y precios más altos. Ambos trabajan el core y la postura, pero el reformer permite más variedad y adaptación."},
            {"q": "¿Es efectivo el pilates de suelo?", "a": "Sí, el pilates de suelo es completamente efectivo para trabajar el core, la postura, la flexibilidad y la fuerza funcional. Es la forma original del método Pilates y ofrece beneficios muy completos, especialmente para quienes empiezan o buscan una práctica de bienestar general."},
            {"q": "¿Cuánto cuesta el pilates de suelo en Valencia?", "a": "El pilates de suelo es la modalidad más económica. Se pueden encontrar mensualidades desde 25-30€ para clases grupales, y clases sueltas desde 10€. Es la opción más accesible para empezar a practicar pilates."},
        ],
    },
]

tpl_tipo = env.get_template("tipo.html")
tipos_generados = 0
tipos_hub = []
for cfg in tipo_config:
    studios_tipo = [s for s in studios if cfg["filtro"](s)]
    if not studios_tipo:
        continue
    tipos_hub.append({
        "slug": cfg["slug"],
        "h1": cfg["h1"],
        "desc_corta": cfg["desc_corta"],
        "icono": cfg["icono"],
        "count": len(studios_tipo),
    })
    html = tpl_tipo.render(
        title=f"{cfg['h1']} | Precios y Centros Especializados",
        description=cfg["desc_larga"],
        canonical=f"{SITE_URL}/tipo/{cfg['slug']}.html",
        root="../", active="tipo", icons=ICONS,
        h1=cfg["h1"], h2_info=cfg["h2_info"],
        studios=studios_tipo,
        descripcion_larga=cfg["desc_larga"],
        texto_informativo=cfg["texto_info"],
        que_es=cfg["que_es"], beneficios=cfg["beneficios"], para_quien=cfg["para_quien"],
        faqs=cfg["faqs"], year=year,
        en_url=f"../en/tipo/{cfg['slug']}.html" if cfg.get("en") else "",
    )
    write(f"tipo/{cfg['slug']}.html", html)
    tipos_generados += 1

# Hub de tipos
tpl_tipo_index = env.get_template("tipo_index.html")
html = tpl_tipo_index.render(
    title="Tipos de Pilates en Valencia | Reformer, Mat, Fisioterapia y Más",
    description="Compará las modalidades de pilates en Valencia: reformer, mat/suelo, todas las máquinas y pilates con fisioterapia. Elegí el tipo que mejor se adapta a tus objetivos.",
    canonical=f"{SITE_URL}/tipo/index.html",
    root="../", active="guia", icons=ICONS, year=year,
    tipos=tipos_hub,
    en_url="",
)
write("tipo/index.html", html)

# Quiz ¿Qué pilates es para mí?
tpl_quiz = env.get_template("pilates-para-ti.html")
html = tpl_quiz.render(
    title="¿Qué pilates es para mí? | Test de pilates en Valencia",
    description="Hacé el test y descubrí qué tipo de pilates es ideal para vos: reformer, mat, todas las máquinas o con fisioterapia. 5 preguntas, resultado instantáneo.",
    canonical=f"{SITE_URL}/pilates-para-ti.html",
    root="", active="guia", icons=ICONS, year=year,
    en_url="",
)
write("pilates-para-ti.html", html)

# Blog / articulos
BLOG_DATA = os.path.join(ROOT, "data", "blog")

articulos_config = [
    {
        "slug": "precio-pilates-valencia",
        "h1": "¿Cuánto cuesta el pilates en Valencia? Precios reales de 2026",
        "description": "Comparativa de precios de pilates en Valencia: clase suelta, bonos y mensualidad, con datos reales de 38 estudios. Reformer vs suelo y como elegir segun tu presupuesto.",
        "fecha_iso": "2026-06-19",
        "fecha_legible": "19 de junio de 2026",
        "faqs": [
            {"q": "¿Cuánto cuesta una clase de pilates en Valencia?", "a": "Una clase suelta cuesta entre 10€ y 49€ según el estudio y la modalidad, con la mayoría de los centros entre 15€ y 35€ por clase."},
            {"q": "¿Es más caro el pilates reformer que el pilates de suelo?", "a": "Sí. El pilates reformer suele costar entre un 30% y un 60% más que el pilates de suelo, debido al equipamiento y a los grupos más reducidos."},
            {"q": "¿Hay estudios de pilates baratos en Valencia?", "a": "Sí, hay opciones de pilates de suelo en grupo desde 25€/mes sin permanencia, y clases sueltas desde 10€."},
        ],
    },
    {
        "slug": "pilates-embarazo-valencia",
        "h1": "Pilates en el embarazo: guía completa por trimestres y dónde practicarlo en Valencia",
        "description": "Guia de pilates para embarazadas escrita por una kinesiologa: beneficios, seguridad, ejercicios por trimestre, posparto y estudios de Valencia con clases para embarazadas.",
        "fecha_iso": "2026-06-22",
        "fecha_legible": "22 de junio de 2026",
        "faqs": [
            {"q": "¿Es seguro hacer pilates durante el embarazo?", "a": "Sí, con autorización médica y adaptando los ejercicios a cada trimestre. Se evitan abdominales clásicos, posiciones boca arriba prolongadas desde el segundo trimestre y cualquier esfuerzo que genere dolor."},
            {"q": "¿Desde qué semana se puede empezar pilates en el embarazo?", "a": "Se puede practicar durante todo el embarazo si no hay contraindicación médica, adaptando la intensidad y los ejercicios según el trimestre."},
            {"q": "¿Cuándo se puede retomar el pilates después del parto?", "a": "Con autorización médica, desde las primeras semanas se puede trabajar respiración y activación suave del abdomen. El trabajo de fuerza progresiva suele incorporarse a partir de las 12 semanas posparto."},
        ],
    },
    {
        "slug": "pilates-principiantes-valencia",
        "h1": "Pilates para principiantes en Valencia: guía completa para empezar",
        "description": "Todo lo que necesitas saber antes de tu primera clase de pilates en Valencia: suelo o reformer, frecuencia, qué esperar, mitos y estudios recomendados para empezar.",
        "fecha_iso": "2026-07-07",
        "fecha_legible": "7 de julio de 2026",
        "faqs": [
            {"q": "¿Necesito condición física para empezar pilates?", "a": "No. El pilates está diseñado para adaptarse a cada persona. Puedes empezar desde cero, con cualquier nivel de condición física, y el instructor adapta los ejercicios desde la primera clase."},
            {"q": "¿Cuántas veces por semana hay que hacer pilates para notar resultados?", "a": "Lo ideal para principiantes son 2 veces por semana. Con esta frecuencia empezarás a notar diferencias en postura y fuerza en el primer mes, y cambios más evidentes a partir del tercer mes."},
            {"q": "¿Es mejor empezar con pilates de suelo o reformer?", "a": "Ambos son válidos para principiantes. El suelo es más económico y te enseña los principios básicos. El reformer ofrece más atención individual por el grupo reducido. Si tienes lesiones o dudas, empieza con un centro que tenga fisioterapeuta."},
            {"q": "¿Cuánto cuesta empezar pilates en Valencia?", "a": "Desde 25-40€/mes para pilates de suelo en grupo, y entre 78€ y 155€/mes para reformer con dos sesiones semanales. Muchos estudios ofrecen una primera clase de prueba gratuita."},
        ],
    },
]

tpl_articulo = env.get_template("articulo.html")
articulos = []
for cfg in articulos_config:
    with open(os.path.join(BLOG_DATA, f"{cfg['slug']}.html"), encoding="utf-8") as f:
        contenido = f.read()
    art = dict(cfg)
    art["contenido"] = contenido
    articulos.append(art)

articulos_generados = 0
for a in articulos:
    html = tpl_articulo.render(
        title=f"{a['h1']} | Blog Pilates Valencia",
        description=a["description"],
        canonical=f"{SITE_URL}/blog/{a['slug']}.html",
        root="../", active="blog", icons=ICONS, year=year,
        h1=a["h1"], fecha_iso=a["fecha_iso"], fecha_legible=a["fecha_legible"],
        contenido=a["contenido"], faqs=a["faqs"], total_estudios=len(studios),
        en_url="",
    )
    write(f"blog/{a['slug']}.html", html)
    articulos_generados += 1

# Blog index
tpl_blog = env.get_template("blog.html")
html_blog = tpl_blog.render(
    title="Blog de Pilates en Valencia | Precios y Guias | Directorio Pilates Valencia",
    description="Guias, precios y consejos sobre pilates en Valencia basados en datos reales de los estudios del directorio.",
    canonical=f"{SITE_URL}/blog/index.html",
    root="../", active="blog", icons=ICONS, year=year,
    articulos=articulos,
    en_url="",
)
write("blog/index.html", html_blog)

total = 1 + len(studios) + zonas_generadas + barrios_generados + tipos_generados + 1 + 1 + 1 + articulos_generados
print(f"Generadas {total} paginas:")
print(f"  - 1 index + {len(studios)} fichas + {zonas_generadas} zonas + {barrios_generados} barrios + {tipos_generados} tipos + 1 tipo-hub + 1 quiz + 1 blog-index + {articulos_generados} articulos")
