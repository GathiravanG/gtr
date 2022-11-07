import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
import seaborn as sns


def predictionCumEvaluation(gok):

    csv_datasets = pd.read_csv("D:\GTR24\predictor\predict.csv")

    csv_dataset = csv_datasets.drop(['Month'], axis=1)

    dates = csv_datasets.drop(['Sales'], axis=1)

    #Finding optimal alpha and optimal gama
    #Based on  mse(mean square error)
    optimal_alpha = None
    optimal_gamma = None
    best_mse = None
    db = csv_dataset.iloc[:, :].values.astype('float32')
    mean_results_for_all_possible_alpha_gamma_values = np.zeros((9, 9))
    for gamma in range(0, 9):
        for alpha in range(0, 9):
            pt = db[0][0]
            bt = db[1][0] - db[0][0]
            mean_for_alpha_gamma = np.zeros(len(db))
            mean_for_alpha_gamma[0] = np.power(db[0][0] - pt, 2)
            for i in range(1, len(db)):
                temp_pt = ((alpha + 1) * 0.1) * db[i][0] + (1 - ((alpha + 1) * 0.1)) * (pt + bt)
                bt = ((gamma + 1) * 0.1) * (temp_pt - pt) + (1 - ((gamma + 1) * 0.1)) * bt
                pt = temp_pt
                mean_for_alpha_gamma[i] = np.power(db[i][0] - pt, 2)
            mean_results_for_all_possible_alpha_gamma_values[gamma][alpha] = np.mean(mean_for_alpha_gamma)
            optimal_gamma, optimal_alpha = np.unravel_index(
                np.argmin(mean_results_for_all_possible_alpha_gamma_values),
                np.shape(mean_results_for_all_possible_alpha_gamma_values))
    optimal_alpha = (optimal_alpha + 1) * 0.1
    optimal_gamma = (optimal_gamma + 1) * 0.1
    best_mse = np.min(mean_results_for_all_possible_alpha_gamma_values)
    print("Best MSE = %s" % best_mse)
    print("Optimal alpha = %s" % optimal_alpha)
    print("Optimal gamma = %s" % optimal_gamma)

    #finding p_t and b_t
    pt = db[0][0]
    bt = db[1][0] - db[0][0]
    for i in range(1, len(db)):
        temp_pt = optimal_alpha * db[i][0] + (1 - optimal_alpha) * (pt + bt)
        bt = optimal_gamma * (temp_pt - pt) + (1 - optimal_gamma) * bt
        pt = temp_pt
    print("P_t = %s" % pt)
    print("b_t = %s" % bt )

    #actual vs prediction .csv file genaration
    forecast = np.zeros(len(db) + 1)
    pt = db[0][0]
    bt = db[1][0] - db[0][0]
    forecast[0] = pt
    for i in range(1, len(db)):
        temp_pt = optimal_alpha * db[i][0] + (1 - optimal_alpha) * (pt + bt)
        bt = optimal_gamma * (temp_pt - pt) + (1 - optimal_gamma) * bt
        pt = temp_pt
        forecast[i] = pt
    forecast[-1] = pt + (1 * bt)

    d = [1]

    for i in range(2,37):
     d.append(i) 


    s = np.atleast_1d(d)
    g = np.atleast_1d(db)

    date = s.flatten()
    real = g.flatten()
    lastElementIndex = len(forecast)-1
    # Removing the last element using slicing 
    forecast = forecast[:lastElementIndex]

    #creating a csv file containing the actual and predicted sales values for the given time period
    output = pd.DataFrame({'Date':date, 'Actual Data':real, 'Predicted Data': forecast})
    output.to_csv('submission.csv', index=False)

    # R squared Value
    rmse = metrics.r2_score(real, forecast)
    print(rmse)


    #generating a csv file for future prediction whose time period is given by the user in frontend
    #future prediction
    future_prediction = [(pt + (1 * bt))]
    for i in range(2,gok+1):
     future_prediction.append(pt + ((i) * bt))
    #along with aldready prdicted data
    for i in range(1,gok+1):
     future = np.append(forecast, future_prediction)


    
    #for serial number
    serial = [1]

    mon = 36 + gok
    for i in range(2,mon+1):
     serial.append(i)

    #for actual data
    p = [0]
    for i in range(2,gok+1):
     p.append(0)

    for i in range(1,gok+1):
     rfuture = np.append(real, p)

    #for ploting the real vs forcasted data
    plt.title('Predicted data along with Actual data')
    plt.plot(rfuture,label = 'real data')
    plt.plot(future, label = 'predicted data')
    plt.legend()
    plt.show()

    se = [0]
    for i in range(1,gok):
     se.append(i)

    f = pd.DataFrame({'Months':se,'Predicted Data': future_prediction})

    # function to add value labels
    def addlabels(x,y):
        for i in range(len(x)):
            plt.text(i, y[i]//2, round(y[i]), ha = 'center')
    
    plt.figure(figsize = (20, 5))
    plt.bar(se, future_prediction)
    addlabels(se, future_prediction)
    plt.title("Future prediction for no. of months provided by the user")
    plt.xlabel("Months")
    plt.ylabel("Sales")
    plt.show()


