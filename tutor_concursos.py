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

    .card { background: linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:22px; border-radius:16px; border:1px solid #FCD34D; margin-bottom:15px; white-space:normal; word-wrap:break-word; box-shadow:0 2px 12px rgba(217,119,6,0.08); }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color: #1A1A2E !important; }

    .card-dark { background:linear-gradient(135deg,#1C1100,#2D1A00); padding:22px; border-radius:16px; border:1px solid #D97706; margin-bottom:15px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#FDE68A !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:22px; border-radius:16px; border:1px solid #93C5FD; margin-bottom:15px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:22px; border-radius:16px; border:1px solid #86EFAC; margin-bottom:15px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:22px; border-radius:16px; border:1px solid #FECACA; margin-bottom:15px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-purple { background:linear-gradient(135deg,#F5F3FF,#EDE9FE); padding:22px; border-radius:16px; border:1px solid #C4B5FD; margin-bottom:15px; white-space:normal; word-wrap:break-word; }
    .stApp .card-purple, .stApp .card-purple p, .stApp .card-purple span, .stApp .card-purple div { color:#4C1D95 !important; }

    .painel-exec { background:linear-gradient(135deg,#1A1A2E,#16213E); border:2px solid #F59E0B; border-radius:20px; padding:28px; margin-bottom:20px; }
    .stApp .painel-exec, .stApp .painel-exec p, .stApp .painel-exec span, .stApp .painel-exec div, .stApp .painel-exec strong { color:#FDE68A !important; }

    .indice-box { background:linear-gradient(135deg,#D97706,#F59E0B); border-radius:18px; padding:24px; text-align:center; box-shadow:0 4px 24px rgba(217,119,6,0.3); margin-bottom:16px; }
    .stApp .indice-box, .stApp .indice-box p, .stApp .indice-box span, .stApp .indice-box div { color:white !important; }
    .indice-numero { font-size:3.5em; font-weight:700; font-family:'Playfair Display',serif; color:white !important; }
    .stApp .indice-numero { color:white !important; }

    .card-orange { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:22px; border-radius:16px; border:1px solid #FCD34D; margin-bottom:15px; white-space:normal; word-wrap:break-word; }
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
    'smc_fase': 'menu',
    'smc_questoes': [],
    'smc_respostas': {},
    'smc_inicio': 0,
    'smc_duracao': 3600,
    'smc_materia': '',
    'smc_n': 10,
    'smc_resultado': None,
    'smc_historico': [],
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
    cols1 = st.columns(10)
    nav1 = [("🏠","Home"),("📊","Painel"),("📋","Perfil"),("📅","Plano"),("📝","Resumo"),
            ("❓","Questoes"),("🧠","Memoria"),("🔄","Revisao"),("🎯","Simulado"),("📋","SimuladoMC")]
    lb1 = {"Home":"Início","Painel":"Painel Executivo","Perfil":"Meu Perfil Completo",
           "Plano":"Plano de Estudos","Resumo":"Criar Resumo","Questoes":"Resolver Questões",
           "Memoria":"Flashcards","Revisao":"Revisão Espaçada","Simulado":"Simulado Inteligente",
           "SimuladoMC":"Simulado de Múltipla Escolha — cronometrado"}
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
        cor_taxa = "#059669" if taxa >= 70 else ("#B45309" if taxa >= 50 else "#B91C1C")
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
            cor = "#059669" if atual else "#475569"
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
    # ──────────────────────────────────────────
    # ⚡ REDAÇÃO TEMA RELÂMPAGO
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Relampago":
        st.header("⚡ Redação Tema Relâmpago")

        tab_aprender, tab_simular = st.tabs(["📚 Aprender os Critérios", "⚡ Fazer Simulado"])

        # ═══════════════════════════════
        # ABA 1 — APRENDER OS CRITÉRIOS
        # ═══════════════════════════════
        with tab_aprender:
            st.markdown("### 📚 Tudo que você precisa saber para fazer uma boa redação")
            st.markdown("Estude cada critério antes de fazer o simulado. A IA vai te avaliar por todos eles.")

            criterios = [
                ("🎯", "ATENDIMENTO AO TEMA", "25 pontos",
                 """Você deve escrever **exatamente sobre o que foi pedido**. Desviar do tema é o erro mais grave.

**Como garantir:**
- Leia o tema com atenção e identifique: *Qual é o assunto? Qual é o recorte? O que está sendo pedido?*
- Releia o tema antes de escrever cada parágrafo
- Se o tema pede um recorte específico (ex: "no Brasil"), não escreva de forma genérica

**Exemplo de erro:** Tema sobre *saúde mental no trabalho* → candidato escreve sobre saúde em geral → FUGA DE TEMA

**Dica:** Após escrever, pergunte: "Meu texto responde ao tema ou apenas fala sobre o assunto?"

**Níveis:**
- 🟢 25 pts — Abordagem completa, precisa e pertinente
- 🟡 15 pts — Abordagem tangencial ou incompleta  
- 🔴 0 pts — Fuga total do tema"""),

                ("🧠", "ARGUMENTAÇÃO", "25 pontos",
                 """Sua capacidade de **defender sua tese com argumentos sólidos**.

**Estrutura de um bom argumento:**
1. **Argumento** — Sua ideia/ponto de vista
2. **Explicação** — Por que esse argumento é válido?
3. **Exemplo ou consequência** — O que isso provoca na prática?

**Tipos de argumento:**
- Por **causa** — Por que o problema existe?
- Por **consequência** — O que o problema gera?
- Por **comparação** — Como outros contextos lidam com isso?
- Por **autoridade** — O que dados ou estudos mostram?

**Erro comum:** Apenas afirmar sem explicar. *"A educação é importante"* não é argumento. *"A falta de investimento em educação básica perpetua o ciclo da pobreza, pois jovens sem qualificação não acessam o mercado formal"* é argumento.

**Níveis:**
- 🟢 25 pts — Argumentos consistentes, bem desenvolvidos
- 🟡 15 pts — Argumentos superficiais ou desconectados
- 🔴 5 pts — Sem argumentação real"""),

                ("🏗️", "ESTRUTURA", "15 pontos",
                 """A redação deve ter **introdução, dois desenvolvimentos e conclusão** claramente definidos.

**Introdução (1 parágrafo):**
- Contextualização do tema
- Apresentação da tese (sua posição central)
- NÃO comece com "Desde os primórdios..." ou com pergunta

**Desenvolvimento 1 (1 parágrafo):**
- Apresente o Argumento 1
- Explique e desenvolva
- Conecte ao tema e à tese

**Desenvolvimento 2 (1 parágrafo):**
- Apresente o Argumento 2 (diferente do primeiro)
- Explique e desenvolva
- Aprofunde a análise

**Conclusão (1 parágrafo):**
- Retomada da tese
- Proposta de intervenção (quem faz o quê)
- Fechamento

**Dica:** Cada parágrafo tem UMA função. Não misture argumentos no mesmo parágrafo.

**Níveis:**
- 🟢 15 pts — Estrutura clara e bem delimitada
- 🟡 10 pts — Estrutura presente mas com falhas
- 🔴 5 pts — Sem estrutura identificável"""),

                ("🔗", "COESÃO E COERÊNCIA", "15 pontos",
                 """**Coesão** = as ideias estão bem conectadas com conectivos adequados?
**Coerência** = as ideias fazem sentido entre si e com o tema?

**Conectivos essenciais por função:**

📌 *Adição:* além disso, ademais, outrossim, também
📌 *Contraste:* porém, entretanto, no entanto, todavia, contudo
📌 *Causa:* porque, visto que, já que, uma vez que
📌 *Consequência:* portanto, logo, assim, dessa forma, por isso
📌 *Conclusão:* em síntese, diante disso, portanto, conclui-se

**Erros comuns de coesão:**
- Usar "porém" quando a frase não é contraste
- Repetir o mesmo conectivo várias vezes
- Começar parágrafos com "E" ou "Mas"

**Erro de coerência:**
- Defender na conclusão o oposto do que defendeu na introdução
- Misturar argumentos contraditórios

**Níveis:**
- 🟢 15 pts — Texto fluido e bem articulado
- 🟡 10 pts — Problemas de conexão que prejudicam a leitura
- 🔴 5 pts — Texto fragmentado e incoerente"""),

                ("📖", "LINGUAGEM E GRAMÁTICA", "15 pontos",
                 """Adequação à **norma culta da língua portuguesa** e ao registro formal.

**O que é avaliado:**
- Concordância verbal e nominal
- Regência verbal e nominal
- Pontuação (vírgula, ponto e vírgula, dois pontos)
- Ortografia
- Uso adequado de crase
- Registro formal (sem gírias, expressões coloquiais)

**Erros mais comuns:**
- *"A maioria das pessoas **acreditam**"* → acredita (concordância)
- *"Vou **ao** reunião"* → à reunião (regência + crase)
- Vírgula separando sujeito do verbo
- Parágrafos sem ponto final

**Registro inadequado:**
- ❌ "O governo tá deixando a peteca cair"
- ✅ "O governo tem negligenciado suas responsabilidades"

**Dica:** Prefira frases curtas quando não tiver certeza da gramática. Frases curtas tendem a ter menos erros.

**Níveis:**
- 🟢 15 pts — Domínio da norma culta
- 🟡 10 pts — Desvios que não comprometem a compreensão
- 🔴 5 pts — Desvios frequentes que prejudicam a leitura"""),

                ("📝", "ADEQUAÇÃO À PROPOSTA", "5 pontos",
                 """A redação atende às **normas técnicas** da proposta?

**O que verificar:**
- Gênero textual correto (dissertativo-argumentativa, não narrativa ou descritiva)
- Extensão mínima (geralmente 20-30 linhas)
- Não usar primeira pessoa do singular em excesso
- Não copiar trechos dos textos motivadores sem reelaboração
- Não usar pseudônimo ou identificação proibida

**Proposta de intervenção (obrigatória em alguns concursos):**
Estrutura: AGENTE + AÇÃO + MEIO + FINALIDADE
Exemplo: *"O Estado, por meio de políticas públicas de incentivo à capacitação profissional, deve investir em programas de requalificação para trabalhadores afetados pela automação, visando reduzir o desemprego estrutural."*

**Níveis:**
- 🟢 5 pts — Atende integralmente
- 🟡 3 pts — Atende parcialmente
- 🔴 0 pts — Não atende"""),
            ]

            for emoji, titulo, pontos, conteudo in criterios:
                with st.expander(f"{emoji} {titulo} — {pontos}"):
                    st.markdown(conteudo)

            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("### ✅ Resumo dos Critérios")
            st.markdown("""
| Critério | Pontos |
|---|---|
| 🎯 Atendimento ao tema | 25 |
| 🧠 Argumentação | 25 |
| 🏗️ Estrutura | 15 |
| 🔗 Coesão e coerência | 15 |
| 📖 Linguagem e gramática | 15 |
| 📝 Adequação à proposta | 5 |
| **TOTAL** | **100** |
""")
            st.markdown("<div class='card-green'>✅ Estudou todos os critérios? Vá para a aba <strong>⚡ Fazer Simulado</strong> e teste seus conhecimentos com um tema surpresa.</div>", unsafe_allow_html=True)

        # ═══════════════════════════════
        # ABA 2 — SIMULADO
        # ═══════════════════════════════
        with tab_simular:

            fase = st.session_state.get('relampago_fase', 'menu')

            # ── MENU ──
            if fase == 'menu':
                st.markdown("### ⚡ Simulado de Redação")
                st.markdown("""
                <div class='card-dark'>
                    ⚡ <strong>Como funciona:</strong><br><br>
                    1. Você escolhe o tempo disponível<br>
                    2. Clica em <strong>INICIAR</strong><br>
                    3. A IA gera um tema surpresa<br>
                    4. O cronômetro começa imediatamente<br>
                    5. Quando o tempo acabar, a IA corrige automaticamente<br><br>
                    📌 <em>A IA encerra e corrige mesmo que você não tenha terminado.</em>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    tempo_min = st.selectbox("⏱️ Tempo disponível:", [
                        "30 minutos", "45 minutos", "60 minutos", "90 minutos"
                    ])
                with col2:
                    concurso_sim = st.text_input("🎯 Concurso (opcional):",
                        value=st.session_state.get('concurso_foco',''),
                        placeholder="ex: PRF, INSS, TRT...")

                if st.button("⚡ GERAR TEMA E INICIAR CRONÔMETRO", use_container_width=True):
                    with st.spinner("Gerando tema surpresa..."):
                        hist_temas = [r.get('tema','') for r in st.session_state.get('relampago_historico',[])]
                        hist_txt = ", ".join(hist_temas[-8:]) if hist_temas else "nenhum"
                        prompt_tema = (
                            f"Gere UM tema de redação dissertativo-argumentativa para concurso público.\n"
                            f"Concurso: {concurso_sim or 'concurso público geral'}.\n"
                            f"Temas já usados (NÃO repita): {hist_txt}\n"
                            f"Seja atual, relevante e compatível com bancas como CEBRASPE, FCC, VUNESP.\n"
                            f"Retorne APENAS o tema, sem explicações nem aspas."
                        )
                        tema_gerado = tutor_ia(prompt_tema).strip().strip('"').strip("'")
                        minutos_num = int(tempo_min.split()[0])

                        import time
                        st.session_state.relampago_fase = 'escrevendo'
                        st.session_state.relampago_tema = tema_gerado
                        st.session_state.relampago_inicio = time.time()
                        st.session_state.relampago_duracao = minutos_num * 60
                        st.session_state.relampago_redacao = ''
                        st.session_state.relampago_aval_redacao = ''
                        st.rerun()

            # ── ESCREVENDO ──
            elif fase == 'escrevendo':
                import time

                tema = st.session_state.relampago_tema
                inicio = st.session_state.relampago_inicio
                duracao = st.session_state.relampago_duracao
                decorrido = time.time() - inicio
                restante = max(0, duracao - decorrido)
                mins = int(restante // 60)
                segs = int(restante % 60)
                pct_tempo = max(0, 1 - decorrido / duracao)
                cor_timer = "#22C55E" if pct_tempo > 0.5 else ("#B45309" if pct_tempo > 0.2 else "#B91C1C")

                # 1. TEMA — topo, destaque máximo
                st.markdown(
                    "<div style='background:linear-gradient(135deg,#FFFBEB,#FEF3C7);"
                    "border:3px solid #F59E0B;border-radius:14px;padding:18px 24px;margin-bottom:12px;'>"
                    "<div style='color:#92400E;font-size:0.72em;letter-spacing:2px;margin-bottom:6px;font-weight:600;'>⚡ TEMA DA REDAÇÃO</div>"
                    f"<div style='color:#1A1A2E;font-size:1.25em;font-weight:700;line-height:1.5;'>{tema}</div>"
                    "</div>",
                    unsafe_allow_html=True
                )

                # 2. CRONÔMETRO — embaixo do tema
                st.markdown(
                    f"<div style='background:#FFFFFF;border:3px solid {cor_timer};border-radius:12px;"
                    f"padding:10px 20px;margin-bottom:12px;display:flex;align-items:center;gap:16px;'>"
                    f"<div style='flex:1;background:#F1F5F9;border-radius:999px;height:10px;overflow:hidden;'>"
                    f"<div style='height:100%;border-radius:999px;background:{cor_timer};width:{pct_tempo*100:.0f}%;'></div>"
                    f"</div>"
                    f"<div style='font-size:2em;font-weight:700;color:{cor_timer};font-family:\"Playfair Display\",serif;white-space:nowrap;'>⏱️ {mins:02d}:{segs:02d}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

                # 3. ÁREA DE ESCRITA — embaixo do cronômetro
                texto_atual = st.text_area(
                    "✍️ Escreva sua redação:",
                    value=st.session_state.relampago_redacao,
                    height=380,
                    placeholder="Comece a escrever sua redação aqui...",
                    key="area_redacao_relampago"
                )
                st.session_state.relampago_redacao = texto_atual
                palavras = len(texto_atual.split()) if texto_atual.strip() else 0
                st.markdown(f"<small style='color:#64748B;'>📝 {palavras} palavras</small>", unsafe_allow_html=True)

                col_e, col_a = st.columns([3,1])
                with col_e:
                    encerrar_manual = st.button("📤 ENCERRAR E CORRIGIR AGORA", use_container_width=True)
                with col_a:
                    if st.button("🗑️ Abandonar", use_container_width=True):
                        st.session_state.relampago_fase = 'menu'; st.rerun()

                # Verifica se tempo acabou OU clicou em encerrar
                tempo_esgotado = restante <= 0

                if encerrar_manual or tempo_esgotado:
                    redacao_final = st.session_state.relampago_redacao
                    if tempo_esgotado and not redacao_final.strip():
                        st.warning("⏱️ Tempo esgotado! Sem texto para corrigir.")
                        st.session_state.relampago_fase = 'menu'; st.rerun()
                    else:
                        with st.spinner("⏱️ Tempo encerrado! A IA está corrigindo sua redação..."):
                            prompt_correcao = (
                                f"Corrija esta redação de concurso público.\n"
                                f"Concurso: {st.session_state.get('concurso_foco','geral')}.\n"
                                f"Tema: {tema}\n\n"
                                f"{'⚠️ ATENÇÃO: O tempo acabou antes da redação ser concluída. Corrija o que foi escrito.' if tempo_esgotado else ''}\n\n"
                                f"Redação do candidato:\n{redacao_final or '(sem texto)'}\n\n"
                                f"FORMATO DA CORREÇÃO:\n\n"
                                f"⏱️ {'TEMPO ESGOTADO — redação incompleta avaliada' if tempo_esgotado else 'Redação concluída pelo candidato'}\n\n"
                                f"📊 NOTA ESTIMADA: [X]/100\n\n"
                                f"| Critério | Pontos obtidos | Máximo |\n"
                                f"|---|---|---|\n"
                                f"| 🎯 Atendimento ao tema | [X] | 25 |\n"
                                f"| 🧠 Argumentação | [X] | 25 |\n"
                                f"| 🏗️ Estrutura | [X] | 15 |\n"
                                f"| 🔗 Coesão e coerência | [X] | 15 |\n"
                                f"| 📖 Linguagem e gramática | [X] | 15 |\n"
                                f"| 📝 Adequação à proposta | [X] | 5 |\n"
                                f"| **TOTAL** | **[X]** | **100** |\n\n"
                                f"✅ PONTOS FORTES:\n[o que você fez bem]\n\n"
                                f"❌ DEFICIÊNCIAS IDENTIFICADAS:\n[lista clara dos problemas com exemplos do texto]\n\n"
                                f"🎯 PLANO DE REFORÇO PERSONALIZADO:\n\n"
                                f"1. PRIORIDADE MÁXIMA — [critério mais fraco]:\n"
                                f"   • Por que você errou: [análise]\n"
                                f"   • O que estudar: [conteúdo específico]\n"
                                f"   • Como praticar: [exercício concreto]\n\n"
                                f"2. PRIORIDADE ALTA — [segundo critério mais fraco]:\n"
                                f"   • Por que você errou: [análise]\n"
                                f"   • O que estudar: [conteúdo específico]\n"
                                f"   • Como praticar: [exercício concreto]\n\n"
                                f"3. MANTER — [o que já está bom e como consolidar]\n\n"
                                f"⚡ PRÓXIMO SIMULADO RECOMENDADO: [quando fazer + foco específico]\n\n"
                                f"⚠️ Esta nota é uma estimativa de treinamento. A nota oficial é atribuída pela banca."
                            )
                            aval = tutor_ia(prompt_correcao)

                        # Salva no histórico
                        if 'relampago_historico' not in st.session_state:
                            st.session_state.relampago_historico = []
                        st.session_state.relampago_historico.append({
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                            'tema': tema,
                            'redacao': redacao_final,
                            'avaliacao': aval,
                            'tempo_esgotado': tempo_esgotado,
                        })
                        salvar_estudo("Relâmpago", tema[:60], aval)
                        ganhar_xp('simulado')
                        st.session_state.relampago_aval_redacao = aval
                        st.session_state.relampago_fase = 'resultado'
                        st.rerun()
                else:
                    # Auto-refresh a cada 10 segundos
                    import time as time_mod
                    time_mod.sleep(0.1)
                    st.rerun()

            # ── RESULTADO ──
            elif fase == 'resultado':
                aval = st.session_state.get('relampago_aval_redacao','')
                tema = st.session_state.get('relampago_tema','')

                st.markdown(f"<div class='card-yellow'><strong>📌 Tema:</strong> {tema}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='card'>{aval}</div>", unsafe_allow_html=True)

                # Redação escrita
                with st.expander("📄 Ver minha redação"):
                    st.text(st.session_state.get('relampago_redacao','(sem texto)'))

                col_dl, col_novo = st.columns(2)
                with col_dl:
                    export = f"TEMA:\n{tema}\n\nREDAÇÃO:\n{st.session_state.get('relampago_redacao','')}\n\nAVALIAÇÃO:\n{aval}"
                    st.download_button("📋 Baixar resultado (.txt)", data=export,
                        file_name="redacao_resultado.txt", mime="text/plain", use_container_width=True)
                with col_novo:
                    if st.button("⚡ NOVO SIMULADO", use_container_width=True):
                        st.session_state.relampago_fase = 'menu'
                        st.session_state.relampago_tema = ''
                        st.session_state.relampago_redacao = ''
                        st.session_state.relampago_aval_redacao = ''
                        st.rerun()

                # Histórico
                hist = st.session_state.get('relampago_historico', [])
                if len(hist) > 1:
                    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
                    st.markdown(f"### 📈 Seus Simulados ({len(hist)} realizados)")
                    for i, h in enumerate(reversed(hist[-5:])):
                        icone = "⏱️" if h.get('tempo_esgotado') else "✅"
                        with st.expander(f"{icone} {h['data']} — {h['tema'][:60]}..."):
                            st.markdown(f"<div class='card'>{h['avaliacao'][:400]}...</div>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # SIMULADO DE MÚLTIPLA ESCOLHA
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "SimuladoMC":
        import time as _tsmc, re as _rsmc

        st.header("📋 Simulado de Múltipla Escolha")
        st.markdown("*Questões sempre novas — o sistema nunca repete uma questão que você já respondeu.*")

        for _k,_v in [('smc_fase','menu'),('smc_questoes',[]),('smc_idx',0),
                      ('smc_respostas',{}),('smc_inicio',0),('smc_duracao',3600),
                      ('smc_materia',''),('smc_resultado',None),('smc_historico',[]),
                      ('smc_vistas',[]),('smc_escolha',None)]:
            if _k not in st.session_state: st.session_state[_k] = _v

        fase_smc = st.session_state.smc_fase

        # ── MENU ──
        if fase_smc == 'menu':
            if st.session_state.smc_resultado:
                res = st.session_state.smc_resultado
                taxa = int(res['acertos']/max(res['total'],1)*100)
                cor_r = "#059669" if taxa>=70 else ("#B45309" if taxa>=50 else "#B91C1C")
                st.markdown(f"<div style='background:#FFFFFF;border:2px solid {cor_r};border-radius:12px;padding:12px 18px;margin-bottom:16px;'><strong style='color:{cor_r};'>Último resultado:</strong> <span style='color:#1A1A2E;'>{res['acertos']}/{res['total']} ({taxa}%) — {res['materia']} — {res['tempo_gasto']}</span></div>", unsafe_allow_html=True)

            total_v = len(st.session_state.smc_vistas)
            if total_v > 0:
                st.markdown(f"<div class='card-yellow' style='padding:10px 14px;font-size:0.88em;'>📚 Você já respondeu <strong>{total_v}</strong> questões únicas. Nunca serão repetidas.</div>", unsafe_allow_html=True)

            col1,col2 = st.columns(2)
            with col1:
                mat = st.text_input("📚 Matéria:", value=st.session_state.smc_materia, placeholder="ex: Direito Constitucional, Matemática...")
                nivel = st.selectbox("Dificuldade:", ["Fácil","Médio","Difícil","Misto"])
            with col2:
                nq = st.selectbox("Questões por rodada:", [5,10,15,20], index=1)
                tempo = st.selectbox("Tempo:", ["30 min","1 hora","2 horas","Sem limite"])
                conc = st.text_input("Concurso (opcional):", value=st.session_state.get('concurso_foco',''))

            if st.button("📋 GERAR E INICIAR", use_container_width=True):
                if mat.strip():
                    with st.spinner(f"Gerando {nq} questões inéditas de {mat}..."):
                        vistas_txt = ", ".join(st.session_state.smc_vistas[-20:]) if st.session_state.smc_vistas else "nenhuma"
                        prompt_q = (
                            f"Crie exatamente {nq} questões de múltipla escolha sobre {mat}.\n"
                            f"Concurso: {conc or 'concurso público geral'}. Dificuldade: {nivel}.\n"
                            f"NÃO repita assuntos similares aos já usados: {vistas_txt}\n\n"
                            f"Use EXATAMENTE este formato para cada questão:\n\n"
                            f"QUESTÃO [N]\n"
                            f"[Enunciado]\n"
                            f"(A) [texto]\n(B) [texto]\n(C) [texto]\n(D) [texto]\n(E) [texto]\n"
                            f"GABARITO: [letra]\n"
                            f"EXPLICAÇÃO: [1-2 linhas]\n\n"
                            f"Repita para todas as {nq} questões."
                        )
                        txt = tutor_ia(prompt_q)
                        # Parse
                        blocos = _rsmc.split(r'QUESTÃO\s+\d+\s*\n', txt)
                        qs = []
                        for b in [x.strip() for x in blocos if len(x.strip())>20]:
                            alts = _rsmc.findall(r'\(([A-E])\)\s*([^\n(]+)', b)
                            gab  = _rsmc.search(r'GABARITO:\s*([A-E])', b)
                            exp  = _rsmc.search(r'EXPLICAÇÃO:\s*(.+?)(?=\nQUESTÃO|\Z)', b, _rsmc.DOTALL)
                            enun = _rsmc.split(r'\([A-E]\)', b)[0]
                            enun = _rsmc.sub(r'GABARITO.*|EXPLICAÇÃO.*','',enun,flags=_rsmc.DOTALL).strip()
                            if len(alts)>=3 and gab and enun:
                                qs.append({'enunciado':enun,'alternativas':{l:t.strip() for l,t in alts},'gabarito':gab.group(1),'explicacao':exp.group(1).strip()[:200] if exp else ''})
                        if qs:
                            dur = {'30 min':1800,'1 hora':3600,'2 horas':7200,'Sem limite':999999}
                            st.session_state.smc_questoes  = qs
                            st.session_state.smc_idx       = 0
                            st.session_state.smc_respostas = {}
                            st.session_state.smc_inicio    = _tsmc.time()
                            st.session_state.smc_duracao   = dur[tempo]
                            st.session_state.smc_materia   = mat
                            st.session_state.smc_resultado = None
                            st.session_state.smc_escolha   = None
                            # Anti-repetição
                            for q in qs:
                                r = q['enunciado'][:50]
                                if r not in st.session_state.smc_vistas:
                                    st.session_state.smc_vistas.append(r)
                            st.session_state.smc_fase = 'fazendo'
                            st.rerun()
                        else:
                            st.error("Não consegui gerar as questões. Tente novamente.")
                else:
                    st.warning("Informe a matéria.")

            if st.session_state.smc_historico:
                st.markdown("<hr class='divider'>", unsafe_allow_html=True)
                st.markdown("### 📈 Histórico")
                for h in reversed(st.session_state.smc_historico[-6:]):
                    taxa_h = int(h['acertos']/max(h['total'],1)*100)
                    cor_h = "#059669" if taxa_h>=70 else ("#B45309" if taxa_h>=50 else "#B91C1C")
                    st.markdown(f"<div class='hist-item'><span class='badge'>{h['materia'][:25]}</span> <small style='color:#888;'>{h['data']}</small><strong style='color:{cor_h};float:right;'>{h['acertos']}/{h['total']} ({taxa_h}%)</strong></div>", unsafe_allow_html=True)

        # ── QUESTÃO POR VEZ ──
        elif fase_smc == 'fazendo':
            qs     = st.session_state.smc_questoes
            idx    = st.session_state.smc_idx
            total  = len(qs)
            dur    = st.session_state.smc_duracao
            dec    = _tsmc.time() - st.session_state.smc_inicio
            sem_lim = dur >= 999999

            if not sem_lim:
                rest = max(0, dur - dec)
                mins_t, segs_t = int(rest//60), int(rest%60)
                pct_t = max(0, 1-dec/dur)
                cor_t = "#22C55E" if pct_t>0.5 else ("#B45309" if pct_t>0.2 else "#B91C1C")
                timer_str = f"⏱️ {mins_t:02d}:{segs_t:02d}"
                esgotado = rest <= 0
            else:
                cor_t, timer_str, esgotado = "#1D4ED8", "⏱️ Sem limite", False

            # Header progresso + timer
            pct_p = int(idx/total*100)
            st.markdown(
                f"<div style='background:#FFFBEB;border:1px solid #FCD34D;border-radius:10px;"
                f"padding:10px 16px;margin-bottom:16px;display:flex;align-items:center;gap:14px;'>"
                f"<div style='flex:1;'><div style='font-size:0.82em;color:#92400E;font-weight:600;margin-bottom:4px;'>"
                f"📋 {st.session_state.smc_materia} — Questão {idx+1} de {total}</div>"
                f"<div style='background:#FEF3C7;border-radius:999px;height:8px;overflow:hidden;'>"
                f"<div style='height:100%;border-radius:999px;background:#D97706;width:{pct_p}%;'></div>"
                f"</div></div>"
                f"<span style='font-size:1.1em;font-weight:700;color:{cor_t};white-space:nowrap;'>{timer_str}</span>"
                f"</div>",
                unsafe_allow_html=True
            )

            if esgotado:
                if st.session_state.smc_escolha:
                    st.session_state.smc_respostas[idx] = st.session_state.smc_escolha
                st.session_state.smc_fase = 'gabarito'; st.rerun()

            if idx < total:
                q = qs[idx]
                st.markdown(f"<div class='questao-box'><strong>Questão {idx+1}</strong><br><br>{q['enunciado']}</div>", unsafe_allow_html=True)

                opcoes = [f"({l}) {t}" for l,t in sorted(q['alternativas'].items())]
                esc = st.session_state.smc_escolha
                idx_s = next((j for j,op in enumerate(opcoes) if esc and op.startswith(f"({esc})")), None)

                escolha = st.radio("", opcoes, index=idx_s, key=f"rq{idx}", label_visibility="collapsed")
                if escolha:
                    st.session_state.smc_escolha = escolha[1]

                col_e, col_a = st.columns([3,1])
                with col_e:
                    lbl = "✅ FINALIZAR E VER GABARITO" if idx==total-1 else "➡️ PRÓXIMA QUESTÃO"
                    if st.button(lbl, use_container_width=True):
                        if st.session_state.smc_escolha:
                            st.session_state.smc_respostas[idx] = st.session_state.smc_escolha
                            if idx < total-1:
                                st.session_state.smc_idx += 1
                                st.session_state.smc_escolha = None
                                st.rerun()
                            else:
                                st.session_state.smc_fase = 'gabarito'; st.rerun()
                        else:
                            st.warning("Selecione uma alternativa antes de avançar.")
                with col_a:
                    if st.button("🚩 Sair", use_container_width=True):
                        st.session_state.smc_fase = 'menu'
                        st.session_state.smc_questoes = []
                        st.rerun()

                if not sem_lim:
                    _tsmc.sleep(0.8); st.rerun()

        # ── GABARITO ──
        elif fase_smc == 'gabarito':
            qs     = st.session_state.smc_questoes
            resps  = st.session_state.smc_respostas
            total  = len(qs)
            dec    = _tsmc.time() - st.session_state.smc_inicio
            tg_m, tg_s = int(dec//60), int(dec%60)
            acertos = sum(1 for i,q in enumerate(qs) if resps.get(i)==q['gabarito'])
            taxa = int(acertos/max(total,1)*100)
            cor_taxa = "#059669" if taxa>=70 else ("#B45309" if taxa>=50 else "#B91C1C")

            if not st.session_state.smc_resultado:
                res = {'acertos':acertos,'total':total,'materia':st.session_state.smc_materia,
                       'tempo_gasto':f"{tg_m}min{tg_s:02d}s",'data':datetime.now().strftime('%d/%m %H:%M')}
                st.session_state.smc_resultado = res
                st.session_state.smc_historico.append(res)
                salvar_estudo("Simulado MC", st.session_state.smc_materia, f"Acertos: {acertos}/{total} ({taxa}%)")
                ganhar_xp('simulado')

            st.markdown(
                f"<div style='background:#FFFFFF;border:3px solid {cor_taxa};border-radius:16px;"
                f"padding:20px 24px;margin-bottom:20px;text-align:center;'>"
                f"<div style='font-size:3em;font-weight:700;color:{cor_taxa};'>{taxa}%</div>"
                f"<div style='color:#1A1A2E;font-size:1em;margin-top:4px;'>{acertos} de {total} corretas · {st.session_state.smc_materia} · {tg_m}min{tg_s:02d}s</div>"
                f"</div>", unsafe_allow_html=True
            )

            st.markdown("### 📋 Gabarito")
            for i,q in enumerate(qs):
                resp = resps.get(i,'—')
                gab  = q['gabarito']
                ok   = resp==gab
                with st.expander(f"{'✅' if ok else '❌'} Questão {i+1} — {'CORRETA' if ok else f'ERRADA — você:({resp}) gabarito:({gab})'}"):
                    st.markdown(f"**{q['enunciado']}**")
                    for l,t in sorted(q['alternativas'].items()):
                        if l==gab:
                            st.markdown(f"<span style='color:#059669;font-weight:700;'>✔ ({l}) {t}</span>", unsafe_allow_html=True)
                        elif l==resp and not ok:
                            st.markdown(f"<span style='color:#B91C1C;'>✗ ({l}) {t}</span>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"({l}) {t}")
                    if q['explicacao']:
                        st.markdown(f"<div class='card-green' style='padding:10px 14px;font-size:0.88em;margin-top:8px;'>💡 {q['explicacao']}</div>", unsafe_allow_html=True)

            col_n, col_d = st.columns(2)
            with col_n:
                if st.button("📋 NOVO SIMULADO", use_container_width=True):
                    st.session_state.smc_fase='menu'; st.session_state.smc_questoes=[]
                    st.session_state.smc_respostas={}; st.session_state.smc_idx=0
                    st.session_state.smc_escolha=None; st.rerun()
            with col_d:
                exp_txt = f"SIMULADO — {st.session_state.smc_materia}\n{acertos}/{total} ({taxa}%)\n\n"
                for i,q in enumerate(qs):
                    r=resps.get(i,'—'); g=q['gabarito']
                    exp_txt += f"Q{i+1}: ({r}) | Gabarito:({g}) | {'OK' if r==g else 'ERROU'}\n{q['enunciado'][:80]}\n{q['explicacao']}\n\n"
                st.download_button("📋 Baixar gabarito", data=exp_txt, file_name="gabarito.txt", mime="text/plain", use_container_width=True)

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Tutor de Concursos IA — Mentor Estratégico · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
