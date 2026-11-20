# Projetos de referência (projetos-base)

O `gerar_projeto_creality.py` precisa de dois `.3mf` salvos no Creality Print:
- **MODELO**: dá a estrutura do arquivo (qualquer projeto com 1 objeto na mesa);
- **CONFIG**: dá o `project_settings.config` com os perfis **calibrados** (impressora + bico + filamento).

Um projeto por combinação serve para os dois papéis. Sem ele, o agente precisa pedir um arquivo a cada peça.

## Arquivos esperados

| Arquivo | Impressora (Printer) | Filamento | Processo |
|---|---|---|---|
| `base_0.4_PLA-FLEXYGREEN.3mf` | Creality K1 Max 0.4 nozzle | PLA FLEXYGREEN | 0.20mm Standard |
| `base_0.4_PETG-MASTERPRINT.3mf` | Creality K1 Max 0.4 nozzle | PETG MASTERPRINT (220/230 °C) | 0.20mm Standard |
| `base_0.2_PLA-FLEXYGREEN.3mf` | Creality K1 Max 0.2 nozzle | PLA FLEXYGREEN @…0.2 nozzle | 0.10mm Standard @…0.2 nozzle |
| `base_0.2_PETG-MASTERPRINT.3mf` | Creality K1 Max 0.2 nozzle | PETG MASTERPRINT @…0.2 nozzle | 0.10mm Standard @…0.2 nozzle |

Status: **nenhum salvo ainda** (19/11/2026).

Enquanto isso, para **bico 0,4 + PLA FLEXYGREEN** existe `.claude/referencias/Snowboarder_1-25_PLA_bico_0.4_detalhe.3mf` (aprovado pelo Alexandre em 20/11/2026). Ele serve de MODELO/CONFIG, mas o processo dele é de miniatura (camada 0,08, slow_down 8): passe no JSON as chaves de processo que a peça nova precisa e avise que o filamento vem com slow_down 8.

## Como salvar cada um (Creality Print 7, modo Expert)
1. File → New Project.
2. Escolha **Printer**, **Filament** e **Process** da tabela, sem alterar nada (sem `*` no nome do perfil).
3. Coloque um cubo simples na mesa (botão direito na mesa → Add Primitive → Cube, ou importe qualquer STL pequeno).
4. Mesa: **High Temp Plate**.
5. File → Save Project As… com o nome da tabela, dentro desta pasta.

Ao recalibrar um filamento, salve de novo o projeto correspondente e anote a data aqui.
