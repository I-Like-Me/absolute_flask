from flask import jsonify
import numpy as np
import pandas as pd

class Viz_Data:

    def calculate_percentage(val, total):
        """Calculates the percentage of a value over a total"""
        percent = np.round((np.divide(val, total) * 100), 2)
        return percent

    def data_creation(data, percent, class_labels, group=None):
        for index, item in enumerate(percent):
            data_instance = {}
            data_instance['category'] = class_labels[index]
            data_instance['value'] = item
            data_instance['group'] = group
            data.append(data_instance)
    

class Pie_Tool:
    def piechart_data(viz_data_df):
        space_labels = ['under 25 GB', 'over 25 GB']
        _ = viz_data_df.groupby('space_counts').size()
        reverse = np.sum(_.values) - _.values[0]
        class_percent = []
        class_percent.append(Viz_Data.calculate_percentage(reverse, np.sum(_.values)))
        class_percent.append(Viz_Data.calculate_percentage(_.values[0], np.sum(_.values)))
        
        piechart_data= []
        Viz_Data.data_creation(piechart_data, class_percent, space_labels)
        return (piechart_data)
    
class Bar_Tool:

    def barchart_data(viz_data_df):
        dept_lables = ["AD", "AD LP", "AI", "AI LP", 
                       "CONF", "CS3", "CS4", "CS BK", 
                       "CS_LP", "FAC", "FAC_LP", "FI", 
                       "FI_LP", "GLOBAL", "HPO", "HPO_LP", 
                       "IF", "IF_LP", "IT", "IT_LP", 
                       "KIT", "LW", "LW_LP", "MC2", 
                       "MC3_Viz_Data", "MC_BK_Viz_Data", "MC_LP_Viz_Data", "MR_Viz_Data", 
                       "MR_LP_Viz_Data", "NH_Viz_Data", "NH_LP_Viz_Data", "OFF_Viz_Data", 
                       "OPTO_Viz_Data", "OPTO_LP_Viz_Data", "PA_Viz_Data", "PA_LP_Viz_Data", 
                       "PC3_Viz_Data", "PC4_Viz_Data", "PC_BK_Viz_Data", "PC_LP_Viz_Data", 
                       "PHA_Viz_Data", "PHA_LP_Viz_Data", "POPUP_Viz_Data", "PSS_LP_Viz_Data", 
                       "PT_Viz_Data", "PT_LP_Viz_Data", "SP_Viz_Data", "SP_LP_Viz_Data", 
                       "WH_Viz_Data", "WH_LP_Viz_Data", "WL_Viz_Data", "WL_LP_Viz_Data"]
        viz_data_df['dept_group'] = pd.cut(viz_data_df.dept_ids, range(50, 2651, 50), labels=dept_lables)
        select_df = viz_data_df[['dept_group','space_counts', 'dept_counts']]
        over_25 = select_df[select_df['space_counts'] == 0]
        under_25 = select_df[select_df['space_counts'] != 0]
        full_count = select_df[select_df['space_counts'] != None]
        _1 = over_25.groupby('space_counts').size().values
        _2 = over_25.groupby('dept_counts').size().values
        over_percent = Viz_Data.calculate_percentage(_1, _2)
        _1 = under_25.groupby('dept_counts').size().values
        _2 = under_25.groupby('dept_counts').size().values
        under_percent = Viz_Data.calculate_percentage(_1, _2)
        _ = full_count['dept_counts'].values
        all_percent = Viz_Data.calculate_percentage(_, np.sum(_))
       
        barchart_data = []
        Viz_Data.data_creation(barchart_data,all_percent, dept_lables, "All")
        Viz_Data.data_creation(barchart_data,under_percent, dept_lables, "under 25 GB")
        Viz_Data.data_creation(barchart_data,over_percent, dept_lables, "over 25 GB")
        return (barchart_data)