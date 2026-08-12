import streamlit as st
from groq import Groq
from datetime import datetime, date, timedelta
import json
import random

st.set_page_config(page_title="TUTOR DE CONCURSOS IA", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500;600&display=swap');

    .stApp { background- color: #000000; font-family: 'DM Sans', sans-serif; }
    [data-testid="stSidebar"] { display: none; }

    .stTextInput>div>div>input,
    .stTextArea>div>textarea,
    .stSelectbox>div>div>div,
    .stNumberInput>div>div>input {
        background-color: #FFFBEB !important;
        color: #000000 !important;
        border: 1px solid #FCD34D !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background: linear-gradient(135deg, #D97706, #F59E0B) !important;
        color: white !important; font-weight: 600; border: none;
        box-shadow: 2px 2px 8px rgba(217,119,6,0.25);
        font-family: 'DM Sans', sans-serif !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover { background: linear-gradient(135deg, #B45309, #D97706) !important; transform: translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color: white !important; }

    .stApp h1, .stApp h2, .stApp h3 { font-family: 'Playfair Display', serif !important; color: #1A1A2E !important; }

    .card { background: linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:22px; border-radius:16px; border:1px solid #FCD34D; margin-bottom:15px; white-space:pre-wrap; box-shadow:0 2px 12px rgba(217,119,6,0.08); }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color: #1A1A2E !important; }

    .card-dark { background:linear-gradient(135deg,#1C1100,#2D1A00); padding:22px; border-radius:16px; border:1px solid #D97706; margin-bottom:15px; white-space:pre-wrap; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#FDE68A !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:22px; border-radius:16px; border:1px solid #93C5FD; margin-bottom:15px; white-space:pre-wrap; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:22px; border-radius:16px; border:1px solid #86EFAC; margin-bottom:15px; white-space:pre-wrap; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:22px; border-radius:16px; border:1px solid #FECACA; margin-bottom:15px; white-space:pre-wrap; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-purple { background:linear-gradient(135deg,#F5F3FF,#EDE9FE); padding:22px; border-radius:16px; border:1px solid #C4B5FD; margin-bottom:15px; white-space:pre-wrap; }
    .stApp .card-purple, .stApp .card-purple p, .stApp .card-purple span, .stApp .card-purple div { color:#4C1D95 !important; }

    .painel-exec { background:linear-gradient(135deg,#1A1A2E,#16213E); border:2px solid #F59E0B; border-radius:20px; padding:28px; margin-bottom:20px; }
    .stApp .painel-exec, .stApp .painel-exec p, .stApp .painel-exec span, .stApp .painel-exec div, .stApp .painel-exec strong { color:#FDE68A !important; }

    .indice-box { background:linear-gradient(135deg,#D97706,#F59E0B); border-radius:18px; padding:24px; text-align:center; box-shadow:0 4px 24px rgba(217,119,6,0.3); margin-bottom:16px; }
    .stApp .indice-box, .stApp .indice-box p, .stApp .indice-box span, .stApp .indice-box div { color:white !important; }
    .indice-numero { font-size:3.5em; font-weight:700; font-family:'Playfair Display',serif; color:white !important; }
    .stApp .indice-numero { color:white !important; }

    .card-orange { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:22px; border-radius:16px; border:1px solid #FCD34D; margin-bottom:15px; white-space:pre-wrap; }
    .stApp .card-orange, .stApp .card-orange p, .stApp .card-orange span,
    .stApp .card-orange div, .stApp .card-orange strong, .stApp .card-orange em { color:#1A1A2E !important; }

    .missao-box { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); border:2px solid #16A34A; border-radius:16px; padding:20px; margin-bottom:16px; }
    .stApp .missao-box, .stApp .missao-box p, .stApp .missao-box span, .stApp .missao-box div, .stApp .missao-box strong { color:#14532D !important; }

    .xp-box { background:linear-gradient(135deg,#F5F3FF,#EDE9FE); border:2px solid #7C3AED; border-radius:16px; padding:20px; text-align:center; margin-bottom:16px; }
    .stApp .xp-box, .stApp .xp-box p, .stApp .xp-box span, .stApp .xp-box div { color:#4C1D95 !important; }

    .conquista-item { background:#FFFBEB; border:1px solid #FCD34D; border-radius:10px; padding:12px 16px; margin-bottom:8px; display:inline-block; margin:4px; }
    .stApp .conquista-item, .stApp .conquista-item p, .stApp .conquista-item span { color:#92400E !important; }

    .radar-item { background:#F8FAFC; border-radius:10px; padding:10px 16px; margin-bottom:6px; border-left:4px solid #F59E0B; }
    .stApp .radar-item, .stApp .radar-item p, .stApp .radar-item span, .stApp .radar-item div { color:#1A1A2E !important; }

    .streak-box { background:linear-gradient(135deg,#FEF3C7,#FFFBEB); border:2px solid #F59E0B; border-radius:16px; padding:20px; text-align:center; margin-bottom:16px; }
    .stApp .streak-box, .stApp .streak-box p, .stApp .streak-box span, .stApp .streak-box div { color:#92400E !important; }


    .stat-box { background:#FFFBEB; border-radius:12px; padding:18px; text-align:center; border:1px solid #FCD34D; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#1A1A2E !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#D97706 !important; font-family:'Playfair Display',serif; }

    .hist-item { background:#FFFBEB; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #F59E0B; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#1A1A2E !important; }

    .badge { background:#D97706; color:white !important; padding:4px 14px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 14px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 14px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#7C3AED; color:white !important; padding:4px 14px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-red { background:#EF4444; color:white !important; padding:4px 14px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .perfil-btn>button { background:linear-gradient(135deg,#D97706,#F59E0B) !important; color:white !important; font-weight:700 !important; border-radius:12px !important; height:3em !important; }
    .perfil-btn>button, .perfil-btn>button p, .perfil-btn>button span { color:white !important; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#FCD34D,transparent); margin:20px 0; }
    .questao-box { background:#FFFFFF; border:2px solid #FCD34D; border-radius:14px; padding:20px; margin-bottom:16px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#1A1A2E !important; }

    /* Garante que texto normal (fora de cards) seja sempre preto no fundo branco */
    .stApp > div > div > div > div { color: #1A1A2E; }
    .stMarkdown p, .stMarkdown span, .stMarkdown div { color: #1A1A2E !important; }
    </style>
""", unsafe_allow_html=True)

# ─── CACHE ───
@st.cache_resource
def get_cache_tutor():
    return {"perfis": {}}
_cache = get_cache_tutor()

# ─── NÍVEIS E XP ───
NIVEIS = [
    (0,    "Iniciante",   "🌱"),
    (100,  "Aprendiz",    "📚"),
    (300,  "Persistente", "💪"),
    (600,  "Estudioso",   "🎯"),
    (1000, "Especialista","⭐"),
    (1500, "Elite",       "🏆"),
    (2500, "Aprovado",    "🎓"),
]
XP_ATIVIDADES = {
    'questao_certa': 10, 'questao_errada': 2, 'resumo': 20,
    'flashcard': 15, 'simulado': 50, 'revisao': 15,
    'plano': 25, 'mapa_mental': 20, 'missao_dia': 30,
}

def calcular_nivel(xp: int):
    nivel_atual = NIVEIS[0]
    for req_xp, nome, emoji in NIVEIS:
        if xp >= req_xp:
            nivel_atual = (req_xp, nome, emoji)
    return nivel_atual

def xp_proximo_nivel(xp: int):
    for i, (req_xp, nome, emoji) in enumerate(NIVEIS):
        if xp < req_xp:
            return req_xp
    return NIVEIS[-1][0]

# ─── CONQUISTAS ───
CONQUISTAS_DEF = [
    ("primeira_questao",   "🎯 Primeira Questão",      "Respondeu sua primeira questão"),
    ("questoes_100",       "💯 Centenário",             "100 questões respondidas"),
    ("questoes_1000",      "🏆 Guerreiro",              "1.000 questões respondidas"),
    ("primeiro_resumo",    "📝 Primeiro Resumo",        "Criou seu primeiro resumo"),
    ("primeiro_plano",     "📅 Planejador",             "Criou seu primeiro plano de estudos"),
    ("primeiro_simulado",  "📊 Simulador",              "Realizou seu primeiro simulado"),
    ("streak_7",           "🔥 7 Dias",                 "7 dias consecutivos de estudo"),
    ("streak_30",          "⚡ 30 Dias",                "30 dias consecutivos de estudo"),
    ("horas_100",          "⏱️ 100 Horas",              "100 horas de estudo acumuladas"),
    ("acerto_90",          "🎯 Mira Certeira",          "Taxa de acerto acima de 90%"),
    ("especialista_mat",   "🔢 Especialista em Matemática", "Acerto >80% em Matemática"),
    ("especialista_port",  "📖 Especialista em Português",  "Acerto >80% em Português"),
    ("especialista_dir",   "⚖️ Especialista em Direito",    "Acerto >80% em Direito"),
    ("nivel_elite",        "🌟 Elite",                  "Atingiu o nível Elite"),
    ("aprovado",           "🎓 Aprovado",               "Atingiu o nível Aprovado"),
]

def verificar_conquistas():
    conquistadas = st.session_state.get('conquistas', [])
    novas = []
    q = st.session_state.questoes_respondidas
    xp = st.session_state.pontuacao_total
    streak = st.session_state.get('streak_atual', 0)
    horas = st.session_state.get('horas_acumuladas', 0)
    taxa = (st.session_state.questoes_certas / max(q,1)) * 100

    checks = [
        ("primeira_questao", q >= 1),
        ("questoes_100", q >= 100),
        ("questoes_1000", q >= 1000),
        ("primeiro_resumo", any(e['tipo']=='Resumo' for e in st.session_state.historico_estudos)),
        ("primeiro_plano", any(e['tipo']=='Plano' for e in st.session_state.historico_estudos)),
        ("primeiro_simulado", any(e['tipo']=='Simulado' for e in st.session_state.historico_estudos)),
        ("streak_7", streak >= 7),
        ("streak_30", streak >= 30),
        ("horas_100", horas >= 100),
        ("acerto_90", taxa >= 90 and q >= 20),
        ("nivel_elite", xp >= 1500),
        ("aprovado", xp >= 2500),
    ]
    for chave, condicao in checks:
        if condicao and chave not in conquistadas:
            conquistadas.append(chave)
            novas.append(chave)
    st.session_state['conquistas'] = conquistadas
    return novas

def calcular_indice_preparacao():
    q = st.session_state.questoes_respondidas
    xp = st.session_state.pontuacao_total
    streak = st.session_state.get('streak_atual', 0)
    horas = st.session_state.get('horas_acumuladas', 0)
    taxa = (st.session_state.questoes_certas / max(q,1)) * 100 if q > 0 else 0

    score = 0
    score += min(taxa * 0.35, 35)
    score += min((q / 500) * 25, 25)
    score += min((horas / 200) * 20, 20)
    score += min((streak / 30) * 10, 10)
    score += min((xp / 2000) * 10, 10)
    return int(min(score, 100))

def classificar_indice(idx):
    if idx >= 85: return "Elite", "Muito Alta", "#059669"
    if idx >= 70: return "Avançado", "Alta", "#16A34A"
    if idx >= 55: return "Intermediário", "Moderada", "#D97706"
    if idx >= 40: return "Básico", "Baixa", "#EA580C"
    return "Iniciante", "Muito Baixa", "#DC2626"

MOTIVACOES = [
    "Cada questão respondida hoje é um passo que seu concorrente não deu.",
    "A aprovação não acontece em um dia — ela acontece em cada dia.",
    "Disciplina é escolher, repetidamente, o que importa sobre o que é fácil.",
    "O estudo de hoje é o cargo de amanhã.",
    "Você não está competindo com os outros — está competindo com quem você era ontem.",
    "Consistência vence talento quando o talento não é consistente.",
    "Cada hora estudada reduz a distância entre você e a aprovação.",
    "A banca não mede esforço — mede domínio. Domine.",
    "O candidato que estuda agora é o servidor que comemora depois.",
    "Cansaço é temporário. Aprovação é permanente.",
]

# ─── PERSISTÊNCIA ───
CHAVES_SALVAR = [
    'usuario','historico_estudos','biblioteca_materiais',
    'concurso_foco','materias_foco','horas_disponiveis',
    'nivel_conhecimento','data_prova','cargo_foco','nota_necessaria',
    'dias_disponiveis','experiencia_anterior','maior_dificuldade',
    'maior_facilidade','metodo_preferido','instituicao',
    'pontuacao_total','questoes_respondidas','questoes_certas',
    'streak_atual','maior_streak','horas_acumuladas',
    'ultima_atividade','dias_estudo','conquistas',
    'radar_materias','missao_hoje','meta_semanal_h',
    'meta_semanal_q','horas_semana','questoes_semana',
    'historico_simulados',
]

def gerar_json_sessao():
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados):
    for k in CHAVES_SALVAR:
        if k in dados:
            st.session_state[k] = dados[k]

def salvar_perfil_cache(u):
    _cache["perfis"][u] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos():
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(u):
    return _cache["perfis"].get(u)

def salvar_estudo(tipo, materia, conteudo):
    st.session_state.historico_estudos.append({
        'data': datetime.now().strftime('%d/%m %H:%M'),
        'tipo': tipo, 'materia': materia, 'conteudo': conteudo,
    })
    st.session_state['ultima_atividade'] = f"{tipo} — {materia}"
    st.session_state['dias_estudo'] = st.session_state.get('dias_estudo', 0) + 1

def ganhar_xp(atividade: str, quantidade: int = 1):
    xp = XP_ATIVIDADES.get(atividade, 10) * quantidade
    st.session_state.pontuacao_total = st.session_state.get('pontuacao_total', 0) + xp
    novas = verificar_conquistas()
    return xp, novas

def atualizar_streak():
    hoje = date.today().isoformat()
    ultimo_dia = st.session_state.get('ultimo_dia_estudo', '')
    if ultimo_dia == hoje:
        return
    ontem = (date.today() - timedelta(days=1)).isoformat()
    if ultimo_dia == ontem:
        st.session_state.streak_atual = st.session_state.get('streak_atual', 0) + 1
    else:
        st.session_state.streak_atual = 1
    if st.session_state.streak_atual > st.session_state.get('maior_streak', 0):
        st.session_state.maior_streak = st.session_state.streak_atual
    st.session_state['ultimo_dia_estudo'] = hoje

# ─── DEFAULTS ───
defaults = {
    'etapa': "Login", 'usuario': "", 'api_key': "", 'pagina': "Home",
    'historico_estudos': [], 'biblioteca_materiais': [],
    'concurso_foco': "", 'materias_foco': "", 'horas_disponiveis': "2",
    'nivel_conhecimento': "Iniciante", 'data_prova': "", 'cargo_foco': "",
    'nota_necessaria': "", 'dias_disponiveis': "5", 'experiencia_anterior': "Nenhuma",
    'maior_dificuldade': "", 'maior_facilidade': "", 'metodo_preferido': "Misto",
    'instituicao': "",
    'pontuacao_total': 0, 'questoes_respondidas': 0, 'questoes_certas': 0,
    'streak_atual': 0, 'maior_streak': 0, 'horas_acumuladas': 0,
    'ultima_atividade': "Nenhuma", 'dias_estudo': 0, 'conquistas': [],
    'radar_materias': {}, 'missao_hoje': None, 'ultimo_dia_estudo': '',
    'meta_semanal_h': 10, 'meta_semanal_q': 100,
    'horas_semana': 0, 'questoes_semana': 0,
    'questoes_ativas': [], 'respondendo_idx': 0, 'respostas_sessao': [],
    'historico_simulados': [],
    'relampago_historico': [],
    'relampago_fase': 'menu',
    'relampago_tema': '',
    'relampago_modo': 'Desafio',
    'relampago_planejamento': {},
    'relampago_redacao': '',
    'relampago_aval_plano': '',
    'relampago_aval_redacao': '',
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── MOTOR DE IA ───
def tutor_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        perfil = (
            f"Aluno: {st.session_state.usuario}. "
            f"Concurso: {st.session_state.concurso_foco or 'não definido'}. "
            f"Cargo: {st.session_state.cargo_foco or 'não definido'}. "
            f"Nível: {st.session_state.nivel_conhecimento}. "
            f"Matérias foco: {st.session_state.materias_foco or 'não definidas'}. "
            f"Maior dificuldade: {st.session_state.maior_dificuldade or 'não informada'}. "
            f"Método preferido: {st.session_state.metodo_preferido}. "
            f"Índice de preparação: {calcular_indice_preparacao()}%. "
            f"XP: {st.session_state.pontuacao_total}. "
            f"Taxa de acerto: {int(st.session_state.questoes_certas/max(st.session_state.questoes_respondidas,1)*100)}%."
        )
        system = (
            f"Você é o Tutor de Concursos IA — um mentor estratégico de preparação para concursos públicos brasileiros. "
            f"Você acompanha toda a jornada do aluno, identifica padrões, explica o raciocínio por trás de cada decisão "
            f"e mantém o foco no objetivo final: a aprovação. "
            f"Sempre baseie conselhos no perfil real do aluno. Nunca seja genérico. "
            f"Português do Brasil. {perfil} {system_extra}"
        )
        response = client.chat.completions.create(
            messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
            model="llama-3.3-70b-versatile",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

# ─── BARRA SALVAR ───
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_u = st.session_state.usuario.lower().replace(' ','_') or 'sessao'
    col_info, col_btn = st.columns([4, 2])
    with col_info:
        xp = st.session_state.pontuacao_total
        _, nivel_nome, nivel_emoji = calcular_nivel(xp)
        concurso = st.session_state.concurso_foco or "—"
        st.markdown(
            f"<div style='background:#FFFBEB;border:1px solid #FCD34D;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Salve seus dados antes de sair.</strong><br>"
            f"<span style='color:#D97706;font-size:0.88em;'>{nivel_emoji} {nivel_nome} · "
            f"{xp} XP · {concurso}</span>"
            f"</div>", unsafe_allow_html=True)
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button("💾 SALVAR DADOS (.json)", data=gerar_json_sessao(),
            file_name=f"tutor_{nome_u}.json", mime="application/json", use_container_width=True)
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ============================================================
# LOGIN
# ============================================================
if st.session_state.etapa == "Login":
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("🎓 TUTOR DE CONCURSOS IA")
        st.markdown("**Seu mentor estratégico de preparação para concursos públicos.**")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div style="background:#FFFBEB;border:1px solid #FCD34D;border-radius:10px;
        padding:12px 16px;margin-bottom:16px;font-size:0.88em;color:#1A1A2E;line-height:1.6;">
        🔒 <strong>ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</strong><br>
        🔗 <a href='https://quizcompremios.com.br/' target='_blank'
        style='color:#D97706;font-weight:600;text-decoration:none;'>quizcompremios.com.br</a>
        </div>""", unsafe_allow_html=True)
        st.markdown("""<div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:10px;
        padding:10px 16px;margin-bottom:16px;font-size:0.82em;color:#14532D;line-height:1.7;">
        🔒 <strong>Privacidade:</strong> seus dados ficam apenas no seu computador.<br>
        📥 Exporte o backup a qualquer momento. Nada é enviado para servidores.
        </div>""", unsafe_allow_html=True)

        perfis = perfis_salvos()
        if perfis:
            chave_r = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_rapida")
            for np in perfis:
                dp = carregar_perfil_cache(np)
                xp_p = dp.get('pontuacao_total',0) if dp else 0
                _, nv, em = calcular_nivel(xp_p)
                st.markdown('<div class="perfil-btn">', unsafe_allow_html=True)
                if st.button(f"🎓 {np}  ·  {em} {nv}  ·  {xp_p} XP", key=f"perfil_{np}", use_container_width=True):
                    if not chave_r.strip():
                        st.warning("Cole sua chave API acima.")
                    else:
                        st.session_state.usuario = np
                        st.session_state.api_key = chave_r
                        carregar_json_sessao(dp)
                        st.session_state.etapa = "App"
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        nome = st.text_input("Seu Nome:", key="input_nome_login")
        chave = st.text_input("Sua Chave API da Groq:", type="password", key="chave_nova")

        if not perfis:
            arq = st.file_uploader("Restaurar Backup (.json):", type=["json"], key="upload_login")
        else:
            arq = None

        dados_login = None
        if arq is not None:
            try:
                dados_login = json.load(arq)
                st.success(f"✅ Backup de **{dados_login.get('usuario','')}** reconhecido!")
            except Exception:
                st.error("Arquivo inválido.")

        if st.button("🎓 ENTRAR E ESTUDAR"):
            if nome and chave:
                st.session_state.usuario = nome
                st.session_state.api_key = chave
                if dados_login:
                    carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")
        st.markdown("🔑 Crie grátis em <a href='https://console.groq.com/keys' target='_blank' style='color:#D97706;'>console.groq.com/keys</a>", unsafe_allow_html=True)


# ============================================================
# APP
# ============================================================
elif st.session_state.etapa == "App":

    atualizar_streak()
    barra_salvar()

    # NAVBAR linha 1
    cols1 = st.columns(9)
    nav1 = [("🏠","Home"),("📊","Painel"),("📋","Perfil"),("📅","Plano"),("📝","Resumo"),
            ("❓","Questoes"),("🧠","Memoria"),("🔄","Revisao"),("🎯","Simulado")]
    lb1 = {"Home":"Início","Painel":"Painel Executivo","Perfil":"Meu Perfil Completo",
           "Plano":"Plano de Estudos","Resumo":"Criar Resumo","Questoes":"Resolver Questões",
           "Memoria":"Flashcards","Revisao":"Revisão Espaçada","Simulado":"Simulado Inteligente"}
    for i,(ic,pg) in enumerate(nav1):
        if cols1[i].button(ic, key=f"nav1_{pg}", help=lb1[pg]):
            st.session_state.pagina = pg; st.rerun()

    # NAVBAR linha 2
    cols2 = st.columns(10)
    nav2 = [("💬","Tutor"),("📚","Biblioteca"),("📈","Progresso"),("🏆","Conquistas"),
            ("🎮","Evolucao"),("📡","Radar"),("📊","Relatorio"),("🧭","Diagnostico"),("❤️","Salvos"),("⚡","Relampago")]
    lb2 = {"Tutor":"Tutor Inteligente","Biblioteca":"Biblioteca de Materiais",
           "Progresso":"Estatísticas e Progresso","Conquistas":"Minhas Conquistas",
           "Evolucao":"XP e Gamificação","Radar":"Radar das Disciplinas",
           "Relatorio":"Relatório Semanal","Diagnostico":"Diagnóstico Inteligente",
           "Salvos":"Materiais Salvos","Relampago":"⚡ Redação Tema Relâmpago"}
    for i,(ic,pg) in enumerate(nav2):
        if cols2[i].button(ic, key=f"nav2_{pg}", help=lb2[pg]):
            st.session_state.pagina = pg; st.rerun()

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # HOME
    # ──────────────────────────────────────────
    if st.session_state.pagina == "Home":
        col_u, col_r = st.columns([3,1])
        with col_u:
            st.title(f"🎓 Olá, {st.session_state.usuario}!")
            concurso = st.session_state.concurso_foco or "Não definido"
            xp = st.session_state.pontuacao_total
            _, nivel_nome, nivel_emoji = calcular_nivel(xp)
            st.markdown(f"<span class='badge'>{nivel_emoji} {nivel_nome}</span> <span class='badge-azul'>🎯 {concurso}</span>", unsafe_allow_html=True)
        with col_r:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚪 Sair"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        if not st.session_state.concurso_foco:
            st.markdown("""<div style="background:#FFFBEB;border:2px solid #F59E0B;border-radius:12px;
            padding:16px 20px;margin-bottom:16px;">
            <span style='font-size:1em;font-weight:600;color:#92400E;'>
            ⚡ Comece pelo 📋 Perfil — configure seu concurso, matérias e data da prova para ativar todos os recursos.
            </span></div>""", unsafe_allow_html=True)
        else:
            # RECUPERAR BACKUP
            if len(st.session_state.historico_estudos) == 0:
                arq_home = st.file_uploader("Restaurar Backup (.json):", type=["json"], key="upload_home")
                if arq_home is not None:
                    try:
                        d = json.load(arq_home)
                        carregar_json_sessao(d)
                        salvar_perfil_cache(st.session_state.usuario)
                        st.success("✅ Backup restaurado!")
                        st.rerun()
                    except Exception:
                        st.error("Arquivo inválido.")

        # CABEÇALHO INSTITUCIONAL
        dias_restantes = "—"
        if st.session_state.data_prova:
            try:
                dp = datetime.strptime(st.session_state.data_prova, "%Y-%m-%d").date()
                dias_restantes = (dp - date.today()).days
                if dias_restantes < 0:
                    dias_restantes = "Prova passada"
            except Exception:
                dias_restantes = "—"

        ultima = st.session_state.get('ultima_atividade', 'Nenhuma')
        st.markdown(f"""
        <div class='painel-exec'>
            <div style='font-size:0.85em;opacity:0.7;letter-spacing:2px;margin-bottom:8px;'>🎓 MENTOR INTELIGENTE DE ESTUDOS</div>
            <div style='font-size:1.1em;opacity:0.7;margin-bottom:16px;'>Seu treinador pessoal com Inteligência Artificial · <span style='color:#22C55E;'>🟢 IA Online</span></div>
            <div style='display:flex;flex-wrap:wrap;gap:20px;'>
                <div><div style='font-size:0.75em;opacity:0.6;'>🎯 OBJETIVO</div><div style='font-size:1.1em;font-weight:700;'>{st.session_state.concurso_foco or "—"} {("— " + st.session_state.cargo_foco) if st.session_state.cargo_foco else ""}</div></div>
                <div><div style='font-size:0.75em;opacity:0.6;'>📅 DIAS RESTANTES</div><div style='font-size:1.1em;font-weight:700;'>{dias_restantes}</div></div>
                <div><div style='font-size:0.75em;opacity:0.6;'>🔥 SEQUÊNCIA</div><div style='font-size:1.1em;font-weight:700;'>{st.session_state.get("streak_atual",0)} dias</div></div>
                <div><div style='font-size:0.75em;opacity:0.6;'>📖 ÚLTIMA ATIVIDADE</div><div style='font-size:1.1em;font-weight:700;'>{ultima}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ÍNDICE DE PREPARAÇÃO
        idx = calcular_indice_preparacao()
        nivel_idx, prob, cor = classificar_indice(idx)
        col_idx, col_mot = st.columns([1, 2])
        with col_idx:
            st.markdown(f"""
            <div class='indice-box'>
                <div style='font-size:0.85em;opacity:0.8;'>ÍNDICE DE PREPARAÇÃO</div>
                <div class='indice-numero'>{idx}%</div>
                <div style='font-size:0.9em;'>Nível: <strong>{nivel_idx}</strong></div>
                <div style='font-size:0.85em;opacity:0.8;'>Prob. estimada: {prob}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_mot:
            frase_mot = random.choice(MOTIVACOES)
            streak = st.session_state.get('streak_atual', 0)
            if streak > 0:
                frase_mot = f"Você está há {streak} dias consecutivos estudando. {frase_mot}"
            st.markdown(f"<div class='card' style='height:120px;display:flex;align-items:center;'><em>💡 {frase_mot}</em></div>", unsafe_allow_html=True)

        # DASHBOARD
        st.markdown("### 📊 Dashboard")
        q = st.session_state.questoes_respondidas
        c_q = st.session_state.questoes_certas
        e_q = q - c_q
        taxa = int(c_q/max(q,1)*100)
        xp = st.session_state.pontuacao_total
        horas = st.session_state.get('horas_acumuladas', 0)
        resumos = sum(1 for e in st.session_state.historico_estudos if e['tipo']=='Resumo')
        flashcards = sum(1 for e in st.session_state.historico_estudos if e['tipo']=='Flashcard')
        simulados = sum(1 for e in st.session_state.historico_estudos if e['tipo']=='Simulado')
        cronogramas = sum(1 for e in st.session_state.historico_estudos if e['tipo']=='Plano')

        d1,d2,d3,d4,d5,d6 = st.columns(6)
        d1.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.get('streak_atual',0)}</div><div>Dias seguidos</div></div>", unsafe_allow_html=True)
        d2.markdown(f"<div class='stat-box'><div class='stat-numero'>{horas:.0f}h</div><div>Horas acumuladas</div></div>", unsafe_allow_html=True)
        d3.markdown(f"<div class='stat-box'><div class='stat-numero'>{q}</div><div>Questões</div></div>", unsafe_allow_html=True)
        d4.markdown(f"<div class='stat-box'><div class='stat-numero'>{taxa}%</div><div>Acertos</div></div>", unsafe_allow_html=True)
        d5.markdown(f"<div class='stat-box'><div class='stat-numero'>{resumos}</div><div>Resumos</div></div>", unsafe_allow_html=True)
        d6.markdown(f"<div class='stat-box'><div class='stat-numero'>{xp}</div><div>XP Total</div></div>", unsafe_allow_html=True)

        d7,d8,d9,d10,d11,d12 = st.columns(6)
        d7.markdown(f"<div class='stat-box'><div class='stat-numero'>{flashcards}</div><div>Flashcards</div></div>", unsafe_allow_html=True)
        d8.markdown(f"<div class='stat-box'><div class='stat-numero'>{simulados}</div><div>Simulados</div></div>", unsafe_allow_html=True)
        d9.markdown(f"<div class='stat-box'><div class='stat-numero'>{cronogramas}</div><div>Planos</div></div>", unsafe_allow_html=True)
        d10.markdown(f"<div class='stat-box'><div class='stat-numero'>{c_q}</div><div>Certas</div></div>", unsafe_allow_html=True)
        d11.markdown(f"<div class='stat-box'><div class='stat-numero'>{e_q}</div><div>Erradas</div></div>", unsafe_allow_html=True)
        d12.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.get('maior_streak',0)}</div><div>Recorde dias</div></div>", unsafe_allow_html=True)

        # MISSÃO DO DIA
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        col_miss, col_meta = st.columns(2)
        with col_miss:
            st.markdown("### ⚡ Missão do Dia")
            if not st.session_state.get('missao_hoje'):
                if st.button("⚡ GERAR MISSÃO DO DIA"):
                    with st.spinner("Gerando missão personalizada..."):
                        materia_critica = st.session_state.maior_dificuldade or st.session_state.materias_foco or "a matéria mais importante do seu concurso"
                        missao_prompt = (
                            f"Crie uma missão de estudo para hoje para o aluno preparando {st.session_state.concurso_foco or 'concurso público'}.\n"
                            f"Horas disponíveis: {st.session_state.horas_disponiveis}h. Maior dificuldade: {materia_critica}.\n"
                            f"Formato:\n\n"
                            f"⚡ MISSÃO DO DIA\n\n"
                            f"[3-4 tarefas específicas com tempo estimado cada]\n\n"
                            f"⏱️ Tempo total previsto: [X]h[Y]min\n"
                            f"🏆 Recompensa: +[XP] XP\n\n"
                            f"💡 Por que essa missão hoje: [1 linha explicando a estratégia]"
                        )
                        missao = tutor_ia(missao_prompt)
                        st.session_state.missao_hoje = missao
                        st.rerun()
            else:
                st.markdown(f"<div class='missao-box'>{st.session_state.missao_hoje}</div>", unsafe_allow_html=True)
                col_ok, col_re = st.columns(2)
                with col_ok:
                    if st.button("✅ MISSÃO CONCLUÍDA!", key="missao_ok"):
                        xp_g, novas = ganhar_xp('missao_dia')
                        st.success(f"🏆 +{xp_g} XP! Excelente trabalho!")
                        st.session_state.missao_hoje = None
                        st.rerun()
                with col_re:
                    if st.button("🔄 Nova missão", key="missao_re"):
                        st.session_state.missao_hoje = None
                        st.rerun()

        with col_meta:
            st.markdown("### 📆 Meta Semanal")
            h_prev = st.session_state.get('meta_semanal_h', 10)
            h_feito = st.session_state.get('horas_semana', 0)
            q_prev = st.session_state.get('meta_semanal_q', 100)
            q_feito = st.session_state.get('questoes_semana', 0)
            pct_h = min(int(h_feito/max(h_prev,1)*100), 100)
            pct_q = min(int(q_feito/max(q_prev,1)*100), 100)
            st.markdown(f"**⏱️ Horas:** {h_feito}/{h_prev}h ({pct_h}%)")
            st.progress(pct_h/100)
            st.markdown(f"**❓ Questões:** {q_feito}/{q_prev} ({pct_q}%)")
            st.progress(pct_q/100)
            col_ma, col_mb = st.columns(2)
            with col_ma:
                if st.button("➕ +1h estudada"):
                    st.session_state.horas_semana = h_feito + 1
                    st.session_state.horas_acumuladas = st.session_state.get('horas_acumuladas',0) + 1
                    st.rerun()
            with col_mb:
                if st.button("⚙️ Definir metas", key="def_metas"):
                    st.session_state.pagina = "Progresso"; st.rerun()

        # ÚLTIMAS ATIVIDADES
        if st.session_state.historico_estudos:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("### 🕐 Últimas Atividades")
            for item in reversed(st.session_state.historico_estudos[-4:]):
                st.markdown(f"<div class='hist-item'><span class='badge'>{item['tipo']}</span> <small style='color:#888'>{item['data']}</small><br><small>{item['materia'][:80]}</small></div>", unsafe_allow_html=True)


    # ──────────────────────────────────────────
    # PAINEL EXECUTIVO
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Painel":
        st.header("📊 Painel Executivo")
        idx = calcular_indice_preparacao()
        nivel_idx, prob, cor = classificar_indice(idx)
        xp = st.session_state.pontuacao_total
        _, nivel_nome, nivel_emoji = calcular_nivel(xp)
        q = st.session_state.questoes_respondidas
        taxa = int(st.session_state.questoes_certas/max(q,1)*100)
        horas = st.session_state.get('horas_acumuladas', 0)
        streak = st.session_state.get('streak_atual', 0)
        pct_meta = min(int(st.session_state.get('horas_semana',0)/max(st.session_state.get('meta_semanal_h',10),1)*100), 100)
        dif = st.session_state.maior_dificuldade or "Não definida"

        # Calcular maior evolução
        materias_radar = st.session_state.get('radar_materias', {})
        maior_evolucao = max(materias_radar.items(), key=lambda x: x[1], default=("—", 0))

        # Variáveis para o HTML (evita expressões condicionais dentro de f-string)
        rec_dif = f"<strong>Maior dificuldade:</strong> {dif}. " if dif != "Não definida" else ""
        rec_acao = f"Priorize {dif} nos próximos dias e mantenha questões diárias." if dif != "Não definida" else "Configure seu perfil completo para recomendações personalizadas."

        st.markdown(f"""
        <div class='painel-exec'>
            <div style='font-size:1.3em;font-weight:700;margin-bottom:20px;letter-spacing:1px;'>🎓 PAINEL DO MENTOR — {st.session_state.usuario.upper()}</div>
            <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:20px;'>
                <div style='text-align:center;background:rgba(255,255,255,0.08);border-radius:12px;padding:16px;'>
                    <div style='font-size:0.72em;opacity:0.6;'>OBJETIVO</div>
                    <div style='font-size:1.1em;font-weight:700;'>{st.session_state.concurso_foco or "—"}</div>
                </div>
                <div style='text-align:center;background:rgba(255,255,255,0.08);border-radius:12px;padding:16px;'>
                    <div style='font-size:0.72em;opacity:0.6;'>ÍNDICE GERAL</div>
                    <div style='font-size:1.8em;font-weight:700;'>{idx}%</div>
                </div>
                <div style='text-align:center;background:rgba(255,255,255,0.08);border-radius:12px;padding:16px;'>
                    <div style='font-size:0.72em;opacity:0.6;'>HORAS ESTUDADAS</div>
                    <div style='font-size:1.8em;font-weight:700;'>{horas:.0f}h</div>
                </div>
                <div style='text-align:center;background:rgba(255,255,255,0.08);border-radius:12px;padding:16px;'>
                    <div style='font-size:0.72em;opacity:0.6;'>QUESTÕES</div>
                    <div style='font-size:1.8em;font-weight:700;'>{q}</div>
                </div>
            </div>
            <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:20px;'>
                <div style='text-align:center;background:rgba(255,255,255,0.08);border-radius:12px;padding:16px;'>
                    <div style='font-size:0.72em;opacity:0.6;'>TAXA DE ACERTO</div>
                    <div style='font-size:1.8em;font-weight:700;'>{taxa}%</div>
                </div>
                <div style='text-align:center;background:rgba(255,255,255,0.08);border-radius:12px;padding:16px;'>
                    <div style='font-size:0.72em;opacity:0.6;'>NÍVEL</div>
                    <div style='font-size:1.1em;font-weight:700;'>{nivel_emoji} {nivel_nome}</div>
                </div>
                <div style='text-align:center;background:rgba(255,255,255,0.08);border-radius:12px;padding:16px;'>
                    <div style='font-size:0.72em;opacity:0.6;'>DIAS CONSECUTIVOS</div>
                    <div style='font-size:1.8em;font-weight:700;'>{streak}</div>
                </div>
                <div style='text-align:center;background:rgba(255,255,255,0.08);border-radius:12px;padding:16px;'>
                    <div style='font-size:0.72em;opacity:0.6;'>META DA SEMANA</div>
                    <div style='font-size:1.8em;font-weight:700;'>{pct_meta}%</div>
                </div>
            </div>
            <div style='background:rgba(255,255,255,0.06);border-radius:12px;padding:16px;'>
                <div style='font-size:0.72em;opacity:0.6;margin-bottom:8px;'>🤖 RECOMENDAÇÃO DA IA</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Recomendação separada para evitar escape de HTML com variáveis
        st.markdown(
            f"<div style='background:rgba(26,26,46,0.05);border:1px solid #FCD34D;border-radius:12px;"
            f"padding:14px 18px;margin-top:-14px;margin-bottom:20px;font-size:0.95em;line-height:1.7;color:#1A1A2E;'>"
            f"{rec_dif}"
            f"Índice de preparação: <strong>{idx}%</strong> — Probabilidade estimada: <strong>{prob}</strong>. "
            f"{rec_acao}"
            f"</div>",
            unsafe_allow_html=True
        )

        if st.button("🤖 RECOMENDAÇÃO ESTRATÉGICA COMPLETA DA IA"):
            with st.spinner("Analisando seu perfil completo..."):
                prompt = (
                    f"Analise o perfil completo deste candidato e dê uma recomendação estratégica detalhada.\n"
                    f"Índice de preparação: {idx}%. Taxa de acerto: {taxa}%. Horas acumuladas: {horas}h. "
                    f"Questões respondidas: {q}. Streak: {streak} dias.\n"
                    f"Concurso: {st.session_state.concurso_foco}. Maior dificuldade: {dif}.\n\n"
                    f"FORMATO:\n\n"
                    f"📊 ANÁLISE ESTRATÉGICA\n\n"
                    f"✅ PONTOS FORTES:\n[o que está bem]\n\n"
                    f"⚠️ PONTOS CRÍTICOS:\n[o que precisa melhorar]\n\n"
                    f"🎯 PRIORIDADES PARA ESTA SEMANA:\n[ordem de estudo com justificativa]\n\n"
                    f"📈 PREVISÃO DE APROVAÇÃO:\n[estimativa honesta com base nos dados — sempre como estimativa, nunca garantia]\n\n"
                    f"🚀 AÇÃO IMEDIATA:\n[o que fazer hoje]"
                )
                res = tutor_ia(prompt)
                salvar_estudo("Análise Estratégica", "Painel Executivo", res)
                st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # PERFIL COMPLETO
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Perfil":
        st.header("📋 Meu Perfil Completo")
        st.markdown("*Configure uma vez — o tutor usa tudo isso para personalizar cada resposta.*")

        with st.form("form_perfil"):
            st.markdown("#### 🎯 Objetivo")
            col1, col2 = st.columns(2)
            with col1:
                p_concurso = st.text_input("Concurso:", value=st.session_state.concurso_foco, placeholder="ex: PRF, INSS, Receita Federal, TRT...")
                p_cargo = st.text_input("Cargo:", value=st.session_state.cargo_foco, placeholder="ex: Policial Rodoviário Federal, Analista...")
                p_instituicao = st.text_input("Instituição organizadora:", value=st.session_state.instituicao, placeholder="ex: CEBRASPE, FCC, VUNESP...")
            with col2:
                p_data = st.text_input("Data prevista da prova (AAAA-MM-DD):", value=st.session_state.data_prova, placeholder="ex: 2027-03-15")
                p_nota = st.text_input("Nota mínima necessária:", value=st.session_state.nota_necessaria, placeholder="ex: 60 pontos ou 50%")
                p_cidade = st.text_input("Cidade/UF onde fará a prova:", placeholder="ex: São Paulo - SP")

            st.markdown("#### 📚 Estudos")
            col3, col4 = st.columns(2)
            with col3:
                p_materias = st.text_area("Matérias do concurso:", value=st.session_state.materias_foco, height=100, placeholder="ex: Português, Matemática, Direito Constitucional, Informática...")
                p_horas = st.selectbox("Horas disponíveis por dia:", ["1","2","3","4","5","6","8","10+"],
                    index=["1","2","3","4","5","6","8","10+"].index(st.session_state.horas_disponiveis) if st.session_state.horas_disponiveis in ["1","2","3","4","5","6","8","10+"] else 1)
                p_dias = st.selectbox("Dias disponíveis por semana:", ["3","4","5","6","7"],
                    index=["3","4","5","6","7"].index(st.session_state.dias_disponiveis) if st.session_state.dias_disponiveis in ["3","4","5","6","7"] else 2)
            with col4:
                p_nivel = st.selectbox("Nível de conhecimento geral:", ["Iniciante","Básico","Intermediário","Avançado"],
                    index=["Iniciante","Básico","Intermediário","Avançado"].index(st.session_state.nivel_conhecimento) if st.session_state.nivel_conhecimento in ["Iniciante","Básico","Intermediário","Avançado"] else 0)
                p_experiencia = st.selectbox("Experiência anterior em concursos:", ["Nenhuma","Já fiz alguns concursos","Já passei em fases anteriores","Concurseiro experiente"],
                    index=["Nenhuma","Já fiz alguns concursos","Já passei em fases anteriores","Concurseiro experiente"].index(st.session_state.experiencia_anterior) if st.session_state.experiencia_anterior in ["Nenhuma","Já fiz alguns concursos","Já passei em fases anteriores","Concurseiro experiente"] else 0)
                p_metodo = st.selectbox("Método de estudo preferido:", ["Leitura","Vídeoaulas","Questões","Misto"],
                    index=["Leitura","Vídeoaulas","Questões","Misto"].index(st.session_state.metodo_preferido) if st.session_state.metodo_preferido in ["Leitura","Vídeoaulas","Questões","Misto"] else 3)

            st.markdown("#### 💡 Autoconhecimento")
            col5, col6 = st.columns(2)
            with col5:
                p_dificuldade = st.text_input("Maior dificuldade:", value=st.session_state.maior_dificuldade, placeholder="ex: Matemática, Direito Administrativo...")
            with col6:
                p_facilidade = st.text_input("Maior facilidade:", value=st.session_state.maior_facilidade, placeholder="ex: Português, Informática...")

            sub = st.form_submit_button("💾 SALVAR PERFIL COMPLETO")
            if sub:
                st.session_state.concurso_foco = p_concurso
                st.session_state.cargo_foco = p_cargo
                st.session_state.instituicao = p_instituicao
                st.session_state.data_prova = p_data
                st.session_state.nota_necessaria = p_nota
                st.session_state.materias_foco = p_materias
                st.session_state.horas_disponiveis = p_horas
                st.session_state.dias_disponiveis = p_dias
                st.session_state.nivel_conhecimento = p_nivel
                st.session_state.experiencia_anterior = p_experiencia
                st.session_state.metodo_preferido = p_metodo
                st.session_state.maior_dificuldade = p_dificuldade
                st.session_state.maior_facilidade = p_facilidade
                st.session_state.meta_semanal_h = int(p_horas.replace('+','')) * int(p_dias)
                salvar_perfil_cache(st.session_state.usuario)
                st.success("✅ Perfil salvo! O tutor agora tem tudo que precisa para te guiar.")

        if st.session_state.concurso_foco and st.button("📅 GERAR PLANEJAMENTO AUTOMÁTICO COMPLETO"):
            with st.spinner("Montando seu cronograma até a data da prova..."):
                prompt = (
                    f"Crie um planejamento de estudos automático e completo para este candidato.\n"
                    f"Concurso: {st.session_state.concurso_foco}. Cargo: {st.session_state.cargo_foco}. "
                    f"Matérias: {st.session_state.materias_foco}. Data da prova: {st.session_state.data_prova or 'não definida'}. "
                    f"Horas/dia: {st.session_state.horas_disponiveis}h. Dias/semana: {st.session_state.dias_disponiveis}. "
                    f"Nível: {st.session_state.nivel_conhecimento}. Maior dificuldade: {st.session_state.maior_dificuldade}.\n\n"
                    f"Inclua: distribuição de matérias, revisões espaçadas, simulados, folgas e metas semanais.\n"
                    f"Formato: cronograma semana a semana até a prova."
                )
                res = tutor_ia(prompt)
                salvar_estudo("Plano", f"Planejamento automático {st.session_state.concurso_foco}", res)
                ganhar_xp('plano')
                st.session_state['plano_temp_perfil'] = res

        if st.session_state.get('plano_temp_perfil'):
            st.markdown(f"<div class='card'>{st.session_state['plano_temp_perfil']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar planejamento (.txt)", data=st.session_state['plano_temp_perfil'],
                file_name="planejamento_concurso.txt", mime="text/plain")

    elif st.session_state.pagina == "Plano":
        st.header("📅 Plano de Estudos Personalizado")
        st.markdown("Cronograma realista e detalhado — do seu nível atual até a aprovação.")

        col1, col2 = st.columns(2)
        with col1:
            concurso  = st.text_input("Concurso/prova:", value=st.session_state.concurso_foco, placeholder="ex: Concurso dos Correios, ENEM, PRF...")
            materias  = st.text_area("Matérias do edital (ou que precisa estudar):", height=100,
                value=st.session_state.materias_foco,
                placeholder="ex: Língua Portuguesa, Matemática, Raciocínio Lógico, Informática Básica...")
            data_prova= st.text_input("Data da prova:", value=st.session_state.data_prova, placeholder="ex: 15/03/2025 ou em 4 meses...")
        with col2:
            horas     = st.selectbox("Horas por dia:", ["1 hora","2 horas","3 horas","4 horas","5+ horas"],
                index=["1 hora","2 horas","3 horas","4 horas","5+ horas"].index(st.session_state.horas_disponiveis) if st.session_state.horas_disponiveis in ["1 hora","2 horas","3 horas","4 horas","5+ horas"] else 1)
            nivel     = st.selectbox("Nível atual:", ["Iniciante","Básico","Intermediário","Avançado"],
                index=["Iniciante","Básico","Intermediário","Avançado"].index(st.session_state.nivel_conhecimento) if st.session_state.nivel_conhecimento in ["Iniciante","Básico","Intermediário","Avançado"] else 0)
            pontos_fracos = st.text_input("Suas maiores dificuldades:", placeholder="ex: matemática, interpretação de texto...")

        if st.button("📅 GERAR MEU PLANO DE ESTUDOS"):
            if concurso.strip() or materias.strip():
                with st.spinner("Montando seu cronograma personalizado..."):
                    prompt = (
                        f"Crie um plano de estudos completo e realista.\n"
                        f"Concurso/prova: {concurso}. Matérias: {materias}.\n"
                        f"Data da prova: {data_prova}. Horas/dia: {horas}. Nível: {nivel}.\n"
                        f"Dificuldades: {pontos_fracos}.\n\n"
                        f"ESTRUTURA DO PLANO:\n\n"
                        f"🎯 DIAGNÓSTICO INICIAL:\n"
                        f"[Análise honesta da situação — é possível passar com esse tempo e dedicação?]\n\n"
                        f"📊 DISTRIBUIÇÃO DE MATÉRIAS:\n"
                        f"[Quanto % do tempo dedicar a cada matéria — baseado no peso no edital e nas dificuldades]\n\n"
                        f"📅 CRONOGRAMA SEMANAL (modelo de semana padrão):\n"
                        f"Segunda: [matéria] [horário sugerido] [o que estudar]\n"
                        f"Terça: ...\n"
                        f"Quarta: ...\n"
                        f"Quinta: ...\n"
                        f"Sexta: ...\n"
                        f"Sábado: [revisão + simulado]\n"
                        f"Domingo: [descanso ou revisão leve]\n\n"
                        f"📈 FASES DO PLANO:\n"
                        f"Fase 1 — Fundação: [o que fazer no primeiro terço do tempo]\n"
                        f"Fase 2 — Consolidação: [o que fazer no segundo terço]\n"
                        f"Fase 3 — Reta final: [o que fazer no último terço]\n\n"
                        f"⚡ REGRAS DE OURO DESSE PLANO:\n"
                        f"[5 regras específicas para esse concurso e esse perfil]\n\n"
                        f"🚨 ARMADILHAS A EVITAR:\n"
                        f"[Os erros mais comuns de quem estuda para {concurso}]\n\n"
                        f"📌 COMEÇAR HOJE:\n"
                        f"[O que fazer nas próximas 2 horas para já começar — específico e imediato]"
                    )
                    res = tutor_ia(prompt)
                    salvar_estudo("Plano", concurso or "Geral", res)
                    st.session_state['plano_temp'] = res
                    st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Preencha o concurso ou as matérias.")

        if st.session_state.get('plano_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar plano (.txt)", data=st.session_state['plano_temp'],
                    file_name="plano_estudos.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("💾 Salvar na Biblioteca", use_container_width=True):
                    st.session_state.biblioteca_materiais.append({
                        'tipo': 'Plano', 'materia': concurso or "Geral",
                        'conteudo': st.session_state['plano_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("✅ Salvo!")

    # ========================
    # GERADOR DE RESUMOS
    # ========================
    elif st.session_state.pagina == "Resumo":
        st.header("📖 Gerador de Resumos")
        st.markdown("Resumos diretos ao ponto — só o que cai em prova, sem enrolação.")

        col1, col2 = st.columns(2)
        with col1:
            materia  = st.text_input("Matéria:", placeholder="ex: Direito Constitucional, Matemática, Português...")
            tema     = st.text_input("Tema específico:", placeholder="ex: Direitos Fundamentais, Porcentagem, Concordância Verbal...")
            concurso_r = st.text_input("Para qual concurso:", value=st.session_state.concurso_foco, placeholder="ex: PRF, Banco do Brasil, ENEM...")
        with col2:
            nivel_r  = st.selectbox("Nível do resumo:", ["Básico — do zero","Intermediário — já conheço o tema","Avançado — revisão rápida"])
            formato  = st.radio("Formato:", ["Texto corrido com tópicos","Esquema visual (tabelas e listas)","Mapa mental em texto"], horizontal=True)
            incluir_exemplos = st.checkbox("Incluir exemplos práticos", value=True)
            incluir_questoes = st.checkbox("Incluir questões de fixação ao final", value=True)

        if st.button("📖 GERAR RESUMO COMPLETO"):
            if tema.strip() or materia.strip():
                with st.spinner("Gerando seu resumo..."):
                    prompt = (
                        f"Crie um resumo completo sobre '{tema or materia}' da matéria {materia}.\n"
                        f"Concurso: {concurso_r}. Nível: {nivel_r}. Formato: {formato}.\n\n"
                        f"ESTRUTURA:\n\n"
                        f"📖 RESUMO: {tema or materia}\n"
                        f"Matéria: {materia} | Concurso: {concurso_r}\n\n"
                        f"🎯 O QUE MAIS CAI EM PROVA SOBRE ESSE TEMA:\n"
                        f"[Liste os pontos que aparecem com maior frequência nas provas]\n\n"
                        f"📚 CONTEÚDO COMPLETO:\n"
                        f"[Desenvolvimento em {formato} — didático, claro e completo]\n\n"
                        + (f"💡 EXEMPLOS PRÁTICOS:\n[3-5 exemplos do dia a dia ou de questões reais]\n\n" if incluir_exemplos else "")
                        + f"⚡ MACETES E DICAS PARA MEMORIZAR:\n"
                        f"[Truques específicos para fixar esse conteúdo]\n\n"
                        f"🚨 PEGADINHAS COMUNS:\n"
                        f"[O que as bancas costumam cobrar de forma capciosa sobre esse tema]\n\n"
                        + (f"❓ QUESTÕES DE FIXAÇÃO (3 questões com gabarito):\n[Questões no estilo da prova com resolução]\n" if incluir_questoes else "")
                    )
                    res = tutor_ia(prompt)
                    salvar_estudo("Resumo", f"{materia} — {tema}", res)
                    st.session_state['resumo_temp'] = res
                    st.markdown(f"<div class='card-blue'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Preencha a matéria e o tema.")

        if st.session_state.get('resumo_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar resumo (.txt)", data=st.session_state['resumo_temp'],
                    file_name=f"resumo_{(tema or materia).replace(' ','_')}.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("💾 Salvar na Biblioteca", key="sv_resumo", use_container_width=True):
                    st.session_state.biblioteca_materiais.append({
                        'tipo': 'Resumo', 'materia': f"{materia} — {tema}",
                        'conteudo': st.session_state['resumo_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("✅ Salvo!")

    # ========================
    # SIMULADO DE QUESTÕES
    # ========================
    elif st.session_state.pagina == "Questoes":
        st.header("❓ Simulado de Questões")
        st.markdown("Questões no estilo da banca — com gabarito comentado e explicação detalhada.")

        col1, col2 = st.columns(2)
        with col1:
            materia_q  = st.text_input("Matéria:", placeholder="ex: Português, Matemática, Direito...")
            tema_q     = st.text_input("Tema:", placeholder="ex: Análise Sintática, Regra de Três, CF/88...")
            concurso_q = st.text_input("Estilo de banca:", value=st.session_state.concurso_foco,
                placeholder="ex: CESPE, FCC, Vunesp, ENEM...")
        with col2:
            qtd_q   = st.slider("Quantidade de questões:", 3, 10, 5)
            nivel_q = st.selectbox("Nível de dificuldade:", ["Fácil","Médio","Difícil","Misto"])
            tipo_q  = st.radio("Tipo:", ["Múltipla escolha (A-E)","Certo ou Errado"], horizontal=True)

        if st.button("❓ GERAR SIMULADO"):
            if materia_q.strip():
                with st.spinner("Gerando suas questões..."):
                    estilo = "no estilo CERTO ou ERRADO" if "Certo" in tipo_q else "de múltipla escolha com 5 alternativas (A, B, C, D, E)"
                    prompt = (
                        f"Crie {qtd_q} questões {estilo} sobre '{tema_q or materia_q}' da matéria {materia_q}.\n"
                        f"Banca/estilo: {concurso_q}. Nível: {nivel_q}.\n\n"
                        f"Para CADA questão use EXATAMENTE este formato:\n\n"
                        f"QUESTÃO [N]\n"
                        f"[Enunciado da questão]\n"
                        + ("[A) opção\nB) opção\nC) opção\nD) opção\nE) opção\n" if "múltipla" in tipo_q else "[  ] CERTO  [  ] ERRADO\n")
                        + f"GABARITO: [letra ou CERTO/ERRADO]\n"
                        f"EXPLICAÇÃO: [resolução detalhada — por que o gabarito está certo e por que as outras estão erradas]\n"
                        f"DICA: [macete para não errar esse tipo de questão]\n\n"
                        f"---\n\n"
                        f"REGRAS:\n"
                        f"- Questões realistas, no estilo de provas reais\n"
                        f"- Varie os assuntos dentro do tema\n"
                        f"- Inclua pelo menos 1 pegadinha típica de banca\n"
                        f"- Explicações claras e educativas"
                    )
                    res = tutor_ia(prompt)
                    salvar_estudo("Simulado", f"{materia_q} — {tema_q}", res)
                    st.session_state.questoes_respondidas += qtd_q
                    st.session_state['simulado_temp'] = res
                    st.markdown(f"<div class='card-purple'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Preencha a matéria antes de gerar o simulado.")

        if st.session_state.get('simulado_temp'):
            col_acerto, col_dl, col_sv = st.columns(3)
            with col_acerto:
                acertos_input = st.number_input("Quantas você acertou?", min_value=0, max_value=qtd_q if 'qtd_q' in dir() else 10, value=0)
                if st.button("✅ Registrar acertos"):
                    st.session_state.questoes_certas += acertos_input
                    st.success(f"✅ {acertos_input} acertos registrados! Taxa geral: {round(st.session_state.questoes_certas/max(1,st.session_state.questoes_respondidas)*100)}%")
            with col_dl:
                st.download_button("📋 Baixar simulado (.txt)", data=st.session_state['simulado_temp'],
                    file_name="simulado.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("💾 Salvar na Biblioteca", key="sv_sim", use_container_width=True):
                    st.session_state.biblioteca_materiais.append({
                        'tipo': 'Simulado', 'materia': f"{materia_q} — {tema_q}",
                        'conteudo': st.session_state['simulado_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("✅ Salvo!")

    # ========================
    # TÉCNICAS DE MEMORIZAÇÃO
    # ========================
    elif st.session_state.pagina == "Memoria":
        st.header("🧠 Técnicas de Memorização")
        st.markdown("Mnemônicos, associações e mapas mentais — para fixar de vez o que você aprende.")

        col1, col2 = st.columns(2)
        with col1:
            conteudo_mem = st.text_area("O que você precisa memorizar?", height=120,
                placeholder="ex: Os artigos 5 ao 17 da CF/88, as fórmulas de área e volume, as preposições...")
            materia_mem  = st.text_input("Matéria:", placeholder="ex: Direito Constitucional, Matemática...")
        with col2:
            tecnica = st.selectbox("Técnica principal:", [
                "Mnemônicos (siglas e frases)",
                "Método Loci (palácio da memória)",
                "Associação com imagens",
                "Histórias e narrativas",
                "Música e ritmo",
                "Todas as técnicas combinadas",
            ])
            nivel_mem = st.radio("Volume de conteúdo:", ["Poucos itens (até 10)","Médio (10-30 itens)","Muito conteúdo (30+)"], horizontal=True)

        if st.button("🧠 CRIAR TÉCNICA DE MEMORIZAÇÃO"):
            if conteudo_mem.strip():
                with st.spinner("Criando sua técnica de memorização..."):
                    prompt = (
                        f"Crie técnicas de memorização para: '{conteudo_mem}'.\n"
                        f"Matéria: {materia_mem}. Técnica: {tecnica}. Volume: {nivel_mem}.\n\n"
                        f"ENTREGUE:\n\n"
                        f"🧠 TÉCNICA PRINCIPAL — {tecnica}:\n"
                        f"[Aplique a técnica escolhida especificamente para esse conteúdo]\n\n"
                        f"🔤 MNEMÔNICOS CRIADOS:\n"
                        f"[Siglas, frases ou acrônimos para fixar os pontos principais]\n\n"
                        f"🖼️ ASSOCIAÇÕES VISUAIS:\n"
                        f"[Como visualizar esse conteúdo de forma memorável]\n\n"
                        f"📖 HISTÓRIA/NARRATIVA:\n"
                        f"[Crie uma mini-história que incorpora todos os itens do conteúdo]\n\n"
                        f"🔁 COMO PRATICAR:\n"
                        f"[Rotina de repetição para fixar em 7 dias]\n\n"
                        f"✅ TESTE RÁPIDO:\n"
                        f"[3 perguntas para verificar se fixou o conteúdo]"
                    )
                    res = tutor_ia(prompt)
                    salvar_estudo("Memorização", materia_mem or "Geral", res)
                    st.session_state['memoria_temp'] = res
                    st.markdown(f"<div class='card-green'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Diga o que você precisa memorizar.")

        if st.session_state.get('memoria_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar técnica (.txt)", data=st.session_state['memoria_temp'],
                    file_name="memorização.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("💾 Salvar na Biblioteca", key="sv_mem", use_container_width=True):
                    st.session_state.biblioteca_materiais.append({
                        'tipo': 'Memorização', 'materia': materia_mem or "Geral",
                        'conteudo': st.session_state['memoria_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("✅ Salvo!")

    # ========================
    # REVISÃO ESPAÇADA
    # ========================
    elif st.session_state.pagina == "Revisao":
        st.header("⚡ Revisão Espaçada")
        st.markdown("O sistema científico para nunca esquecer o que estudou — baseado na curva do esquecimento.")

        col1, col2 = st.columns(2)
        with col1:
            materias_rev = st.text_area("Matérias e temas que já estudou:", height=120,
                placeholder="ex: Aprendi concordância verbal (há 1 semana), Porcentagem (há 3 dias), CF/88 art. 5 (hoje)...")
            data_prova_r = st.text_input("Data da prova:", value=st.session_state.data_prova,
                placeholder="ex: daqui 2 meses, 15/03/2025...")
        with col2:
            horas_rev    = st.selectbox("Horas disponíveis para revisão por dia:", ["30 min","1 hora","1h30","2 horas","3+ horas"])
            prioridade   = st.radio("Prioridade de revisão:", ["O que estudei há mais tempo","O que tenho mais dificuldade","Balanceado"], horizontal=True)

        if st.button("⚡ CRIAR PLANO DE REVISÃO"):
            if materias_rev.strip():
                with st.spinner("Montando seu sistema de revisão..."):
                    prompt = (
                        f"Crie um plano de revisão espaçada baseado na curva do esquecimento de Ebbinghaus.\n"
                        f"Conteúdos estudados: {materias_rev}.\n"
                        f"Data da prova: {data_prova_r}. Tempo para revisão: {horas_rev}/dia. Prioridade: {prioridade}.\n\n"
                        f"ESTRUTURA:\n\n"
                        f"📊 COMO FUNCIONA A REVISÃO ESPAÇADA:\n"
                        f"[Explicação rápida da curva do esquecimento — por que revisar no momento certo]\n\n"
                        f"📅 CRONOGRAMA DE REVISÃO (próximos 30 dias):\n"
                        f"[Dia a dia — o que revisar em cada dia com base no tempo desde o estudo]\n"
                        f"Organize assim:\n"
                        f"Hoje: [o que revisar]\n"
                        f"Amanhã: [o que revisar]\n"
                        f"Em 3 dias: [o que revisar]\n"
                        f"Em 1 semana: [o que revisar]\n"
                        f"Em 2 semanas: [o que revisar]\n"
                        f"[Continue até a data da prova]\n\n"
                        f"⚡ MÉTODO DE REVISÃO RÁPIDA:\n"
                        f"[Como revisar em pouco tempo sem reler tudo do zero]\n\n"
                        f"🃏 SISTEMA DE FLASHCARDS:\n"
                        f"[Como criar e usar flashcards para cada matéria listada]\n\n"
                        f"📌 REVISÃO DE VÉSPERA:\n"
                        f"[O que fazer nas 48h antes da prova — o que revisar e o que NÃO fazer]"
                    )
                    res = tutor_ia(prompt)
                    salvar_estudo("Revisão Espaçada", "Múltiplas matérias", res)
                    st.session_state['revisao_temp'] = res
                    st.markdown(f"<div class='card-orange' style='background:linear-gradient(135deg,#FFFBEB,#FEF3C7);border:1px solid #FCD34D;'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Liste as matérias que já estudou.")

        if st.session_state.get('revisao_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar plano de revisão (.txt)", data=st.session_state['revisao_temp'],
                    file_name="revisao_espacada.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("💾 Salvar na Biblioteca", key="sv_rev", use_container_width=True):
                    st.session_state.biblioteca_materiais.append({
                        'tipo': 'Revisão Espaçada', 'materia': 'Múltiplas matérias',
                        'conteudo': st.session_state['revisao_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("✅ Salvo!")

    # ========================
    # TUTOR AO VIVO
    # ========================
    elif st.session_state.pagina == "Tutor":
        st.header("💬 Tutor ao Vivo")
        st.markdown("Tire qualquer dúvida sobre qualquer matéria — explicação na hora, sem enrolação.")

        if 'chat_tutor' not in st.session_state:
            st.session_state.chat_tutor = []
        if 'chat_key' not in st.session_state:
            st.session_state.chat_key = 0

        # Histórico
        if st.session_state.chat_tutor:
            for msg in st.session_state.chat_tutor:
                if msg['role'] == 'user':
                    st.markdown(f"<div style='background:#FEF3C7;border:1px solid #FCD34D;border-radius:12px 12px 4px 12px;padding:12px 16px;margin:8px 0;'><b>Você:</b> {msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='card' style='margin:8px 0;'><b>🎓 Tutor:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background:#FFFBEB;border:1px solid #FCD34D;border-radius:12px;padding:16px;text-align:center;color:#92400E;">
            🎓 <strong>Olá! Sou seu tutor.</strong> Pode me perguntar qualquer coisa sobre suas matérias.<br>
            <small>Ex: "Explica o que é concordância verbal", "Qual a diferença entre mês e mês passado em cálculos?", "Resuma os direitos fundamentais"</small>
            </div>""", unsafe_allow_html=True)

        # Sugestões rápidas
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**⚡ Perguntas rápidas:**")
        col_s1, col_s2, col_s3 = st.columns(3)
        sugestoes = [
            f"Explique {st.session_state.materias_foco.split(',')[0].strip() if st.session_state.materias_foco else 'Português'} do zero",
            f"O que mais cai em {st.session_state.concurso_foco or 'concursos'} de {st.session_state.materias_foco.split(',')[0].strip() if st.session_state.materias_foco else 'Matemática'}?",
            "Qual a diferença entre... (complete sua dúvida)",
        ]
        for idx, (col, sug) in enumerate(zip([col_s1, col_s2, col_s3], sugestoes)):
            if col.button(f"→ {sug[:35]}...", key=f"sug_{idx}"):
                with st.spinner("Tutor respondendo..."):
                    resp = tutor_ia(sug, "Responda de forma didática e clara. Máximo 4 parágrafos.")
                st.session_state.chat_tutor.append({"role": "user", "content": sug})
                st.session_state.chat_tutor.append({"role": "assistant", "content": resp})
                st.rerun()

        # Input
        pergunta = st.text_input("Sua dúvida:", key=f"tutor_input_{st.session_state.chat_key}",
            placeholder="Digite sua dúvida aqui — sobre qualquer matéria...")

        col_env, col_limpar = st.columns([3, 1])
        with col_env:
            if st.button("📤 PERGUNTAR AO TUTOR"):
                if pergunta.strip():
                    with st.spinner("Tutor respondendo..."):
                        historico_msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_tutor[-10:]]
                        resp = tutor_ia(pergunta, "Responda de forma didática. Máximo 4 parágrafos curtos. Dê exemplos práticos.")
                    st.session_state.chat_tutor.append({"role": "user", "content": pergunta})
                    st.session_state.chat_tutor.append({"role": "assistant", "content": resp})
                    st.session_state.chat_key += 1
                    salvar_estudo("Tutor", pergunta[:60], resp)
                    st.rerun()
                else:
                    st.warning("Digite sua dúvida.")
        with col_limpar:
            if st.button("🗑️ Limpar"):
                st.session_state.chat_tutor = []
                st.rerun()

    # ========================
    # BIBLIOTECA
    # ========================
    elif st.session_state.pagina == "Biblioteca":
        st.header("📚 Biblioteca de Materiais")
        st.markdown("Seus resumos, planos e simulados salvos — organizados por matéria.")

        if not st.session_state.biblioteca_materiais:
            st.info("Biblioteca vazia. Gere materiais nas outras abas e salve os melhores aqui!")
        else:
            tipos_bib = list(set(m['tipo'] for m in st.session_state.biblioteca_materiais))
            filtro    = st.selectbox("Filtrar por tipo:", ["Todos"] + tipos_bib)

            mats_filtrados = [
                m for m in st.session_state.biblioteca_materiais
                if filtro == "Todos" or m['tipo'] == filtro
            ]

            st.markdown(f"**{len(mats_filtrados)} material(is) encontrado(s)**")
            st.markdown("<br>", unsafe_allow_html=True)

            for i, item in enumerate(reversed(mats_filtrados)):
                idx_real = len(st.session_state.biblioteca_materiais) - 1 - i
                with st.expander(f"[{item['tipo']}] {item['materia']} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_dl, col_del = st.columns([3, 1])
                    with col_dl:
                        st.download_button("📋 Baixar", data=item['conteudo'],
                            file_name=f"{item['tipo'].lower().replace(' ','_')}_{item['data'][:5].replace('/','')}.txt",
                            mime="text/plain", key=f"dl_bib_{i}")
                    with col_del:
                        if st.button("🗑️ Remover", key=f"del_bib_{i}"):
                            st.session_state.biblioteca_materiais.pop(idx_real)
                            st.rerun()

    # ========================
    # PROGRESSO
    # ========================
    elif st.session_state.pagina == "Progresso":
        st.header("📈 Meu Progresso de Estudos")

        total       = len(st.session_state.historico_estudos)
        bib         = len(st.session_state.biblioteca_materiais)
        respondidas = st.session_state.questoes_respondidas
        certas      = st.session_state.questoes_certas
        taxa        = round(certas / respondidas * 100) if respondidas > 0 else 0
        tipos = {}
        for e in st.session_state.historico_estudos:
            tipos[e['tipo']] = tipos.get(e['tipo'], 0) + 1

        # Cor da taxa de acerto
        cor_taxa = "#059669" if taxa >= 70 else ("#F59E0B" if taxa >= 50 else "#EF4444")
        msg_taxa = "🟢 Ótimo!" if taxa >= 70 else ("🟡 Melhorando..." if taxa >= 50 else "🔴 Precisa praticar mais")

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total}</div><div>Materiais gerados</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{respondidas}</div><div>Questões feitas</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero' style='color:{cor_taxa} !important;'>{taxa}%</div><div>Taxa de acerto {msg_taxa}</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Resumo',0)}</div><div>Resumos</div></div>", unsafe_allow_html=True)
        c5.markdown(f"<div class='stat-box'><div class='stat-numero'>{bib}</div><div>Na biblioteca</div></div>", unsafe_allow_html=True)

        # Ajuste manual de questões
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("✏️ Ajustar contagem de questões"):
            col_r, col_c = st.columns(2)
            with col_r:
                nova_r = st.number_input("Total de questões respondidas:", min_value=0, value=respondidas)
            with col_c:
                nova_c = st.number_input("Total de acertos:", min_value=0, max_value=nova_r, value=min(certas, nova_r))
            if st.button("Salvar contagem"):
                st.session_state.questoes_respondidas = nova_r
                st.session_state.questoes_certas      = nova_c
                st.success("✅ Contagem atualizada!")
                st.rerun()

        if st.session_state.historico_estudos:
            st.markdown("<br>", unsafe_allow_html=True)
            col_f, col_ex = st.columns([3, 1])
            with col_f:
                filtro = st.selectbox("Filtrar:", ["Todos"] + list(tipos.keys()))
            with col_ex:
                st.markdown("<br>", unsafe_allow_html=True)
                historico_txt = "\n\n".join(
                    f"[{e['data']}] {e['tipo']} — {e['materia']}\n{e['conteudo']}\n{'─'*40}"
                    for e in st.session_state.historico_estudos
                )
                st.download_button("⬇️ Exportar TXT", data=historico_txt,
                    file_name="historico_estudos.txt", mime="text/plain")

            for i, item in enumerate(reversed(st.session_state.historico_estudos)):
                if filtro != "Todos" and item['tipo'] != filtro:
                    continue
                idx_real = len(st.session_state.historico_estudos) - 1 - i
                with st.expander(f"[{item['tipo']}] {item['materia']} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_sv, col_del = st.columns([3, 1])
                    with col_sv:
                        if st.button("💾 Salvar na Biblioteca", key=f"sv_hist_{i}"):
                            st.session_state.biblioteca_materiais.append(item.copy())
                            st.success("Salvo!")
                    with col_del:
                        if st.button("🗑️", key=f"del_hist_{i}"):
                            st.session_state.historico_estudos.pop(idx_real)
                            st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Limpar Todo o Histórico"):
                st.session_state.historico_estudos = []
                st.rerun()
        else:
            st.info("Nenhum material gerado ainda. Comece pelo Plano de Estudos!")


    # ──────────────────────────────────────────
    # SIMULADO INTELIGENTE
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Simulado":
        st.header("🎯 Simulado Inteligente")
        st.markdown("A IA cria uma prova personalizada, cronometrada e corrige automaticamente.")

        if not st.session_state.get('simulado_ativo'):
            col1, col2 = st.columns(2)
            with col1:
                mat_sim = st.multiselect("Matérias:", (st.session_state.materias_foco or "").split(",") + ["Português","Matemática","Direito Constitucional","Direito Administrativo","Informática","Raciocínio Lógico"])
                n_questoes_sim = st.selectbox("Número de questões:", [10, 20, 30, 40, 50])
            with col2:
                nivel_sim = st.selectbox("Dificuldade:", ["Fácil","Médio","Difícil","Misto"])
                tempo_sim = st.selectbox("Tempo:", ["30 min","1 hora","2 horas","3 horas","Sem limite"])

            if st.button("🎯 INICIAR SIMULADO"):
                with st.spinner("Gerando seu simulado..."):
                    mats = ", ".join(mat_sim) if mat_sim else st.session_state.materias_foco or "as matérias do concurso"
                    prompt = (
                        f"Crie um simulado de {n_questoes_sim} questões de múltipla escolha (A/B/C/D/E) para {st.session_state.concurso_foco or 'concurso público'}.\n"
                        f"Matérias: {mats}. Dificuldade: {nivel_sim}.\n\n"
                        f"Para cada questão use o formato exato:\n\n"
                        f"QUESTÃO [N] — [MATÉRIA] — [DIFICULDADE]\n"
                        f"[Enunciado completo]\n"
                        f"(A) [alternativa]\n(B) [alternativa]\n(C) [alternativa]\n(D) [alternativa]\n(E) [alternativa]\n"
                        f"GABARITO: [letra]\n"
                        f"EXPLICAÇÃO: [explicação em 2-3 linhas]\n\n"
                        f"[repita para todas as questões]"
                    )
                    res = tutor_ia(prompt)
                    st.session_state.simulado_ativo = {
                        'conteudo': res, 'inicio': datetime.now().isoformat(),
                        'tempo': tempo_sim, 'n': n_questoes_sim, 'materias': mats,
                    }
                    st.rerun()
        else:
            sim = st.session_state.simulado_ativo
            inicio = datetime.fromisoformat(sim['inicio'])
            decorrido = int((datetime.now() - inicio).total_seconds() / 60)
            col_t, col_e = st.columns([3,1])
            with col_t:
                st.markdown(f"**Matérias:** {sim['materias']} · **Questões:** {sim['n']} · **Tempo:** {sim['tempo']}")
            with col_e:
                st.markdown(f"⏱️ **{decorrido} min decorridos**")

            st.markdown(f"<div class='card'>{sim['conteudo']}</div>", unsafe_allow_html=True)

            acerto_sim = st.number_input("Quantas questões você acertou?", min_value=0, max_value=sim['n'], value=0)
            if st.button("✅ FINALIZAR E CORRIGIR"):
                taxa_sim = int(acerto_sim / sim['n'] * 100)
                st.session_state.questoes_respondidas += sim['n']
                st.session_state.questoes_certas += acerto_sim
                st.session_state.questoes_semana = st.session_state.get('questoes_semana',0) + sim['n']
                xp_g, _ = ganhar_xp('simulado')
                resultado_sim = {
                    'data': datetime.now().strftime('%d/%m %H:%M'),
                    'materias': sim['materias'], 'n': sim['n'],
                    'acertos': acerto_sim, 'taxa': taxa_sim, 'tempo': decorrido
                }
                if 'historico_simulados' not in st.session_state:
                    st.session_state.historico_simulados = []
                st.session_state.historico_simulados.append(resultado_sim)
                salvar_estudo("Simulado", sim['materias'], f"Taxa: {taxa_sim}% ({acerto_sim}/{sim['n']})")
                st.success(f"🏆 Simulado concluído! Taxa: {taxa_sim}% · +{xp_g} XP")
                del st.session_state.simulado_ativo
                st.rerun()

            if st.session_state.historico_simulados:
                with st.expander("📊 Histórico de simulados"):
                    for s in reversed(st.session_state.historico_simulados[-5:]):
                        cor = "#059669" if s['taxa'] >= 70 else ("#D97706" if s['taxa'] >= 50 else "#DC2626")
                        st.markdown(f"<div class='hist-item'>{s['data']} — {s['materias'][:40]} — <strong style='color:{cor}'>{s['taxa']}%</strong> ({s['acertos']}/{s['n']})</div>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # CONQUISTAS
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Conquistas":
        st.header("🏆 Minhas Conquistas")
        conquistadas = st.session_state.get('conquistas', [])
        total = len(CONQUISTAS_DEF)
        obtidas = len(conquistadas)
        st.markdown(f"**{obtidas} de {total} conquistas desbloqueadas**")
        st.progress(obtidas / total if total > 0 else 0)
        st.markdown("<br>", unsafe_allow_html=True)

        cols_c = st.columns(3)
        for i, (chave, nome, desc) in enumerate(CONQUISTAS_DEF):
            obtida = chave in conquistadas
            estilo = "background:#FFFBEB;border:2px solid #F59E0B;" if obtida else "background:#F8FAFC;border:1px solid #E2E8F0;opacity:0.5;"
            icon = "🏆" if obtida else "🔒"
            with cols_c[i % 3]:
                st.markdown(f"<div style='{estilo}border-radius:12px;padding:14px;margin-bottom:10px;text-align:center;'>"
                    f"<div style='font-size:1.5em;'>{icon}</div>"
                    f"<div style='font-weight:700;font-size:0.9em;color:#1A1A2E;'>{nome}</div>"
                    f"<div style='font-size:0.78em;color:#64748B;'>{desc}</div>"
                    f"</div>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # XP E GAMIFICAÇÃO
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Evolucao":
        st.header("🎮 XP e Evolução")
        xp = st.session_state.pontuacao_total
        req_xp, nivel_nome, nivel_emoji = calcular_nivel(xp)
        prox = xp_proximo_nivel(xp)
        pct_nivel = min(int((xp - req_xp) / max(prox - req_xp, 1) * 100), 100) if prox > req_xp else 100

        st.markdown(f"""
        <div class='xp-box'>
            <div style='font-size:0.85em;'>NÍVEL ATUAL</div>
            <div style='font-size:2.5em;font-weight:700;'>{nivel_emoji} {nivel_nome}</div>
            <div style='font-size:1.2em;'>{xp} XP</div>
            <div style='font-size:0.82em;opacity:0.7;'>Próximo nível: {prox} XP</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(pct_nivel / 100)
        st.markdown(f"**{pct_nivel}% para o próximo nível**")

        st.markdown("### 📊 Tabela de Níveis")
        for req, nome, em in NIVEIS:
            atual = xp >= req
            cor = "#059669" if atual else "#94A3B8"
            st.markdown(f"<div style='background:#F8FAFC;border-left:4px solid {cor};border-radius:8px;padding:10px 16px;margin-bottom:6px;'>"
                f"<strong>{em} {nome}</strong> — {req} XP {'✅' if atual else ''}</div>", unsafe_allow_html=True)

        st.markdown("### 🎯 XP por Atividade")
        for ativ, pts in XP_ATIVIDADES.items():
            nomes_ativ = {'questao_certa':'Questão certa','questao_errada':'Questão tentada','resumo':'Resumo criado',
                'flashcard':'Flashcard criado','simulado':'Simulado completo','revisao':'Revisão feita',
                'plano':'Plano criado','mapa_mental':'Mapa mental','missao_dia':'Missão do dia concluída'}
            st.markdown(f"**{nomes_ativ.get(ativ, ativ)}** — +{pts} XP")

        st.markdown("### 🔥 Sequência de Estudos")
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        col_s1.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.get('streak_atual',0)}</div><div>Dias seguidos</div></div>", unsafe_allow_html=True)
        col_s2.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.get('maior_streak',0)}</div><div>Maior sequência</div></div>", unsafe_allow_html=True)
        col_s3.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.get('dias_estudo',0)}</div><div>Total de dias</div></div>", unsafe_allow_html=True)
        col_s4.markdown(f"<div class='stat-box'><div class='stat-numero'>{xp}</div><div>XP Total</div></div>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # RADAR DAS DISCIPLINAS
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Radar":
        st.header("📡 Radar das Disciplinas")
        st.markdown("*Atualize manualmente ou deixe a IA calcular com base no seu histórico.*")

        materias_list = [m.strip() for m in (st.session_state.materias_foco or "Português,Matemática,Direito").split(",") if m.strip()]
        radar = st.session_state.get('radar_materias', {})

        for mat in materias_list:
            if mat not in radar:
                radar[mat] = 50

        st.markdown("#### 📊 Sua performance por matéria")
        for mat in materias_list:
            nota = radar.get(mat, 50)
            cor = "#059669" if nota >= 70 else ("#D97706" if nota >= 50 else "#DC2626")
            col_n, col_b = st.columns([2, 3])
            with col_n:
                nova = st.slider(mat, 0, 100, nota, key=f"radar_{mat}")
                radar[mat] = nova
            with col_b:
                st.markdown(f"<div style='margin-top:28px;'><div style='background:#F1F5F9;border-radius:999px;height:12px;overflow:hidden;'>"
                    f"<div style='height:100%;border-radius:999px;background:{cor};width:{nova}%;'></div></div>"
                    f"<small style='color:{cor};font-weight:600;'>{nova}% — {'Dominado' if nova>=70 else ('Em progresso' if nova>=50 else 'Crítico')}</small></div>",
                    unsafe_allow_html=True)

        st.session_state.radar_materias = radar

        if st.button("🤖 ANALISAR RADAR COM IA"):
            with st.spinner("Analisando..."):
                radar_txt = "\n".join(f"- {m}: {radar.get(m,50)}%" for m in materias_list)
                prompt = (
                    f"Analise o radar de disciplinas deste candidato e dê recomendações estratégicas.\n"
                    f"Concurso: {st.session_state.concurso_foco}.\nDesempenho por matéria:\n{radar_txt}\n\n"
                    f"FORMATO:\n\n"
                    f"📡 ANÁLISE DO RADAR\n\n"
                    f"✅ DISCIPLINAS DOMINADAS (acima de 70%):\n[lista e o que fazer para manter]\n\n"
                    f"⚠️ EM PROGRESSO (50-70%):\n[lista e como avançar]\n\n"
                    f"🚨 DISCIPLINAS CRÍTICAS (abaixo de 50%):\n[lista, impacto na aprovação e plano de ataque]\n\n"
                    f"🎯 PRIORIDADES DESTA SEMANA:\n[ordem exata de estudo com justificativa]"
                )
                res = tutor_ia(prompt)
                salvar_estudo("Radar", "Análise de Disciplinas", res)
                st.session_state['radar_analise_temp'] = res

        if st.session_state.get('radar_analise_temp'):
            st.markdown(f"<div class='card'>{st.session_state['radar_analise_temp']}</div>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # RELATÓRIO SEMANAL
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Relatorio":
        st.header("📊 Relatório Semanal")

        q = st.session_state.questoes_respondidas
        taxa = int(st.session_state.questoes_certas/max(q,1)*100)
        horas = st.session_state.get('horas_acumuladas', 0)
        streak = st.session_state.get('streak_atual', 0)
        idx = calcular_indice_preparacao()

        col1, col2, col3, col4 = st.columns(4)
        col1.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.get('horas_semana',0):.0f}h</div><div>Horas esta semana</div></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.get('questoes_semana',0)}</div><div>Questões esta semana</div></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='stat-box'><div class='stat-numero'>{taxa}%</div><div>Taxa de acerto</div></div>", unsafe_allow_html=True)
        col4.markdown(f"<div class='stat-box'><div class='stat-numero'>{idx}%</div><div>Índice de prep.</div></div>", unsafe_allow_html=True)

        if st.button("📊 GERAR RELATÓRIO COMPLETO DA SEMANA"):
            with st.spinner("Gerando relatório..."):
                prompt = (
                    f"Crie um relatório semanal completo de estudos para este candidato.\n"
                    f"Concurso: {st.session_state.concurso_foco}. "
                    f"Horas esta semana: {st.session_state.get('horas_semana',0)}. "
                    f"Questões: {st.session_state.get('questoes_semana',0)}. Taxa: {taxa}%. "
                    f"Streak: {streak} dias. Índice: {idx}%.\n\n"
                    f"FORMATO:\n\n"
                    f"📊 RELATÓRIO SEMANAL\n\n"
                    f"✅ O QUE FOI FEITO:\n[resumo da semana]\n\n"
                    f"📈 EVOLUÇÃO:\n[análise do desempenho]\n\n"
                    f"⭐ PONTOS FORTES DA SEMANA:\n[o que está funcionando]\n\n"
                    f"⚠️ PONTOS A MELHORAR:\n[o que ajustar]\n\n"
                    f"🎯 OBJETIVOS DA PRÓXIMA SEMANA:\n[metas específicas]\n\n"
                    f"📈 ESTIMATIVA DE APROVAÇÃO:\n[baseada nos dados atuais — sempre como estimativa, nunca garantia]"
                )
                res = tutor_ia(prompt)
                salvar_estudo("Relatório", "Relatório Semanal", res)
                st.session_state['relatorio_temp'] = res

                # Zera contadores semanais
                st.session_state.horas_semana = 0
                st.session_state.questoes_semana = 0

        if st.session_state.get('relatorio_temp'):
            st.markdown(f"<div class='card'>{st.session_state['relatorio_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar relatório (.txt)", data=st.session_state['relatorio_temp'],
                file_name="relatorio_semanal.txt", mime="text/plain")

    # ──────────────────────────────────────────
    # DIAGNÓSTICO INTELIGENTE
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Diagnostico":
        st.header("🧭 Diagnóstico Inteligente")
        st.markdown("*A IA analisa todo o seu histórico e diz exatamente onde focar.*")

        if st.button("🧭 GERAR DIAGNÓSTICO COMPLETO"):
            with st.spinner("Analisando todo o seu histórico..."):
                q = st.session_state.questoes_respondidas
                taxa = int(st.session_state.questoes_certas/max(q,1)*100)
                horas = st.session_state.get('horas_acumuladas', 0)
                radar = st.session_state.get('radar_materias', {})
                radar_txt = "\n".join(f"- {m}: {v}%" for m,v in radar.items()) if radar else "Não configurado"
                hist_tipos = {}
                for e in st.session_state.historico_estudos:
                    hist_tipos[e['tipo']] = hist_tipos.get(e['tipo'], 0) + 1

                prompt = (
                    f"Faça um diagnóstico inteligente completo deste candidato.\n"
                    f"Concurso: {st.session_state.concurso_foco}. Nível: {st.session_state.nivel_conhecimento}. "
                    f"Questões: {q}. Taxa: {taxa}%. Horas: {horas}h. Streak: {st.session_state.get('streak_atual',0)} dias. "
                    f"Maior dificuldade: {st.session_state.maior_dificuldade}. Maior facilidade: {st.session_state.maior_facilidade}.\n"
                    f"Radar de matérias:\n{radar_txt}\n"
                    f"Histórico de atividades: {hist_tipos}\n\n"
                    f"FORMATO:\n\n"
                    f"🧭 DIAGNÓSTICO INTELIGENTE\n\n"
                    f"✅ PONTOS FORTES:\n[o que está bem — com evidências dos dados]\n\n"
                    f"⚠️ PONTOS FRACOS:\n[o que precisa melhorar — com evidências]\n\n"
                    f"📚 DISCIPLINAS DOMINADAS:\n[lista com base no radar e histórico]\n\n"
                    f"🚨 DISCIPLINAS CRÍTICAS:\n[lista com impacto na aprovação]\n\n"
                    f"💡 RECOMENDAÇÃO DA SEMANA:\n[o que fazer nos próximos 7 dias]\n\n"
                    f"🎯 PRÓXIMO FOCO:\n[a UMA coisa mais importante para fazer agora]\n\n"
                    f"📈 PRIORIDADES INTELIGENTES:\n"
                    f"Hoje (★★★★★): [matéria]\n"
                    f"Depois (★★★★☆): [matéria]\n"
                    f"Em seguida (★★★☆☆): [matéria]\n\n"
                    f"🔮 PREVISÃO DE APROVAÇÃO:\n[estimativa baseada nos dados, com ações para melhorar — sempre como estimativa]"
                )
                res = tutor_ia(prompt)
                salvar_estudo("Diagnóstico", "Diagnóstico Inteligente", res)
                st.session_state['diag_temp'] = res

        if st.session_state.get('diag_temp'):
            st.markdown(f"<div class='card'>{st.session_state['diag_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['diag_temp'],
                    file_name="diagnostico.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_diag", use_container_width=True):
                    st.session_state.biblioteca_materiais.append({
                        'tipo':'Diagnóstico','materia':'Análise Completa',
                        'conteudo':st.session_state['diag_temp'],'data':datetime.now().strftime('%d/%m %H:%M'),
                        'favorito':False})
                    st.success("❤️ Salvo!")

    # ──────────────────────────────────────────
    # ⚡ REDAÇÃO TEMA RELÂMPAGO
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Relampago":
        st.header("⚡ Redação Tema Relâmpago")
        st.markdown("*Você não sabe qual será o tema da sua prova. Por isso, aprenda a reagir a qualquer tema.*")

        # Tabs principais
        tab_teoria, tab_praticar, tab_correcao, tab_evolucao = st.tabs([
            "📚 Teoria — A Escada","⚡ Praticar Agora","✍️ Corrigir Redação","📈 Minha Evolução"
        ])

        # ─── TEORIA ───
        with tab_teoria:
            st.markdown("## 🪜 A Escada do Tema Relâmpago")
            st.markdown("*Quando um tema aparecer na prova, suba a escada — não entre em pânico e não comece a escrever imediatamente.*")

            degraus = [
                ("1️⃣","ENTENDA O TEMA",
                 "Faça três perguntas antes de escrever:\n\n"
                 "📌 **Qual é o assunto?** — Sobre o que estamos falando?\n\n"
                 "📌 **Qual é o recorte?** — Qual aspecto desse assunto está sendo discutido?\n\n"
                 "📌 **Qual é a questão central?** — O que precisa ser analisado?\n\n"
                 "**Exemplo:** *Os desafios da inteligência artificial no mercado de trabalho brasileiro.*\n\n"
                 "❌ Não pense apenas: 'O tema é inteligência artificial.'\n\n"
                 "✅ Identifique: ASSUNTO → inteligência artificial · RECORTE → mercado de trabalho · CONTEXTO → Brasil · QUESTÃO → quais desafios a IA provoca?"),
                ("2️⃣","QUEBRE O TEMA",
                 "Transforme um tema grande em partes menores. Pegue as principais palavras e associe livremente.\n\n"
                 "**INTELIGÊNCIA ARTIFICIAL** → automação · tecnologia · produtividade · profissões · inovação\n\n"
                 "**MERCADO DE TRABALHO** → empregos · salários · qualificação · desemprego · oportunidades\n\n"
                 "**BRASIL** → desigualdade · educação · políticas públicas · acesso à tecnologia\n\n"
                 "Agora você já tem vários caminhos possíveis."),
                ("3️⃣","FAÇA ASSOCIAÇÕES",
                 "Use a **Teia de Associações** quando faltar ideia:\n\n"
                 "👤 **Indivíduo** — Como isso afeta as pessoas?\n"
                 "👨‍👩‍👧 **Sociedade** — Como afeta a sociedade?\n"
                 "💰 **Economia** — Existe impacto econômico?\n"
                 "🏛️ **Estado** — Qual é o papel do governo?\n"
                 "🎓 **Educação** — Existe relação com qualificação?\n"
                 "⚖️ **Direitos** — Existe questão de igualdade ou cidadania?\n"
                 "🌎 **Meio Ambiente** — Existe impacto ambiental?\n"
                 "💻 **Tecnologia** — Existe relação com inovação?"),
                ("4️⃣","FAÇA AS PERGUNTAS MÁGICAS",
                 "Quando estiver sem ideias, pergunte:\n\n"
                 "❓ Por que isso acontece? · O que causa esse problema?\n"
                 "❓ Quais são as consequências? · Quem é afetado?\n"
                 "❓ Por que o problema continua? · O que poderia ser feito?\n"
                 "❓ Quem deveria agir? · O que acontece se nada mudar?\n\n"
                 "Essas perguntas funcionam como um **gerador de ideias**."),
                ("5️⃣","ENCONTRE CAUSAS E CONSEQUÊNCIAS",
                 "Separe:\n\n"
                 "🔴 **CAUSAS** — Por que o problema existe?\n"
                 "🟢 **CONSEQUÊNCIAS** — O que o problema provoca?\n\n"
                 "**Exemplo:** *Desafios da educação digital no Brasil*\n\n"
                 "CAUSAS → desigualdade de acesso · falta de infraestrutura · dificuldade de capacitação\n\n"
                 "CONSEQUÊNCIAS → exclusão digital · dificuldades de aprendizagem · aumento das desigualdades\n\n"
                 "Você já encontrou vários argumentos sem precisar decorar nada."),
                ("6️⃣","ESCOLHA DOIS ARGUMENTOS",
                 "Você não precisa de dez ideias. **Precisa de duas boas ideias.**\n\n"
                 "Escolha os dois argumentos que:\n"
                 "✅ Têm relação direta com o tema\n"
                 "✅ São fáceis de explicar\n"
                 "✅ Permitem apresentar consequências ou exemplos\n"
                 "✅ Podem ser desenvolvidos em um parágrafo\n\n"
                 "⚠️ Evite escolher dois argumentos praticamente iguais."),
                ("7️⃣","DEFINA SUA TESE",
                 "Responda: **Qual é a minha ideia central sobre esse tema?**\n\n"
                 "A tese não precisa ser complicada. Precisa ser clara, coerente e defensável.\n\n"
                 "**Exemplo:** *A expansão da inteligência artificial transforma o mercado de trabalho e exige investimentos em qualificação profissional para reduzir os impactos da desigualdade.*\n\n"
                 "Agora você sabe o que vai defender."),
                ("8️⃣","MONTE O MAPA",
                 "📝 **INTRODUÇÃO** → Tema + contextualização + tese\n\n"
                 "🧠 **DESENVOLVIMENTO 1** → Argumento 1 + explicação + exemplo/consequência\n\n"
                 "🧠 **DESENVOLVIMENTO 2** → Argumento 2 + explicação + exemplo/consequência\n\n"
                 "🏁 **CONCLUSÃO** → Retomada + solução/proposta + fechamento"),
                ("9️⃣","ESCREVA",
                 "Você não está mais diante de uma folha em branco. Você possui:\n\n"
                 "✅ Tema compreendido · ✅ Tese · ✅ Dois argumentos · ✅ Estrutura · ✅ Caminho para a conclusão\n\n"
                 "**⚠️ REGRA IMPORTANTE:** Não escreva para descobrir o que você pensa. **Pense primeiro. Escreva depois.**"),
                ("🔟","REVISE",
                 "Não entregue imediatamente. Verifique:\n\n"
                 "🎯 **Tema** — Estou realmente respondendo ao tema?\n"
                 "🧠 **Tese** — Minha posição está clara?\n"
                 "🏗️ **Estrutura** — Cada parágrafo possui uma função?\n"
                 "🔗 **Coesão** — As ideias estão conectadas?\n"
                 "📖 **Gramática** — Existem erros que posso corrigir?\n"
                 "🏁 **Conclusão** — Fecha o raciocínio?"),
            ]

            for num, titulo, conteudo in degraus:
                with st.expander(f"{num} {titulo}"):
                    st.markdown(conteudo)

            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("### 🎓 Modos de Treinamento")
            col1, col2, col3, col4 = st.columns(4)
            col1.markdown("<div class='card-green'><strong>🟢 Aprendiz</strong><br>10 min · Com orientações<br><small>Ideal para quem está aprendendo</small></div>", unsafe_allow_html=True)
            col2.markdown("<div class='card-yellow'><strong>🟡 Desafio</strong><br>10 min · Sem sugestões<br><small>Aplique o método sozinho</small></div>", unsafe_allow_html=True)
            col3.markdown("<div class='card-orange'><strong>🔴 Pressão</strong><br>8 min · Mais exigente<br><small>Maior velocidade</small></div>", unsafe_allow_html=True)
            col4.markdown("<div class='card-dark'><strong>⚡ Relâmpago Extremo</strong><br>5 min · Máxima dificuldade<br><small>Estrutura no menor tempo</small></div>", unsafe_allow_html=True)

        # ─── PRATICAR ───
        with tab_praticar:
            fase = st.session_state.relampago_fase

            # ── MENU ──
            if fase == 'menu':
                st.markdown("### ⚡ Seu Desafio Tema Relâmpago")
                st.markdown("""<div class='card-yellow'>
                ⚠️ <strong>Você não verá o tema antes de iniciar.</strong><br>
                Ao clicar no botão, a IA revelará um tema surpresa e o cronômetro começará.<br>
                Você usará os campos de planejamento para aplicar a Escada do Tema Relâmpago.
                </div>""", unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    modo = st.selectbox("Modo de treino:", ["🟢 Aprendiz (10 min)","🟡 Desafio (10 min)","🔴 Pressão (8 min)","⚡ Relâmpago Extremo (5 min)"])
                    st.session_state.relampago_modo = modo
                with col2:
                    concurso_rel = st.text_input("Concurso (para temas relevantes):", value=st.session_state.concurso_foco or "", placeholder="ex: PRF, INSS, TRT...")

                if st.button("⚡ REVELAR MEU TEMA — INICIAR AGORA", use_container_width=True):
                    with st.spinner("Gerando tema surpresa..."):
                        hist_temas = [r.get('tema','') for r in st.session_state.relampago_historico[-10:]]
                        hist_txt = ", ".join(hist_temas) if hist_temas else "nenhum"
                        prompt_tema = (
                            f"Gere UM tema de redação dissertativo-argumentativa para concurso público.\n"
                            f"Concurso alvo: {concurso_rel or 'concurso público geral'}.\n"
                            f"Temas já usados (NÃO repita): {hist_txt}\n"
                            f"O tema deve ser atual, relevante e compatível com bancas como CEBRASPE, FCC, VUNESP.\n"
                            f"Retorne APENAS o tema, sem explicações. Exemplo: 'Os desafios da saúde mental no ambiente de trabalho brasileiro.'"
                        )
                        tema = tutor_ia(prompt_tema)
                        tema = tema.strip().strip('"').strip("'")
                        st.session_state.relampago_tema = tema
                        st.session_state.relampago_fase = 'planejamento'
                        st.session_state.relampago_planejamento = {}
                        st.session_state.relampago_aval_plano = ''
                        st.session_state.relampago_aval_redacao = ''
                        st.session_state.relampago_redacao = ''
                        st.rerun()

                # Treinamento por habilidade
                st.markdown("<hr class='divider'>", unsafe_allow_html=True)
                st.markdown("### 🎯 Treinar por Habilidade Específica")
                habilidades = ["🔎 Interpretar Temas","🔗 Fazer Associações","💡 Criar Teses",
                               "🧠 Criar Argumentos","🏗️ Montar Estruturas","✍️ Introduções",
                               "🏁 Conclusões","🔗 Coesão","📖 Linguagem","⏱️ Velocidade"]
                hab_sel = st.selectbox("Escolha a habilidade:", habilidades)
                if st.button("🎯 TREINAR ESTA HABILIDADE"):
                    with st.spinner("Criando exercício..."):
                        prompt_hab = (
                            f"Crie um exercício focado em: {hab_sel} para redação de concurso público.\n"
                            f"Concurso: {concurso_rel or 'geral'}.\n\n"
                            f"FORMATO:\n\n"
                            f"🎯 EXERCÍCIO: {hab_sel.upper()}\n\n"
                            f"📖 CONCEITO:\n[explicação clara e direta]\n\n"
                            f"💡 EXEMPLO PRÁTICO:\n[demonstração concreta]\n\n"
                            f"✍️ SEU DESAFIO:\n[exercício para o candidato praticar agora]\n\n"
                            f"⭐ CRITÉRIO DE SUCESSO:\n[como saber se conseguiu]"
                        )
                        res_hab = tutor_ia(prompt_hab)
                        salvar_estudo("Treino Habilidade", hab_sel, res_hab)
                        st.session_state['rel_hab_temp'] = res_hab

                if st.session_state.get('rel_hab_temp'):
                    st.markdown(f"<div class='card'>{st.session_state['rel_hab_temp']}</div>", unsafe_allow_html=True)

            # ── PLANEJAMENTO ──
            elif fase == 'planejamento':
                tema = st.session_state.relampago_tema
                modo = st.session_state.relampago_modo
                minutos = 5 if "5" in modo else (8 if "8" in modo else 10)
                aprendiz = "Aprendiz" in modo

                st.markdown(f"""
                <div style='background:linear-gradient(135deg,#1A1A2E,#0F172A);border:2px solid #F59E0B;
                border-radius:16px;padding:20px 24px;margin-bottom:20px;'>
                    <div style='color:#FDE68A;font-size:0.8em;letter-spacing:2px;'>⚡ TEMA RELÂMPAGO — {modo.upper()}</div>
                    <div style='color:#FDE68A;font-size:1.4em;font-weight:700;margin-top:8px;'>{tema}</div>
                    <div style='color:#94A3B8;font-size:0.85em;margin-top:6px;'>⏱️ Você tem {minutos} minutos para completar o planejamento.</div>
                </div>
                """, unsafe_allow_html=True)

                if aprendiz:
                    st.markdown("""<div class='card-green'>
                    💡 <strong>Modo Aprendiz:</strong> Lembre-se da Escada — ENTENDA → QUEBRE → ASSOCIE → QUESTIONE → CAUSAS/CONSEQUÊNCIAS → 2 ARGUMENTOS → TESE → MAPA
                    </div>""", unsafe_allow_html=True)

                st.markdown("### 🧠 Seu Planejamento")
                pl = st.session_state.relampago_planejamento

                with st.form("form_planejamento_relampago"):
                    p1 = st.text_area("1. O que o tema está pedindo? (Assunto, recorte e questão central)", value=pl.get('p1',''), height=80)
                    p2 = st.text_area("2. Quebre o tema — principais palavras e suas associações:", value=pl.get('p2',''), height=80)
                    p3 = st.text_area("3. Associações (Indivíduo, Sociedade, Economia, Estado, Educação, Direitos...):", value=pl.get('p3',''), height=80)
                    p4 = st.text_area("4. Possíveis causas do problema:", value=pl.get('p4',''), height=80)
                    p5 = st.text_area("5. Possíveis consequências:", value=pl.get('p5',''), height=80)
                    p6 = st.text_area("6. Seu Argumento 1:", value=pl.get('p6',''), height=80)
                    p7 = st.text_area("7. Seu Argumento 2:", value=pl.get('p7',''), height=80)
                    p8 = st.text_area("8. Sua Tese (posição central):", value=pl.get('p8',''), height=80)

                    st.markdown("### 🏗️ Mapa da Redação")
                    m1 = st.text_area("📝 INTRODUÇÃO (tema + contextualização + tese):", value=pl.get('m1',''), height=80)
                    m2 = st.text_area("🧠 DESENVOLVIMENTO 1 (argumento + explicação + exemplo):", value=pl.get('m2',''), height=80)
                    m3 = st.text_area("🧠 DESENVOLVIMENTO 2 (argumento + explicação + exemplo):", value=pl.get('m3',''), height=80)
                    m4 = st.text_area("🏁 CONCLUSÃO (retomada + proposta + fechamento):", value=pl.get('m4',''), height=80)

                    submitted_plan = st.form_submit_button("⚡ FINALIZAR PLANEJAMENTO E AVALIAR")

                if submitted_plan:
                    pl_novo = {'p1':p1,'p2':p2,'p3':p3,'p4':p4,'p5':p5,'p6':p6,'p7':p7,'p8':p8,'m1':m1,'m2':m2,'m3':m3,'m4':m4}
                    st.session_state.relampago_planejamento = pl_novo

                    with st.spinner("A IA está avaliando seu planejamento..."):
                        prompt_aval_plan = (
                            f"Avalie o planejamento de redação deste candidato.\n"
                            f"Tema: {tema}\n\n"
                            f"Planejamento do candidato:\n"
                            f"1. Interpretação: {p1}\n2. Palavras-chave: {p2}\n3. Associações: {p3}\n"
                            f"4. Causas: {p4}\n5. Consequências: {p5}\n6. Arg1: {p6}\n7. Arg2: {p7}\n8. Tese: {p8}\n"
                            f"Mapa: Introdução: {m1} | Dev1: {m2} | Dev2: {m3} | Conclusão: {m4}\n\n"
                            f"FORMATO:\n\n"
                            f"⚡ AVALIAÇÃO DO PLANEJAMENTO — TEMA RELÂMPAGO\n\n"
                            f"📊 SEU DESEMPENHO:\n"
                            f"🎯 Interpretação do tema: [X]%\n"
                            f"🔗 Associações: [X]%\n"
                            f"💡 Construção de argumentos: [X]%\n"
                            f"🧠 Tese: [X]%\n"
                            f"🏗️ Organização/Mapa: [X]%\n\n"
                            f"✅ VOCÊ FOI BEM EM:\n[lista dos pontos fortes]\n\n"
                            f"⚠️ PRECISA MELHORAR:\n[lista dos pontos a desenvolver]\n\n"
                            f"🎯 SEU PRINCIPAL PONTO DE MELHORIA:\n[análise específica do ponto mais crítico]\n\n"
                            f"💡 SUGESTÃO DE TESE ALTERNATIVA:\n[uma tese mais precisa, se a do candidato puder melhorar]"
                        )
                        aval_plan = tutor_ia(prompt_aval_plan)
                        st.session_state.relampago_aval_plano = aval_plan
                        st.session_state.relampago_fase = 'redacao'
                        salvar_estudo("Relâmpago — Planejamento", tema, aval_plan)
                        st.rerun()

            # ── REDAÇÃO ──
            elif fase == 'redacao':
                tema = st.session_state.relampago_tema
                modo = st.session_state.relampago_modo

                # Avaliação do planejamento
                if st.session_state.relampago_aval_plano:
                    with st.expander("📊 Ver avaliação do planejamento"):
                        st.markdown(f"<div class='card'>{st.session_state.relampago_aval_plano}</div>", unsafe_allow_html=True)

                st.markdown(f"""
                <div style='background:linear-gradient(135deg,#052E16,#064E3B);border:2px solid #16A34A;
                border-radius:14px;padding:16px 20px;margin-bottom:16px;'>
                    <div style='color:#86EFAC;font-size:0.8em;'>✅ PLANEJAMENTO CONCLUÍDO — FASE 2</div>
                    <div style='color:#A7F3D0;font-size:1.2em;font-weight:700;margin-top:6px;'>✍️ Agora transforme seu plano em redação</div>
                    <div style='color:#6EE7B7;font-size:0.85em;margin-top:4px;'>Tema: {tema}</div>
                </div>
                """, unsafe_allow_html=True)

                # Planejamento na lateral
                pl = st.session_state.relampago_planejamento
                with st.expander("📋 Ver seu planejamento"):
                    if pl.get('p8'): st.markdown(f"**Tese:** {pl['p8']}")
                    if pl.get('p6'): st.markdown(f"**Arg. 1:** {pl['p6']}")
                    if pl.get('p7'): st.markdown(f"**Arg. 2:** {pl['p7']}")
                    if pl.get('m1'): st.markdown(f"**Intro:** {pl['m1']}")
                    if pl.get('m4'): st.markdown(f"**Conclusão:** {pl['m4']}")

                col1, col2 = st.columns([3,1])
                with col1:
                    tempo_red = st.selectbox("⏱️ Tempo para a redação:", ["30 minutos","45 minutos","60 minutos"])
                with col2:
                    concurso_c = st.text_input("Concurso:", value=st.session_state.concurso_foco or "")

                redacao_txt = st.text_area("✍️ Escreva sua redação aqui:", height=400,
                    value=st.session_state.relampago_redacao,
                    placeholder="Escreva sua redação dissertativo-argumentativa...")

                palavras = len(redacao_txt.split()) if redacao_txt.strip() else 0
                linhas = redacao_txt.count('\n') + 1 if redacao_txt.strip() else 0
                st.markdown(f"**Palavras:** {palavras} · **Linhas estimadas:** {linhas}")

                st.session_state.relampago_redacao = redacao_txt

                if st.button("📤 FINALIZAR E CORRIGIR REDAÇÃO", use_container_width=True):
                    if redacao_txt.strip() and len(redacao_txt.split()) > 50:
                        with st.spinner("A IA está corrigindo sua redação..."):
                            prompt_correcao = (
                                f"Corrija esta redação de concurso público com análise detalhada por critério.\n"
                                f"Concurso: {concurso_c or 'geral'}. Tema: {tema}\n\n"
                                f"Redação do candidato:\n{redacao_txt}\n\n"
                                f"FORMATO:\n\n"
                                f"📊 RAIO-X DA SUA REDAÇÃO\n\n"
                                f"📝 NOTA ESTIMADA: [X]/100\n\n"
                                f"| Critério | Pontos | Máximo |\n|---|---|---|\n"
                                f"| 🎯 Atendimento ao tema | [X] | 25 |\n"
                                f"| 🧠 Argumentação | [X] | 25 |\n"
                                f"| 🏗️ Estrutura | [X] | 15 |\n"
                                f"| 🔗 Coesão e coerência | [X] | 15 |\n"
                                f"| 📖 Linguagem/Gramática | [X] | 15 |\n"
                                f"| 📝 Adequação à proposta | [X] | 5 |\n"
                                f"| **TOTAL** | **[X]** | **100** |\n\n"
                                f"🟢 ONDE VOCÊ FOI BEM:\n[pontos fortes específicos]\n\n"
                                f"⚠️ ONDE VOCÊ PODE MELHORAR:\n\n"
                                f"🔴 PRINCIPAL PONTO DE ATENÇÃO:\n"
                                f"[critério mais problemático]\n"
                                f"SEU TRECHO: [cite o trecho problemático]\n"
                                f"O PROBLEMA: [explicação]\n"
                                f"COMO MELHORAR: [orientação prática]\n"
                                f"REGRA PARA LEMBRAR: [princípio didático]\n\n"
                                f"✏️ APRENDA COM SEU TEXTO:\n"
                                f"SEU TRECHO: [trecho para reescrever]\n"
                                f"VERSÃO MELHORADA: [sugestão]\n"
                                f"POR QUÊ MELHOROU: [explicação]\n\n"
                                f"⚠️ AVISO IMPORTANTE: Esta nota é uma estimativa de treinamento baseada nos critérios configurados. "
                                f"A nota oficial somente pode ser atribuída pela banca examinadora responsável.\n\n"
                                f"🎯 PRÓXIMO TREINO RECOMENDADO: [habilidade a desenvolver]"
                            )
                            aval_red = tutor_ia(prompt_correcao)
                            st.session_state.relampago_aval_redacao = aval_red

                            # Registra no histórico
                            st.session_state.relampago_historico.append({
                                'data': datetime.now().strftime('%d/%m %H:%M'),
                                'tema': tema,
                                'modo': modo,
                                'planejamento': pl,
                                'redacao': redacao_txt,
                                'avaliacao': aval_red,
                            })
                            salvar_estudo("Relâmpago — Redação", tema, aval_red)
                            ganhar_xp('simulado')
                            st.session_state.relampago_fase = 'resultado'
                            st.rerun()
                    else:
                        st.warning("Escreva pelo menos 50 palavras antes de finalizar.")

                col_volta, col_novo = st.columns(2)
                with col_volta:
                    if st.button("← Voltar ao planejamento"):
                        st.session_state.relampago_fase = 'planejamento'; st.rerun()
                with col_novo:
                    if st.button("🔄 Novo tema (descartar)"):
                        st.session_state.relampago_fase = 'menu'; st.rerun()

            # ── RESULTADO ──
            elif fase == 'resultado':
                tema = st.session_state.relampago_tema
                aval_red = st.session_state.relampago_aval_redacao

                st.success("🔥 Desafio concluído! Aqui está a análise completa.")

                if aval_red:
                    st.markdown(f"<div class='card'>{aval_red}</div>", unsafe_allow_html=True)

                    # Desafio de reescrita
                    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
                    st.markdown("### 🔄 Desafio de Reescrita")
                    st.markdown("*Selecione o trecho mais fraco e tente melhorar.*")
                    trecho_reescrita = st.text_area("✏️ Cole o trecho que quer reescrever:", height=120)
                    if st.button("✅ REESCREVER E COMPARAR") and trecho_reescrita.strip():
                        with st.spinner("Comparando versões..."):
                            prompt_reesc = (
                                f"Compare as duas versões deste trecho de redação.\n"
                                f"Tema: {tema}\n\n"
                                f"VERSÃO ORIGINAL:\n{trecho_reescrita}\n\n"
                                f"Analise o que melhorou, o que pode ainda melhorar e dê uma estimativa de ganho de pontos.\n\n"
                                f"FORMATO:\n\n"
                                f"PRIMEIRA VERSÃO — PROBLEMAS:\n[análise]\n\n"
                                f"💡 COMO FICARIA MELHOR:\n[versão sugerida]\n\n"
                                f"🏆 O QUE VOCÊ APRENDEU:\n[lição didática]"
                            )
                            res_reesc = tutor_ia(prompt_reesc)
                            st.markdown(f"<div class='card-green'>{res_reesc}</div>", unsafe_allow_html=True)

                col_baixar, col_novo = st.columns(2)
                with col_baixar:
                    conteudo_export = f"TEMA: {tema}\n\nAVALIAÇÃO:\n{aval_red}\n\nREDAÇÃO:\n{st.session_state.relampago_redacao}"
                    st.download_button("📋 Baixar resultado (.txt)", data=conteudo_export,
                        file_name="relampago_resultado.txt", mime="text/plain", use_container_width=True)
                with col_novo:
                    if st.button("⚡ NOVO DESAFIO", use_container_width=True):
                        st.session_state.relampago_fase = 'menu'
                        st.session_state.relampago_tema = ''
                        st.rerun()

        # ─── CORRIGIR REDAÇÃO ───
        with tab_correcao:
            st.markdown("## 🤖 Correção Inteligente da Redação")
            st.markdown("*Corrija qualquer redação com análise detalhada por critério.*")

            st.markdown("""<div class='card-yellow'>
            ⚠️ A nota apresentada é uma <strong>estimativa de treinamento</strong> baseada nos critérios configurados.
            A nota oficial somente pode ser atribuída pela banca examinadora responsável.
            </div>""", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                concurso_cor = st.text_input("🎯 Concurso:", value=st.session_state.concurso_foco or "",
                    placeholder="ex: PRF, INSS, TRT, PC...")
                banca_cor = st.selectbox("🏛️ Banca:", ["CEBRASPE/CESPE","FCC","VUNESP","FGV","IDECAN","AOCP","Outra"])
            with col2:
                tipo_cor = st.selectbox("📝 Tipo:", ["Dissertativo-argumentativa","Outro"])
                valor_cor = st.number_input("📊 Valor da redação na prova:", min_value=0, max_value=200, value=100)

            tema_cor = st.text_input("📌 Tema da redação:", placeholder="Digite o tema proposto...")
            redacao_cor = st.text_area("✍️ Cole sua redação:", height=350, placeholder="Cole aqui a redação que deseja corrigir...")

            if st.button("🤖 CORRIGIR REDAÇÃO AGORA", use_container_width=True):
                if redacao_cor.strip() and tema_cor.strip():
                    with st.spinner("Analisando sua redação..."):
                        max_nota = valor_cor
                        prompt_cor_manual = (
                            f"Corrija esta redação com análise detalhada.\n"
                            f"Concurso: {concurso_cor}. Banca: {banca_cor}. Tipo: {tipo_cor}.\n"
                            f"Valor total da redação: {valor_cor} pontos.\n"
                            f"Tema: {tema_cor}\n\n"
                            f"Redação:\n{redacao_cor}\n\n"
                            f"Adapte os critérios ao valor total ({valor_cor} pts). Use proporção: tema 25%, argumentação 25%, estrutura 15%, coesão 15%, linguagem 15%, adequação 5%.\n\n"
                            f"FORMATO:\n\n"
                            f"📊 NOTA ESTIMADA: [X]/{valor_cor}\n\n"
                            f"CRITÉRIO | PONTOS | MÁXIMO | STATUS\n"
                            f"🎯 Atendimento ao tema | [X] | [{int(valor_cor*0.25)}] | [🟢/🟡/🔴]\n"
                            f"🧠 Argumentação | [X] | [{int(valor_cor*0.25)}] | [🟢/🟡/🔴]\n"
                            f"🏗️ Estrutura | [X] | [{int(valor_cor*0.15)}] | [🟢/🟡/🔴]\n"
                            f"🔗 Coesão e coerência | [X] | [{int(valor_cor*0.15)}] | [🟢/🟡/🔴]\n"
                            f"📖 Linguagem/Gramática | [X] | [{int(valor_cor*0.15)}] | [🟢/🟡/🔴]\n"
                            f"📝 Adequação | [X] | [{int(valor_cor*0.05)}] | [🟢/🟡/🔴]\n\n"
                            f"🟢 SEUS PONTOS FORTES:\n[análise dos acertos]\n\n"
                            f"🔴 PRINCIPAL PROBLEMA:\n"
                            f"Critério: [nome]\nSeu trecho: [cite]\nProblema: [explique]\nComo melhorar: [oriente]\n\n"
                            f"✏️ APRENDA COM SEU TEXTO:\n"
                            f"SEU TRECHO: [trecho]\nVERSÃO MELHORADA: [sugestão]\nPOR QUÊ: [explicação]\n\n"
                            f"📈 NOTA DE CONFIANÇA DA AVALIAÇÃO: [Alta/Média/Baixa]\n"
                            f"(depende dos critérios disponíveis para {banca_cor})\n\n"
                            f"⚠️ Esta é uma estimativa de treinamento. A nota oficial é atribuída pela banca."
                        )
                        res_cor = tutor_ia(prompt_cor_manual)
                        salvar_estudo("Correção de Redação", tema_cor, res_cor)
                        ganhar_xp('simulado')
                        st.session_state['correcao_manual_temp'] = res_cor
                else:
                    st.warning("Preencha o tema e a redação antes de corrigir.")

            if st.session_state.get('correcao_manual_temp'):
                st.markdown(f"<div class='card'>{st.session_state['correcao_manual_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar correção (.txt)",
                    data=st.session_state['correcao_manual_temp'],
                    file_name="correcao_redacao.txt", mime="text/plain")

                # Reescrita
                st.markdown("<hr class='divider'>", unsafe_allow_html=True)
                st.markdown("### 🔄 Desafio de Reescrita")
                trecho_r = st.text_area("Cole o trecho que quer reescrever:", height=100, key="reescrita_manual")
                if st.button("🔄 REESCREVER E COMPARAR", key="btn_reescrita_manual") and trecho_r.strip():
                    with st.spinner("..."):
                        prompt_rr = (f"Compare e ensine com este trecho de redação sobre o tema '{tema_cor}'.\n\n"
                                     f"TRECHO ORIGINAL:\n{trecho_r}\n\n"
                                     f"Analise o problema, sugira uma versão melhorada e explique a lição.")
                        res_rr = tutor_ia(prompt_rr)
                        st.markdown(f"<div class='card-green'>{res_rr}</div>", unsafe_allow_html=True)

        # ─── EVOLUÇÃO ───
        with tab_evolucao:
            st.markdown("## 📈 Minha Evolução no Tema Relâmpago")

            hist = st.session_state.relampago_historico
            if not hist:
                st.info("Realize seu primeiro desafio Tema Relâmpago para ver sua evolução aqui.")
            else:
                total = len(hist)
                st.markdown(f"**{total} desafio(s) realizado(s)**")

                c1, c2, c3 = st.columns(3)
                c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total}</div><div>Temas Relâmpago</div></div>", unsafe_allow_html=True)
                c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{len([h for h in hist if 'Relâmpago' in h.get('modo','')])+len(hist)}</div><div>Desafios totais</div></div>", unsafe_allow_html=True)
                c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{hist[-1]['modo'].split('(')[0].strip() if hist else '—'}</div><div>Último modo</div></div>", unsafe_allow_html=True)

                st.markdown("<hr class='divider'>", unsafe_allow_html=True)
                st.markdown("### 🏆 Histórico de Desafios")
                for i, h in enumerate(reversed(hist[-10:])):
                    with st.expander(f"#{total-i} — {h['tema'][:60]}... — {h['data']} — {h['modo']}"):
                        st.markdown(f"**Tema:** {h['tema']}")
                        if h.get('avaliacao'):
                            st.markdown(f"<div class='card'>{h['avaliacao'][:500]}...</div>", unsafe_allow_html=True)

                if st.button("🤖 ANÁLISE DE EVOLUÇÃO PELA IA"):
                    with st.spinner("Analisando seu progresso..."):
                        hist_resumo = "\n".join(f"Tema: {h['tema'][:50]}, Modo: {h['modo']}" for h in hist[-5:])
                        prompt_evolucao = (
                            f"Analise a evolução deste candidato no treinamento Tema Relâmpago.\n"
                            f"Total de desafios: {total}.\n"
                            f"Últimos desafios: {hist_resumo}\n\n"
                            f"FORMATO:\n\n"
                            f"📈 ANÁLISE DE EVOLUÇÃO\n\n"
                            f"🏆 O QUE ESTÁ EVOLUINDO:\n[pontos de crescimento]\n\n"
                            f"⚠️ MAIOR DIFICULDADE IDENTIFICADA:\n[habilidade mais crítica]\n\n"
                            f"🎯 PRÓXIMO OBJETIVO:\n[meta específica]\n\n"
                            f"⚡ TREINAMENTO RECOMENDADO:\n[qual modo e habilidade praticar agora]"
                        )
                        res_ev = tutor_ia(prompt_evolucao)
                        st.markdown(f"<div class='card'>{res_ev}</div>", unsafe_allow_html=True)

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Tutor de Concursos IA — Mentor Estratégico · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
