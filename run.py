from init import app

app.config["DEBUG"] = True
app.run(host='0.0.0.0', port=5000)