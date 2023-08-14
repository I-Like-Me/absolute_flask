import pandas as pd
from app.main.absolute_api import Abs_Actions
from app.main.tool_box import Dict_Builder, Data_fillers
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, Div
from bokeh.io import curdoc
from bokeh.core.enums import SizingMode

full_device_dict = Abs_Actions.abs_all_devices("pageSize=500&select=deviceName,localIp,volumes,espInfo.encryptionStatus,systemManufacturer,operatingSystem&agentStatus=A")
raw_citrix_data = Abs_Actions.app_version_get("/v3/reporting/applications-advanced", "filter=(appNameContains eq 'receiver' or appNameContains eq 'workspace')&select=deviceName, appName, appVersion&pageSize=500&agentStatus=A")
raw_zoom_data = Abs_Actions.app_version_get("/v3/reporting/applications-advanced", "filter=(appNameContains eq 'Zoom')&select=deviceName, appName, appVersion&pageSize=500&agentStatus=A")
raw_cortex_data = Abs_Actions.app_version_get("/v3/reporting/applications-advanced", "filter=(appNameContains eq 'Cortex')&select=deviceName&pageSize=500&agentStatus=A")
raw_insightvm_data = Abs_Actions.app_version_get("/v3/reporting/applications-advanced", "filter=(appNameContains eq 'Rapid7')&select=deviceName&pageSize=500&agentStatus=A")    
all_device_dicts = Data_fillers.fill_device_series(full_device_dict, raw_citrix_data, raw_zoom_data, raw_cortex_data, raw_insightvm_data)
all_dept_dicts = Data_fillers.fill_dept_series(all_device_dicts)
all_depts_data = Dict_Builder.dict_for_df(all_dept_dicts)
df = pd.DataFrame(all_depts_data)
display_names = ['Admin', 'Allergy', 'Conference', 'Counseling', 
                         'Facilities', 'Finance', 'Global', 'HPO', 
                         'Informatics', 'IT', 'Kitchen', 'LiveWell', 
                         'Moses', 'Medical Records', 'Nursing Hub', 'OffSite', 
                         'Optometry', 'Patient Accounts', 'Pharmacy', 
                         'Popup Clinic', 'Primary Care', 'PSS', 'PT', 
                         'Specialty', 'Wellness', 'Womens Health']
display_names.reverse()

d_type = 'stock'
f_type = 'all'

d_types = {
    'stock': {
        'data_id': 'dept_counts',
        'title': 'devices in department - Total: '
    },
    'space': {
        'data_id': 'space_counts',
        'title': 'devices under 25 gigs - Total: '
    },
    'bitlock': {
        'data_id': 'bit_counts',
        'title': 'devices that are encripted Total: - Total: '
    },
    'citrix': {
        'data_id': 'ctx_ver_counts',
        'title': 'Different Citrix versions - Max: '
    },
    'zoom': {
        'data_id': 'zm_ver_counts',
        'title': 'Different Zoom versions - Max: '
    },
    'Windows': {
        'data_id': 'wpl_ver_counts',
        'title': 'Different Windows build levels - Max: '
    },
    'Dell': {
        'data_id': 'dell_counts',
        'title': 'Dell machines - Total: '
    },
    'Lenovo': {
        'data_id': 'lenovo_counts',
        'title': 'Lenovo machines - Total: '
    },
    'Cortex': {
        'data_id': 'cor_counts',
        'title': 'machines with Cortex - Total: '
    },
    'Insight VM': {
        'data_id': 'ivm_counts',
        'title': 'machines with Insight VM - Total: '
    },
    '1 Year': {
        'data_id': 'year_1_counts',
        'title': 'machines one year old or less - Total: '
    },
    '2 Year': {
        'data_id': 'year_2_counts',
        'title': 'machines 2 years old - Total: '
    },
    '3 Year': {
        'data_id': 'year_3_counts',
        'title': 'machines 3 years old - Total: '
    },
    '4 Year': {
        'data_id': 'year_4_counts',
        'title': 'machines 4 years old - Total: '
    },
    '5 Year': {
        'data_id': 'year_5_counts',
        'title': 'machines 5 years old or more - Total: '
    }
}

f_types = {
    'laptops': {
        'filter_id': 'filter_lp'
    },
    'brooklyn': {
        'filter_id': 'filter_bk'
    },
    'all': {
        'filter_id': 'filter_all'
    },
    'third floor': {
        'filter_id': 'filter_third_floor'
    },
    'fourth floor': {
        'filter_id': 'filter_fourth_floor'
    },
    'second floor': {
        'filter_id': 'filter_second_floor'
    },
    '726 broadway': {
        'filter_id': 'filter_726'
    }
}


class B_Getter:
    def get_dataset(src, d_type, f_type):

        group_dict = {"dept_names": [], "space_counts": [], "dept_counts": [], "bit_counts": [],
                      "ctx_ver_counts": [], "zm_ver_counts": [], "wpl_ver_counts": [], "cor_counts": [],
                      "ivm_counts": [], "dell_counts": [], "lenovo_counts": [], "vul_counts": [], 
                      "exp_counts": [], "mal_counts": [], "year_1_counts": [], "year_2_counts": [],
                      "year_3_counts": [], "year_4_counts": [], "year_5_counts": []
        }

        for name in display_names:
            group_dict['dept_names'].append(name)
            cur_group = df.loc[(src[f_type] == 'yes') & (src['dept_group_tag'] == name)]
            cur_group = cur_group.drop(['dept_names', 'dept_group_tag', 'filter_lp', 'filter_726', 'filter_bk', 'filter_third_floor', 'filter_fourth_floor', 'filter_second_floor', 'filter_all'], axis=1)
            cur_group = cur_group.sum()
            for key, val in cur_group.items():
                group_dict[key].append(val)
        prepped_df = pd.DataFrame(group_dict)    
        dept_names = prepped_df.dept_names.values.tolist()
        data_counts = prepped_df[d_type].values.tolist()
        return ColumnDataSource(data=dict(dept_names=dept_names, data_counts=data_counts))
    
    def get_total(src, d_type):
        if d_types[d_type]['data_id'] == 'ctx_ver_counts':
            return max(src.data['data_counts'])
        if d_types[d_type]['data_id'] == 'zm_ver_counts':
            return max(src.data['data_counts'])
        if d_types[d_type]['data_id'] == 'wpl_ver_counts':
            return max(src.data['data_counts'])
        return sum(src.data['data_counts'])
        

ToolTips = [('Name', '@dept_names'), ('Count', '@data_counts')] 

class B_Maker:
    
    def make_plot(source, title):
        plot = figure(y_range=display_names,
                      sizing_mode = "scale_both",
                      max_height= 650,
                      tools="hover", 
                      tooltips=ToolTips, 
                      toolbar_location=None)
        plot.title.text = f"{title} {B_Getter.get_total(source, d_type)}"
        plot.hbar(y='dept_names', right='data_counts', height=0.3, source=source)
        plot.ygrid.grid_line_color = None
        plot.x_range.start = 0


        return plot  

class B_Updater:
    def update_plot(attrname, old, new):
        d_type = d_type_select.value
        f_type = f_type_select.value

        src = B_Getter.get_dataset(df, d_types[d_type]['data_id'], f_types[f_type]['filter_id'])
        source.data.update(src.data)
        plot.title.text = f"{d_types[d_type]['title']} {B_Getter.get_total(source, d_type)}"


d_type_select = Select(value=d_type, title='Data Type', options=sorted(d_types.keys()))
f_type_select = Select(value=f_type, title='Filter Type', options=sorted(f_types.keys()))

source = B_Getter.get_dataset(df, d_types[d_type]['data_id'], f_types[f_type]['filter_id'])
plot = B_Maker.make_plot(source, "Number of " + d_types[d_type]['title'])  

d_type_select.on_change('value', B_Updater.update_plot)
f_type_select.on_change('value', B_Updater.update_plot)

controls_and_total = row(d_type_select, f_type_select)

curdoc().add_root(controls_and_total)
curdoc().add_root(plot)
