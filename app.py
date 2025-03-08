from flask import Flask, jsonify
from scraper import get_nba_scores
import os

def create_app():
    app = Flask(__name__)

    @app.route('/api/nba-scores', methods=['GET'])
    def nba_scores():
        scores = get_nba_scores()
        if "error" in scores:
            response = jsonify(scores)
            response.status_code = 500
            return response
        return jsonify(scores)

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)