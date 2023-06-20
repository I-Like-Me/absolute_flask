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
        contract_labels = ['Month-to-month', 'One year', 'Two year']
        _ = viz_data_df.groupby('Contract').size().values
        class_percent = Viz_Data.calculate_percentage(_, np.sum(_)) #Getting the value counts and total

        piechart_data= []
        Viz_Data.data_creation(piechart_data, class_percent, contract_labels)
        return (piechart_data)
    
class Bar_Tool:
    def barchart_data(viz_data_df):
        tenure_labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79']
        viz_data_df['tenure_group'] = pd.cut(viz_data_df.tenure, range(0, 81, 10), labels=tenure_labels)
        select_df = viz_data_df[['tenure_group','Contract']]
        contract_month = select_df[select_df['Contract']=='Month-to-month']
        contract_one = select_df[select_df['Contract']=='One year']
        contract_two =  select_df[select_df['Contract']=='Two year']
        _ = contract_month.groupby('tenure_group').size().values
        mon_percent = Viz_Data.calculate_percentage(_, np.sum(_))
        _ = contract_one.groupby('tenure_group').size().values
        one_percent = Viz_Data.calculate_percentage(_, np.sum(_))
        _ = contract_two.groupby('tenure_group').size().values
        two_percent = Viz_Data.calculate_percentage(_, np.sum(_))
        _ = select_df.groupby('tenure_group').size().values
        all_percent = Viz_Data.calculate_percentage(_, np.sum(_))

        barchart_data = []
        Viz_Data.data_creation(barchart_data,all_percent, tenure_labels, "All")
        Viz_Data.data_creation(barchart_data,mon_percent, tenure_labels, "Month-to-month")
        Viz_Data.data_creation(barchart_data,one_percent, tenure_labels, "One year")
        Viz_Data.data_creation(barchart_data,two_percent, tenure_labels, "Two year")
        return (barchart_data)