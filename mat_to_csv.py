import pandas as pd
import argparse
from scipy.io import loadmat


mat_data_folder = 'D:\竞赛、项目\LSTM预测电池论文\数据集\Battery Data Set（电池数据集）\BatteryAgingARC-FY08Q4    5_6_7_18/'
# battery_idx = 'B0006'
battery_idx = 'B0007'
# battery_idx = 'B0018'
# battery_idx = 'B0005'
# mat_data = loadmat(mat_data_folder + 'B0018.mat')[battery_idx]
# mat_data = loadmat(mat_data_folder + 'B0005.mat')[battery_idx]
# mat_data = loadmat(mat_data_folder + 'B0006.mat')[battery_idx]
mat_data = loadmat(mat_data_folder + 'B0007.mat')[battery_idx]
# print (type(mat_data))
# print(mat_data.keys())


def to_df(mat_db):
    """Returns one pd.DataFrame per cycle type"""

    # Features common for every cycle
    cycles_cols = ['type', 'ambient_temperature', 'time']

    # Features monitored during the cycle
    features_cols = {
        'charge': ['Voltage_measured', 'Current_measured', 'Temperature_measured',
                   'Current_charge', 'Voltage_charge', 'Time'],
        'discharge': ['Voltage_measured', 'Current_measured', 'Temperature_measured',
                      'Current_charge', 'Voltage_charge', 'Time', 'Capacity'],
        'impedance': ['Sense_current', 'Battery_current', 'Current_ratio',
                      'Battery_impedance', 'Rectified_impedance', 'Re', 'Rct']
    }

    # Define one pd.DataFrame per cycle type
    df = {key: pd.DataFrame() for key in features_cols.keys()}

    # Get every cycle
    print(f'Number of cycles: {mat_db[0][0][0].shape[1]}')
    cycles = [[row.flat[0] for row in line] for line in mat_db[0][0][0][0]]

    # Get measures for every cycle
    for cycle_id, cycle_data in enumerate(cycles):
        tmp = pd.DataFrame()

        # Data series for every cycle
        features_x_cycle = cycle_data[-1]

        # Get features for the specific cycle type
        features = features_cols[cycle_data[0]]

        for feature, data in zip(features, features_x_cycle):
            if len(data[0]) > 1:
                # Correct number of records
                tmp[feature] = data[0]
            else:
                # Single value, so assign it to all rows
                tmp[feature] = data[0][0]

        # Add columns common to the cycle measurements
        tmp['id_cycle'] = cycle_id
        for k, col in enumerate(cycles_cols):
            tmp[col] = cycle_data[k]

        # Append cycle data to the right pd.DataFrame
        cycle_type = cycle_data[0]
        df[cycle_type] = df[cycle_type].append(tmp, ignore_index=True)

    return df



dfs = to_df(mat_data)
dfs_charge = dfs['charge']
dfs_discharge = dfs['discharge']
dfs_impedance = dfs['impedance']

dfs_charge.to_csv(mat_data_folder + battery_idx + '_charge.csv', index=False)
dfs_discharge.to_csv(mat_data_folder + battery_idx + '_discharge.csv', index=False)
dfs_impedance.to_csv(mat_data_folder + battery_idx + '_impedance.csv', index=False)