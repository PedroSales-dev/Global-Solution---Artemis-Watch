
import csv
import os

# ─────────────────────────────────────────────
# SEÇÃO 1 — DADOS SIMULADOS DA MISSÃO
# ─────────────────────────────────────────────

# Caminho dos arquivos CSV de dados
ARQUIVO_TELEMETRIA = os.path.join(os.path.dirname(__file__), '..', 'data', 'telemetria.csv')
ARQUIVO_LOG        = os.path.join(os.path.dirname(__file__), '..', 'data', 'log_eventos.csv')

# Limites operacionais de segurança (faixas definidas pela missão)
LIMITES = {
    'reserva_bateria_critica'  : 15.0,   # % abaixo = crítico
    'reserva_bateria_alerta'   : 30.0,   # % abaixo = alerta
    'temperatura_interna_max'  : 30.0,   # °C acima = alerta
    'temperatura_interna_min'  : 18.0,   # °C abaixo = alerta
    'radiacao_alerta'          : 3.0,    # mSv/h acima = alerta
    'radiacao_critica'         : 4.0,    # mSv/h acima = crítico
    'qualidade_sinal_alerta'   : 75.0,   # % abaixo = alerta
    'qualidade_sinal_critica'  : 50.0,   # % abaixo = crítico
    'consumo_max'              : 50.0,   # kWh — limite de consumo aceitável
}

# Status binários dos módulos críticos (1 = operacional, 0 = falha)
# Expressão booleana do diagnóstico geral:
# missao_segura = suporte_vida AND energia AND comunicacao AND habitat
#                 AND NOT (radiacao_critica OR temperatura_anomala)
MODULOS = {
    'suporte_vida' : 1,   # Sistema de suporte à vida (oxigênio, pressão)
    'energia'      : 1,   # Sistema de geração e armazenamento de energia
    'comunicacao'  : 1,   # Antena e transponder de comunicação
    'habitat'      : 1,   # Módulo de habitação tripulada
    'laboratorio'  : 0,   # Laboratório científico (em reinicialização)
    'armazenamento': 1,   # Depósito de suprimentos e amostras
}

# Hierarquia da missão representada como dicionário aninhado (árvore)
HIERARQUIA_MISSAO = {
    'LUNA-7': {
        'energia': {
            'solar'   : {'status': 0, 'desc': 'Painéis solares — eclipse ativo'},
            'baterias': {'status': 1, 'desc': 'Baterias de íon-lítio — operacional'},
            'nuclear' : {'status': 1, 'desc': 'RTG auxiliar — operacional'},
        },
        'habitat': {
            'oxigenio'    : {'status': 1, 'desc': 'Gerador de O2 — normal'},
            'temperatura' : {'status': 1, 'desc': 'Controle térmico — normal'},
            'pressao'     : {'status': 1, 'desc': 'Pressurização — normal'},
        },
        'comunicacao': {
            'antena_principal': {'status': 1, 'desc': 'Antena X-band — operacional'},
            'antena_backup'   : {'status': 1, 'desc': 'Antena UHF backup — standby'},
        },
    }
}


# ─────────────────────────────────────────────
# SEÇÃO 2 — LEITURA E ORGANIZAÇÃO DOS DADOS
# ─────────────────────────────────────────────

def carregar_telemetria(caminho: str) -> list:
    """
    Lê o arquivo CSV de telemetria e retorna uma lista de dicionários.
    Cada dicionário representa uma leitura horária da missão.
    Estrutura usada: LISTA de registros.
    """
    registros = []
    try:
        with open(caminho, newline='', encoding='utf-8') as f:
            leitor = csv.DictReader(f)
            for linha in leitor:
                # Converte campos numéricos; mantém string nos campos de tempo
                registro = {
                    'horario'                : linha['horario'],
                    'geracao_solar_kwh'      : float(linha['geracao_solar_kwh']),
                    'consumo_kwh'            : float(linha['consumo_kwh']),
                    'reserva_bateria_pct'    : float(linha['reserva_bateria_pct']),
                    'temperatura_interna_c'  : float(linha['temperatura_interna_c']),
                    'temperatura_externa_c'  : float(linha['temperatura_externa_c']),
                    'radiacao_msv'           : float(linha['radiacao_msv']),
                    'qualidade_sinal_pct'    : float(linha['qualidade_sinal_pct']),
                    'vento_lunar_ms'         : float(linha['vento_lunar_ms']),
                }
                registros.append(registro)
    except FileNotFoundError:
        print(f"[AVISO] Arquivo não encontrado: {caminho}. Usando dados embutidos.")
        registros = gerar_dados_embutidos()
    return registros


def gerar_dados_embutidos() -> list:
    """
    Fallback: retorna dados simulados embutidos no código caso
    os arquivos CSV não sejam encontrados.
    """
    return [
        {'horario':'06:00','geracao_solar_kwh':42.5,'consumo_kwh':38.2,'reserva_bateria_pct':87.0,'temperatura_interna_c':21.3,'temperatura_externa_c':-142.0,'radiacao_msv':0.8,'qualidade_sinal_pct':95.0,'vento_lunar_ms':0.0},
        {'horario':'08:00','geracao_solar_kwh':55.1,'consumo_kwh':40.7,'reserva_bateria_pct':91.2,'temperatura_interna_c':22.1,'temperatura_externa_c':-138.5,'radiacao_msv':1.1,'qualidade_sinal_pct':97.0,'vento_lunar_ms':0.0},
        {'horario':'10:00','geracao_solar_kwh':61.3,'consumo_kwh':43.5,'reserva_bateria_pct':94.8,'temperatura_interna_c':22.8,'temperatura_externa_c':-130.0,'radiacao_msv':1.4,'qualidade_sinal_pct':98.0,'vento_lunar_ms':0.0},
        {'horario':'12:00','geracao_solar_kwh':58.7,'consumo_kwh':45.2,'reserva_bateria_pct':96.1,'temperatura_interna_c':23.5,'temperatura_externa_c':-128.0,'radiacao_msv':1.6,'qualidade_sinal_pct':96.0,'vento_lunar_ms':0.0},
        {'horario':'14:00','geracao_solar_kwh':47.9,'consumo_kwh':46.8,'reserva_bateria_pct':93.4,'temperatura_interna_c':23.9,'temperatura_externa_c':-131.0,'radiacao_msv':1.9,'qualidade_sinal_pct':94.0,'vento_lunar_ms':0.0},
        {'horario':'16:00','geracao_solar_kwh':31.2,'consumo_kwh':47.5,'reserva_bateria_pct':85.7,'temperatura_interna_c':24.1,'temperatura_externa_c':-135.0,'radiacao_msv':2.3,'qualidade_sinal_pct':91.0,'vento_lunar_ms':0.0},
        {'horario':'18:00','geracao_solar_kwh':12.4,'consumo_kwh':48.1,'reserva_bateria_pct':72.3,'temperatura_interna_c':23.7,'temperatura_externa_c':-140.0,'radiacao_msv':2.7,'qualidade_sinal_pct':88.0,'vento_lunar_ms':0.0},
        {'horario':'20:00','geracao_solar_kwh':0.0,'consumo_kwh':48.9,'reserva_bateria_pct':58.6,'temperatura_interna_c':23.2,'temperatura_externa_c':-145.0,'radiacao_msv':3.1,'qualidade_sinal_pct':85.0,'vento_lunar_ms':0.0},
        {'horario':'22:00','geracao_solar_kwh':0.0,'consumo_kwh':49.3,'reserva_bateria_pct':44.1,'temperatura_interna_c':22.8,'temperatura_externa_c':-149.0,'radiacao_msv':3.4,'qualidade_sinal_pct':83.0,'vento_lunar_ms':0.0},
        {'horario':'00:00','geracao_solar_kwh':0.0,'consumo_kwh':50.2,'reserva_bateria_pct':28.9,'temperatura_interna_c':22.1,'temperatura_externa_c':-152.0,'radiacao_msv':3.8,'qualidade_sinal_pct':80.0,'vento_lunar_ms':0.0},
        {'horario':'02:00','geracao_solar_kwh':0.0,'consumo_kwh':51.7,'reserva_bateria_pct':12.4,'temperatura_interna_c':21.5,'temperatura_externa_c':-155.0,'radiacao_msv':4.2,'qualidade_sinal_pct':76.0,'vento_lunar_ms':0.0},
        {'horario':'04:00','geracao_solar_kwh':0.0,'consumo_kwh':52.1,'reserva_bateria_pct':8.3,'temperatura_interna_c':220.0,'temperatura_externa_c':-158.0,'radiacao_msv':4.5,'qualidade_sinal_pct':71.0,'vento_lunar_ms':0.0},
    ]


def carregar_log_eventos(caminho: str) -> list:
    """
    Lê o arquivo de log e retorna lista de eventos ordenados por timestamp.
    Estrutura: LISTA de dicionários.
    """
    eventos = []
    try:
        with open(caminho, newline='', encoding='utf-8') as f:
            leitor = csv.DictReader(f)
            for linha in leitor:
                eventos.append({
                    'timestamp': linha['timestamp'],
                    'tipo'     : linha['tipo'],
                    'modulo'   : linha['modulo'],
                    'descricao': linha['descricao'],
                })
    except FileNotFoundError:
        pass
    return eventos


def construir_estruturas(registros: list) -> dict:
    """
    Organiza os dados brutos em todas as estruturas exigidas pelo projeto:
      - Listas de séries temporais
      - Dicionário (hash) de leitura atual por variável
      - Matriz horário × variável
    """
    # LISTAS — séries temporais de cada variável crítica
    lista_geracao    = [r['geracao_solar_kwh']   for r in registros]
    lista_consumo    = [r['consumo_kwh']          for r in registros]
    lista_reserva    = [r['reserva_bateria_pct']  for r in registros]
    lista_temp_int   = [r['temperatura_interna_c'] for r in registros]
    lista_radiacao   = [r['radiacao_msv']          for r in registros]
    lista_sinal      = [r['qualidade_sinal_pct']   for r in registros]
    lista_horarios   = [r['horario']               for r in registros]

    # DICIONÁRIO (hash) — acesso rápido ao valor mais recente por variável
    leitura_atual = {
        'geracao_solar_kwh'    : registros[-1]['geracao_solar_kwh'],
        'consumo_kwh'          : registros[-1]['consumo_kwh'],
        'reserva_bateria_pct'  : registros[-1]['reserva_bateria_pct'],
        'temperatura_interna_c': registros[-1]['temperatura_interna_c'],
        'temperatura_externa_c': registros[-1]['temperatura_externa_c'],
        'radiacao_msv'         : registros[-1]['radiacao_msv'],
        'qualidade_sinal_pct'  : registros[-1]['qualidade_sinal_pct'],
    }

    # MATRIZ — leituras numéricas por horário e variável
    # Colunas: geracao, consumo, reserva, temp_int, radiacao, sinal
    colunas_matriz = ['geracao_solar_kwh', 'consumo_kwh', 'reserva_bateria_pct',
                      'temperatura_interna_c', 'radiacao_msv', 'qualidade_sinal_pct']
    matriz_telemetria = []
    for r in registros:
        linha_matriz = [r[col] for col in colunas_matriz]
        matriz_telemetria.append(linha_matriz)

    return {
        'lista_geracao'    : lista_geracao,
        'lista_consumo'    : lista_consumo,
        'lista_reserva'    : lista_reserva,
        'lista_temp_int'   : lista_temp_int,
        'lista_radiacao'   : lista_radiacao,
        'lista_sinal'      : lista_sinal,
        'lista_horarios'   : lista_horarios,
        'leitura_atual'    : leitura_atual,
        'matriz_telemetria': matriz_telemetria,
        'colunas_matriz'   : colunas_matriz,
    }


# ─────────────────────────────────────────────
# SEÇÃO 3 — DIAGNÓSTICO E REGRAS LÓGICAS
# ─────────────────────────────────────────────

def detectar_inconsistencias(registros: list, limites: dict) -> list:
    """
    Verifica os dados em busca de leituras fisicamente impossíveis
    ou fora de qualquer faixa plausível (anomalias de sensor).
    Retorna lista com inconsistências encontradas.

    Regra booleana:
      anomalia = (temp_interna > 100 OR temp_interna < -50) OR
                 (reserva > 100 OR reserva < 0) OR
                 (geracao < 0)
    """
    anomalias = []
    for r in registros:
        # Temperatura interna humana impossível fora de [-10, 60] °C na cabine
        if r['temperatura_interna_c'] > 100 or r['temperatura_interna_c'] < -10:
            anomalias.append({
                'horario': r['horario'],
                'campo'  : 'temperatura_interna_c',
                'valor'  : r['temperatura_interna_c'],
                'motivo' : 'Leitura fora da faixa física possível para cabine pressurizada',
            })
        # Reserva de bateria deve estar entre 0 e 100
        if not (0.0 <= r['reserva_bateria_pct'] <= 100.0):
            anomalias.append({
                'horario': r['horario'],
                'campo'  : 'reserva_bateria_pct',
                'valor'  : r['reserva_bateria_pct'],
                'motivo' : 'Percentual de bateria fora do intervalo [0, 100]',
            })
        # Geração solar não pode ser negativa
        if r['geracao_solar_kwh'] < 0:
            anomalias.append({
                'horario': r['horario'],
                'campo'  : 'geracao_solar_kwh',
                'valor'  : r['geracao_solar_kwh'],
                'motivo' : 'Valor negativo de geração solar é impossível',
            })
    return anomalias


def classificar_modulos(modulos: dict) -> dict:
    """
    Classifica cada módulo em: NORMAL, ALERTA ou CRÍTICO.
    Módulos não binários poderiam ter leituras parciais; aqui
    usamos o estado binário (0/1) diretamente.
    """
    status_modulos = {}
    for nome, estado in modulos.items():
        if estado == 1:
            status_modulos[nome] = 'NORMAL'
        else:
            # Se o módulo é suporte à vida ou energia, a falha é CRÍTICA
            if nome in ('suporte_vida', 'energia'):
                status_modulos[nome] = 'CRÍTICO'
            else:
                status_modulos[nome] = 'ALERTA'
    return status_modulos


def diagnosticar_missao(leitura: dict, modulos: dict, limites: dict) -> dict:
    """
    Avalia o estado geral da missão aplicando regras lógicas combinadas.

    Expressão booleana principal:
      EMERGENCIA = (reserva < critica AND NOT comunicacao) OR
                   (NOT suporte_vida) OR
                   (NOT energia AND reserva < critica)

      CRITICO    = (reserva < critica) OR (radiacao >= critica) OR
                   (temperatura_anomala AND NOT emergencia)

      ALERTA     = (reserva < alerta) OR (radiacao >= alerta) OR
                   (sinal < alerta) OR (modulo_nao_essencial_falho)

      NORMAL     = NOT (EMERGENCIA OR CRITICO OR ALERTA)
    """
    reserva    = leitura['reserva_bateria_pct']
    radiacao   = leitura['radiacao_msv']
    sinal      = leitura['qualidade_sinal_pct']
    temp_int   = leitura['temperatura_interna_c']

    # Estados derivados dos módulos
    com_comunicacao  = bool(modulos['comunicacao'])
    com_energia      = bool(modulos['energia'])
    com_suporte_vida = bool(modulos['suporte_vida'])

    # Flags de condição ambiental
    reserva_critica   = reserva  < limites['reserva_bateria_critica']
    reserva_alerta    = reserva  < limites['reserva_bateria_alerta']
    radiacao_critica  = radiacao >= limites['radiacao_critica']
    radiacao_alerta   = radiacao >= limites['radiacao_alerta']
    sinal_alerta      = sinal    < limites['qualidade_sinal_alerta']
    sinal_critico     = sinal    < limites['qualidade_sinal_critica']
    temp_anomala      = (temp_int > limites['temperatura_interna_max'] or
                         temp_int < limites['temperatura_interna_min'])

    # ── Regra 1: EMERGÊNCIA (AND com múltiplas falhas simultâneas)
    emergencia = (
        (reserva_critica and not com_comunicacao) or
        (not com_suporte_vida) or
        (not com_energia and reserva_critica)
    )

    # ── Regra 2: CRÍTICO (OR de condições graves individuais)
    critico = (
        reserva_critica or
        radiacao_critica or
        (temp_anomala and not emergencia) or
        sinal_critico
    )

    # ── Regra 3: ALERTA (OR de condições moderadas, NOT emergência/crítico)
    alerta = (
        not emergencia and not critico and (
            reserva_alerta or
            radiacao_alerta or
            sinal_alerta or
            modulos['laboratorio'] == 0
        )
    )

    # Estado final
    if emergencia:
        estado = 'EMERGÊNCIA'
    elif critico:
        estado = 'CRÍTICO'
    elif alerta:
        estado = 'ALERTA'
    else:
        estado = 'NORMAL'

    return {
        'estado'          : estado,
        'reserva_critica' : reserva_critica,
        'reserva_alerta'  : reserva_alerta,
        'radiacao_critica': radiacao_critica,
        'radiacao_alerta' : radiacao_alerta,
        'sinal_alerta'    : sinal_alerta,
        'sinal_critico'   : sinal_critico,
        'temp_anomala'    : temp_anomala,
        'emergencia'      : emergencia,
    }


# ─────────────────────────────────────────────
# SEÇÃO 4 — FILA DE ALERTAS E PILHA DE EVENTOS
# ─────────────────────────────────────────────

def gerar_alertas(diagnostico: dict, leitura: dict, modulos: dict) -> list:
    """
    Cria alertas priorizados com base no diagnóstico.
    Retorna uma FILA (lista ordenada por severidade) de alertas pendentes.

    Severidade: 3 = Emergência | 2 = Crítico | 1 = Alerta | 0 = Info
    """
    fila_alertas = []   # Estrutura FILA — append + sort por prioridade

    # ── Alertas de módulos
    if not modulos['suporte_vida']:
        fila_alertas.append({
            'severidade': 3,
            'nivel'     : 'EMERGÊNCIA',
            'modulo'    : 'SUPORTE À VIDA',
            'mensagem'  : 'Falha crítica no suporte à vida detectada.',
            'acao'      : 'Acionar protocolo RED-ALPHA imediatamente. Verificar O2 e pressão da cabine.',
        })

    if not modulos['energia']:
        fila_alertas.append({
            'severidade': 3,
            'nivel'     : 'EMERGÊNCIA',
            'modulo'    : 'ENERGIA',
            'mensagem'  : 'Sistema de energia principal inoperante.',
            'acao'      : 'Ativar RTG de emergência. Isolar todos os circuitos não essenciais.',
        })

    reserva = leitura['reserva_bateria_pct']
    if reserva < 15.0:
        fila_alertas.append({
            'severidade': 2,
            'nivel'     : 'CRÍTICO',
            'modulo'    : 'BATERIA',
            'mensagem'  : f'Reserva de bateria em {reserva:.1f}% — abaixo do limite crítico (15%).',
            'acao'      : 'Desligar laboratório, sistemas de pesquisa e aquecimento não vital. Priorizar suporte à vida e comunicação.',
        })
    elif reserva < 30.0:
        fila_alertas.append({
            'severidade': 1,
            'nivel'     : 'ALERTA',
            'modulo'    : 'BATERIA',
            'mensagem'  : f'Reserva de bateria em {reserva:.1f}% — abaixo de 30%.',
            'acao'      : 'Ativar modo de economia energética. Reduzir consumo de sistemas secundários.',
        })

    radiacao = leitura['radiacao_msv']
    if radiacao >= 4.0:
        fila_alertas.append({
            'severidade': 2,
            'nivel'     : 'CRÍTICO',
            'modulo'    : 'RADIAÇÃO',
            'mensagem'  : f'Nível de radiação em {radiacao:.1f} mSv/h — acima do limite crítico (4.0).',
            'acao'      : 'Mover tripulação para compartimento blindado. Cancelar EVAs.',
        })
    elif radiacao >= 3.0:
        fila_alertas.append({
            'severidade': 1,
            'nivel'     : 'ALERTA',
            'modulo'    : 'RADIAÇÃO',
            'mensagem'  : f'Nível de radiação em {radiacao:.1f} mSv/h — acima do limite de alerta (3.0).',
            'acao'      : 'Suspender atividades externas. Monitorar dosimetria individual.',
        })

    sinal = leitura['qualidade_sinal_pct']
    if sinal < 50.0:
        fila_alertas.append({
            'severidade': 2,
            'nivel'     : 'CRÍTICO',
            'modulo'    : 'COMUNICAÇÃO',
            'mensagem'  : f'Qualidade de sinal em {sinal:.0f}% — comunicação severamente degradada.',
            'acao'      : 'Ativar antena UHF de backup. Enviar pacote de status comprimido à Terra.',
        })
    elif sinal < 75.0:
        fila_alertas.append({
            'severidade': 1,
            'nivel'     : 'ALERTA',
            'modulo'    : 'COMUNICAÇÃO',
            'mensagem'  : f'Qualidade de sinal em {sinal:.0f}% — degradação detectada.',
            'acao'      : 'Verificar orientação da antena principal. Reduzir volume de telemetria enviada.',
        })

    if diagnostico['temp_anomala']:
        temp = leitura['temperatura_interna_c']
        fila_alertas.append({
            'severidade': 2,
            'nivel'     : 'CRÍTICO',
            'modulo'    : 'HABITAT/SENSOR',
            'mensagem'  : f'Temperatura interna anômala: {temp:.1f}°C — possível falha de sensor ou emergência térmica.',
            'acao'      : 'Verificar sensor BMP-07 do habitat. Checar sistema de controle térmico.',
        })

    if not modulos['laboratorio']:
        fila_alertas.append({
            'severidade': 0,
            'nivel'     : 'INFO',
            'modulo'    : 'LABORATÓRIO',
            'mensagem'  : 'Módulo de laboratório está offline.',
            'acao'      : 'Experimentos científicos suspensos. Reinicializar após estabilização energética.',
        })

    # Ordena a fila: maior severidade primeiro (prioridade decrescente)
    fila_alertas.sort(key=lambda x: x['severidade'], reverse=True)
    return fila_alertas


def registrar_pilha_eventos(log_eventos: list, n: int = 5) -> list:
    """
    Extrai os N eventos mais recentes do log e os organiza como PILHA
    (último evento no topo = índice 0 após reverter).
    Estrutura: PILHA — last-in, first-out.
    """
    # Filtra apenas eventos CRÍTICOS para a pilha de análise
    criticos = [e for e in log_eventos if e['tipo'] in ('CRITICO', 'REINICIALIZACAO')]
    pilha = list(reversed(criticos[-n:]))  # topo = evento mais recente
    return pilha


# ─────────────────────────────────────────────
# SEÇÃO 5 — ANÁLISE E PREVISÃO ENERGÉTICA
# ─────────────────────────────────────────────

def regressao_linear_simples(x: list, y: list):
    """
    Calcula os coeficientes de regressão linear (mínimos quadrados)
    sem bibliotecas externas.

    Fórmula:
      b = (n * Σxy - Σx * Σy) / (n * Σx² - (Σx)²)
      a = (Σy - b * Σx) / n

    Retorna (a, b) onde y_previsto = a + b * x
    """
    n = len(x)
    soma_x   = sum(x)
    soma_y   = sum(y)
    soma_xy  = sum(x[i] * y[i] for i in range(n))
    soma_x2  = sum(xi ** 2 for xi in x)

    denominador = n * soma_x2 - soma_x ** 2
    if denominador == 0:
        return soma_y / n, 0.0   # linha horizontal

    b = (n * soma_xy - soma_x * soma_y) / denominador
    a = (soma_y - b * soma_x) / n
    return a, b


def prever_energia(lista_reserva: list, lista_horarios: list) -> dict:
    """
    Aplica regressão linear sobre a reserva de bateria para estimar
    o comportamento nos próximos 2 ciclos de 2 horas (4 horas à frente).

    A variável x é o índice temporal (0, 1, 2, …), e y é a reserva (%).
    A previsão influencia as recomendações do sistema.
    """
    n = len(lista_reserva)
    x = list(range(n))
    y = lista_reserva

    a, b = regressao_linear_simples(x, y)

    # Previsão para os próximos 2 pontos
    previsao = []
    for passo in range(1, 3):
        x_futuro  = n - 1 + passo
        y_previsto = a + b * x_futuro
        y_previsto = max(0.0, min(100.0, y_previsto))   # clamp [0, 100]
        previsao.append({
            'passo'    : passo,
            'x_futuro' : x_futuro,
            'reserva_prevista_pct': round(y_previsto, 2),
        })

    tendencia = 'QUEDA' if b < -0.5 else ('ESTÁVEL' if abs(b) <= 0.5 else 'ALTA')

    return {
        'coef_angular'  : round(b, 4),
        'coef_linear'   : round(a, 4),
        'tendencia'     : tendencia,
        'previsao'      : previsao,
        'ultimo_valor'  : lista_reserva[-1],
        'ultimo_horario': lista_horarios[-1],
    }


def gerar_recomendacoes(diagnostico: dict, previsao: dict, leitura: dict) -> list:
    """
    Gera recomendações técnicas priorizadas baseadas no diagnóstico
    e na previsão energética.

    A previsão influencia diretamente as recomendações:
    se a reserva prevista for < 15%, recomendações de emergência são
    geradas mesmo que a situação atual ainda não seja crítica.
    """
    recs = []
    estado  = diagnostico['estado']
    reserva = leitura['reserva_bateria_pct']

    # Recomendações sempre presentes
    if diagnostico['temp_anomala']:
        recs.append(('[CRÍTICO] Verificar sensor BMP-07 do habitat — leitura de temperatura '
                     'incompatível com operação segura.'))

    if estado in ('EMERGÊNCIA', 'CRÍTICO'):
        recs.append(('[CRÍTICO] Ativar Protocolo de Preservação de Missão: '
                     'manter suporte à vida e comunicação de emergência como prioridade absoluta.'))

    if diagnostico['reserva_critica']:
        recs.append(('[CRÍTICO] Desligar imediatamente: laboratório, '
                     'iluminação não essencial e aquecimento de compartimentos desocupados.'))

    if diagnostico['reserva_alerta'] and not diagnostico['reserva_critica']:
        recs.append(('[ALTO] Ativar modo de economia energética nível 2: '
                     'reduzir processamento científico e heating de módulos secundários.'))

    if diagnostico['radiacao_critica']:
        recs.append(('[CRÍTICO] Recolher tripulação ao abrigo blindado central. '
                     'Cancelar qualquer EVA planejado.'))

    if diagnostico['sinal_alerta']:
        recs.append(('[ALTO] Ativar antena UHF de backup. '
                     'Priorizar transmissão de dados de telemetria essenciais.'))

    # Recomendações baseadas na previsão (look-ahead)
    for p in previsao['previsao']:
        if p['reserva_prevista_pct'] < 15.0:
            recs.append((f'[PREVISÃO — EMERGÊNCIA] Em {p["passo"]*2}h a reserva atingirá '
                         f'{p["reserva_prevista_pct"]:.1f}%. '
                         'Iniciar redirecionamento de carga para RTG agora.'))
        elif p['reserva_prevista_pct'] < 30.0:
            recs.append((f'[PREVISÃO — ALERTA] Em {p["passo"]*2}h a reserva será '
                         f'{p["reserva_prevista_pct"]:.1f}%. '
                         'Planejar redução de carga preventiva.'))

    if previsao['tendencia'] == 'QUEDA':
        recs.append(('[ESTRATÉGICO] Tendência de queda energética confirmada. '
                     'Verificar previsão de fim do eclipse e ajustar orientação dos painéis.'))

    if not recs:
        recs.append('[INFO] Missão operando dentro dos parâmetros normais. Continuar monitoramento de rotina.')

    return recs


# ─────────────────────────────────────────────
# SEÇÃO 6 — SAÍDA FORMATADA NO TERMINAL
# ─────────────────────────────────────────────

def separador(char: str = '─', largura: int = 65) -> str:
    return char * largura


def exibir_cabecalho():
    print(separador('═'))
    print('  ARTEMIS-WATCH v1.0  |  Sistema de Monitoramento Lunar')
    print('  Missão: LUNA-7  |  Órbita Lunar Baixa  |  FIAP 2026')
    print(separador('═'))
    print()


def exibir_status_modulos(modulos: dict, status_classificado: dict):
    print(separador())
    print('  STATUS DOS MÓDULOS CRÍTICOS')
    print(separador())
    icones = {'NORMAL': '✓', 'ALERTA': '!', 'CRÍTICO': '✗'}
    for nome, status in status_classificado.items():
        icone = icones.get(status, '?')
        bin_val = modulos[nome]
        print(f'  [{icone}] {nome.upper():<16} {status:<10} (bin: {bin_val})')
    print()


def exibir_leituras_atuais(leitura: dict):
    print(separador())
    print('  LEITURA ATUAL DOS SENSORES (Último ciclo registrado)')
    print(separador())
    print(f"  Reserva de bateria   : {leitura['reserva_bateria_pct']:.1f} %")
    print(f"  Geração solar        : {leitura['geracao_solar_kwh']:.1f} kWh")
    print(f"  Consumo              : {leitura['consumo_kwh']:.1f} kWh")
    print(f"  Temperatura interna  : {leitura['temperatura_interna_c']:.1f} °C")
    print(f"  Temperatura externa  : {leitura['temperatura_externa_c']:.1f} °C")
    print(f"  Radiação             : {leitura['radiacao_msv']:.1f} mSv/h")
    print(f"  Qualidade do sinal   : {leitura['qualidade_sinal_pct']:.0f} %")
    print()


def exibir_inconsistencias(anomalias: list):
    print(separador())
    print('  DIAGNÓSTICO DE INCONSISTÊNCIAS NOS DADOS')
    print(separador())
    if not anomalias:
        print('  Nenhuma inconsistência detectada.')
    else:
        for a in anomalias:
            print(f"  [!] Horário {a['horario']} | Campo: {a['campo']}")
            print(f"      Valor lido : {a['valor']}")
            print(f"      Motivo     : {a['motivo']}")
    print()


def exibir_diagnostico(diagnostico: dict):
    print(separador('═'))
    estado = diagnostico['estado']
    marcadores = {
        'NORMAL'    : '[ NORMAL ]',
        'ALERTA'    : '[! ALERTA ]',
        'CRÍTICO'   : '[!! CRÍTICO !!]',
        'EMERGÊNCIA': '[!!! EMERGÊNCIA !!!]',
    }
    print(f"  ESTADO DA MISSÃO: {marcadores.get(estado, estado)}")
    print(separador('═'))
    print()


def exibir_matriz_telemetria(matriz: list, colunas: list, horarios: list):
    print(separador())
    print('  MATRIZ DE TELEMETRIA (horário × variável)')
    print(separador())
    # Cabeçalho encurtado
    nomes_curtos = ['Geração', 'Consumo', 'Reserva%', 'T.Int°C', 'Rad.mSv', 'Sinal%']
    header = f"  {'Hora':<7}" + ''.join(f"{n:>10}" for n in nomes_curtos)
    print(header)
    print('  ' + '-' * 63)
    for i, linha in enumerate(matriz):
        hora = horarios[i] if i < len(horarios) else str(i)
        valores = ''.join(f'{v:>10.1f}' for v in linha)
        print(f'  {hora:<7}{valores}')
    print()


def exibir_pilha_eventos(pilha: list):
    print(separador())
    print('  PILHA DE EVENTOS CRÍTICOS RECENTES (topo = mais recente)')
    print(separador())
    if not pilha:
        print('  Nenhum evento crítico registrado.')
    else:
        for i, ev in enumerate(pilha):
            prefixo = '>> TOPO' if i == 0 else f'   [{i+1}]  '
            print(f'  {prefixo} {ev["timestamp"]}')
            print(f'           Tipo: {ev["tipo"]} | Módulo: {ev["modulo"]}')
            print(f'           {ev["descricao"]}')
    print()


def exibir_fila_alertas(fila: list):
    print(separador())
    print('  FILA DE ALERTAS ATIVOS (ordem de prioridade)')
    print(separador())
    if not fila:
        print('  Nenhum alerta ativo no momento.')
    else:
        for i, al in enumerate(fila):
            print(f'  #{i+1} [{al["nivel"]}] — {al["modulo"]}')
            print(f'     Mensagem : {al["mensagem"]}')
            print(f'     Ação     : {al["acao"]}')
    print()


def exibir_previsao(previsao: dict):
    print(separador())
    print('  ANÁLISE E PREVISÃO ENERGÉTICA — Regressão Linear')
    print(separador())
    print(f"  Último valor registrado : {previsao['ultimo_valor']:.1f}% às {previsao['ultimo_horario']}")
    print(f"  Coeficiente angular (b) : {previsao['coef_angular']:.4f}  (variação/ciclo)")
    print(f"  Coeficiente linear  (a) : {previsao['coef_linear']:.4f}")
    print(f"  Tendência detectada     : {previsao['tendencia']}")
    print()
    print('  Projeções futuras:')
    for p in previsao['previsao']:
        horas = p['passo'] * 2
        print(f"    Em +{horas}h → Reserva prevista: {p['reserva_prevista_pct']:.2f}%")
    print()


def exibir_hierarquia(hierarquia: dict):
    print(separador())
    print('  HIERARQUIA DA MISSÃO LUNA-7')
    print(separador())
    for missao, subsistemas in hierarquia.items():
        print(f'  {missao}')
        for subsistema, componentes in subsistemas.items():
            print(f'  ├── {subsistema.upper()}')
            itens = list(componentes.items())
            for j, (comp, info) in enumerate(itens):
                prefix = '│   └──' if j == len(itens) - 1 else '│   ├──'
                status_str = 'OK' if info['status'] == 1 else 'FALHA'
                print(f'  {prefix} {comp}: [{status_str}] {info["desc"]}')
    print()


def exibir_recomendacoes(recs: list):
    print(separador('═'))
    print('  RECOMENDAÇÕES DO SISTEMA')
    print(separador('═'))
    for i, rec in enumerate(recs, 1):
        print(f'  {i}. {rec}')
    print()


# ─────────────────────────────────────────────
# SEÇÃO 7 — PROGRAMA PRINCIPAL
# ─────────────────────────────────────────────

def main():
    exibir_cabecalho()

    # 1. Carregar dados
    registros    = carregar_telemetria(ARQUIVO_TELEMETRIA)
    log_eventos  = carregar_log_eventos(ARQUIVO_LOG)

    # 2. Construir estruturas de dados
    estruturas = construir_estruturas(registros)
    leitura_atual    = estruturas['leitura_atual']
    lista_reserva    = estruturas['lista_reserva']
    lista_horarios   = estruturas['lista_horarios']
    matriz           = estruturas['matriz_telemetria']
    colunas          = estruturas['colunas_matriz']

    # 3. Diagnóstico
    anomalias         = detectar_inconsistencias(registros, LIMITES)
    status_modulos    = classificar_modulos(MODULOS)
    diagnostico       = diagnosticar_missao(leitura_atual, MODULOS, LIMITES)

    # 4. Alertas e eventos
    fila_alertas      = gerar_alertas(diagnostico, leitura_atual, MODULOS)
    pilha_eventos     = registrar_pilha_eventos(log_eventos)

    # 5. Previsão energética
    previsao_energia  = prever_energia(lista_reserva, lista_horarios)

    # 6. Recomendações
    recomendacoes     = gerar_recomendacoes(diagnostico, previsao_energia, leitura_atual)

    # 7. Exibição
    exibir_status_modulos(MODULOS, status_modulos)
    exibir_leituras_atuais(leitura_atual)
    exibir_inconsistencias(anomalias)
    exibir_diagnostico(diagnostico)
    exibir_matriz_telemetria(matriz, colunas, lista_horarios)
    exibir_pilha_eventos(pilha_eventos)
    exibir_fila_alertas(fila_alertas)
    exibir_previsao(previsao_energia)
    exibir_hierarquia(HIERARQUIA_MISSAO)
    exibir_recomendacoes(recomendacoes)

    print(separador('═'))
    print('  Monitoramento concluído. Próxima varredura em 2h.')
    print(separador('═'))


if __name__ == '__main__':
    main()
