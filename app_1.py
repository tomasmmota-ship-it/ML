from flask import Flask, render_template, request
from Machine_Learning import load_models, predict_from_input

app = Flask(__name__)
models = load_models()

@app.route('/')
def hello():
    return render_template('index1.html', message='Prediction of Joint Characteristics')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        rivet_length = float(request.form['L'])
        rivet_inner_diameter = float(request.form['Di'])
        die_diameter = float(request.form['Dc'])
        die_depth = float(request.form['Ld'])
    except (KeyError, ValueError):
        form_values = {
            'L': request.form.get('L', ''),
            'Di': request.form.get('Di', ''),
            'Dc': request.form.get('Dc', ''),
            'Ld': request.form.get('Ld', ''),
        }
        return render_template(
            'index1.html',
            message='Prediction of Joint Characteristics',
            error='Por favor insira valores numéricos válidos para todos os campos.',
            form_values=form_values
        )

    interlock_pred, bottom_pred, force_pred = predict_from_input(
        models,
        rivet_length,
        rivet_inner_diameter,
        die_diameter,
        die_depth
    )

    form_values = {
        'L': request.form.get('L', ''),
        'Di': request.form.get('Di', ''),
        'Dc': request.form.get('Dc', ''),
        'Ld': request.form.get('Ld', ''),
    }
    predictions = {
        'interlock': interlock_pred,
        'bottom_thickness': bottom_pred,
        'joining_force': force_pred,
    }

    return render_template(
        'index1.html',
        message='Prediction of Joint Characteristics',
        predictions=predictions,
        form_values=form_values
    )

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
