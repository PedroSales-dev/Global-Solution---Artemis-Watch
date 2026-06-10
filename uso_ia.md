# Registro de Uso de Inteligência Artificial

## Partes em que a IA foi utilizada

A inteligência artificial (Claude — Anthropic) foi utilizada como apoio nas seguintes etapas:

1. **Geração de dados simulados:** A IA auxiliou na criação de valores realistas para a telemetria da missão (leituras de energia, temperatura, radiação), garantindo coerência com cenários documentados de missões lunares reais (Apollo, Artemis).

2. **Revisão de texto:** Trechos do README e do relatório foram revisados pela IA para clareza e coesão, mas o conteúdo técnico e as conclusões são originais.

3. **Explicação de conceitos:** A IA foi consultada para esclarecer a fórmula de mínimos quadrados da regressão linear simples durante a implementação.

## O que NÃO foi feito pela IA

- A lógica computacional completa (regras booleanas, classificação de estados, geração de alertas) foi estruturada e codificada pelo aluno.
- As escolhas de estruturas de dados e sua justificativa são decisões próprias.
- A análise das inconsistências e a interpretação dos resultados foram realizadas pelo aluno.

## Validação crítica realizada

- Todos os dados simulados foram verificados manualmente para garantir que refletem uma progressão lógica de eclipse lunar (energia solar decrescente → bateria caindo → radiação aumentando).
- A inconsistência proposital (temperatura 220°C) foi inserida conscientemente e verificada que o sistema a detecta corretamente.
- Os coeficientes da regressão linear foram calculados manualmente em uma planilha para validar o resultado do código.
- O código foi executado e testado localmente antes da entrega.
