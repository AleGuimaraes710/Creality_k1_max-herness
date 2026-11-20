---
name: k1max-calibracao
description: Roteiro e contas das calibrações do Creality Print 7 na K1 Max do Alexandre (flow, pressure advance, fluxo volumétrico, retração) e procedimento de troca de bico 0,4/0,2. Use quando ele for calibrar filamento, trocar bico ou criar perfil novo.
---

# Calibração – K1 Max

## Antes de calibrar
- **Presets:** a impressora do bico em uso e o filamento **da versão daquele bico**. Por exemplo, para o bico 0,2: `PLA FLEXYGREEN @Creality K1 Max 0.2 nozzle`.
  - Nunca calibre em cima do perfil de outro bico, porque sobrescreve a calibração dele.
- **Processo:** o Standard do bico (`0.10mm Standard @Creality K1 Max 0.2 nozzle-1` ou o Standard 0,4).
  - Não use o processo Detalhe Miniaturas, porque o suporte e o brim ligados atrapalham as peças de teste.
- **Mesa:** High Temp Plate.
- **Depois de trocar o bico:** autoteste e nivelamento automático pela tela da impressora.

## Ordem recomendada
1. Fluxo (flow rate), primeiro o teste grosso e depois o fino.
2. Pressure advance.
3. Fluxo volumétrico máximo.
4. Retração (opcional, só se houver fiapos).
5. Torre de temperatura (opcional).

Depois de cada teste: clique no lápis do filamento, coloque o valor novo e **salve por cima do mesmo preset**, não com "salvar como".

## Contas

### Flow
- **Teste 1 (grosso):** flow novo = flow atual × (100 + valor) ÷ 100.
  - Exemplo: 0,98 com +10 dá 1,078.
- **Salve o resultado do teste 1 antes de rodar o teste 2.** O teste 2 é calculado sobre o flow salvo.
- **Teste 2 (fino):** flow final = flow do teste 1 × (100 + valor) ÷ 100.
  - Exemplo: 1,078 com −4 dá 1,035.
- Se ele rodou o teste 2 sem salvar o 1, o teste 2 não vale. Refaça.

### Pressure advance
- **Pattern:** escolha a linha com cantos mais nítidos; o valor está impresso ao lado.
- **Torre:** PA = início + altura do ponto bom (mm) × passo por mm.
  - Com início 0, fim 0,30 e passo 0,01, a torre tem cerca de 31 mm (30 mm de teste mais a base), e cada mm vale 0,01.
  - Exemplo: ponto bom a cerca de 20 mm dá PA 0,20.
- **Referências da Creality para o bico 0,2:** Hyper PLA 0,24; CR-PETG 0,29. Com o bico 0,4, o PA fica perto de 0,03–0,06.

### Fluxo volumétrico máximo
- Valor = início + altura × passo por mm.
  - Com início 1, fim 5 e passo 0,5, a torre tem 8 mm de teste mais a base, cerca de 10 mm.
- **Se a torre inteira saiu perfeita**, o limite real está acima do fim do teste. Salve o fim (já está comprovado) ou rode de novo com faixa maior (por exemplo, de 5 a 12).
- **Se falhou**, use cerca de 10% abaixo do ponto de falha.

### Retração
- Faixa de 0,2 a 1,0 mm. A dele no PLA é 0,4 mm, contra 0,8 mm no perfil da Creality para o bico 0,2.

## Resultados atuais
| Filamento / bico | Flow | PA | Fluxo máximo | Observação |
|---|---|---|---|---|
| PLA FLEXYGREEN / 0,4 | 0.98 | 0.052 | 20 | calibração original |
| PLA FLEXYGREEN / 0,2 | **1.035** | **0.20** | **5** | calibrado em 18/11/2026 |
| PETG MASTERPRINT / 0,4 | 0.95 | 0.025 | 18 | calibração original |
| PETG MASTERPRINT / 0,2 | 0.95 | 0.025 | 2.5 | **ainda não calibrado** (referência Creality: PA 0.29) |

Atualize esta tabela sempre que ele mandar resultados novos.

**Pendências sugeridas:**
- **PLA FLEXYGREEN / 0,4:** teste de retração. O perfil usa 0,4 mm e deu fios com várias peças na mesa; 0,8 mm é o padrão da Creality.
- **PETG MASTERPRINT / 0,4:** teste de fluxo volumétrico máximo. Os 18 mm³/s nunca foram testados, e acelerar uma impressão em PETG depende disso.

## Bico 0,2: dados oficiais da Creality (wiki da K1 Series)
- **Impressora:**
  - camada mín. 0,04 / máx. 0,14;
  - retração 0,8 mm, velocidade 30/30;
  - z-hop Slope, ângulo 3, limite de deslocamento 1 mm;
  - retração antes do wipe 90%, wipe 2 mm.
- **Processo:**
  - camada 0,10, 1ª 0,14, linha 0,22, 4 paredes, topo 7, base 5, 15% grid;
  - velocidades: externa 110, interna 130, infill 120, topo 100, gap 50, 1ª camada 18;
  - aceleração 10000 / paredes 3000 / 1ª camada 2000; jerk 3.
- **Hyper PLA:** 220 °C, mesa 50, flow 0,98, PA 0,24, fluxo máximo 3, tempo mínimo de camada 12 s, ventoinha lateral 80%.
- **CR-PETG:** 250 °C, mesa 70, flow 0,98, PA 0,29, fluxo máximo 2,5, ventoinha 40–80, lateral 0%.
- **Fontes externas:**
  - Bambu: fluxo máximo de 2 mm³/s (conservador); usuários usam de 5 a 10.
  - Evitar filamentos com partículas no bico 0,2.
  - As camadas grudam menos entre si do que com o 0,4.
