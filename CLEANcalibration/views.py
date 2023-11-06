from django.shortcuts import render
from .forms import CLEANcalibrationNewDevice_form
from .models import CLEANcalibrationNewDeviceModel
from django.contrib import messages
from multiprocessing import Process
import os
import shutil
from django.shortcuts import render, get_object_or_404, redirect
#from .mainCLEANcalibration import mainCLEANcalibration
import zipfile


def CLEANcalibrationNewDevice (request):
    if request.method == 'POST':
        form = CLEANcalibrationNewDevice_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            CLEANcalib = CLEANcalibrationNewDeviceModel.objects.all().last()
            BASE = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            deviceId = CLEANcalib.deviceId

            RUN_FOLDER = BASE + "/media/calibration/"+ str(deviceId).zfill(2) + "/"

            if os.path.isdir(RUN_FOLDER) ==0:
                os.makedirs(RUN_FOLDER, exist_ok=True)
            else:
                shutil.rmtree(RUN_FOLDER)

            # if os.path.isdir(RUN_FOLDER+'Inputs/CLEAN') ==0:
            #     os.makedirs(RUN_FOLDER+'Inputs/CLEAN', exist_ok=True)

            # if os.path.isdir(RUN_FOLDER+'Outputs') ==0:
            #     os.makedirs(RUN_FOLDER+'Inputs/Reference', exist_ok=True)
            #     os.makedirs(RUN_FOLDER+'Outputs', exist_ok=True)

            if CLEANcalib.outzip:
                #shutil.copy(CLEANcalib.ouzip.path,RUN_FOLDER+'Ouputs/'+CLEANcalib.ouzip.path.split('/')[-1])
                print(CLEANcalib.outzip.path)
                with zipfile.ZipFile(CLEANcalib.outzip.path, 'r') as zip_ref:
                    zip_ref.extractall(RUN_FOLDER)


            # if CLEANcalib.CLEAN01:
            #     shutil.copy(CLEANcalib.CLEAN01.path,RUN_FOLDER+'Inputs/CLEAN/'+CLEANcalib.CLEAN01.path.split('/')[-1])
            # if CLEANcalib.CLEAN02:
            #     shutil.copy(CLEANcalib.CLEAN02.path,RUN_FOLDER+'Inputs/CLEAN/'+CLEANcalib.CLEAN02.path.split('/')[-1])
            # if CLEANcalib.CLEAN03:
            #     shutil.copy(CLEANcalib.CLEAN03.path,RUN_FOLDER+'Inputs/CLEAN/'+CLEANcalib.CLEAN03.path.split('/')[-1])
            # if CLEANcalib.CLEAN04:
            #     shutil.copy(CLEANcalib.CLEAN04.path,RUN_FOLDER+'Inputs/CLEAN/'+CLEANcalib.CLEAN04.path.split('/')[-1])
            # if CLEANcalib.CLEAN05:
            #     shutil.copy(CLEANcalib.CLEAN05.path,RUN_FOLDER+'Inputs/CLEAN/'+CLEANcalib.CLEAN05.path.split('/')[-1])
            # if CLEANcalib.CLEAN06:
            #     shutil.copy(CLEANcalib.CLEAN06.path,RUN_FOLDER+'Inputs/CLEAN/'+CLEANcalib.CLEAN06.path.split('/')[-1])

            # if CLEANcalib.REF01:
            #     shutil.copy(CLEANcalib.REF01.path,RUN_FOLDER+'Inputs/Reference/'+CLEANcalib.REF01.path.split('/')[-1])
            # if CLEANcalib.REF02:
            #     shutil.copy(CLEANcalib.REF02.path,RUN_FOLDER+'Inputs/Reference/'+CLEANcalib.REF02.path.split('/')[-1])
            # if CLEANcalib.REF03:
            #     shutil.copy(CLEANcalib.REF03.path,RUN_FOLDER+'Inputs/Reference/'+CLEANcalib.REF03.path.split('/')[-1])
            # if CLEANcalib.REF04:
            #     shutil.copy(CLEANcalib.REF04.path,RUN_FOLDER+'Inputs/Reference/'+CLEANcalib.REF04.path.split('/')[-1])
            # if CLEANcalib.REF05:
            #     shutil.copy(CLEANcalib.REF05.path,RUN_FOLDER+'Inputs/Reference/'+CLEANcalib.REF05.path.split('/')[-1])
            # if CLEANcalib.REF06:
            #     shutil.copy(CLEANcalib.REF06.path,RUN_FOLDER+'Inputs/Reference/'+CLEANcalib.REF06.path.split('/')[-1])

            
            # CLEANpollutants = [f.split('_')[1] for f in os.listdir(RUN_FOLDER+'Inputs/CLEAN/') if os.path.isfile(os.path.join(RUN_FOLDER+'Inputs/CLEAN/', f))]
            
            # REFpollutants = [f.split('_')[1] for f in os.listdir(RUN_FOLDER+'Inputs/Reference/') if os.path.isfile(os.path.join(RUN_FOLDER+'Inputs/Reference/', f))]
            # refpols =[]
            # for pols in REFpollutants:
            #     refpols.append(pols.split('.')[0])

            # print(refpols)

            #pollutants = mainCLEANcalibration(BASE,deviceId,CLEANpollutants,refpols,1,50,1000,'raw')
            #asyncio.run(mainCLEANcalibration(BASE,deviceId,CLEANpollutants,refpols,1,50,10,'raw'))
            #print(pollutants)
            #p = Process(target=mainCLEANcalibration, args=(BASE,deviceId,CLEANpollutants,refpols,1,50,10,'raw'))
            #p.start()
            messages.success(request, f'Your file was updated!')
            return redirect('CLEANcalibrationNewDevice')


            
    else:
        form = CLEANcalibrationNewDevice_form()

    return render(request, 'CLEANcalibrationNewDevice.html',{'form': form})


