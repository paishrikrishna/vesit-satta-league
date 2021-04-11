from django import forms
from .models import login_model , fixture_model , prediction_model

class login_form(forms.ModelForm):
	class Meta:
		model = login_model
		fields={
			'username',
			'password',
			'points',
			'rank',
		}

class fixture_form(forms.ModelForm):
	class Meta:
		model = fixture_model
		fields={
			'match_no',
			'team1',
			'team2',
			'deadline',
			'winner_predict',
		}

class prediciton_form(forms.ModelForm):
	class Meta:
		model = prediction_model
		fields={
			'username',
			'winner',
			'match_no',
			'date_time',
		}
