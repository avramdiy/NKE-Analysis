from flask import Flask, Response
import pandas as pd
import os

app = Flask(__name__)

DATA_PATH = r"C:\Users\avram\OneDrive\Desktop\Bloomtech TRG\TRG Week 39\nke.us.txt"

@app.route('/load-data', methods=['GET'])
def load_data():
	if not os.path.exists(DATA_PATH):
		return Response("<h2>File not found.</h2>", status=404, mimetype='text/html')
	try:
		df = pd.read_csv(DATA_PATH, sep=None, engine='python')
		html_table = df.to_html(index=False)
		return Response(html_table, mimetype='text/html')
	except Exception as e:
		return Response(f"<h2>Error: {str(e)}</h2>", status=500, mimetype='text/html')

if __name__ == "__main__":
	app.run(debug=True)
