# ML Prediction Web App

Esta aplicação Flask lê os dados de `Total.xlsx`, treina três modelos e permite prever:
- `Interlock [mm]`
- `Bottom Thickness [mm]`
- `Joining Force [kN]`

## Executar localmente

1. Ativa o ambiente virtual:

```powershell
cd c:\Users\tomas\Documents\workspace\ml
.\myenv\Scripts\Activate.ps1
```

2. Executa a app:

```powershell
python app_1.py
```

3. Abre no browser:

```text
http://127.0.0.1:5000/
```

## Deploy no Render

1. Sobe o repositório para o GitHub.
2. Cria uma conta no [Render](https://render.com).
3. Cria um novo serviço do tipo `Web Service`.
4. Liga ao teu repositório GitHub.
5. Usa estas configurações:
   - `Environment`: `Python`
   - `Build Command`: `pip install -r requirements.txt`
   - `Start Command`: `gunicorn app_1:app`
6. O Render vai gerar um URL público que pode ser usado em qualquer computador.

## Ficheiros importantes

- `Procfile` — comando usado pelo Render/Heroku para iniciar a app.
- `requirements.txt` — dependências Python.
- `app_1.py` — aplicação Flask.
- `Machine_Learning.py` — carga de dados, treino e predição.
- `templates/index1.html` — interface do usuário.
