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
		# Filter by date range
		df['Date'] = pd.to_datetime(df['Date'])
		df = df[(df['Date'] >= '1987-08-19') & (df['Date'] <= '2017-11-10')]
		# Drop OpenInt column if it exists
		if 'OpenInt' in df.columns:
			df = df.drop(columns=['OpenInt'])
		# Split into three time periods
		periods = [
			('1987-08-19', '1997-12-31'),
			('1998-01-01', '2007-12-31'),
			('2008-01-01', '2017-11-10')
		]
		dfs = []
		for start, end in periods:
			dfs.append(df[(df['Date'] >= start) & (df['Date'] <= end)])
		# Render each period as HTML table
		html = ""
		for i, period_df in enumerate(dfs, 1):
			html += f"<h2>Period {i}: {periods[i-1][0]} to {periods[i-1][1]}</h2>"
			html += period_df.to_html(index=False)
		return Response(html, mimetype='text/html')
	except Exception as e:
		return Response(f"<h2>Error: {str(e)}</h2>", status=500, mimetype='text/html')
	
@app.route('/average-close', methods=['GET'])
def average_close():
	if not os.path.exists(DATA_PATH):
		return Response("<h2>File not found.</h2>", status=404, mimetype='text/html')
	try:
		df = pd.read_csv(DATA_PATH, sep=None, engine='python')
		df['Date'] = pd.to_datetime(df['Date'])
		df = df[(df['Date'] >= '1987-08-19') & (df['Date'] <= '2017-11-10')]
		if 'OpenInt' in df.columns:
			df = df.drop(columns=['OpenInt'])
		periods = [
			('1987-08-19', '1997-12-31'),
			('1998-01-01', '2007-12-31'),
			('2008-01-01', '2017-11-10')
		]
		avg_closes = []
		for start, end in periods:
			period_df = df[(df['Date'] >= start) & (df['Date'] <= end)]
			avg_close = period_df['Close'].mean()
			avg_closes.append((start, end, avg_close))
		html = "<h2>Average Close Price by Period</h2><ul>"
		for i, (start, end, avg) in enumerate(avg_closes, 1):
			html += f"<li>Period {i} ({start} to {end}): <b>{avg:.2f}</b></li>"
		html += "</ul>"
		return Response(html, mimetype='text/html')
	except Exception as e:
		return Response(f"<h2>Error: {str(e)}</h2>", status=500, mimetype='text/html')

if __name__ == "__main__":
	app.run(debug=True)
