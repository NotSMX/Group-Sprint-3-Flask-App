from flask import Flask, render_template, send_from_directory
from views import main_blueprint

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"
app.register_blueprint(main_blueprint)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
