# AGENTS.md – Harness da Creality K1 Max

Este repositório guarda o agente e as skills que ajudam o **Alexandre** e o **Marcelo** (irmãos que dividem a mesma **Creality K1 Max**) a **projetar peças** e preparar impressões, entregando projetos `.3mf` do **Creality Print 7** prontos para fatiar.

## Idioma e estilo
- Responda sempre em **português**.
- Entregue arquivos prontos, não explicações longas. **Precisão vale mais que velocidade.**
- Se notar uma melhoria, **pergunte antes de aplicar** (múltipla escolha curta, opção recomendada primeiro).

## Estrutura
| Caminho | O que é |
|---|---|
| `.claude/agents/configurador-impressao-k1max.md` | Subagente principal: fluxo de trabalho, regras invioláveis e checklist de entrega |
| `.claude/skills/k1max-config-impressao/SKILL.md` | Equipamento, perfis de filamento calibrados e receitas por tipo de peça |
| `.claude/skills/modelagem-3d/SKILL.md` | Projetar uma peça do zero (SolidCraft via MCP): regras de projeto para a K1 Max, prévia e exportação |
| `.claude/skills/creality-print-3mf/SKILL.md` | Estrutura do `.3mf`, chaves de configuração, como gerar/revisar/alterar projetos por script e onde fica cada opção no Creality Print aberto |
| `.claude/skills/creality-print-3mf/gerar_projeto_creality.py` | Gera o `.3mf` de um **modelo novo** a partir de um projeto modelo + projeto de configuração |
| `.claude/skills/creality-print-3mf/alterar_config_3mf.py` | Altera só as configurações de um **`.3mf` existente** (malhas intactas); `--sem-altura-variavel` para suporte Organic |
| `.claude/skills/k1max-calibracao/SKILL.md` | Calibração (flow, PA, fluxo volumétrico, retração) e troca de bico 0,4/0,2 |
| `projetos-base/` | Projetos `.3mf` de referência (por bico e filamento) usados como `MODELO`/`CONFIG` na geração |
| `requirements.txt` | Bibliotecas Python dos scripts e da análise de malha |

## Quando usar o quê
- **Projetar uma peça nova** (a partir de medidas, desenho ou foto) → skill `modelagem-3d` para modelar; depois o agente `configurador-impressao-k1max` prepara a impressão.
- **Qualquer pedido de impressão** (STL, 3MF, GLB, STEP), revisão de `.3mf`, troca de bico ou calibração → delegue ao agente `configurador-impressao-k1max`.
- O agente lê `k1max-config-impressao` **sempre**, `creality-print-3mf` ao gerar/editar projeto e `k1max-calibracao` só para calibração.

## Regras invioláveis (resumo – detalhes no agente)
- Não alterar configurações de **filamento** sem pedir.
- Brim encostado: `brim_object_gap = 0` **e** `elefant_foot_compensation = 0`.
- Não usar reparo automático de malha (pymeshfix etc.).
- Nunca afirmar algo que não aconteceu.
- PLA: lembrar da **tampa aberta**. Trocou o bico: **autoteste e nivelamento**.
- Todo projeto entregue vai acompanhado do **checklist** do agente, verificado por código.

## Ambientes por pessoa
Antes de salvar ou rodar algo, identifique **em qual computador** a sessão está (`uname`, caminho do repositório). Não use o caminho de um no computador do outro.

| | Alexandre | Marcelo |
|---|---|---|
| Sistema | Windows | macOS |
| Pasta de entrega | `C:\Users\alemg\Downloads` | `~/Downloads` (`/Users/marcelosander/Downloads`) |
| Python | **não instalado** (em 19/11/2026): use PowerShell (veja `creality-print-3mf`) | `.venv` do repositório (`.venv/bin/python`) |
| Creality Print | 7.x, perfis em `AppData\Roaming\Creality` (não editar direto) | instalado em `/Applications/Creality Print.app` |
| Modelagem | Fusion 360 e SolidCraft (com MCP) | SolidCraft com MCP (em configuração) |

- Primeira vez num Mac/Linux: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`.
- Rode os scripts com o Python do `.venv`, por exemplo `.venv/bin/python .claude/skills/creality-print-3mf/gerar_projeto_creality.py ...`.
- Os perfis do Creality não são editados diretamente: entregue perfis como pacote `.creality_printer` para importar.

## Manutenção
- Skills novas: `.claude/skills/<nome>/SKILL.md` com frontmatter `name` e `description`.
- Agentes novos: `.claude/agents/<nome>.md`.
- Ao calibrar um filamento novo, atualize a tabela de perfis em `k1max-config-impressao`.
- Ao salvar um projeto de referência novo, coloque em `projetos-base/` e atualize o `README.md` de lá.
