from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Jira App Server is running."

@app.route('/api/jira', methods=['POST'])
def jira_webhook():
    data = request.json
    # Placeholder: process incoming Jira webhook data
    return jsonify({"status": "received", "data": data})

if __name__ == '__main__':
    app.run(debug=True)
