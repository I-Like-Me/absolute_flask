from flask import jsonify
import numpy as np
import pandas as pd

class Loopers:

    def age_dept_loop(age_data, dept_data):
        count = 0
        year_n_percent = []
        while count != 51:
            if age_data.values[count] == 0 and dept_data.values[count] == 0:
                year_n_percent.append(0.0)
            else:
                year_n_percent.append(Viz_Data.calculate_percentage(age_data.values[count], np.sum(dept_data.values[count])))
            count += 1
        return year_n_percent

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
        age_labels = ['Y<=1', 'Y==2', 'Y==3', 'Y==4', 'Y>=5']
        y1_lst = viz_data_df['year_1_counts'].values
        _1 = np.sum(y1_lst)
        y2_lst = viz_data_df['year_2_counts'].values
        _2 = np.sum(y2_lst)
        y3_lst = viz_data_df['year_3_counts'].values
        _3 = np.sum(y3_lst)
        y4_lst = viz_data_df['year_4_counts'].values
        _4 = np.sum(y4_lst)
        y5_lst = viz_data_df['year_5_counts'].values
        _5 = np.sum(y5_lst)
        _ = [_1, _2, _3, _4, _5]
        class_percent = Viz_Data.calculate_percentage(_, np.sum(_))
        
        piechart_data= []
        
        Viz_Data.data_creation(piechart_data, class_percent, age_labels)
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
        select_df = viz_data_df[['dept_group','year_1_counts', 'year_2_counts', 'year_3_counts', 'year_4_counts', 'year_5_counts', 'dept_counts']]
        year_1 = select_df['year_1_counts']
        year_2 = select_df['year_2_counts']
        year_3 = select_df['year_3_counts']
        year_4 = select_df['year_4_counts']
        year_5 = select_df['year_5_counts']
        departments = select_df['dept_counts']
        
        year_1_percent = Loopers.age_dept_loop(year_1, departments)
        year_2_percent = Loopers.age_dept_loop(year_2, departments)
        year_3_percent = Loopers.age_dept_loop(year_3, departments)
        year_4_percent = Loopers.age_dept_loop(year_4, departments)
        year_5_percent = Loopers.age_dept_loop(year_5, departments)
       
        barchart_data = []
        Viz_Data.data_creation(barchart_data,year_1_percent, dept_lables, "All")
        Viz_Data.data_creation(barchart_data,year_1_percent, dept_lables, "Y<=1")
        Viz_Data.data_creation(barchart_data,year_2_percent, dept_lables, "Y==2")
        Viz_Data.data_creation(barchart_data,year_3_percent, dept_lables, "Y==3")
        Viz_Data.data_creation(barchart_data,year_4_percent, dept_lables, "Y==4")
        Viz_Data.data_creation(barchart_data,year_5_percent, dept_lables, "Y>=5")
        return (barchart_data)