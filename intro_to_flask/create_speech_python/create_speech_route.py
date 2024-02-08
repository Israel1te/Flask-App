import os
import openai
from openai import OpenAI
import re # regular expressions module
from markupsafe import escape #protects projects against injection attacks
from intro_to_flask import app
import sys 
import io
sys.dont_write_bytecode = True
from flask import render_template, request, Flask, Blueprint, Response
from gtts import gTTS
from .create_speech_form import SpeakmeForm

speech_blueprint = Blueprint('speakme', __name__)

@speech_blueprint.route('/create_speech',methods=['GET', 'POST'])
@app.route('/create_speech',methods=['GET', 'POST'])
def create_speech():
  form = SpeakmeForm(request.form)
  
  if request.method == 'POST':
      if form.validate() == False:
        return render_template('create_speech.html', form=form)
      else:
        # The following response code adapted from example on: 
        # https://platform.openai.com/docs/api-reference/images
        client = OpenAI()

     #   response = client.audio.speech.create(
     #       model="tts-1",
     #       engine="davinci",
     #       parameters={
     #           "voice": "alloy",  # Choose the voice
     #       },
     #       input = "text" = form.prompt.data,
     #   )
        
        tts = gTTS(form.prompt.data)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)  # Write the speech to the in-memory file-like object

        audio_bytes.seek(0)  # Move the cursor to the beginning of the in-memory file
        speech_response = audio_bytes

      return render_template('create_speech.html', create_speech_prompt=form.prompt.data,create_speech_response=speech_response,success=True)
      
  elif request.method == 'GET':
      return render_template('create_speech.html', form=form)