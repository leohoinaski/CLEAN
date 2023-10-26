from django.shortcuts import render
from .forms import CLEANcalibrationNewDevice_form
from django.contrib import messages

from django.shortcuts import render, get_object_or_404, redirect





def CLEANcalibrationNewDevice (request):
    if request.method == 'POST':
        form = CLEANcalibrationNewDevice_form(request.POST, request.FILES)
        if form.is_valid():
        	form.save()
        	messages.success(request, f'Your file was updated!')
        	return redirect('CLEANcalibrationNewDevice')
            
    else:
        form = CLEANcalibrationNewDevice_form()

    return render(request, 'CLEANcalibrationNewDevice.html',{'form': form})


