import pandas as pd
# import pyodbc
# import numpy as np
# from tqdm import tqdm
# import time
# import sys
# import logging
import warnings

# import time
warnings.filterwarnings('ignore')

df = pd.DataFrame({'Time Points': [[1], [1, 3, 6], [1, 3, 6, 9], [1, 3, 6, 9, 12], [1, 3, 6, 9, 12, 18], [1], [1, 3],
                                   [1, 3, 6], [1, 3, 6, 9], [1], [1, 3, 6], [1, 3, 6, 9], [1, 3, 6, 9, 12],
                                   [1, 3, 6, 9, 12, 18], [1], [1, 3], [1, 3, 6], [1, 3, 6, 9]],
                   'Test Results': [[10], [9, 18, 27], [8, 16, 24, 32], [7, 14, 21, 28, 35], [6, 12, 18, 24, 30, 36],
                                    [10], [9, 18], [8, 16, 24], [7, 14, 21, 28], [10], [9, 18, 27], [8, 16, 24, 32],
                                    [7, 14, 21, 28, 35], [6, 12, 18, 24, 30, 36], [10], [9, 18], [8, 16, 24],
                                    [7, 14, 21, 28]],
                   'Unique_Name': ['a_1', 'a_2', 'a_3', 'a_4', 'a_5', 'b_1', 'b_2', 'b_3', 'b_4', 'c_1', 'c_2', 'c_3',
                                   'c_4', 'c_5', 'd_1', 'd_2', 'd_3', 'd_4'],
                   'Name': ['a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'c', 'c', 'c', 'c', 'c', 'd', 'd', 'd', 'd'],
                   'Batch_No': ['1', '2', '3', '4', '5', '1', '2', '3', '4', '1', '2', '3', '4', '5', '1', '2', '3',
                                '4'],
                   "specification_id": ["s1", "s1", "s1", "s1", "s1", "s2", "s2", "s2", "s2", "s3", "s3", "s3", "s3",
                                        "s3", "s4", "s4", "s4", "s4"],
                   "Product_Name": ["para", "para", "para", "para", "para", "omez", "omez", "omez", "omez", "Nise",
                                    "Nise", "Nise", "Nise", "Nise", "Razo", "Razo", "Razo", "Razo"],
                   "Market": ["USA", "USA", "USA", "USA", "Russia", "Russia", "Russia", "Russia", "USA", "India",
                              "India", "India", "India", "Russia", "Canada", "Canada", "Canada", "USA"]
                   })
df['Maximum'] = 50
df['Minimum'] = 4
mini = df['Minimum'].tolist()[0]
maxi = df['Maximum'].tolist()[0]

max_len = max([len(i) for i in df['Time Points']])

# Add columns to the dataframe for each time point, with a prefix of 'delta_' and a number
# corresponding to the index of the time point
df[['delta_' + str(i) for i in range(max_len)]
] = pd.DataFrame([[0] * max_len for i in range(len(df))])

# Loop through each row in the dataframe and calculate the difference between each test result
# and the previous test result, as well as the slope of that change
for i, row in df.iterrows():
    tp = row['Time Points']
    tr = row['Test Results']
    for j in range(1, len(tp)):
        delta = tr[j] - tr[j - 1]
        slope = delta / (tp[j] - tp[j - 1])
        # Assign the calculated delta value to the corresponding 'delta_' column for the current row
        df.at[i, 'delta_' + str(j - 1)] = delta

# Add columns to the dataframe for each time point, with a prefix of 'delta_time_' and a number
# corresponding to the index of the time point
df[['delta_time_' + str(i) for i in range(max_len)]
] = pd.DataFrame([[0] * max_len for i in range(len(df))])

# Loop through each row in the dataframe and calculate the difference in time between each time point
for i, row in df.iterrows():
    tp = row['Time Points']
    for j in range(1, len(tp)):
        delta_time = tp[j] - tp[j - 1]
        # Assign the calculated delta_time value to the corresponding 'delta_time_' column for the current row
        df.at[i, 'delta_time_' + str(j - 1)] = delta_time
df['max_len'] = df.apply(lambda x: max(
    [len(x['Test Results']), len(x['Time Points'])]), axis=1)


# print(df.head())

def fill_missing_values(df, batch_numbers, names, specification_ids, product_names, markets):
    # Filter the dataframe to only include rows that match the specified batch numbers, names,
    # specification IDs, product names, and markets
    df_filtered = df[df['Batch_No'].isin(batch_numbers) &
                     df['Name'].isin(names) &
                     df['specification_id'].isin(specification_ids) &
                     df['Product_Name'].isin(product_names) &
                     df['Market'].isin(markets)
                     ]

    # Sort the filtered dataframe by the 'max_len' column in ascending order
    df_filtered = df_filtered.sort_values(by='max_len', ascending=True)

    # Loop through each 'delta_' column and replace any missing values with the mean of the non-missing values
    for col in ['delta_0', 'delta_1', 'delta_2', 'delta_3', 'delta_4']:
        mean = df_filtered.loc[df_filtered[col] > 0, col].mean()
        df_filtered[col] = df_filtered[col].where(df_filtered[col] > 0, mean)

    # Loop through each 'delta_time_' column and replace any missing values with the mean of the non-missing values
    for col in ['delta_time_0', 'delta_time_1', 'delta_time_2', 'delta_time_3', 'delta_time_4']:
        mean = df_filtered.loc[df_filtered[col] > 0, col].mean()
        df_filtered[col] = df_filtered[col].where(df_filtered[col] > 0, mean)

    # Return the filtered and updated dataframe
    return df_filtered


batch_numbers = ['1', '2', '3', '4']
names = ['a', 'b']
specification_ids = ['s1', 's2']
product_names = ['para', 'omez']
markets = ['USA', 'Russia']
df1 = fill_missing_values(df, batch_numbers, names, specification_ids, product_names, markets)


def calculate_new_test_results(test_results, delta_values):
    # Initialize the new test results list with the first test result in the original list
    new_test_results = [test_results[0]]

    # Loop through the delta values and calculate the new test results based on the previous result and the delta value
    for i in range(len(delta_values)):
        new_result = new_test_results[i] + delta_values[i]
        # If the new result is equal to the previous result, set it to 0
        if i > 0 and new_result == new_test_results[-1]:
            new_result = 0
        # Add the new result to the list of new test results
        new_test_results.append(new_result)

    # Return the list of new test results
    return new_test_results


# Apply the 'calculate_new_test_results' function to each row of the 'df1' dataframe, using the delta values in the
# 'delta_' and 'delta_time_' columns to calculate the new test results and time points, and create new 'New_Test_Results'
# and 'New_Time_Points' columns to store the results
df1['New_Test_Results'] = df1.apply(lambda x: calculate_new_test_results(x['Test Results'],
                                                                         [x['delta_0'], x['delta_1'], x['delta_2'],
                                                                          x['delta_3'], x['delta_4']]), axis=1)
df1['New_Time_Points'] = df1.apply(lambda x: calculate_new_test_results(x['Time Points'],
                                                                        [x['delta_time_0'], x['delta_time_1'],
                                                                         x['delta_time_2'], x['delta_time_3'],
                                                                         x['delta_time_4']]), axis=1)

# Replace any NaN values in the 'New_Test_Results' and 'New_Time_Points' columns with 0
df1['New_Test_Results'] = df1['New_Test_Results'].apply(lambda x: [0 if pd.isna(i) else i for i in x])
df1['New_Time_Points'] = df1['New_Time_Points'].apply(lambda x: [0 if pd.isna(i) else i for i in x])


def plot_results(df, name):
    df1 = df[df['Name'].isin(names)]
    mini = df['Minimum'].tolist()[0]
    maxi = df['Maximum'].tolist()[0]

    import plotly.graph_objs as go

    fig = go.Figure()

    colors = ['red', 'blue', 'green', 'purple', 'orange', 'black']

    for idx, val in df1.iterrows():
        y_2 = val['Test Results']
        x = val['Time Points']
        b_no = val['Name'] + '_' + val['Batch_No']
        color = colors[idx % len(colors)]

        y_2 = [y for y in y_2 if y != 0]
        x = [x for x, y in zip(x, y_2) if y != 0]

        fig.add_trace(
            go.Scatter(x=x, y=y_2, mode='lines+markers', name=b_no, legendgroup=b_no, marker=dict(color=color),
                       line=dict(color=color)))

        y_pred = val['New_Test_Results']
        x_pred = val['New_Time_Points']
        y_pred = [y for y in y_pred if y != 0]
        x_pred = [x for x, y in zip(x_pred, y_pred) if y != 0]

        fig.add_trace(
            go.Scatter(x=x_pred, y=y_pred, mode='lines+markers', name=b_no, line=dict(dash='dot', color=color),
                       legendgroup=b_no, marker=dict(color=color)))

    fig.add_hline(y=maxi, line_color='red')
    fig.add_hline(y=mini, line_color='blue')

    fig.update_layout(xaxis_title='Time Points', yaxis_title='Test Results',
                      title="Actual and Predicted Test Results vs Time Points",
                      width=900, height=600,
                      legend=dict(x=0.4, y=-0.2, xanchor='center', yanchor='top', traceorder="normal",
                                  font=dict(family="sans-serif", size=12, color="black")))

    return fig


plot_results(df1, ['a', 'b'])