from django.shortcuts import render
from .forms import CLEANcalibrationNewDevice_form
from .models import CLEANcalibrationNewDevice
from django.contrib import messages


from django.shortcuts import render, get_object_or_404, redirect



def CLEANcalibrationNewDevice (request):
    if request.method == 'POST':
        form = CLEANcalibrationNewDevice_form(request.POST, request.FILES)
        if form.is_valid():
        	form.save()
            
            CLEANcalib = CLEANcalibrationNewDevice.objects.all().last()
            BASE = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            deviceId = CLEANcalib.deviceId

            RUN_FOLDER = BASE + "/media/calibration/"+ str(deviceId) + "/"
            if os.path.isdir(BASE + "/media/getElev/") ==0:
                os.mkdir(BASE + "/media/getElev/")
            if os.path.isdir(RUN_FOLDER) ==1:
                shutil.rmtree(RUN_FOLDER)
                os.mkdir(RUN_FOLDER)
            else:
                os.mkdir(RUN_FOLDER)

            STATIC_SRTM = BASE+'/static/inventory/SRTM/'
            SRTM_selectGetElev(STATIC_SRTM,RUN_FOLDER,getElev_OBJ.srcFile.path)
            getElevSRTM(RUN_FOLDER,getElev_OBJ.srcFile.path)

            file_path = RUN_FOLDER + "/getElev.csv"
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="text/csv")
                    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                    return response
                    #return redirect('blog-smart')
            shutil.rmtree(RUN_FOLDER)
            shutil.rmtree(BASE + "/media/getElev/")


        	messages.success(request, f'Your file was updated!')

        	return redirect('CLEANcalibrationNewDevice')


            
    else:
        form = CLEANcalibrationNewDevice_form()

    return render(request, 'CLEANcalibrationNewDevice.html',{'form': form})


