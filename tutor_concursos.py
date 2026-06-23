import streamlit as st
from groq import Groq
from datetime import datetime
import json
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="TUTOR DE CONCURSOS", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500;600&display=swap');

    .stApp { background-color: #FFFFFF; color: #000000; font-family: 'DM Sans', sans-serif; }
    [data-testid="stSidebar"] { display: none; }

    .stTextInput>div>div>input,
    .stTextArea>div>textarea,
    .stSelectbox>div>div>div {
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

    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #1A1A2E !important; }
    p, span, label, div { color: #1A1A2E !important; font-family: 'DM Sans', sans-serif; }

    .card {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #FCD34D; margin-bottom: 15px;
        color: #1A1A2E; box-shadow: 0 2px 12px rgba(217,119,6,0.08);
        white-space: pre-wrap;
    }
    .card-dark {
        background: linear-gradient(135deg, #1C1100 0%, #2D1A00 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #D97706; margin-bottom: 15px;
        white-space: pre-wrap;
    }
    .card-dark, .card-dark * { color: #FDE68A !important; }

    .card-blue {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #93C5FD; margin-bottom: 15px;
        white-space: pre-wrap;
    }
    .card-green {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #86EFAC; margin-bottom: 15px;
        white-space: pre-wrap;
    }
    .card-red {
        background: linear-gradient(135deg, #FFF5F5 0%, #FEE2E2 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #FECACA; margin-bottom: 15px;
        white-space: pre-wrap;
    }
    .card-purple {
        background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #C4B5FD; margin-bottom: 15px;
        white-space: pre-wrap;
    }

    .badge         { background: #D97706; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-verde   { background: #059669; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-azul    { background: #1D4ED8; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-roxo    { background: #7C3AED; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-red     { background: #EF4444; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }

    .stat-box { background: #FFFBEB; border-radius: 12px; padding: 18px; text-align: center; border: 1px solid #FCD34D; }
    .stat-numero { font-size: 2em; font-weight: 700; color: #D97706 !important; font-family: 'Playfair Display', serif; }

    .hist-item { background: #FFFBEB; border-radius: 10px; padding: 12px 16px; margin-bottom: 8px; border-left: 4px solid #F59E0B; }

    .questao-box {
        background: #FFFFFF; border: 2px solid #FCD34D; border-radius: 14px;
        padding: 20px; margin-bottom: 16px;
    }
    .perfil-btn>button {
        background: linear-gradient(135deg, #D97706, #F59E0B) !important;
        color: white !important; font-weight: 700 !important;
        border-radius: 12px !important; height: 3em !important;
    }

    .divider { border: none; height: 1px; background: linear-gradient(to right, transparent, #FCD34D, transparent); margin: 20px 0; }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_tutor():
    return {"perfis": {}}

_cache = get_cache_tutor()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'historico_estudos', 'biblioteca_materiais',
    'concurso_foco', 'materias_foco', 'horas_disponiveis',
    'nivel_conhecimento', 'data_prova', 'pontuacao_total',
    'questoes_respondidas', 'questoes_certas',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados: dict):
    for k in CHAVES_SALVAR:
        if k in dados:
            st.session_state[k] = dados[k]

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_estudo(tipo: str, materia: str, conteudo: str):
    st.session_state.historico_estudos.append({
        'data':    datetime.now().strftime('%d/%m %H:%M'),
        'tipo':    tipo,
        'materia': materia,
        'conteudo': conteudo,
    })

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa':               "Login",
    'usuario':             "",
    'api_key':             "",
    'pagina':              "Home",
    'historico_estudos':   [],
    'biblioteca_materiais':[],
    'concurso_foco':       "",
    'materias_foco':       "",
    'horas_disponiveis':   "2",
    'nivel_conhecimento':  "Iniciante",
    'data_prova':          "",
    'pontuacao_total':     0,
    'questoes_respondidas':0,
    'questoes_certas':     0,
    'questoes_ativas':     [],
    'respondendo_idx':     0,
    'respostas_sessao':    [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- MOTOR DE IA ---
def tutor_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f"""Você é um tutor especialista em concursos públicos e estudos no Brasil.
Usuário: {st.session_state.usuario}.
Concurso/área foco: {st.session_state.concurso_foco or 'não informado'}.
{system_extra}
Seja didático, claro e motivador. Use exemplos práticos.
Foque no que cai mais em provas. Escreva em português brasileiro."""
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt},
            ],
            model="llama-3.3-70b-versatile",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total = len(st.session_state.historico_estudos)
    acertos = st.session_state.questoes_certas
    respondidas = st.session_state.questoes_respondidas
    taxa = round(acertos / respondidas * 100) if respondidas > 0 else 0

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#FFFBEB;border:1px solid #FCD34D;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} materiais gerados · "
            f"{respondidas} questões respondidas · {taxa}% de acerto</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="💾 SALVAR MEUS DADOS (.json)",
            data=gerar_json_sessao(),
            file_name=f"tutor_concursos_{nome_usuario}.json",
            mime="application/json",
            use_container_width=True,
        )
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if st.session_state.etapa == "Login":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("📚 TUTOR DE CONCURSOS")
        st.markdown("**Seu Tutor de Estudos e Concursos com Inteligência Artificial**")

        st.markdown("""<div style="background:#FFFBEB;border:1px solid #FCD34D;border-radius:10px;
        padding:10px 16px;margin:10px 0 16px 0;font-size:0.88em;color:#1A1A2E;line-height:1.6;">
        🔒 <strong>ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</strong><br>
        🔗 <a href="https://quizcompremios.com.br/" target="_blank"
        style="color:#D97706;font-weight:600;text-decoration:none;">quizcompremios.com.br</a>
        </div>""", unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        # ── PERFIS SALVOS NO SERVIDOR ─────────────────────────
        perfis = perfis_salvos()
        if perfis:
            st.markdown("#### 📚 Tutor de Concursos — clique para acessar seus dados")
            st.caption("Seus dados e progresso estão no servidor. Um clique e você entra.")
            chave_rapida = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_rapida")
            for nome_p in perfis:
                dados_p      = carregar_perfil_cache(nome_p)
                concurso_p   = dados_p.get('concurso_foco', '') if dados_p else ''
                respondidas_p= dados_p.get('questoes_respondidas', 0) if dados_p else 0
                certas_p     = dados_p.get('questoes_certas', 0) if dados_p else 0
                taxa_p       = round(certas_p / respondidas_p * 100) if respondidas_p > 0 else 0
                st.markdown('<div class="perfil-btn">', unsafe_allow_html=True)
                if st.button(
                    f"📚 {nome_p}  —  {concurso_p or 'concurso não definido'}  ·  {respondidas_p} questões  ·  {taxa_p}% acerto",
                    key=f"perfil_{nome_p}",
                    use_container_width=True
                ):
                    if not chave_rapida.strip():
                        st.warning("Cole sua chave API acima antes de entrar.")
                    else:
                        st.session_state.usuario = nome_p
                        st.session_state.api_key = chave_rapida
                        carregar_json_sessao(dados_p)
                        st.session_state.etapa = "App"
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("**Ou entre com outro nome:**")

        nome  = st.text_input("Seu Nome:")
        chave = st.text_input("Sua Chave API da Groq:", type="password", key="chave_nova")

        if not perfis:
            st.markdown("""<div style="background:#FFFBEB;border:1px solid #FCD34D;border-radius:10px;
            padding:12px 16px;font-size:0.86em;color:#1A1A2E;line-height:1.7;margin:10px 0;">
            📥 <strong>Seus dados sumiram?</strong> Isso acontece quando o servidor reinicia.<br>
            Selecione abaixo o arquivo <strong>.json</strong> que você salvou antes — seu progresso volta completo.
            </div>""", unsafe_allow_html=True)
            arq_login = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_login")
        else:
            arq_login = None

        dados_login = None
        if arq_login is not None:
            try:
                dados_login = json.load(arq_login)
                nome_login  = dados_login.get('usuario', '')
                st.success(f"✅ Dados de **{nome_login}** reconhecidos! Clique em Entrar.")
            except Exception:
                st.error("Arquivo inválido.")
                dados_login = None

        if st.button("✨ ENTRAR E ESTUDAR"):
            if nome and chave:
                st.session_state.usuario = nome
                st.session_state.api_key = chave
                if dados_login:
                    carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

        st.markdown("🔑 Não tem chave Groq? Crie grátis em <a href='https://console.groq.com/keys' target='_blank' style='color:#D97706;font-weight:600;'>console.groq.com/keys</a>", unsafe_allow_html=True)

# ============================================================
# TELA: APP
# ============================================================
elif st.session_state.etapa == "App":

    barra_salvar()

    # NAVBAR
    cols = st.columns(9)
    paginas = [
        ("🏠", "Home"),
        ("📅", "Plano"),
        ("📖", "Resumo"),
        ("❓", "Questoes"),
        ("🧠", "Memoria"),
        ("⚡", "Revisao"),
        ("💬", "Tutor"),
        ("📚", "Biblioteca"),
        ("📈", "Progresso"),
    ]
    nomes_paginas = {
        "Home":      "Painel Principal",
        "Plano":     "Plano de Estudos",
        "Resumo":    "Gerador de Resumos",
        "Questoes":  "Simulado de Questões",
        "Memoria":   "Técnicas de Memorização",
        "Revisao":   "Revisão Espaçada",
        "Tutor":     "Tutor ao Vivo",
        "Biblioteca":"Biblioteca de Materiais",
        "Progresso": "Meu Progresso",
    }
    for i, (icone, pagina) in enumerate(paginas):
        if cols[i].button(icone, key=f"nav_{pagina}", help=nomes_paginas[pagina]):
            st.session_state.pagina = pagina
            st.rerun()

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ========================
    # HOME
    # ========================
    if st.session_state.pagina == "Home":
        col_u, col_r = st.columns([3, 1])
        with col_u:
            st.title(f"Olá, {st.session_state.usuario}! 📚")
            st.markdown("<span class='badge'>Modo Estudo</span>", unsafe_allow_html=True)
        with col_r:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚪 Sair"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        # AVISO SE DADOS SUMIRAM
        total_h = len(st.session_state.historico_estudos)
        if total_h == 0 and st.session_state.questoes_respondidas == 0:
            st.markdown("""<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
            padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
            ⚠️ Seus dados não estão mais no servidor.
            </div>""", unsafe_allow_html=True)
            arq_home = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_home")
            if arq_home is not None:
                try:
                    dados_home = json.load(arq_home)
                    carregar_json_sessao(dados_home)
                    salvar_perfil_cache(st.session_state.usuario)
                    st.success("✅ Dados e progresso recuperados!")
                    st.rerun()
                except Exception:
                    st.error("Arquivo inválido.")
            st.markdown("<br>", unsafe_allow_html=True)

        # PERFIL DO ESTUDANTE
        st.markdown("#### ⚙️ Configure seu perfil de estudos")
        col_a, col_b = st.columns(2)
        with col_a:
            st.session_state.concurso_foco     = st.text_input("Concurso ou área de estudo:", value=st.session_state.concurso_foco, placeholder="ex: ENEM, PRF, Banco do Brasil, OAB, Medicina...")
            st.session_state.materias_foco     = st.text_input("Matérias prioritárias:", value=st.session_state.materias_foco, placeholder="ex: Português, Matemática, Direito Constitucional...")
            st.session_state.data_prova        = st.text_input("Data da prova (se souber):", value=st.session_state.data_prova, placeholder="ex: março/2025, em 6 meses...")
        with col_b:
            st.session_state.horas_disponiveis = st.selectbox("Horas disponíveis por dia:", ["1 hora","2 horas","3 horas","4 horas","5+ horas"], index=["1 hora","2 horas","3 horas","4 horas","5+ horas"].index(st.session_state.horas_disponiveis) if st.session_state.horas_disponiveis in ["1 hora","2 horas","3 horas","4 horas","5+ horas"] else 1)
            st.session_state.nivel_conhecimento= st.selectbox("Seu nível atual:", ["Iniciante","Básico","Intermediário","Avançado"], index=["Iniciante","Básico","Intermediário","Avançado"].index(st.session_state.nivel_conhecimento) if st.session_state.nivel_conhecimento in ["Iniciante","Básico","Intermediário","Avançado"] else 0)

        st.markdown("<br>", unsafe_allow_html=True)

        # MÉTRICAS
        respondidas = st.session_state.questoes_respondidas
        certas      = st.session_state.questoes_certas
        taxa        = round(certas / respondidas * 100) if respondidas > 0 else 0
        tipos = {}
        for e in st.session_state.historico_estudos:
            tipos[e['tipo']] = tipos.get(e['tipo'], 0) + 1

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total_h}</div><div>Materiais gerados</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{respondidas}</div><div>Questões feitas</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{taxa}%</div><div>Taxa de acerto</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Resumo',0)}</div><div>Resumos</div></div>", unsafe_allow_html=True)
        c5.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Plano',0)}</div><div>Planos criados</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='card'>💡 <em>'Não é quem estuda mais que passa. É quem estuda certo.'</em></div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ O que cada aba faz")
        guia = {
            "📅 Plano":          "Cria seu cronograma de estudos personalizado — dia a dia até a prova",
            "📖 Resumo":         "Gera resumos completos de qualquer matéria ou tema específico",
            "❓ Questões":        "Simulado com questões no estilo da prova — gabarito e explicação",
            "🧠 Memória":         "Técnicas de memorização: mnemônicos, mapas mentais e associações",
            "⚡ Revisão":         "Sistema de revisão espaçada — o que revisar hoje para não esquecer",
            "💬 Tutor ao Vivo":   "Tire dúvidas sobre qualquer matéria com o tutor em tempo real",
            "📚 Biblioteca":      "Seus resumos e materiais salvos organizados por matéria",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — {desc}")

        if st.session_state.historico_estudos:
            st.markdown("### 🕐 Últimos Materiais Gerados")
            for item in reversed(st.session_state.historico_estudos[-4:]):
                st.markdown(
                    f"<div class='hist-item'>"
                    f"<span class='badge'>{item['tipo']}</span> "
                    f"<span class='badge-azul'>{item['materia'][:30]}</span> "
                    f"<small style='color:#888'>{item['data']}</small></div>",
                    unsafe_allow_html=True
                )

    # ========================
    # PLANO DE ESTUDOS
    # ========================
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

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Tutor de Concursos — Estudos e Aprovação com IA · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
