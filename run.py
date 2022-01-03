from api import app

if __name__ == "__main__":
    port = 8224
    app.run(host="0.0.0.0", port=port, threaded=True)
