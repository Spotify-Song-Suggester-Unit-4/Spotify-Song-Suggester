from flask import Flask, render_template, request
from os import getenv
from flask_assets import Bundle, Environment
from .api import parse_input #uses api query to parse input from both text boxes
from .models import retrieve_recs # get track_ids for embeds

input_id = parse_input(song_name_input, artist_input)
rec_id_list = retrieve_recs(input_id)

