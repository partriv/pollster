'''
Created on Apr 4, 2009

@author: par
'''
from pygooglechart import PieChart2D
from encodings import utf_8


class GChartFactory():
    chart_dispatch = None
    def __init__(self):
        # initialize chart dispatcher
        self.chart_dispatch = {'pie':self.__get_pie_chart}
    
    def get_chart(self, results, width=850, height=350, type=None):
        if type == None or type.strip() == "":
            type = 'pie'
        return self.chart_dispatch[type](results, width, height)
    
    def __get_pie_chart(self, results, width, height):
        
        # Create a chart object of 200x100 pixels
        pchart = PieChart2D(width, height)
    
        # Add some data
        votes = []
        labels = []
        for prli in results:
            votes.append(prli.votes)
            labels.append(prli.answer.answer)
        print votes
        print labels
        # Add some data
        pchart.add_data(votes)
    
        # Assign the labels to the pie data
        pchart.set_pie_labels(labels)

        return pchart
        
        
        
        