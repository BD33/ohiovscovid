from django.shortcuts import render
import requests
import json 
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import Scatter
import datetime



def home(request):
    

    resp = requests.get('https://covidtracking.com/api/v1/states/OH/current.json')
    total = json.loads(resp.text)
    


    ## Time line of Deaths
    dailyResp = requests.get('https://covidtracking.com/api/v1/states/OH/daily.json')
    dailyText = json.loads(dailyResp.text)

    dailyDeaths = []
    dates = []
    for day in dailyText:
        dailyDeaths.append(day.get('death'))
        s_datetime = datetime.datetime.strptime(str(day.get('date')),'%Y%m%d')
        dates.append(s_datetime)

    dailyDeaths.reverse()  


    dates.reverse()
    print(len(dates))
    print(len(dailyDeaths))
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=dates, y=dailyDeaths, name = "Corona Deaths in Ohio" , mode='lines+markers',line=dict(color='royalblue', width=4)))
    linegraph =plot(fig1, output_type='div')




    fig = go.Figure(data=[
    go.Bar(name='Covid-19 Positive', x= ['Positive Cases of Covid-19'], y = [total["positive"]]),
    ])
    pltPositive_div =plot(fig, output_type='div')
   
    figDeath = go.Figure(data=[
    go.Bar(name='Covid-19 Deaths', x= ['Deaths caused of Covid-19'], y = [total["death"]]),
    ])
    pltDeath_div =plot(figDeath, output_type='div')

    figHop = go.Figure(data=[
    go.Bar(name='Covid-19 Deaths', x= ['Deaths in Ohio'], y = [total["death"]]),
    go.Bar(name='Covid-19 Positive', x= ['Positive Cases in Ohio'], y = [total["positive"]]),
    ])
    figHop.update_layout(barmode='group')
    pltHop_div =plot(figHop, output_type='div')

    fatalityRate =  round(int(total["death"]) / int(total["positive"]),2) * 100


    usCovid = requests.get('https://covidtracking.com/api/v1/us/current.json')   
    ustotal = json.loads(usCovid.text)


    figDeathCompare = go.Figure(data=[
    go.Bar(name='Covid-19 Deaths', x= ['Deaths caused of Covid-19 in Ohio'], y = [total["death"]]),
    go.Bar(name='Covid-19 Deaths', x= ['Deaths caused of Covid-19 in US'], y = [ustotal[0]["death"]]),
    ])
    figDeathCompare.update_layout(barmode='group')

    pltTotalDeath_div =plot(figDeathCompare, output_type='div')


    context={'object' : total,
    'positiveGraph': pltPositive_div,
    'deathGraph' :pltDeath_div,
    'HopGraph':pltHop_div,
    'fatRate' : fatalityRate,
    'totalDeathGraph' : pltTotalDeath_div,
    'deaths' :linegraph
     }

    return render(request, 'covid/home.html', context)

