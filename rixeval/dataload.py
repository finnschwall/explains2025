import pandas as pd

class XAIData:

    def __init__(self):
        datapoints = pd.read_csv("../data/explanations_table.csv")
        actual_target = datapoints["actual_target"]
        datapoint_summary = datapoints["datapoint_summary"]
        lime_explanation = datapoints["lime_explanation"]
        shap_explanation = datapoints["shap_explanation"]
        datapoint_id = datapoints["datapoint_id"]
        datapoints.drop(columns=["actual_target", "datapoint_summary", "lime_explanation", "shap_explanation","datapoint_id"],
                        inplace=True)

        pdp = pd.read_csv("../data/pdp_explanations.csv")
        histograms = pd.read_csv("../data/histogram_explanations.csv")
        counterfactual1 = pd.read_csv("../data/counterfactual_explanations_1.csv")
        counterfactual2 = pd.read_csv("../data/counterfactual_explanations_2.csv")
        counterfactual3 = pd.read_csv("../data/counterfactual_explanations_3.csv")
        counterfactual4 = pd.read_csv("../data/counterfactual_explanations_4.csv")

        global_methods = {
            "pdp": pdp,
            "histograms": histograms,
            "shap": shap_explanation[0]
        }
        datapoint_list = []
        for i, row in datapoints.iterrows():
            dp = {
                "datapoint": row.to_dict(),
                "actual_target": actual_target[i],
                "datapoint_summary": datapoint_summary[i],
                "lime_explanation": lime_explanation[i],
                "datapoint_id": datapoint_id[i],
                "counterfactual1" : counterfactual1.iloc[i].drop("datapoint_id").to_dict(),
                "counterfactual2" : counterfactual2.iloc[i].drop("datapoint_id").to_dict(),
                "counterfactual3" : counterfactual3.iloc[i].drop("datapoint_id").to_dict(),
                "counterfactual4" : counterfactual4.iloc[i].drop("datapoint_id").to_dict(),
            }
            datapoint_list.append(dp)
        self.global_methods = global_methods
        self.datapoints = datapoint_list


