from flask import Flask, request, render_template_string

app = Flask(__name__)

# Plantilla HTML para el formulario y para mostrar el resultado, con mejoras en el diseño
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Risk Calculation</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        form { margin-top: 20px; }
        .form-group { margin-bottom: 10px; }
        label { display: block; margin-bottom: 5px; }
        input[type="number"] { width: 100%; padding: 8px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { background-color: #4CAF50; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background-color: #45a049; }
    </style>
</head>
<body>
    <h1>Prostate Cancer Biopsy Risk Calculator</h1>
    {% if p_pos is not none %}
    <h2>Risk of Positive Biopsy: {{ p_pos|round(4) }}%</h2>
    <a href="/">Calculate Again</a>
    {% else %}
    <p>Please enter the number of lesions for each RADS category:</p>
    <form action="/" method="post">
        <div class="form-group">
            <label for="n1">RADS1 (Lowest Risk):</label>
            <input type="number" id="n1" name="n1" value="0">
        </div>
        <div class="form-group">
            <label for="n2">RADS2:</label>
            <input type="number" id="n2" name="n2" value="0">
        </div>
        <div class="form-group">
            <label for="n3">RADS3:</label>
            <input type="number" id="n3" name="n3" value="0">
        </div>
        <div class="form-group">
            <label for="n4">RADS4:</label>
            <input type="number" id="n4" name="n4" value="0">
        </div>
        <div class="form-group">
            <label for="n5">RADS5 (Highest Risk):</label>
            <input type="number" id="n5" name="n5" value="0">
        </div>
        <button type="submit">Calculate Risk</button>
    </form>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def calculate_risk():
    if request.method == 'POST':
        # Obtener los valores del formulario
        n1 = int(request.form.get('n1', 0))
        n2 = int(request.form.get('n2', 0))
        n3 = int(request.form.get('n3', 0))
        n4 = int(request.form.get('n4', 0))
        n5 = int(request.form.get('n5', 0))
        
        # Calcular el riesgo
        P_neg = (1-0.025)**n1 * (1-0.075)**n2 * (1 - 0.25)**n3 * (1 - 0.6)**n4 * (1-0.825)**n5
        p_pos = 1 - P_neg

        # Lo presentamos en porcentaje
        p_pos = p_pos * 100
        
        # Renderizar resultado
        return render_template_string(HTML, p_pos=p_pos)
    else:
        # Renderizar formulario
        return render_template_string(HTML, p_pos=None)

if __name__ == '__main__':
    app.run(debug=True)