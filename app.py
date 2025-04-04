import streamlit as st
import plotly.graph_objects as go
import math

# Función para calcular los puntos de un hexágono
def get_hexagon_points(x, y, size):
    points_x = []
    points_y = []
    for angle in range(0, 360, 60):
        x_point = x + size * math.cos(math.radians(angle))
        y_point = y + size * math.sin(math.radians(angle))
        points_x.append(x_point)
        points_y.append(y_point)
    points_x.append(points_x[0])  # Cerrar el hexágono
    points_y.append(points_y[0])
    return points_x, points_y

# Función para dibujar el tablero HEX
def draw_hex_grid(grid_size, hex_size):
    fig = go.Figure()

    for row in range(grid_size):
        for col in range(grid_size):
            x_offset = col * 1.5 * hex_size
            y_offset = row * math.sqrt(3) * hex_size
            if col % 2 == 1:
                y_offset += math.sqrt(3) * hex_size / 2
            
            # Obtener los puntos del hexágono
            x_points, y_points = get_hexagon_points(x_offset, y_offset, hex_size)
            
            # Dibujar el hexágono en la figura
            fig.add_trace(go.Scatter(
                x=x_points,
                y=y_points,
                mode='lines',
                line=dict(color='black'),
                fill='toself',
                fillcolor='white',
                name=f"Hex ({row}, {col})",
                hoverinfo="text",
                text=f"Hexágono ({row}, {col})"
            ))

    # Ajustar diseño del gráfico
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
        width=600,
        height=600
    )
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig

# Configuración de Streamlit
st.title("Juego HEX - Tablero Visual")

# Controladores interactivos
grid_size = st.slider("Tamaño del tablero (eje X y Y):", min_value=5, max_value=15, value=8)
hex_size = st.slider("Tamaño de cada celda hexagonal:", min_value=10, max_value=50, value=30)

# Dibujar y mostrar el tablero
fig = draw_hex_grid(grid_size, hex_size)
st.plotly_chart(fig)