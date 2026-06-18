# pyrefly: ignore [missing-import]
import streamlit as st
import os
import pandas as pd
import re
import matplotlib.pyplot as plt

# Configuração da Página
st.set_page_config(
    page_title="Stardew Valley - Painel Científico de Dados",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- MAPAS DE REFERÊNCIA ---
crop_to_seed = {
    "Chirívia": "Sementes de chirívia",
    "Chirivia": "Sementes de chirívia",
    "Couve": "Sementes de couve",
    "Batata": "Sementes de batata",
    "Jasmim-azul": "Sementes de Jasmim-azul",
    "Vagem": "Mudas de feijão",
    "Couve-flor": "Sementes de Couve-flor",
    "Ruibarbo": "Sementes de ruibarbo",
    "Alho": "Sementes de alho",
    "Pimenta quente": "Sementes de pimenta",
    "Rabanete": "Sementes de rabanete",
    "Papoula": "Sementes de papoula",
    "Tomate": "Sementes de tomante",  # Grafado como 'tomante' no CSV
    "Melão": "Sementes de Melão",
    "Mirtilo": "Sementes de mirtilo",
    "Milho": "Sementes de milho",
    "Repolho roxo": "Sementes de repolho vermelho",
    "Couve chinesa": "Sementes de couve chinesa",
    "Berinjela": "Sementes de berinjela",
    "Amaranto": "Sementes de amaranto",
    "Oxicoco": "Sementes de oxicoco",
    "Inhame": "Sementes de inhame",
    "Abóbora": "Sementes de abóbora",
    "Beterraba": "Sementes de beterraba",
    "Alcachofra": "Sementes de alcachofra",
    "Abacaxi": "Sementes de Abacaxi",
    "Inhame-coco": "Sementes de Miçanga",
    "Girassol": "Sementes de Girassol",
    "Tulipa": "Bulbo de Tulipa",
    "Carambola": "Sementes de carambola",
    "Fibra": "Semente de Fibra  (4)",
    "Arroz": "Broto de arroz",
    "Trigo": "Sementes de trigo",
    "Uva": "Mudas de uva",
    "Lúpulo": "Mudas de lúpulo",
}

fruit_to_sapling = {
    "Damasco": "Muda de damasqueiro",
    "Cereja": "Muda de cerejeira",
    "Laranja": "Muda de laranjeira",
    "Pêssego": "Muda de pessegueira",
    "Banana": "Muda de bananeira",
    "Manga": "Muda de mangueira",
    "Maçã": "Muda de macieira",
    "Romã": "Muda de romanzeira",
}

artisan_good_to_machine = {
    "Vinho": "Barril",
    "Cerveja": "Barril",
    "Pale Ale": "Barril",
    "Hidromel": "Barril",
    "Café": "Barril",
    "Geléia": "Jarra de conserva",
    "Picles": "Jarra de conserva",
    "Maionese": "Máquina de maionese",
    "Maionese de Dinossauro": "Máquina de maionese",
    "Maionese de ovo de pato": "Máquina de maionese",
    "Maionese nula": "Máquina de maionese",
    "Queijo": "Prensa de queijo",
    "Queijo de cabra": "Prensa de queijo",
    "Tecido": "Tear",
    "Óleo": "Gerador de óleo",
    "Óleo de trufas": "Gerador de óleo",
    "Caviar": "Jarra de conserva",
    "Ovas Maturadas": "Jarra de conserva",
}

# --- ESTILIZAÇÃO PREMIUM (CSS) ---
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF7E5F, #FEB47B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        font-size: 1.2rem;
        color: #888888;
        margin-bottom: 2rem;
    }
    
    .stButton>button {
        border-radius: 8px;
        background-color: #1e1e24;
        color: #ffffff;
        border: 1px solid #33333f;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #FF7E5F, #FEB47B);
        color: #000000;
        border: 1px solid transparent;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 126, 95, 0.4);
    }
    
    .card {
        background-color: #16161a;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #24242b;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .badge-ok {
        background-color: rgba(46, 204, 113, 0.2);
        color: #2ecc71;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .badge-error {
        background-color: rgba(231, 76, 60, 0.2);
        color: #e74c3c;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""",
    unsafe_allow_html=True,
)


# --- HELPERS ---
def ensure_directories():
    os.makedirs("docs_raw", exist_ok=True)
    os.makedirs("docs_bronze", exist_ok=True)
    os.makedirs("docs_silver", exist_ok=True)


def parse_building_cost(cost_str):
    if pd.isna(cost_str) or not isinstance(cost_str, str):
        return []
    ingredients = []
    # Verifica o custo em ouro (ex: 10 000 ouros)
    gold_match = re.search(r"(\d+[\s\d]*)\s*(?:ouros|g)", cost_str)
    if gold_match:
        gold_val = int(gold_match.group(1).replace("\xa0", "").replace(" ", ""))
        ingredients.append(("Ouro", gold_val))

    # Verifica itens com parênteses (ex: Madeira (450))
    item_matches = re.findall(r"([^()]+?)\s*\((\d+)\)", cost_str)
    for item_name, qty in item_matches:
        clean_name = item_name.replace("ouros", "").replace("g", "").strip()
        if clean_name.replace(" ", "").isdigit():
            continue
        ingredients.append((clean_name, int(qty)))
    return ingredients


def parse_artisan_ingredients(ing_str):
    if pd.isna(ing_str) or not isinstance(ing_str, str):
        return []
    # Trata alternativas simples como "ou"
    if "ou" in ing_str:
        if "Ovo" in ing_str:
            return [("Ovo (Qualquer)", 1)]
        if "Leite" in ing_str:
            return [("Leite (Qualquer)", 1)]
    matches = re.findall(r"([^()]+?)\s*\((\d+)\)", ing_str)
    res = []
    for name, qty in matches:
        res.append((name.strip(), int(qty)))
    if not res:
        return [(ing_str.strip(), 1)]
    return res


# --- CARREGAR REQUISITOS DE DADOS ---
@st.cache_data
def load_recipes_databases():
    def safe_read(name):
        path = os.path.join("docs_silver", name)
        if os.path.exists(path):
            try:
                return pd.read_csv(path, encoding="utf-8")
            except Exception:
                pass
        return pd.DataFrame()

    return {
        "artesanato": safe_read("artesanato.csv"),
        "culinaria": safe_read("culinaria.csv"),
        "casa": safe_read("casa.csv"),
        "maquinas": safe_read("maquinas.csv"),
        "lavouras": safe_read("lavouras.csv"),
        "peixes": safe_read("peixes.csv"),
        "coleta": safe_read("coleta.csv"),
        "animais": safe_read("animais.csv"),
    }


def get_node_dependencies(item_name, db):
    deps = []
    clean_name = item_name.strip().lower()

    # 1. Culinária / Receitas de mercadorias artesanais
    df_cul = db["culinaria"]
    if not df_cul.empty:
        match_cul = df_cul[df_cul["Nome"].str.strip().str.lower() == clean_name]
        if not match_cul.empty:
            row = match_cul.iloc[0]
            if row["Tipo"] == "mercadorias_artesanais":
                machine = (
                    row["Fonte"]
                    if not pd.isna(row["Fonte"])
                    else artisan_good_to_machine.get(row["Nome"], "Barril")
                )
                deps.append(
                    {"name": str(machine), "qty": 1, "source": "Refino (Máquina)"}
                )

                input_item = (
                    row["Item de entrada"]
                    if "Item de entrada" in row and not pd.isna(row["Item de entrada"])
                    else None
                )
                if input_item:
                    ingredients = parse_artisan_ingredients(str(input_item))
                    for ing, qty in ingredients:
                        deps.append(
                            {"name": ing, "qty": qty, "source": "Ingrediente de Refino"}
                        )
                return deps
            elif row["Tipo"] == "receitas":
                ing_str = (
                    row["Ingredientes"]
                    if "Ingredientes" in row and not pd.isna(row["Ingredientes"])
                    else None
                )
                if ing_str:
                    ingredients = re.findall(r"([^()]+?)\s*\((\d+)\)", str(ing_str))
                    for ing, qty in ingredients:
                        deps.append(
                            {
                                "name": ing.strip(),
                                "qty": int(qty),
                                "source": "Ingrediente de Culinária",
                            }
                        )
                return deps

    # 2. Artesanato
    df_art = db["artesanato"]
    if not df_art.empty:
        art_match = df_art[df_art["Nome"].str.strip().str.lower() == clean_name]
        if art_match.empty:
            art_match = df_art[
                df_art["Nome"]
                .str.strip()
                .str.lower()
                .str.contains(clean_name, regex=False)
            ]
        if not art_match.empty:
            matched_name = art_match.iloc[0]["Nome"]
            item_rows = df_art[df_art["Nome"] == matched_name]
            for idx, row in item_rows.iterrows():
                ing_name = row["Ingredientes_item"]
                if pd.isna(ing_name) or not ing_name:
                    continue
                ing_qty = (
                    int(row["Ingredientes_qtd"])
                    if not pd.isna(row["Ingredientes_qtd"])
                    else 1
                )
                deps.append(
                    {
                        "name": str(ing_name).strip(),
                        "qty": ing_qty,
                        "source": "Ingrediente de Artesanato",
                    }
                )
            return deps

    # 3. Construções
    df_casa = db["casa"]
    if not df_casa.empty:
        casa_match = df_casa[df_casa["Nome"].str.strip().str.lower() == clean_name]
        if not casa_match.empty:
            row = casa_match.iloc[0]
            cost_ingredients = parse_building_cost(row["Custo"])
            for ing, qty in cost_ingredients:
                deps.append({"name": ing, "qty": qty, "source": "Custo de Construção"})
            return deps

    # 4. Máquinas
    df_maq = db["maquinas"]
    if not df_maq.empty:
        maq_match = df_maq[df_maq["Nome"].str.strip().str.lower() == clean_name]
        if not maq_match.empty:
            matched_name = maq_match.iloc[0]["Nome"]
            item_rows = df_maq[df_maq["Nome"] == matched_name]
            for idx, row in item_rows.iterrows():
                ing_name = row["Ingredientes_item"]
                if pd.isna(ing_name) or not ing_name:
                    continue
                ing_qty = (
                    int(row["Ingredientes_qtd"])
                    if not pd.isna(row["Ingredientes_qtd"])
                    else 1
                )
                deps.append(
                    {
                        "name": str(ing_name).strip(),
                        "qty": ing_qty,
                        "source": "Ingrediente de Máquina",
                    }
                )
            return deps

    # 5. Lavouras / Cultivos
    seed_name = None
    for crop, seed in crop_to_seed.items():
        if crop.lower() == clean_name:
            seed_name = seed
            break
    if seed_name:
        deps.append({"name": seed_name, "qty": 1, "source": "Semente de Lavoura"})
        return deps

    # 6. Árvores
    sapling_name = None
    for fruit, sapling in fruit_to_sapling.items():
        if fruit.lower() == clean_name:
            sapling_name = sapling
            break
    if sapling_name:
        deps.append({"name": sapling_name, "qty": 1, "source": "Muda de Árvore"})
        return deps

    # 7. Produtos Animais
    df_anim = db["animais"]
    if not df_anim.empty:
        anim_match = df_anim[
            df_anim["Produz_item"].str.strip().str.lower() == clean_name
        ]
        if not anim_match.empty:
            row = anim_match.iloc[0]
            deps.append(
                {
                    "name": str(row["Nome"]).capitalize(),
                    "qty": 1,
                    "source": "Produzido por Animal",
                }
            )
            return deps

    # 8. Animais propriamente ditos
    if not df_anim.empty:
        anim_self = df_anim[df_anim["Nome"].str.strip().str.lower() == clean_name]
        if not anim_self.empty:
            row = anim_self.iloc[0]
            gold_cost = int(row["Custo"]) if not pd.isna(row["Custo"]) else 0
            if gold_cost > 0:
                deps.append(
                    {"name": "Ouro", "qty": gold_cost, "source": "Custo de Compra"}
                )
            req_building = row["Requisitos"]
            if not pd.isna(req_building) and isinstance(req_building, str):
                deps.append(
                    {
                        "name": req_building.strip(),
                        "qty": 1,
                        "source": "Requisito de Construção",
                    }
                )
            return deps

    return []


def build_tree_data(item_name, qty=1, visited=None, depth=0, max_depth=5, db=None):
    if visited is None:
        visited = set()

    node = {
        "name": item_name,
        "qty": qty,
        "depth": depth,
        "source": "Recurso Básico",
        "extra_info": "",
        "children": [],
    }

    clean_name = item_name.strip().lower()

    # Adicionar metadados extras das tabelas (Origem, Peixes, Coleta)
    df_lav = db["lavouras"]
    if not df_lav.empty:
        lav_match = df_lav[df_lav["Semente"].str.strip().str.lower() == clean_name]
        if not lav_match.empty:
            row = lav_match.iloc[0]
            if not pd.isna(row["Origem"]):
                node["extra_info"] = f"Adquirido em: {row['Origem']}"
                node["source"] = "Semente Comprada"

    df_peixes = db["peixes"]
    if not df_peixes.empty:
        fish_match = df_peixes[df_peixes["Nome"].str.strip().str.lower() == clean_name]
        if not fish_match.empty:
            row = fish_match.iloc[0]
            node["extra_info"] = (
                f"Tipo: {row['Tipo']} | Estação: {row['Estação'] if 'Estação' in row else ''}"
            )
            node["source"] = "Peixe"

    df_coleta = db["coleta"]
    if not df_coleta.empty:
        coleta_match = df_coleta[
            df_coleta["Nome"].str.strip().str.lower() == clean_name
        ]
        if not coleta_match.empty:
            row = coleta_match.iloc[0]
            orig = row["origem"] if "origem" in row else ""
            node["extra_info"] = f"Local: {row['Encontrado em']} | Estação: {orig}"
            node["source"] = "Coleta"

    if item_name in visited or depth >= max_depth:
        return node

    visited.add(item_name)

    dependencies = get_node_dependencies(item_name, db)
    if dependencies:
        node["source"] = dependencies[0]["source"]
        for dep in dependencies:
            child_node = build_tree_data(
                dep["name"], dep["qty"] * qty, visited.copy(), depth + 1, max_depth, db
            )
            node["children"].append(child_node)

    return node


def get_all_possible_items(db):
    items = set()
    if "culinaria" in db and not db["culinaria"].empty:
        items.update(db["culinaria"]["Nome"].dropna().unique())
    if "artesanato" in db and not db["artesanato"].empty:
        items.update(db["artesanato"]["Nome"].dropna().unique())
    if "casa" in db and not db["casa"].empty:
        items.update(db["casa"]["Nome"].dropna().unique())
    if "maquinas" in db and not db["maquinas"].empty:
        items.update(db["maquinas"]["Nome"].dropna().unique())
    if "lavouras" in db and not db["lavouras"].empty:
        items.update(db["lavouras"]["Semente"].dropna().unique())
    if "peixes" in db and not db["peixes"].empty:
        items.update(db["peixes"]["Nome"].dropna().unique())
    if "coleta" in db and not db["coleta"].empty:
        items.update(db["coleta"]["Nome"].dropna().unique())
    if "animais" in db and not db["animais"].empty:
        items.update(db["animais"]["Nome"].dropna().unique())
        items.update(db["animais"]["Produz_item"].dropna().unique())

    items.update(crop_to_seed.keys())
    items.update(fruit_to_sapling.keys())

    items = {str(x).strip() for x in items if pd.notna(x) and str(x).strip()}
    return sorted(list(items))


def render_text_tree(node, prefix="", is_last=True):
    emoji_map = {
        "Refino (Máquina)": "⚙️",
        "Ingrediente de Refino": "🌾",
        "Ingrediente de Artesanato": "🪵",
        "Custo de Construção": "🧱",
        "Ingrediente de Máquina": "⚙️",
        "Semente de Lavoura": "🌱",
        "Muda de Árvore": "🌳",
        "Produzido por Animal": "🐄",
        "Custo de Compra": "🪙",
        "Requisito de Construção": "🛖",
        "Semente Comprada": "🪙",
        "Peixe": "🐟",
        "Coleta": "🍄",
        "Recurso Básico": "📦",
    }
    emoji = emoji_map.get(node["source"], "📦")
    name = node["name"]
    qty = node["qty"]
    src = node["source"]
    extra = f" *( {node['extra_info']} )*" if node["extra_info"] else ""

    node_str = f"{prefix}{'└── ' if is_last else '├── '}{emoji} **{name}** x{qty} *[{src}]*{extra}\n"

    child_prefix = prefix + ("    " if is_last else "│   ")
    children_str = ""
    for i, child in enumerate(node["children"]):
        is_last_child = i == len(node["children"]) - 1
        children_str += render_text_tree(child, child_prefix, is_last_child)

    return node_str + children_str


def get_full_text_tree(node):
    emoji_map = {
        "Refino (Máquina)": "⚙️",
        "Ingrediente de Refino": "🌾",
        "Ingrediente de Artesanato": "🪵",
        "Custo de Construção": "🧱",
        "Ingrediente de Máquina": "⚙️",
        "Semente de Lavoura": "🌱",
        "Muda de Árvore": "🌳",
        "Produzido por Animal": "🐄",
        "Custo de Compra": "🪙",
        "Requisito de Construção": "🛖",
        "Semente Comprada": "🪙",
        "Peixe": "🐟",
        "Coleta": "🍄",
        "Recurso Básico": "📦",
    }
    emoji = emoji_map.get(node["source"], "📦")
    root_str = f"{emoji} **{node['name']}** x{node['qty']} *[{node['source']}]*{' *( ' + node['extra_info'] + ' )*' if node['extra_info'] else ''}\n"

    children_str = ""
    for i, child in enumerate(node["children"]):
        is_last_child = i == len(node["children"]) - 1
        children_str += render_text_tree(child, "", is_last_child)

    return root_str + children_str


def generate_mermaid_graph(node):
    lines = ["graph TD"]
    counter = [0]

    def add_nodes(curr_node):
        node_id = f"node_{counter[0]}"
        counter[0] += 1

        emoji_map = {
            "Refino (Máquina)": "⚙️",
            "Ingrediente de Refino": "🌾",
            "Ingrediente de Artesanato": "🪵",
            "Custo de Construção": "🧱",
            "Ingrediente de Máquina": "⚙️",
            "Semente de Lavoura": "🌱",
            "Muda de Árvore": "🌳",
            "Produzido por Animal": "🐄",
            "Custo de Compra": "🪙",
            "Requisito de Construção": "🛖",
            "Semente Comprada": "🪙",
            "Peixe": "🐟",
            "Coleta": "🍄",
            "Recurso Básico": "📦",
        }
        emoji = emoji_map.get(curr_node["source"], "📦")
        clean_display = curr_node["name"].replace('"', '\\"')
        lines.append(f'    {node_id}["{emoji} {clean_display} (x{curr_node["qty"]})"]')

        for child in curr_node["children"]:
            child_id = add_nodes(child)
            lines.append(f"    {node_id} --> {child_id}")

        return node_id

    add_nodes(node)
    return "\n".join(lines)


def scan_and_validate_silver_tables():
    folder = "docs_silver"
    if not os.path.exists(folder):
        return [], {}

    csv_files = sorted([f for f in os.listdir(folder) if f.endswith(".csv")])
    table_details = {}

    for f in csv_files:
        path = os.path.join(folder, f)
        size_kb = os.path.getsize(path) / 1024.0
        errors = []
        shape = (0, 0)
        try:
            df = pd.read_csv(path, encoding="utf-8")
            shape = df.shape
            if df.empty:
                errors.append("Tabela vazia (0 registros)")
            # Checa por colunas com todos os registros NaNs
            nan_cols = [col for col in df.columns if df[col].isna().all()]
            if nan_cols:
                errors.append(f"Colunas totalmente vazias: {', '.join(nan_cols[:2])}")
        except Exception as e:
            errors.append(f"Erro ao ler CSV: {e}")

        table_details[f] = {
            "name": f.replace(".csv", "").capitalize(),
            "file_name": f,
            "path": path,
            "size_kb": round(size_kb, 2),
            "rows": shape[0],
            "cols": shape[1],
            "errors": errors,
            "status": "OK" if not errors else "Erro/Aviso",
        }
    return csv_files, table_details


# --- PIPELINES DE PROCESSAMENTO ---
def run_process_pipeline():
    # pyrefly: ignore [missing-import]
    import src.process_html_to_csv as process

    process.df_cultivo(html="docs_raw/sopa_Cultivo.html")
    process.df_mineracao(html="docs_raw/sopa_Mineração.html")
    process.df_coleta(html="docs_raw/sopa_Coleta.html")
    process.df_pesca(html="docs_raw/sopa_Pesca.html")
    process.df_combate(html="docs_raw/sopa_Combate.html")
    process.df_lavouras(html="docs_raw/sopa_Lavouras.html")
    process.df_animais(html="docs_raw/sopa_Animais.html")
    process.df_arvores_frutiferas(html="docs_raw/sopa_Árvores_frutíferas.html")
    process.df_mercadorias_artesanais(html="docs_raw/sopa_Mercadorias_Artesanais.html")
    process.df_casa_fazenda(html="docs_raw/sopa_Casa_da_Fazenda.html")
    process.df_caverna(html="docs_raw/sopa_A_Caverna.html")
    process.df_estufa(html="docs_raw/sopa_Estufa.html")
    process.df_casa(html="docs_raw/sopa_Casa.html")
    process.df_clima(html="docs_raw/sopa_Clima.html")
    process.df_primavera(html="docs_raw/sopa_Primavera.html")
    process.df_verao(html="docs_raw/sopa_Verão.html")
    process.df_outono(html="docs_raw/sopa_Outono.html")
    process.df_inverno(html="docs_raw/sopa_Inverno.html")
    process.df_missoes(html="docs_raw/sopa_Missões.html")
    process.df_conjuntos(html="docs_raw/sopa_Conjuntos.html")
    process.df_conquistas(html="docs_raw/sopa_Conquistas.html")
    process.df_ferramentas(html="docs_raw/sopa_ferramentas.html")
    process.df_armas(html="docs_raw/sopa_Armas.html")
    process.df_chapeus(html="docs_raw/sopa_Chapéus.html")
    process.df_calcados(html="docs_raw/sopa_Calçados.html")
    process.df_aneis(html="docs_raw/sopa_Anéis.html")
    process.df_peixes(html="docs_raw/sopa_Peixes.html")
    process.df_iscas(html="docs_raw/sopa_Isca.html")
    process.df_fertilizantes(html="docs_raw/sopa_Fertilizante.html")
    process.df_culinaria(html="docs_raw/sopa_Culinária.html")
    process.df_artesanato(html="docs_raw/sopa_Artesanato.html")
    process.df_carteira(html="docs_raw/sopa_Carteira.html")
    process.df_artefatos(html="docs_raw/sopa_Artefatos.html")
    process.df_minerais(html="docs_raw/sopa_Minerais.html")
    process.df_mobilia(html="docs_raw/sopa_Mobília.html")
    process.df_presentes_favoritos(
        html="docs_raw/sopa_Lista_de_Todos_os_Presentes.html"
    )
    process.df_construcoes_fazenda(html="docs_raw/sopa_Carpintaria.html")


def run_enrich_pipeline():
    import src.enrich_and_compile_csv as enrich

    enrich.profissoes()
    enrich.limpar_csv("docs_bronze/xp_coleta.csv")
    enrich.xp()
    enrich.concat_dataframes()


# --- MAIN STREAMLIT APP ---
def main():
    ensure_directories()

    st.markdown(
        '<div class="main-title">Stardew Valley DataLab 🌾</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sub-title">Painel Unificado de ETL, Auditoria de Dados e Árvores de Requisitos Científicas</div>',
        unsafe_allow_html=True,
    )

    # Inicialização das bases de dados em cache
    db = load_recipes_databases()

    # Definição das Abas
    tab_nav, tab_exp, tab_charts, tab_tree, tab_update = st.tabs(
        [
            "🧭 Navegação Geral",
            "📂 Explorador & Auditoria",
            "📈 Gráficos Científicos",
            "🌳 Árvore de Requisitos",
            "🔄 Atualizar Base (ETL)",
        ]
    )

    # ------------------ ABA 1: NAVEGAÇÃO GERAL ------------------
    with tab_nav:
        st.subheader("Página Inicial - Central de Categorias")
        st.write(
            "Navegue pelo menu abaixo para acessar as análises de categorias detalhadas:"
        )

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Animais 🐄"):
                st.switch_page("pages/animais.py")
            if st.button("Armas ⚔️"):
                st.switch_page("pages/armas.py")
            if st.button("Artefatos 🏺"):
                st.switch_page("pages/artefatos.py")
            if st.button("Árvores 🌳"):
                st.switch_page("pages/arvores.py")
            if st.button("Atributos de Luta 🛡️"):
                st.switch_page("pages/atributos_luta.py")
            if st.button("Calendário 📅"):
                st.switch_page("pages/calendario.py")
            if st.button("Carteira 💼"):
                st.switch_page("pages/carteira.py")
            if st.button("Casa 🏠"):
                st.switch_page("pages/casa.py")

        with col2:
            if st.button("Caverna 🦇"):
                st.switch_page("pages/caverna.py")
            if st.button("Clima 🌦️"):
                st.switch_page("pages/clima.py")
            if st.button("Coleta 🍄"):
                st.switch_page("pages/coleta.py")
            if st.button("Conjunto 🎒"):
                st.switch_page("pages/conjunto.py")
            if st.button("Culinária 🍳"):
                st.switch_page("pages/culinaria.py")
            if st.button("Ferramentas 🪓"):
                st.switch_page("pages/ferramentas.py")
            if st.button("Iscas 🪱"):
                st.switch_page("pages/iscas.py")
            if st.button("Lavoura 🌱"):
                st.switch_page("pages/lavoura.py")

        with col3:
            if st.button("Lista de presentes 🎁"):
                st.switch_page("pages/lista_presentes.py")
            if st.button("Máquina ⚙️"):
                st.switch_page("pages/maquina.py")
            if st.button("Mercadorias 📦"):
                st.switch_page("pages/mercadorias.py")
            if st.button("Minerais 💎"):
                st.switch_page("pages/minerais.py")
            if st.button("Missões 📜"):
                st.switch_page("pages/missoes.py")
            if st.button("Mobílias 🪑"):
                st.switch_page("pages/mobilias.py")
            if st.button("Nós de Minério 🪨"):
                st.switch_page("pages/nos_minerio.py")
            if st.button("Peixes 🐟"):
                st.switch_page("pages/peixes.py")

        with col4:
            if st.button("Pescas 🎣"):
                st.switch_page("pages/pescas.py")
            if st.button("Produção de Solos 🧪"):
                st.switch_page("pages/producao_solos.py")
            if st.button("Produtos 🥫"):
                st.switch_page("pages/produtos.py")
            if st.button("Profissões 🏆"):
                st.switch_page("pages/profissoes.py")
            if st.button("Solo foliar 🍁"):
                st.switch_page("pages/solo_foliar.py")
            if st.button("Vestuário 👕"):
                st.switch_page("pages/vestuarios.py")
            if st.button("XP ⚡"):
                st.switch_page("pages/xp.py")

        st.write("---")
        # Imagem de background
        if os.path.exists(os.path.join("src", "pages", "static", "background-h.jpg")):
            st.image(
                os.path.join("src", "pages", "static", "background-h.jpg"),
                use_container_width=True,
            )

    # ------------------ ABA 2: EXPLORADOR & AUDITORIA ------------------
    with tab_exp:
        st.subheader("📂 Explorador e Validador de Bases de Dados")
        st.write(
            "Verifique a disponibilidade, o tamanho e a integridade de todas as tabelas prontas para uso:"
        )

        csv_files, table_details = scan_and_validate_silver_tables()

        if not csv_files:
            st.warning(
                "Nenhum arquivo CSV encontrado em `docs_silver/`. Execute o pipeline de atualização para gerá-los."
            )
        else:
            # Grid resumo
            col_ok, col_warn = st.columns(2)
            ok_count = sum(1 for t in table_details.values() if t["status"] == "OK")
            warn_count = sum(1 for t in table_details.values() if t["status"] != "OK")

            with col_ok:
                st.metric("Tabelas 100% Integras (OK) 🟢", ok_count)
            with col_warn:
                st.metric("Tabelas com Alertas/Erros ⚠️", warn_count)

            st.write("---")

            # Detalhamento em lista com Preview
            selected_table_file = st.selectbox(
                "Escolha uma tabela para inspecionar os detalhes e ver uma prévia:",
                options=csv_files,
                format_func=lambda x: f"{table_details[x]['name']} ({table_details[x]['rows']} registros, {table_details[x]['size_kb']} KB) - Status: {table_details[x]['status']}",
            )

            if selected_table_file:
                info = table_details[selected_table_file]

                # Exibe status da tabela
                if info["status"] == "OK":
                    st.markdown(
                        f'<span class="badge-ok">Integridade OK</span>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<span class="badge-error">Erros/Alertas Detectados</span>',
                        unsafe_allow_html=True,
                    )
                    for err in info["errors"]:
                        st.error(f"⚠️ {err}")

                # Exibir dataframe
                try:
                    df = pd.read_csv(info["path"], encoding="utf-8")
                    # remove unnamed columns
                    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
                    st.dataframe(df.head(15), use_container_width=True)
                    st.caption(
                        f"Exibindo as primeiras 15 de {info['rows']} linhas da tabela."
                    )
                except Exception as e:
                    st.error(f"Não foi possível exibir o preview: {e}")

    # ------------------ ABA 3: GRÁFICOS CIENTÍFICOS ------------------
    with tab_charts:
        if not table_details:
            st.info("Carregue as bases de dados na aba de ETL primeiro.")
        else:
            st.subheader("📊 Gerador de Gráficos de Tabelas Lidas")
            st.write("Plote facilmente os dados de qualquer tabela silver ativa:")

            selected_file = st.selectbox(
                "Selecione a tabela para visualização gráfica:",
                options=list(table_details.keys()),
                key="charts_tab_select",
                format_func=lambda x: f"{table_details[x]['name']} ({table_details[x]['rows']} linhas)",
            )

            if selected_file:
                details = table_details[selected_file]
                try:
                    df = pd.read_csv(details["path"], encoding="utf-8")
                    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

                    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
                    all_cols = df.columns.tolist()

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        x_col = st.selectbox(
                            "Eixo X (Geralmente Categoria/Nome):",
                            options=all_cols,
                            index=0 if all_cols else None,
                        )
                    with col2:
                        y_col = st.selectbox(
                            "Eixo Y (Métrica Numérica):",
                            options=numeric_cols,
                            index=0 if numeric_cols else None,
                        )
                    with col3:
                        chart_type = st.selectbox(
                            "Formato do Gráfico:",
                            ["Barra", "Linha", "Área", "Dispersão"],
                        )

                    if x_col and y_col:
                        max_rows = st.slider(
                            "Quantidade máxima de itens a plotar:",
                            5,
                            100,
                            min(details["rows"], 20),
                        )
                        sort_order = st.checkbox(
                            "Ordenar por eixo Y decrescente", value=True
                        )

                        df_plot = df.dropna(subset=[x_col, y_col])
                        if sort_order:
                            df_plot = df_plot.sort_values(by=y_col, ascending=False)

                        df_plot = df_plot.head(max_rows)

                        chart_data = df_plot[[x_col, y_col]].set_index(x_col)

                        st.write(
                            f"Exibindo Gráfico de **{y_col}** por **{x_col}** (Top {len(df_plot)} registros):"
                        )

                        if chart_type == "Barra":
                            st.bar_chart(chart_data)
                        elif chart_type == "Linha":
                            st.line_chart(chart_data)
                        elif chart_type == "Área":
                            st.area_chart(chart_data)
                        elif chart_type == "Dispersão":
                            st.scatter_chart(df_plot, x=x_col, y=y_col)
                    else:
                        st.info(
                            "⚠️ O eixo Y precisa ser uma coluna numérica e o eixo X uma coluna de identificação."
                        )
                except Exception as e:
                    st.error(f"Erro ao gerar o gráfico: {e}")

    # ------------------ ABA 4: ÁRVORE DE REQUISITOS ------------------
    with tab_tree:
        st.subheader("🌳 Tech Tree de Requisitos Recursivos")
        st.write(
            "Descubra a cadeia completa de ingredientes, máquinas de refino, custos de animais e construções para obter qualquer item:"
        )

        all_items = get_all_possible_items(db)

        if not all_items:
            st.warning(
                "Tabelas vazias ou não encontradas. Atualize a base de dados primeiro."
            )
        else:
            # Campo de busca com autocomplemento
            selected_item = st.selectbox(
                "Digite ou selecione o item para rastrear:",
                options=all_items,
                index=(
                    all_items.index("Queijo de cabra")
                    if "Queijo de cabra" in all_items
                    else 0
                ),
            )

            max_depth = st.slider("Profundidade máxima de busca na árvore:", 1, 8, 5)

            if selected_item:
                # Resolve a árvore recursivamente
                tree = build_tree_data(selected_item, qty=1, max_depth=max_depth, db=db)

                col_tree, col_diagram = st.columns([1, 1])

                with col_tree:
                    st.markdown("### 📋 Árvore de Requisitos Detalhada")
                    text_tree = get_full_text_tree(tree)
                    st.markdown(f"```text\n{text_tree}```")

                with col_diagram:
                    st.markdown("### 🔀 Diagrama de Dependências (Mermaid)")
                    mermaid_code = generate_mermaid_graph(tree)
                    st.markdown(f"```mermaid\n{mermaid_code}\n```")

                    st.info(
                        "💡 Legenda dos ícones: ⚙️ Máquina | 🪵 Artesanato | 🌾 Refino | 🌱 Semente | 🌳 Muda | 🐄 Animal | 🛖 Construção | 🪙 Ouro"
                    )

    # ------------------ ABA 5: ATUALIZAR BASE ------------------
    with tab_update:
        st.subheader("🔄 Central de Atualização de Banco de Dados (ETL)")
        st.write("Execute processos de limpeza e estruturação de dados em tempo real:")

        st.markdown(
            """
        <div class="card">
            <h4>1. Processamento e Compilação Local</h4>
            <p>Roda os scripts de migração locais para gerar arquivos CSV em docs_bronze edocs_silver.
            Utiliza os arquivos HTML brutos que já estão baixados localmente na pasta docs_raw/.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button("Executar Recompilação Local (Rápido) 🚀"):
            with st.status("Processando dados locais...", expanded=True) as status:
                try:
                    st.write(
                        "Passo 1: Lendo arquivos de `docs_raw` e parseando tabelas para `docs_bronze`..."
                    )
                    run_process_pipeline()
                    st.write(
                        "Passo 2: Compilando, limpando e enriquecendo dados para `docs_silver`..."
                    )
                    run_enrich_pipeline()
                    status.update(
                        label="Recompilação concluída com sucesso! 🎉",
                        state="complete",
                        expanded=False,
                    )
                    st.success("Tabelas locais re-processadas e enriquecidas!")
                    st.rerun()
                except Exception as e:
                    status.update(
                        label="Falha no pipeline de recompilação local!", state="error"
                    )
                    st.error(f"Erro detalhado: {e}")

        st.write("---")

        st.markdown(
            """
        <div class="card">
            <h4>2. Baixar Dados da Wiki Oficial e Recompilar</h4>
            <p><strong>Cuidado:</strong> Esse processo faz web scraping de cerca de 64 páginas da wiki oficial de Stardew Valley.
            Pode demorar entre 1 a 2 minutos para concluir devido à velocidade de rede e limites de requisição.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button("Baixar Dados da Wiki e Recompilar Completo (Demorado) 🌐"):
            with st.status("Extraindo dados da Wiki...", expanded=True) as status:
                try:
                    st.write(
                        "Passo 1: Conectando com a Stardew Valley Wiki e baixando páginas HTML..."
                    )
                    import src.extract_bs4 as extract

                    extract.extrair_sopa()

                    st.write(
                        "Passo 2: Parseando arquivos de `docs_raw` para `docs_bronze`..."
                    )
                    run_process_pipeline()

                    st.write("Passo 3: Limpando e salvando tabelas em `docs_silver`...")
                    run_enrich_pipeline()

                    status.update(
                        label="Web Scraping e Recompilação Concluídos! 🎉",
                        state="complete",
                        expanded=False,
                    )
                    st.success(
                        "Todas as tabelas foram atualizadas da Wiki e re-processadas!"
                    )
                    st.rerun()
                except Exception as e:
                    status.update(
                        label="Falha no pipeline completo de scraping!", state="error"
                    )
                    st.error(f"Erro detalhado: {e}")


if __name__ == "__main__":
    main()
