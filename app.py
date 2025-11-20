from flask import Flask, render_template, request, jsonify, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Simple in-memory high score storage (reset on restart)
# In a real app, use a database or file
high_score = 0

@app.route('/')
def index():
    return render_template('index.html', high_score=high_score)

@app.route('/api/highscore', methods=['GET', 'POST'])
def handle_highscore():
    global high_score
    if request.method == 'POST':
        data = request.get_json()
        new_score = data.get('score', 0)
        if new_score > high_score:
            high_score = new_score
            return jsonify({'success': True, 'new_high_score': high_score})
        return jsonify({'success': True, 'new_high_score': high_score})
    
    return jsonify({'high_score': high_score})

if __name__ == '__main__':
    app.run(debug=True)
