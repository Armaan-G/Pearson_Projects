import pandas as pd
import numpy as np
import lightgbm as lgb
import xgboost as xgb

deliveries_data = pd.read_excel('Monthly_Metrics_Data_2022-2024_test.xlsx') # sets deliveries_data equal to CITB_Emails.xlsx
deliveries_data['Date'] = pd.to_datetime(deliveries_data['Date']) # sets the Date perameter within deliveries_data to pandas version
deliveries_data.set_index('Date', inplace=True) # runs set_index with specific parameters


deliveries_data_filled = deliveries_data.fillna(0) # fills all na data with 0
deliveries_data_cleaned = deliveries_data_filled.replace([np.inf, -np.inf], np.finfo(np.float64).max) #sets all instances of infinity to the maximum float value in pandas

deliveries_data_cleaned = pd.DataFrame(deliveries_data_cleaned)

deliveries_data_cleaned.head() #gives the frst 5 rows of the dataset


train_data = deliveries_data_cleaned[:'2023-10-31'] # set train_data to the cleanded data


test_data_dates = pd.date_range(start='2023-11-01', end='2023-11-30', freq='B') # finding the range of the dataset

# LightGBM and XGBoost
ordinal_dates = deliveries_data_cleaned.index.map(pd.Timestamp.toordinal).values.reshape(-1, 1) # makes ordinal_dates 2D NumPy array where each row contains the ordinal date representation of the corresponding index entry from the deliveries_data_cleaned

lightgbm_forecasts = {}
xgboost_forecasts = {}


for client_name in deliveries_data_cleaned.columns: #loop will run for every client name in the data set
    client_deliveries_data = deliveries_data_cleaned[client_name].values

    # LightGBM
    lgb_model = lgb.LGBMRegressor(max_depth=5, num_leaves=20, n_estimators=10)  #  creates an instance of the LightGBM Regressor model
    lgb_model.fit(ordinal_dates[:-len(test_data_dates)], client_deliveries_data[:-len(test_data_dates)]) # fits the data set to the regressor model
    lgb_forecast = lgb_model.predict(ordinal_dates[-len(test_data_dates):]) # after training uses the model to predict delivery data for the dates specified in test_data_dates
    lightgbm_forecasts[client_name] = np.maximum(lgb_forecast, 0) # line ensures that all forecasted values are non-negative
    # XGBoost 
    # does the same thing as the first one j with different application 
    xgb_model = xgb.XGBRegressor(max_depth=5, n_estimators=50) 
    xgb_model.fit(ordinal_dates[:-len(test_data_dates)], client_deliveries_data[:-len(test_data_dates)])
    xgb_forecast = xgb_model.predict(ordinal_dates[-len(test_data_dates):])
    xgboost_forecasts[client_name] = np.maximum(xgb_forecast, 0)  #  non-negative


lightgbm_df = pd.DataFrame(lightgbm_forecasts)
xgboost_df = pd.DataFrame(xgboost_forecasts)

#creates new excel sheets with the predicted data
with pd.ExcelWriter('predictedData.xlsx', engine='openpyxl') as writer:
    lightgbm_df.to_excel(writer, sheet_name='LightGBM')
    xgboost_df.to_excel(writer, sheet_name='XGBoost')

#cmVmdGtuOjAxOjE3NTM0Nzk5MTg6ejk4Y0RRdVdMaHhZcDZtZXgxYVdYcjd1TDAz