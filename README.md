<div align="center">

<br>

```
 █████╗ ██████╗ ████████╗███████╗███╗   ███╗██╗███████╗    ██╗    ██╗ █████╗ ████████╗ ██████╗██╗  ██╗
██╔══██╗██╔══██╗╚══██╔══╝██╔════╝████╗ ████║██║██╔════╝    ██║    ██║██╔══██╗╚══██╔══╝██╔════╝██║  ██║
███████║██████╔╝   ██║   █████╗  ██╔████╔██║██║███████╗    ██║ █╗ ██║███████║   ██║   ██║     ███████║
██╔══██║██╔══██╗   ██║   ██╔══╝  ██║╚██╔╝██║██║╚════██║    ██║███╗██║██╔══██║   ██║   ██║     ██╔══██║
██║  ██║██║  ██║   ██║   ███████╗██║ ╚═╝ ██║██║███████║    ╚███╔███╔╝██║  ██║   ██║   ╚██████╗██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝╚══════╝     ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝
```

**Sistema Inteligente de Monitoramento de Missão Lunar**

<br>

[![Python](https://img.shields.io/badge/Python-3.8+-1a3a5c?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Status](https://img.shields.io/badge/Status-Operacional-27ae60?style=flat-square&logoColor=white)]()
[![Missão](https://img.shields.io/badge/Missão-LUNA--7-2e86ab?style=flat-square&logoColor=white)]()
[![FIAP](https://img.shields.io/badge/FIAP-Global_Solution_2026-ed1c24?style=flat-square&logoColor=white)]()

<br>

</div>

---

> *"No silêncio da órbita lunar, dados são o único elo entre a tripulação e a sobrevivência."*

O **ARTEMIS-WATCH** é um sistema de monitoramento operacional desenvolvido para a missão **LUNA-7**. Durante um eclipse lunar de 12 horas — sem geração solar — ele interpreta telemetria em tempo real, classifica o estado da missão, detecta anomalias de sensores, gera alertas priorizados e prevê o colapso energético antes que ele aconteça.

<br>

---

<br>

## Identificação

<br>

| Campo | |
|:---|:---|
| **Aluno** | Pedro Sales |
| **RM** | RM572709 |
| **Curso** | Ciência da Computação — FIAP |
| **Período** | 1.º Semestre · Fases 1, 2 e 3 |
| **Entrega** | Global Solution · Junho de 2026 |

<br>

---

<br>

## O Cenário

A missão **LUNA-7** opera em órbita lunar baixa (LLO) a 100 km de altitude. Um eclipse lunar prolongado cessa completamente a geração solar — a sobrevivência depende das baterias de íon-lítio e do RTG auxiliar.

O que o sistema observa ao longo das 22 horas monitoradas:

```
  Horário   Reserva de Bateria                              Situação
  ────────  ──────────────────────────────────────────────  ─────────────────────
  06:00     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░   87.0%  Geração solar ativa
  12:00     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░   96.1%  Pico de geração
  18:00     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░   72.3%  Eclipse iniciando
  00:00     ▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░   28.9%  Eclipse total
  02:00     ▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   12.4%  ALERTA CRÍTICO
  04:00     ▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    8.3%  COLAPSO IMINENTE
```

Simultaneamente, a radiação sobe de **0.8 → 4.5 mSv/h** e o sinal de comunicação cai de **95% → 71%**. Uma leitura de **220°C** na temperatura interna sinaliza falha do sensor BMP-07.

<br>

---

<br>

## Estrutura do Repositório

```
global-solution/
│
├── src/
│   └── sistema.py            ← código principal — execute aqui
│
├── data/
│   ├── telemetria.csv        ← 12 leituras horárias · 8 variáveis por ciclo
│   └── log_eventos.csv       ← 12 eventos registrados ao longo da missão
│
├── docs/
│   ├── relatorio.pdf         ← relatório técnico completo (8 páginas)
│   ├── uso_ia.md             ← registro de uso de inteligência artificial
│   └── link_video.txt        ← link do vídeo no YouTube
│
└── README.md
```

<br>

---

<br>

## Como Executar

```bash
# Clone o repositório
git clone <URL_DO_REPOSITORIO>
cd global-solution

# Execute — Python puro, sem dependências externas
python src/sistema.py
```

O sistema localiza automaticamente os arquivos CSV em `data/`. Caso não os encontre, utiliza dados embutidos no código como fallback.

<br>

---

<br>

## Estruturas de Dados

Cada estrutura foi escolhida pela adequação ao problema — não por requisito formal.

<br>

| Estrutura | Aplicação no sistema | Justificativa técnica |
|:---|:---|:---|
| **Lista** | Séries temporais de geração, consumo, reserva, temperatura, radiação e sinal | Iteração cronológica, indexação direta e fatiamento para a regressão linear |
| **Fila** | Alertas ativos ordenados por severidade | Alertas críticos (prioridade 3) são processados antes dos informativos (prioridade 0) |
| **Pilha** | Últimos 5 eventos críticos do log — LIFO | O evento mais recente fica no topo, refletindo o estado imediato da missão |
| **Dicionário** | Leitura atual dos sensores; status dos módulos por nome | Acesso O(1) por chave — consulta direta sem iteração linear |
| **Dicionário aninhado** | Hierarquia `LUNA-7 → subsistemas → componentes` | Representa a estrutura pai-filho real de uma missão espacial com profundidade arbitrária |
| **Matriz (lista de listas)** | Tabela 12 × 6 de leituras horárias × variáveis | Organização bidimensional natural para dados multivariados ao longo do tempo |

<br>

---

<br>

## Lógica Booleana

O diagnóstico opera em cascata — um estado mais grave impede a ativação dos menos graves.

```python
EMERGÊNCIA = (reserva_critica AND NOT comunicacao)
          OR (NOT suporte_vida)
          OR (NOT energia AND reserva_critica)

CRÍTICO    = reserva_critica OR radiacao_critica
          OR (temp_anomala AND NOT emergencia)
          OR sinal_critico

ALERTA     = NOT emergencia AND NOT critico
         AND (reserva_alerta OR radiacao_alerta OR sinal_alerta OR NOT laboratorio)

NORMAL     = NOT (EMERGÊNCIA OR CRÍTICO OR ALERTA)
```

<br>

| Regra | Operadores usados | Razão da escolha |
|:---|:---:|:---|
| Emergência | `AND`, `NOT` | Exige falhas simultâneas — uma condição isolada não justifica o nível máximo |
| Crítico | `OR` | Qualquer condição grave individual já demanda ação imediata |
| Alerta | `AND NOT` | Impede que estados graves sejam reclassificados como simples alertas |
| Anomalia de sensor | `OR` com limites físicos | `temp > 100 OR temp < -10` — fora da física possível, independente da causa |

<br>

---

<br>

## Análise e Previsão Energética

**Técnica aplicada:** Regressão Linear Simples — implementada manualmente, sem bibliotecas externas.

```
  b  =  ( n · Σxy  −  Σx · Σy )  /  ( n · Σx²  −  (Σx)² )
  a  =  ( Σy  −  b · Σx )  /  n
  ŷ  =  a  +  b · x
```

Onde `x` é o índice temporal do ciclo (0 a 11) e `y` é a reserva de bateria em %.

<br>

| Parâmetro | Resultado |
|:---|:---|
| Coeficiente angular `b` | `−8.44` % por ciclo de 2 horas |
| Coeficiente linear `a` | `110.82` |
| Tendência detectada | **QUEDA** |
| Reserva atual — 04:00 | 8.3% |
| Previsão em +2h | 9.54% |
| Previsão em +4h | **1.10%** — colapso iminente |

A previsão influencia diretamente o sistema de recomendações: qualquer horizonte projetado abaixo de **15%** dispara automaticamente um alerta `PREVISÃO — EMERGÊNCIA`, antecipando a ação corretiva antes que o limite seja atingido.

<br>

---

<br>

## Saída do Sistema

```
═════════════════════════════════════════════════════════════════
  ARTEMIS-WATCH v1.0  |  Sistema de Monitoramento Lunar
  Missão: LUNA-7  |  Órbita Lunar Baixa  |  FIAP 2026
═════════════════════════════════════════════════════════════════

  STATUS DOS MÓDULOS CRÍTICOS
  ─────────────────────────────────────────────────────────────
  [✓] SUPORTE_VIDA     NORMAL     (bin: 1)
  [✓] ENERGIA          NORMAL     (bin: 1)
  [✓] COMUNICACAO      NORMAL     (bin: 1)
  [✓] HABITAT          NORMAL     (bin: 1)
  [!] LABORATORIO      ALERTA     (bin: 0)
  [✓] ARMAZENAMENTO    NORMAL     (bin: 1)

  DIAGNÓSTICO DE INCONSISTÊNCIAS
  ─────────────────────────────────────────────────────────────
  [!] 04:00 | temperatura_interna_c = 220.0°C
      Motivo: Leitura fora da faixa física possível para cabine pressurizada

═════════════════════════════════════════════════════════════════
  ESTADO DA MISSÃO: [!! CRÍTICO !!]
═════════════════════════════════════════════════════════════════

  FILA DE ALERTAS ATIVOS
  ─────────────────────────────────────────────────────────────
  #1 [CRÍTICO]  BATERIA      — Reserva em 8.3%    → Desligar sistemas não essenciais
  #2 [CRÍTICO]  RADIAÇÃO     — 4.5 mSv/h          → Recolher tripulação ao abrigo blindado
  #3 [CRÍTICO]  HABITAT      — 220.0°C (anomalia) → Verificar sensor BMP-07
  #4 [ALERTA]   COMUNICAÇÃO  — Sinal em 71%       → Ativar antena UHF backup
  #5 [INFO]     LABORATÓRIO  — Módulo offline     → Reinicializar após estabilização

  PREVISÃO ENERGÉTICA — Regressão Linear
  ─────────────────────────────────────────────────────────────
  Em +2h  →  reserva prevista: 9.54%
  Em +4h  →  reserva prevista: 1.10%  ← EMERGÊNCIA IMINENTE

  RECOMENDAÇÕES
  ═════════════════════════════════════════════════════════════
  1. [CRÍTICO]    Verificar sensor BMP-07 — leitura incompatível com operação segura
  2. [CRÍTICO]    Ativar Protocolo de Preservação de Missão
  3. [CRÍTICO]    Desligar laboratório, iluminação e aquecimento não vital
  4. [CRÍTICO]    Recolher tripulação ao abrigo blindado — cancelar EVAs
  5. [ALTO]       Ativar antena UHF de backup
  6. [PREVISÃO]   Em 2h reserva → 9.5% — redirecionar carga para RTG agora
  7. [PREVISÃO]   Em 4h reserva → 1.1% — emergência energética iminente
  8. [ESTRATÉGI.] Verificar fim do eclipse e reorientar painéis solares
```

<br>

---


<br>

## Conclusões

O **ARTEMIS-WATCH** demonstrou que listas, filas, pilhas, dicionários e matrizes não são abstrações acadêmicas — são as ferramentas que decidem se uma missão sobrevive a um eclipse de 12 horas.

A regressão linear implementada do zero foi o exercício mais revelador: saber que a bateria atingirá **1.1% em 4 horas** transforma um número em urgência operacional real. A inconsistência proposital no sensor de temperatura confirmou que validação de dados não é um detalhe opcional em sistemas críticos — é parte central do design.

Mais do que entregar código funcional, o projeto exigiu pensar como engenheiro: interpretar dados incompletos, justificar cada escolha técnica e transformar telemetria em decisões que protegem vidas.

<br>

---

<div align="center">

<br>

*FIAP · Engenharia de Software · Global Solution 2026*

</div>
