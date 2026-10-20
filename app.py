from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>Despliegue Continuo</title>
        </head>

        <body style="
            background-color: #16213e;
            color: white;
            text-align: center;
            font-family: Arial;
            padding-top: 100px;
        ">

            <h1>Despliegue Continuo Exitoso</h1>

            <h2>Flask + GitHub + Render</h2>

            <p>La aplicacion se actualizo automaticamente.</p>

            <p>Version 2.0</p>

        </body>
    </html>
    """

if __name__ == "__main__":
    app.run()
