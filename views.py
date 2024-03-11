from Recommendation_Engine import Recommender
from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            title = request.form['title']
            title = title.split()
            capitalized_title = [word.capitalize() for word in title]
            capitalized_name = ' '.join(capitalized_title)
            engine = Recommender()
            data = engine.get_recommendations(capitalized_name)
            names = data['Names']
            links = data['Links']
            cuisines = data['Cuisines']
            collections = data['Collections']
            # timings = data['Timings']
            return render_template('index.html', names=names, links=links, cuisines=cuisines, collections=collections, data=data)
            # return render_template('test.html', title=capitalized_name)
        except KeyError:
            title = request.form['title']
            title = title.split()
            capitalized_title = [word.capitalize() for word in title]
            capitalized_name = ' '.join(capitalized_title)
            engine = Recommender()
            data = engine.food_based_recommend(capitalized_name)
            if data['Name'] == {}:
                return render_template('index.html', error=True)
            names = list(data['Name'].values())
            links = list(data['Links'].values())
            cuisines = list(data['Cuisines'].values())
            collections = list(data['Collections'].values())
            # timings = data['Timings']
            return render_template('index.html', names=names, links=links, cuisines=cuisines, collections=collections, data=data) 
            # return render_template('test.html', title=title)
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    engine = Recommender()
    dataframe = engine.create_data_frame()
    return render_template('dashboard.html', dataframe=dataframe)