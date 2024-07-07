# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 22:14:12 2021

@author: Tron
"""
from tkinter import *
from tkinter import ttk
from tkcalendar import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_pdf import PdfPages as pdf
from matplotlib.figure import Figure
import numpy as np
import matplotlib
import datetime
import requests
import json
import os

import pandas as pd
import matplotlib.pyplot as plt
os.system('cls')

root = Tk()
root.title('Corona-Stats') #naslov programa
#root.iconbitmap(r"C:\Users\Dominik\Desktop\Faks\Programiranje-Skriptni Jezici\covIcon.ico")
root.iconbitmap(r"C:\Users\Tron\Desktop\projekt_covid\covIcon.ico")
#root.iconbitmap(r"") #ovdje unjeti svoju adresu do ikonice
root.geometry("990x600") #dimenzije

def generateGraph():
    
    if(calStart.get_date().strftime("%Y-%m-%d") >= calEnd.get_date().strftime("%Y-%m-%d")):
       messagebox.showwarning(title="Krivi Datum", message="Početni datum ne može biti veći ili isti od krajnjeg")
       return
    elif(calStart.get_date() > calStart.get_date().today() or calEnd.get_date() > calEnd.get_date().today()):
        messagebox.showwarning(title="Krivi Datum", message="Izabran je datum u budućnosti")
        return
    
    DD = datetime.timedelta(days=1)
    dayBefore = calStart.get_date() - DD
    dates = {'from':dayBefore.strftime("%Y-%m-%d"), 'to':calEnd.get_date().strftime("%Y-%m-%d")}
    r = requests.get('https://api.covid19api.com/country/' + countryChosen.get() , params=dates)
    parse = json.loads(r.text)
    totalDeaths = []
    dateVar = []
    totalCases = []
    totalRecovered = []
    activeCases = []
    dailyCases = []
    dailyRecovered = []
    dailyDeaths = []
    dateDates = []
    for i in range(len(parse)):
        if(i == 0):
            totalCases.append(parse[i]['Confirmed'])
            totalDeaths.append(parse[i]['Deaths'])
            totalRecovered.append(parse[i]['Recovered'])
            continue
        
        totalCases.append(parse[i]['Confirmed'])
        totalDeaths.append(parse[i]['Deaths'])
        totalRecovered.append(parse[i]['Recovered'])
        dailyCases.append(totalCases[i] - totalCases[i-1])
        dailyDeaths.append(totalDeaths[i] - totalDeaths[i-1])
        dailyRecovered.append(totalRecovered[i] - totalRecovered[i-1])
        activeCases.append(parse[i]['Active'])
        dateVar.append(parse[i]['Date'][:10])
    
    for i in range(len(dateVar)):
        dateDates.append(datetime.datetime.strptime(dateVar[i], '%Y-%m-%d'))
    
    fig1 = Figure(figsize = (10,8), dpi = 100)
    a = fig1.add_subplot(111)
    width = np.diff(dateDates).min()
    a.plot(dateDates, totalCases[1:], label = 'Ukupno zaraženih', marker = 'o', lw = 2)
    a.plot(dateDates, totalRecovered[1:], label = 'Ukupno ozdravljenih', marker = 'o', lw = 2)
    a.xaxis_date()
    fig1.autofmt_xdate()
    a.set_title("Broj zaraženih i oporavljenih")
    a.legend()
    a.grid()
    
    fig2 = Figure(figsize = (10,8), dpi = 100)
    b = fig2.add_subplot(111)
    b.bar(dateDates, dailyCases, label = 'Dnevno zaraženih', width = width)
    b.xaxis_date()
    fig2.autofmt_xdate()
    b.set_title("Broj dnevnih slučajeva")
    b.legend()
    b.grid()
    
    fig3 = Figure(figsize = (10,8), dpi = 100)
    c = fig3.add_subplot(111)
    c.bar(dateDates, dailyRecovered, label = 'Dnevno ozdravljenih')
    c.bar(dateDates, dailyDeaths, label = 'Dnevno umrlih')
    c.xaxis_date()
    fig3.autofmt_xdate()
    c.set_title("Dnevni broj oporavljenih i umrlih")
    c.legend()
    c.grid()
    
    fig4 = Figure(figsize = (10,8), dpi = 100)
    d = fig4.add_subplot(111)
    d.plot(dateDates, activeCases, label = 'Aktivni slučajevi')
    d.xaxis_date()
    fig4.autofmt_xdate()
    d.set_title("Aktivni slučajevi")
    d.legend()
    d.grid()
    
    canvA = FigureCanvasTkAgg(fig1, master = third_frame)
    canvA.draw()
    
    canvB = FigureCanvasTkAgg(fig2, master = third_frame)
    canvB.draw()
    
    canvC = FigureCanvasTkAgg(fig3, master = third_frame)
    canvC.draw()
    
    canvD = FigureCanvasTkAgg(fig4, master = third_frame)
    canvD.draw()

    get_widzA = canvA.get_tk_widget()
    get_widzA.grid(row = 0, column = 0)
    
    get_widzB = canvB.get_tk_widget()
    get_widzB.grid(row = 1, column = 0, pady = 30)
    
    get_widzC = canvC.get_tk_widget()
    get_widzC.grid(row = 2, column = 0)
    
    get_widzD = canvD.get_tk_widget()
    get_widzD.grid(row = 3, column = 0, pady = 30)
    
    if(clicker == 1):
        with pdf(r"C:\Users\Tron\Desktop\projekt_covid\\" + parse[0]['Country'] + "_" + dateVar[0] + "_" + dateVar[-1] + ".pdf") as image:
            #u redu iznad je potrebno unjeti svoju adresu do zeljenje putanje gdje da se pdf spremi
            image.savefig(fig1, bbox_inches = "tight", dpi = 300)
            image.savefig(fig2, bbox_inches = "tight", dpi = 300)
            image.savefig(fig3, bbox_inches = "tight", dpi = 300)
            image.savefig(fig4, bbox_inches = "tight", dpi = 300)
    
        
def writePDF():
    global clicker
    clicker = 1
    generateGraph()


clicker = 0
      
frame_main = Frame(root)
frame_main.pack(fill = BOTH, expand = 1)

my_canvas = Canvas(frame_main, height = 100)
my_canvas.pack(side = TOP, fill = BOTH, expand = 0)

plotCanvas = Canvas(frame_main)
plotCanvas.pack(side = LEFT, fill = BOTH, expand = 1)

scrollbarV = Scrollbar(frame_main, orient = VERTICAL, command = plotCanvas.yview)
scrollbarV.pack(side = RIGHT, fill = Y)

plotCanvas.configure(yscrollcommand = scrollbarV.set)
plotCanvas.bind('<Configure>', lambda e: plotCanvas.configure(scrollregion = plotCanvas.bbox("all")))

second_frame = Frame(my_canvas)
third_frame = Frame(plotCanvas)

my_canvas.create_window((0, 0), window = second_frame, anchor = "nw")
plotCanvas.create_window((0, 0), window = third_frame, anchor = "nw")
  
labelStart = Label(second_frame, text="Odaberi početni datum:")
labelStart.grid(row = 0, column = 5, pady=10) #pady je dovoljan samo na jednome elementu retka

labelEnd = Label(second_frame, text="Odaberi krajnji datum:")
labelEnd.grid(row = 0, column = 9)    

labelCountry = Label(second_frame, text="Odaberi državu:")
labelCountry.grid(row = 0, column = 13)    
    

dd = datetime.timedelta(days=14)
calStart = DateEntry(second_frame, date_pattern = 'y-mm-dd')
calStart.set_date(calStart.get_date() - dd)
calStart.grid(row = 1, column = 5)

dd = datetime.timedelta(days=1)
calEnd = DateEntry(second_frame, date_pattern = 'y-mm-dd')
calEnd.set_date(calEnd.get_date() - dd)
calEnd.grid(row = 1, column = 9)

country = StringVar(second_frame)
country.set("Croatia") # default value 

countryChosen = ttk.Combobox(second_frame, width = 27, textvariable = country)
  
countryChosen['values'] = ('Croatia', 'Italy', 'Slovenia', 'Austria', 'Hungary', 'Serbia', 'Bosnia-and-Herzegovina', 'Montenegro', 'Kosovo') 
  
countryChosen.grid(row = 1, column = 13) 

countryChosen.current(0)

createGraph = Button(second_frame,text="Nacrtaj Graf", command=generateGraph)
createGraph.grid(row = 1, column = 17)   

exportPdf = Button(second_frame,text="Izvezi PDF",command=writePDF)
exportPdf.grid(row = 1, column = 21)

col_count, row_count = second_frame.grid_size()

for col in range(col_count):
    second_frame.grid_columnconfigure(col, minsize=20)

for row in range(2):
    second_frame.grid_rowconfigure(row, minsize=20)

root.mainloop()