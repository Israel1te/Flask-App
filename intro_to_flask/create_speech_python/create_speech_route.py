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
from .create_speech_form import SpeakmeForm
import base64


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

        response = openai.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input= form.prompt.data,
        )
        
        #print(response.content)
        audio_data = response.content

        audio_base64 = base64.b64encode(audio_data).decode('utf-8')

      return render_template('create_speech.html', create_speech_prompt=form.prompt.data, create_speech_response=audio_base64, success=True)
      
  elif request.method == 'GET':
      return render_template('create_speech.html', form=form)