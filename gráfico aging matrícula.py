# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd

df = dataset.copy()
col_data = df.columns[0]
col_legado = df.columns[1]
col_aging = df.columns[2]
col_valor = df.columns[-1]

# -----------------------------
# Tratamento dos dados
# -----------------------------
df[col_data] = pd.to_datetime(df[col_data])

def formatar_aging(x):
    if pd.isna(x):
        return ""
    x = int(x)
    return f"+{x}" if x > 0 else "0"

df[col_aging] = df[col_aging].apply(formatar_aging)

# Ordem fixa das faixas
ordem_aging = ["0", "+1", "+7", "+15", "+30", "+60", "+90", "+120"]
# Ordem dos legados conforme aparecem na base
ordem_legado = list(dict.fromkeys(df[col_legado]))

# -----------------------------
# Pivot
# -----------------------------
pivot = df.pivot_table(
    index=col_data,
    columns=[col_legado, col_aging],
    values=col_valor,
    aggfunc="sum",
    fill_value=0
).sort_index()

# -----------------------------
# Tabela final
# -----------------------------
final = pd.DataFrame(index=pivot.index)
final.index.name = "Data"

header_top = ["Data"]
header_sub = [""]

for legado in ordem_legado:
    if legado not in pivot.columns.get_level_values(0):
        continue
    for aging in ordem_aging:
        coluna = (legado, aging)
        if coluna in pivot.columns:
            nome = f"{legado}_{aging}"
            final[nome] = pivot[coluna]
            header_top.append(legado)
            header_sub.append(aging)

final = final.reset_index()
final["Data"] = pd.to_datetime(final["Data"]).dt.strftime("%d/%m/%Y")

colunas_valor = final.columns[1:]
final["Total no Dia"] = final[colunas_valor].sum(axis=1)

header_top.append("Total")
header_sub.append("Total")

linha_total = {"Data": "Total"}
for c in final.columns[1:]:
    linha_total[c] = final[c].sum()

exib = pd.concat([final, pd.DataFrame([linha_total])], ignore_index=True)
cell_text = [header_sub] + exib.values.tolist()

# -----------------------------
# Plot
# -----------------------------
fig, ax = plt.subplots(figsize=(12, 6), dpi=200)
ax.axis("off")

tbl = ax.table(
    cellText=cell_text,
    colLabels=header_top,
    cellLoc="center",
    bbox=[0, 0, 1, 1]
)

tbl.auto_set_font_size(False)
tbl.set_fontsize(9)

header_bg = "#1f4e78"
sub_bg = "#2c6b9c"
alt = "#f9fbfd"
total_bg = "#e6eeea"

# Configuração da linha divisória customizada
cor_divisoria = "#2C6B9C"  # Vermelho vivo (altere se quiser outra cor)
espessura_divisoria = 2.5

rows = len(cell_text) + 1

# Mapeia onde começa cada legado
primeira = {}
for i, h in enumerate(header_top):
    if h not in ("Data", "Total") and h not in primeira:
        primeira[h] = i

# Identifica os índices das colunas de início
indices_inicio = list(primeira.values())

for (r, c), cell in tbl.get_celld().items():
    cell.set_linewidth(.5)
    cell.set_edgecolor("#cccccc")
    
    # 1. Configuração dos cabeçalhos principais
    if r == 0:
        cell.set_facecolor(header_bg)
        cell.set_text_props(color="white", weight="bold", fontsize=11)
        if c in primeira.values():
            cell.get_text().set_text(header_top[c])
        elif header_top[c] not in ("Data", "Total"):
            cell.get_text().set_text("")
        else:
            cell.get_text().set_text(header_top[c])
            
    # 2. Configuração do sub-cabeçalho
    elif r == 1:
        cell.set_facecolor(sub_bg)
        cell.set_text_props(color="white", weight="bold", fontsize=10)
        
    # 3. Configuração dos dados e linha total
    else:
        if r == rows - 1:
            cell.set_facecolor(total_bg)
            cell.set_text_props(weight="bold", color=header_bg, fontsize=11)
        else:
            cell.set_facecolor(alt if r % 2 == 0 else "white")
            cell.set_text_props(fontsize=12)
        
        # Oculta o valor se for zero (ignora a primeira coluna da Data)
        if c > 0:
            texto_atual = cell.get_text().get_text().strip()
            if texto_atual in ("0", "0.0"):
                cell.get_text().set_text("")

    # -------------------------------------------------------------
    # NOVA LOGICA: Adiciona a linha divisória colorida à direita 
    # da célula anterior à troca de Legado
    # -------------------------------------------------------------
    # Se houver mais de um legado, aplica na divisória entre eles
    if len(indices_inicio) > 1:
        coluna_divisao = indices_inicio[1] - 1  # Última coluna do primeiro grupo
        if c == coluna_divisao:
            # Como o Matplotlib reconstrói as bordas, acessamos o "Path" visual da célula
            cell.visible_edges = cell.visible_edges + 'R'  # Garante que a borda direita (Right) está ativa
            # Força o desenho visual do lado direito de forma nativa na célula
            cell._loc = 'center' 
            
# Remapeamento fino via desenho customizado para não quebrar a tabela
# Desenhamos uma linha vertical nativa nos eixos passando exatamente por cima da divisão
# Isso garante que ela cruze verticalmente do topo ao rodapé perfeitamente limpa.
if len(indices_inicio) > 1:
    col_idx = indices_inicio[1]
    total_cols = len(header_top)
    # Calcula a posição X exata da linha divisória de forma proporcional
    x_pos = col_idx / total_cols
    # Desenha a linha vertical que cruza o bounding box (bbox) da tabela de cima a baixo
    ax.axvline(x=x_pos, color=cor_divisoria, linestyle="-", linewidth=espessura_divisoria, zorder=5)

plt.tight_layout()
plt.show()

