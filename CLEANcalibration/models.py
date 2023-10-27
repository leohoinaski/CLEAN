from django.db import models
from django.utils import timezone

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.user.id, filename)


class CLEANcalibrationNewDeviceModel (models.Model):
	date_posted = models.DateTimeField(default=timezone.now,blank=True, null=True)
	CLEAN01 = models.FileField(upload_to='calibration', max_length=100,null=True, blank=True)
	CLEAN02 = models.FileField(upload_to='calibration', max_length=100,null=True, blank=True)
	CLEAN03 = models.FileField(upload_to='calibration', max_length=100,null=True, blank=True)
	CLEAN04 = models.FileField(upload_to='calibration', max_length=100,null=True, blank=True)
	CLEAN05 = models.FileField(upload_to='calibration', max_length=100,null=True, blank=True)
	CLEAN06 = models.FileField(upload_to='calibration', max_length=100,null=True, blank=True)
	CLEAN07 = models.FileField(upload_to='calibration', max_length=100,null=True, blank=True)
	CLEAN08 = models.FileField(upload_to='calibration', max_length=100,null=True, blank=True)

	REF01 = models.FileField(upload_to='calibration', max_length=100,null=True, blank=True)
	REF02 = models.FileField(upload_to='calibration', max_length=100,null=True, blank=True)
	REF03 = models.FileField(upload_to='calibration', max_length=100,null=True, blank=True)
	REF04 = models.FileField(upload_to='calibration', max_length=100,null=True, blank=True)
	REF05 = models.FileField(upload_to='calibration', max_length=100,null=True, blank=True)
	REF06 = models.FileField(upload_to='calibration', max_length=100,null=True, blank=True)
	REF07 = models.FileField(upload_to='calibration', max_length=100,null=True, blank=True)
	REF08 = models.FileField(upload_to='calibration', max_length=100,null=True, blank=True)
	#author = models.ForeignKey(User, on_delete=models.CASCADE)
	lon = models.FloatField(null=False, blank=False, default=-49.0)
	lat = models.FloatField(null=False, blank=False, default=-27.0)
	deviceId = models.IntegerField(null=False, blank=False, default=0)

	def __str__(self):
		return self.table

	def save(self,*args,**kawargs):
		super().save(*args,**kawargs)
		
	def delete(self,*args,**kawargs):
	 	self.table.delete()
	 	super().delete(*args,**kawargs)
	def save_model(self, request, obj, form, change):
		obj.save()


