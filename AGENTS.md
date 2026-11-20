# AGENTS.md – Harness da Creality K1 Max

Este repositório guarda o agente e as skills que preparam impressões 3D para a **Creality K1 Max** do Alexandre, entregando projetos `.3mf` do **Creality Print 7** prontos para fatiar.

## Idioma e estilo
- Responda sempre em **português**.
- Entregue arquivos prontos, não explicações longas. **Precisão vale mais que velocidade.**
- Se notar uma melhoria, **pergunte antes de aplicar** (múltipla escolha curta, opção recomendada primeiro).

## Estrutura
| Caminho | O que é |
|---|---|
| `.claude/agents/configurador-impressao-k1max.md` | Subagente principal: fluxo de trabalho, regras invioláveis e checklist de entrega |
| `.claude/skills/k1max-config-impressao/SKILL.md` | Equipamento, perfis de filamento calibrados e receitas por tipo de peça |
| `.claude/skills/creality-print-3mf/SKILL.md` | Estrutura do `.3mf`, chaves de configuração, como gerar/revisar/alterar projetos por script e onde fica cada opção no Creality Print aberto |
| `.claude/skills/creality-print-3mf/gerar_projeto_creality.py` | Gera o `.3mf` de um **modelo novo** a partir de um projeto modelo + projeto de configuração |
| `.claude/skills/creality-print-3mf/alterar_config_3mf.py` | Altera só as configurações de um **`.3mf` existente** (malhas intactas); `--sem-altura-variavel` para suporte Organic |
| `.claude/skills/creality-print-3mf/adicionar_bloqueador_3mf.py` | Acrescenta caixas de **bloqueio ou reforço de suporte** a um objeto, em coordenadas da mesa |
| `.claude/skills/k1max-calibracao/SKILL.md` | Calibração (flow, PA, fluxo volumétrico, retração) e troca de bico 0,4/0,2 |
| `.claude/perfis/K1_Max_bico_0.2_Alexandre.creality_printer` | Pacote de perfis do bico 0,2 (impressora, processos e filamentos) para importar no Creality |
| `.claude/referencias/` | Projetos `.3mf` aprovados, usados como base (snowboarder 1:25, bico 0,4 detalhe e bico 0,2 v5) |

## Quando usar o quê
- **Qualquer pedido de impressão** (STL, 3MF, GLB, STEP), revisão de `.3mf`, troca de bico ou calibração → delegue ao agente `configurador-impressao-k1max`.
- O agente lê `k1max-config-impressao` **sempre**, `creality-print-3mf` ao gerar/editar projeto e `k1max-calibracao` só para calibração.

## Regras invioláveis (resumo – detalhes no agente)
- Não alterar configurações de **filamento** sem pedir.
- Brim encostado: `brim_object_gap = 0` **e** `elefant_foot_compensation = 0`.
- Não usar reparo automático de malha (pymeshfix etc.).
- Nunca afirmar algo que não aconteceu.
- PLA: lembrar da **tampa aberta**. Trocou o bico: **autoteste e nivelamento**.
- Todo projeto entregue vai acompanhado do **checklist** do agente, verificado por código.

## Ambiente
- Windows; pasta de entrega: `C:\Users\alemg\Downloads`.
- Python com `trimesh`, `numpy` e `manifold3d` para análise de malha (`pip install trimesh numpy manifold3d`). **No PC dele o Python não está instalado:** use PowerShell (veja o fim da skill `creality-print-3mf`).
- Os perfis do Creality (`AppData\Roaming\Creality`) não são editados diretamente: entregue perfis como pacote `.creality_printer` para importar.

## Manutenção
- Skills novas: `.claude/skills/<nome>/SKILL.md` com frontmatter `name` e `description`.
- Agentes novos: `.claude/agents/<nome>.md`.
- Ao calibrar um filamento novo, atualize a tabela de perfis em `k1max-config-impressao`.
