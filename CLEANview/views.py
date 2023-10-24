from django.shortcuts import render

from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from .consumers import GraphConsumer

# Create your views here.



def index(request):
	
	return render(request, 'base.html',context={'text':'hello'})




class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["O3"]

    def get_data(self):
        """Return 3 datasets to plot."""


        return [[75, 44, 92, 11, 44, 95, 35]]


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()