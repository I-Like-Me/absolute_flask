import pandas as pd
from app.main.absolute_api import Abs_Actions
from app.main.tool_box import Dict_Builder, Data_fillers
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select
from bokeh.io import curdoc

full_device_dict = Abs_Actions.abs_all_devices("pageSize=500&select=deviceName,localIp,volumes,espInfo.encryptionStatus,systemManufacturer,operatingSystem&agentStatus=A")
raw_citrix_data = Abs_Actions.app_version_get("/v3/reporting/applications-advanced", "filter=(appNameContains eq 'receiver' or appNameContains eq 'workspace')&select=deviceName, appName, appVersion&pageSize=500&agentStatus=A")
raw_zoom_data = Abs_Actions.app_version_get("/v3/reporting/applications-advanced", "filter=(appNameContains eq 'Zoom')&select=deviceName, appName, appVersion&pageSize=500&agentStatus=A")
raw_cortex_data = Abs_Actions.app_version_get("/v3/reporting/applications-advanced", "filter=(appNameContains eq 'Cortex')&select=deviceName&pageSize=500&agentStatus=A")
raw_insightvm_data = Abs_Actions.app_version_get("/v3/reporting/applications-advanced", "filter=(appNameContains eq 'Rapid7')&select=deviceName&pageSize=500&agentStatus=A")    
all_device_dicts = Data_fillers.fill_device_series(full_device_dict, raw_citrix_data, raw_zoom_data, raw_cortex_data, raw_insightvm_data)
all_dept_dicts = Data_fillers.fill_dept_series(all_device_dicts)
all_depts_data = Dict_Builder.dict_for_df(all_dept_dicts)
df = pd.DataFrame(all_depts_data)
departments = df.dept_names.values.tolist()

d_type = 'stock'

d_types = {
    'stock': {
        'data_id': 'dept_counts',
        'title': 'Devices in department'
    },
    'space': {
        'data_id': 'space_counts',
        'title': 'Devices under 25 gigs'
    },
    'bitlock': {
        'data_id': 'bit_counts',
        'title': 'Devices that are encripted'
    }
}

class B_Getter:
    def get_dataset(src, d_type):
        
        return ColumnDataSource(data=dict(dept_names = src.dept_names.values.tolist(), data_counts = src[d_type].values.tolist()))
 
class B_Maker:
    def make_plot(source, title):
        plot = figure(y_range=departments, height=700, toolbar_location=None)
        plot.title.text = title
        plot.hbar(y='dept_names', right='data_counts', height=0.3, source=source)
        plot.ygrid.grid_line_color = None
        plot.x_range.start = 0

        return plot
    
        
        

class B_Updater:
    def update_plot(attrname, old, new):
        d_type = d_type_select.value
        plot.title.text = "Data for " + d_types[d_type]['title']

        src = B_Getter.get_dataset(df, d_types[d_type]['data_id'])
        source.data.update(src.data)

        

d_type_select = Select(value=d_type, title='Data Type', options=sorted(d_types.keys()))

source = B_Getter.get_dataset(df, "dept_counts")
plot = B_Maker.make_plot(source, "Data for " + d_types[d_type]['title'])  

d_type_select.on_change('value', B_Updater.update_plot)

controls = column(d_type_select)

curdoc().add_root(row(plot, controls))
