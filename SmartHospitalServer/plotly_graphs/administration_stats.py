import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.express as px
import numpy as np
import pandas as pd
import json
from datetime import date, datetime, timedelta

with open('./assets/wards.geojson', 'r') as load_file:
    wards = json.load(load_file)

ward_map = {
    '400001': 'A', '400002': 'C', '400003': 'B', '400004': 'D', '400005': 'A', '400006': 'D', '400007': 'D', '400008': 'E',
    '400009': 'B', '400010': 'E', '400011': 'E', '400012': 'F/S', '400013': 'G/S', '400014': 'F/N', '400015': 'F/S',
    '400016': 'G/N', '400017': 'G/N', '400018': 'G/S', '400019': 'F/N', '400020': 'A', '400021': 'A', '400022': 'F/N',
    '400024': 'L', '400025': 'G/S', '400026': 'D', '400027': 'E', '400028': 'G/N', '400029': 'H/E', '400030': 'G/S',
    '400031': 'F/N', '400032': 'A', '400033': 'F/S', '400034': 'D', '400035': 'D', '400037': 'F/N', '400042': 'S',
    '400043': 'M/E', '400049': 'K/W', '400050': 'H/W', '400051': 'H/E', '400052': 'H/W', '400053': 'K/W',
    '400054': 'H/W', '400055': 'H/E', '400056': 'K/W', '400057': 'K/E', '400058': 'K/W', '400059': 'K/E',
    '400060': 'K/E', '400061': 'P/N', '400063': 'P/S', '400064': 'P/N', '400065': 'P/S', '400066': 'R/C',
    '400067': 'R/S', '400068': 'R/N', '400069': 'K/E', '400070': 'L', '400071': 'M/W', '400072': 'L', '400074': 'M/W',
    '400075': 'N', '400076': 'S', '400077': 'N', '400078': 'S', '400079': 'N', '400080': 'T', '400081': 'T',
    '400082': 'T', '400083': 'N', '400084': 'L', '400085': 'M/E', '400086': 'N', '400087': 'S', '400088': 'M/E',
    '400089': 'M/W', '400091': 'R/C', '400092': 'R/C', '400093': 'K/E', '400094': 'M/E', '400095': 'P/N',
    '400096': 'K/E', '400097': 'P/N', '400098': 'H/E', '400099': 'K/E', '400101': 'T', '400102': 'K/W',
    '400103': 'R/C', '400104': 'P/S'
}

def room_occupancy(patient_db):
    print("Room Occupancy")
    avail_rooms = np.arange(1, 51)
    occupied_rooms = np.unique([x.room_number for x in patient_db if (x.room_number is not None) & (x.room_number in avail_rooms)])

    occupied_rooms_num = occupied_rooms.shape[0]
    unoccupied_rooms_num = avail_rooms.shape[0] - occupied_rooms_num

    values = [occupied_rooms_num, unoccupied_rooms_num]
    labels = ['Occupied', 'Unoccupied']
    data = [
        go.Pie(
            values = values, labels = labels, pull = [0.05, 0],
            marker = dict(line = dict(color = 'black', width = 1)),
            hovertemplate = "No. of %{label} Rooms: %{value}<extra></extra>",
            hoverlabel = dict(font = dict(size = 20)),
            showlegend = False,
            textfont = dict(size = 20)
        )
    ]
    layout = go.Layout(
        paper_bgcolor = '#114B5F' , plot_bgcolor = '#114B5F',
        margin = dict(t=5, b=5, l=0, r=0)
    )
    fig = go.Figure(data = data, layout = layout)
    pyo.plot(fig, filename = './assets/PlotlyGraphs/room_occupancy.html', auto_open = False, output_type = 'file', include_plotlyjs = True)

def monthly_billing(bill_db):
    bill_df = pd.DataFrame(bill_db.values('date', 'charge'))
    bill_df['month'] = bill_df['date'].apply(lambda x: x.month)
    bill_df['year'] = bill_df['date'].apply(lambda x: x.year)
    
    def month_year_range(start, end):
        pairs = [start]
        year = start[0]
        month = start[1]
        while(True):
            if((year == end[0]) & (month == end[1])):
                break
            month += 1
            if(month == 13):
                month = 1
                year += 1
            pairs.append((year, month))
        return pairs
    
    bill_df = bill_df.groupby(['year', 'month'])[['charge']].aggregate('sum')
    bill_df['year_month'] = pd.Series(list(bill_df.index), index = bill_df.index)
    all_dates = pd.DataFrame.from_dict({'year_month': month_year_range(bill_df.index.min(), bill_df.index.max())})
    bill_df = bill_df.reset_index(drop = True)
    bill_df = all_dates.merge(bill_df, on = 'year_month', how = 'left')
    bill_df = bill_df.fillna(0)

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    def create_date_str(year_month):
        return months[year_month[1] - 1] + ', ' + str(year_month[0])
    bill_df['year_month'] = bill_df['year_month'].apply(create_date_str)
    
    data = [
        go.Bar(
            x = bill_df['year_month'].apply(str), y = bill_df['charge'],
            hovertemplate = "%{y}",
            hoverlabel = dict(font = dict(size = 20)),
        )
    ]
    layout = go.Layout(
        xaxis = dict(rangeslider = dict(autorange = True, bordercolor = 'black', bgcolor = '#90BEDE'),
        type = 'category', color = 'white', title = 'Timeline', showgrid = False),
        yaxis = dict(color = 'white', title = 'Billing Charges'),
        margin = dict(t=5, b=5, l=0, r=0),
        paper_bgcolor = '#114B5F', plot_bgcolor = '#114B5F'
    )
    fig = go.Figure(data = data, layout = layout)
    pyo.plot(fig, filename = './assets/PlotlyGraphs/monthly_billing.html', auto_open = False, output_type = 'file', include_plotlyjs = True)

def gender_ratio(staff_db):
    staff_df = pd.DataFrame(staff_db.values('id', 'occupation', 'gender'))
    staff_df['occupation'] = staff_df['occupation'].replace({'D': 'Doctors', 'N': 'Nurses'})
    staff_df['gender'] = staff_df['gender'].replace({'M': 'Male', 'F': 'Female'})
    staff_df = staff_df.groupby(['occupation', 'gender'])['id'].aggregate('count')

    def find_len(df, idx):
        try:
            return df.loc[idx].sum()
        except:
            return 0
    
    data = [
        go.Sunburst(
            ids = ['Nurses', 'Doctors', 'Nurses - Male', 'Nurses - Female', 'Doctors - Male', 'Doctors - Female'],
            labels = ['Nurses', 'Doctors', 'Male', 'Female', 'Male', 'Female'],
            parents = ['', '', 'Nurses', 'Nurses', 'Doctors', 'Doctors'],
            values = [
                find_len(staff_df, 'Nurses'),
                find_len(staff_df, 'Doctors'),
                find_len(staff_df, ('Nurses', 'Male')),
                find_len(staff_df, ('Nurses', 'Female')),
                find_len(staff_df, ('Doctors', 'Male')),
                find_len(staff_df, ('Doctors', 'Female'))
            ],
            branchvalues = 'total',
            textfont = dict(color = 'white'),
            hoverlabel = dict(font = dict(size = 20)),
        )
    ]
    layout = go.Layout(
        margin = dict(t=0, b=0, l=0, r=0),
        paper_bgcolor = '#114B5F', plot_bgcolor = '#114B5F'
    )
    fig = go.Figure(data = data, layout = layout)
    pyo.plot(fig, filename = './assets/PlotlyGraphs/gender_ratio.html', auto_open = False, output_type = 'file', include_plotlyjs = True)

def daily_billing(bill_db):
    bill_df = pd.DataFrame(bill_db.values('charge', 'date'))
    bill_df['charge'] = bill_df['charge'].astype('float32')
    bill_df['DOW'] = bill_df['date'].apply(lambda x: x.weekday())
    bill_df = bill_df.groupby('DOW')[['charge']].aggregate('mean').reset_index(drop = False)
    all_dows = pd.DataFrame.from_dict({'DOW': np.arange(7)})
    bill_df = all_dows.merge(bill_df, on = 'DOW', how = 'left')
    bill_df = bill_df.fillna(0)
    bill_df['DOW'] = bill_df['DOW'].replace({0: 'MON', 1: 'TUE', 2: 'WED', 3: 'THU', 4: 'FRI', 5: 'SAT', 6: 'SUN'})
    
    data = [
        go.Barpolar(
            r = bill_df['charge'],
            hovertemplate = "Average Billing: Rs. %{r}<extra></extra>",
            hoverlabel = dict(font = dict(size = 20)),
        )
    ]
    layout = go.Layout(
        polar = dict(
            angularaxis = dict(showgrid = False, tickmode = 'array', tickvals = [360/7*i for i in range(7)], ticktext = bill_df['DOW'], color = 'white'),
            radialaxis = dict(nticks = 5, linecolor = 'red', color = 'black'),
            bgcolor = '#90BEDE'
        ),
        paper_bgcolor = '#114B5F', plot_bgcolor = '#114B5F',
        margin = dict(t=15, b=15, r=15, l=15)
    )
    fig = go.Figure(data = data, layout = layout)
    pyo.plot(fig, filename = './assets/PlotlyGraphs/daily_billing.html', auto_open = False, output_type = 'file', include_plotlyjs = True)

def patient_geomap(patient_db):
    patient_df = pd.DataFrame(patient_db.values('id', 'pin_code'))

    patient_df['ward_code'] = patient_df['pin_code'].map(ward_map)
    patient_df = patient_df.groupby('ward_code')['id'].aggregate('count').reset_index(drop = False)
    patient_df['ward_label'] = 'Ward: ' + patient_df['ward_code']
    patient_df = patient_df.rename({'id': 'count'}, axis = 1)

    fig = px.choropleth_mapbox(
        patient_df,
        wards,
        locations = 'ward_code',
        color = 'count',
        featureidkey = 'properties.name',
        mapbox_style = 'carto-positron',
        center = {'lat': 19.075983, 'lon': 72.877655},
        hover_name = 'ward_label',
        hover_data = {'ward_code': False, 'count': True},
        zoom = 9,
        opacity = 0.5,
    )
    fig.update_layout(dict(
        margin = dict(t=0, b=0, r=0, l=0),
        paper_bgcolor = '#114B5F', plot_bgcolor = '#114B5F',
        coloraxis = dict(colorbar = dict(thickness = 8, tickfont = dict(color = 'white'), titlefont = dict(color = 'white'))),
    ))
    pyo.plot(fig, filename = './assets/PlotlyGraphs/patient_geomap.html', auto_open = False, output_type = 'file', include_plotlyjs = True)

def age_histogram(patient_db):
    patient_df = pd.DataFrame(patient_db.values('age', 'gender'))
    data = [
        go.Histogram(
            x = patient_df[patient_df['gender'] == 'M'].reset_index(drop = True)['age'],
            xbins = dict(start = 0, end = 100, size = 5),
            opacity = 0.75, name = 'Males',
            hovertemplate = 'Age Range: (%{x})<br>Count: %{y}<extra></extra>',
        ),
        go.Histogram(
            x = patient_df[patient_df['gender'] == 'F'].reset_index(drop = True)['age'],
            xbins = dict(start = 0, end = 100, size = 5),
            opacity = 0.75, name = 'Females',
            hovertemplate = 'Age Range: (%{x})<br>Count: %{y}<extra></extra>'
        )
    ]
    layout = go.Layout(
        xaxis = dict(range = [0, 100], title = "Age", color = 'white', showgrid = False),
        yaxis = dict(title = 'Count', color = 'white', showgrid = False),
        barmode = 'overlay',
        margin = dict(t=15, b=15, l=0, r=0),
        paper_bgcolor = '#114B5F', plot_bgcolor = '#114B5F',
        legend = dict(font = dict(color = 'white')),
    )
    fig = go.Figure(data = data, layout = layout)
    pyo.plot(fig, filename = './assets/PlotlyGraphs/age_histogram.html', auto_open = False, output_type = 'file', include_plotlyjs = True)

def admission_discharge_rate(all_patient_db):
    patient_df = pd.DataFrame(all_patient_db.values("id", 'admission_date', 'discharge_date'))
    patient_df['admission_date'] = patient_df['admission_date'].astype('datetime64')
    patient_df['discharge_date'] = patient_df['discharge_date'].astype('datetime64')

    today_date = date.today()
    last_month_dates = [today_date + timedelta(-x) for x in range(30)]
    all_dates = pd.DataFrame.from_dict({'date': last_month_dates})
    all_dates['date'] = all_dates['date'].astype('datetime64')
    admission = patient_df.groupby('admission_date')['id'].aggregate('count').reset_index(drop = False)
    discharge = patient_df.groupby('discharge_date')['id'].aggregate('count').reset_index(drop = False)
    #%%
    admission = all_dates.merge(admission, how = 'left', left_on = 'date', right_on = 'admission_date')[['date', 'id']].fillna(0)
    discharge = all_dates.merge(discharge, how = 'left', left_on = 'date', right_on = 'discharge_date')[['date', 'id']].fillna(0)
    #%%
    data = [
        go.Scatter(
            x = admission['date'], y = admission['id'],
            name = 'Admission', fill = 'tozerox',
            mode = 'lines', line = dict(color = 'blue'),
            hovertemplate = 'Admissions: %{y}<br>%{x}<extra></extra>'
        ),
        go.Scatter(
            x = discharge['date'], y = discharge['id'],
            name = 'Discharge', fill = 'tozerox',
            mode = 'lines', line = dict(color = 'red'),
            hovertemplate = 'Discharges: %{y}<br>%{x}<extra></extra>'
        ),
    ]
    layout = go.Layout(
        paper_bgcolor = '#114B5F', plot_bgcolor = '#114B5F',
        xaxis = dict(title = 'Timeline', color = 'white', showgrid = False),
        yaxis = dict(title = 'Count', color = 'white', showgrid = False),
        legend = dict(font = dict(color = 'white')),
        margin = dict(t=15, b=15, l=0, r=0)
    )
    fig = go.Figure(data = data, layout = layout)
    pyo.plot(fig, filename = './assets/PlotlyGraphs/admission_discharge_rate.html', auto_open = False, output_type = 'file', include_plotlyjs = True)