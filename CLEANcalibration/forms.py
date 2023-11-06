from django import forms
from django.forms import ModelForm, ClearableFileInput
from .models import CLEANcalibrationNewDeviceModel


class CLEANcalibrationNewDevice_form (forms.ModelForm):
	class Meta:
		model = CLEANcalibrationNewDeviceModel
		fields = ['date_posted',
		'CLEAN01','CLEAN02','CLEAN03','CLEAN04','CLEAN05','CLEAN06','CLEAN07','CLEAN08',
		'REF01','REF02','REF03','REF04','REF05','REF06','REF07','REF08',
		'outzip',
		'lon','lat','deviceId']

