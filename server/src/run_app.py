import app

app.app.run(host = '0.0.0.0', port = int(os.environ.get('PORT', 8080)))
