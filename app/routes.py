from flask import Flask, render_template, request
from os import getenv
from flask_assets import Bundle, Environment
from .api import parse_input #uses api query to parse input from both text boxes
from .talk_db import retrieve_recs # get track_ids for embeds

def build_app():

    app = Flask(__name__)

    # To use the provided javascript and css template
    js = Bundle('breakpoints.min.js', 'browser.min.js',
                'jquery.min.js', 'jquery.scrolly.min.js', 'main.js',
                'util.js', output='gen/all.js')

    css = Bundle('fontawesome-all.min.css',
                 'main.css', output='gen/all.css')

    assets = Environment(app)

    assets.register('all_js', js)
    assets.register('all_css', css)

    @app.route('/')
    def root():
        return render_template('index.html')

    @app.route('/rec', methods=['POST'])
    def recommend():
        # retrieve input from text boxes
        song_name = request.values['song_name_input']
        artist = request.values['artist_input']


        try:
            # use spotify api to parse input and get track_id
            input_id_api = parse_input(song_name, artist)
        except:
            message = 'We couldn\'t locate that song on Spotify. Please try again.'
            return render_template('index.html', message=message)

        try:
            #use track_id from parsed input to retreive recs in database
            #list of 5 track_ids, first is same song
            rec_id_list = retrieve_recs(input_id_api) 
            # #testing data, for Juice by Lizzo
            # rec_id_list = ['0k664IuFwVP557Gnx7RhIl',
            #                 '5ehVOwEZ1Q7Ckkdtq0dY1W',
            #                 '7iMDaY1LnASwCk2uUpMtii',
            #                 '45xU99QgWETDFGhgivpYce',
            #                 '6oYkwjI1TKP9D0Y9II1GT7']


        except:
            message = '''That song is a little too obscure for us to have 
                        recommendations for it. Please choose another song. 
                        Our database includes 170,000 musical tracks released 
                        between 1950 and 2020, so we should have something 
                        else that suits you.'''
            return render_template('index.html', message=message)

        
        return render_template('rec.html', 
                                input_id = input_id_api, # rec_id_list[0] or input_id_api?
                                rec1=rec_id_list[1], 
                                rec2=rec_id_list[2], 
                                rec3=rec_id_list[3], 
                                rec4=rec_id_list[4])
                                   
    return app