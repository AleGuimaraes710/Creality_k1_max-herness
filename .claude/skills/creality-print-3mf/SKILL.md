---
name: creality-print-3mf
description: Como ler, revisar e gerar projetos .3mf do Creality Print 7 (base OrcaSlicer) sem abrir o programa — troca de malha, posição na mesa, chaves de processo/filamento/impressora e conferência. Use sempre que for criar ou editar um .3mf para a K1 Max.
---

# Projetos .3mf do Creality Print 7

## Estrutura (um arquivo ZIP)
| Arquivo | Conteúdo |
|---|---|
| `3D/3dmodel.model` | itens na mesa; a posição fica em `transform` (12 números: matriz 3×3 + x y z) |
| `3D/Objects/object_N.model` | malha (`<vertex x y z>`, `<triangle v1 v2 v3>`) |
| `Metadata/project_settings.config` | JSON com **todas** as configurações (impressora + filamento + processo) |
| `Metadata/model_settings.config` | nome do objeto, `assemble_item transform` e configurações por objeto, se houver |
| `Metadata/layer_heights_profile.txt` | altura de camada variável, quando existe (incompatível com suporte Organic) |
| `Metadata/plate_*.png/json` | miniaturas e placa; o Creality regenera ao fatiar |

**Posição na mesa:** a malha fica centrada em XY na origem, com o meio da altura em z = 0. O `transform` do item é `1 0 0 0 1 0 0 0 1 150 150 <meia altura>`, igual no `3dmodel.model` e no `assemble_item`.

## Chaves de controle em `project_settings.config`
- `different_settings_to_system`: lista de 3 strings separadas por `;`:
  - [0] = processo, [1] = filamento, [2] = impressora.
  - Toda chave alterada precisa estar no grupo certo, senão o Creality pode tratar como valor de fábrica.
- Identificação dos perfis:
  - `print_settings_id`, `filament_settings_id` (lista), `printer_settings_id`;
  - `inherits_group` = [processo, filamento, impressora].
- **Valores por extrusora vão em lista:** `"outer_wall_speed": ["80"]`, `"nozzle_diameter": ["0.2"]`. Respeite o tipo que já está no arquivo.
- Algumas chaves usadas com frequência:
  - **Camada:** `layer_height`, `initial_layer_print_height`.
  - **Paredes e preenchimento:** `wall_loops`, `top_shell_layers`, `bottom_shell_layers`, `sparse_infill_density`, `sparse_infill_pattern`, `wall_generator` (classic ou arachne).
  - **Larguras de linha:** `line_width`, `outer_wall_line_width`, `inner_wall_line_width`, `top_surface_line_width`, `sparse_infill_line_width`, `internal_solid_infill_line_width`, `support_line_width`, `initial_layer_line_width`.
  - **Velocidade e aceleração:** `outer_wall_speed`, `inner_wall_speed`, `sparse_infill_speed`, `internal_solid_infill_speed`, `top_surface_speed`, `support_speed`, `outer_wall_acceleration`.
  - **Suporte:**
    - `enable_support`, `support_type` (normal(auto) ou tree(auto)), `support_style` (snug, tree_slim ou organic);
    - `support_threshold_angle`, `support_top_z_distance`, `support_bottom_z_distance`;
    - `support_interface_top_layers`, `support_interface_bottom_layers`;
    - `support_object_xy_distance`, `support_xy_overrides_z`, `independent_support_layer_height`;
    - `tree_support_tip_diameter`, `tree_support_branch_diameter_organic`, `tree_support_wall_count`.
  - **Brim:** `brim_type` (outer_only ou auto_brim), `brim_width`, `brim_object_gap`, `elefant_foot_compensation`.
  - **Compensações:** `xy_hole_compensation`, `xy_contour_compensation`.
  - **Outras:** `seam_position`, `reduce_crossing_wall`.
  - **Impressora:** `nozzle_diameter`, `max_layer_height`, `min_layer_height`, `curr_bed_type`.
  - **Filamento (não mexer sem pedir):** `nozzle_temperature*`, `hot_plate_temp*`, `filament_flow_ratio`, `pressure_advance`, `filament_retraction_length`, `filament_max_volumetric_speed`, `fan_*`, `slow_down_layer_time`.

## Fluxo para gerar um projeto
1. **Modelo:** um projeto salvo no Creality com 1 objeto na mesa, usado só pela estrutura.
2. **Configurações:** um projeto do Alexandre com a impressora, o bico e o filamento certos, para herdar a calibração.
   - Se não existir projeto para aquele bico ou filamento, **peça que ele salve um**. Não invente perfil.
3. **Gerar:** rode `gerar_projeto_creality.py` (nesta pasta) com o JSON só das chaves de processo.
4. Se mudar chaves de filamento ou impressora, ajuste à mão e coloque as chaves no índice [1] ou [2] de `different_settings_to_system`.
5. **Altura de camada variável:** se usar suporte Organic, remova `Metadata/layer_heights_profile.txt` ao copiar o ZIP.
6. **Conferência por código:**
   - `testzip()`;
   - releia a malha de `object_1.model`: dimensões e se está fechada;
   - imprima as chaves do checklist (impressora, bico, filamento, temperaturas, flow, PA, brim gap, compensação de pé de elefante, suporte).

```bash
python3 gerar_projeto_creality.py MODELO.3mf CONFIG.3mf peca.stl SAIDA.3mf "Nome" \
  '{"layer_height":"0.12","wall_loops":"3","brim_object_gap":"0","elefant_foot_compensation":"0"}'
```

## Revisar um projeto salvo por ele
- Compare `project_settings.config` com a versão anterior e liste as chaves que mudaram.
- Verifique `layer_heights_profile.txt` e configurações por objeto em `model_settings.config`.
- Projetos com vários objetos: mude só o `project_settings.config` e confirme que os arquivos `3D/*` ficaram idênticos byte a byte.

## Pacotes de perfil (.creality_printer)
- Também é um ZIP:
  - `bundle_structure.json` com `printer_config`, `filament_config`, `process_config` e `printer_preset_name`;
  - pastas `printer/`, `filament/` e `process/` com JSONs do tipo `"from": "User"` e `"inherits": "<perfil de sistema>"`.
- **Filamento de usuário:** herde de `Generic PLA @Creality K1 Max 0.4 nozzle` (ou PETG) e mude só o necessário. A impressora 0,2 herda da 0,4, então fica compatível.
- **Atenção:** o pacote da Creality vem com `curr_bed_type = Cool Plate`. Troque para `High Temp Plate`.
- **Importar:** File → Import → Import Configuration.

## Acesso aos arquivos dele
- Pasta conectada: `C:\Users\alemg\Downloads`. Use stage e commit pela ponte com o computador.
- A pasta `AppData\Roaming\Creality` (perfis) não está liberada. Entregue perfis como pacote para importar.
