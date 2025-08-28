import pandas as pd
import numpy as np
from typing import Dict, List, Any, Union, Optional
import krippendorff


def calculate_krippendorff_alpha(df):
    # Create a matrix where rows are datapoints and columns are raters (variations)
    datapoints = df['datapoint_idx'].unique()
    max_variations = df['datapoint_idx'].value_counts().max()

    # Create reliability data matrix
    reliability_data = []

    for datapoint_idx in datapoints:
        decisions = df[df['datapoint_idx'] == datapoint_idx]['llm_decision'].tolist()
        # Convert to numeric (Check-Out = 1, Cancellation = 0)
        numeric_decisions = [1 if d == 'Check-Out' else 0 for d in decisions]

        # Pad with NaN if fewer variations than max
        while len(numeric_decisions) < max_variations:
            numeric_decisions.append(np.nan)

        reliability_data.append(numeric_decisions)

    # Transpose for krippendorff format (raters as rows, items as columns)
    reliability_data = np.array(reliability_data).T

    # Calculate Krippendorff's Alpha
    alpha = krippendorff.alpha(reliability_data, level_of_measurement='nominal')
    return alpha

class ResultAnalyzer:
    def __init__(self, results_df: pd.DataFrame):
        self.df = results_df.copy()
        self._encode_outcomes()

    def _encode_outcomes(self):
        outcome_mapping = {'Check-Out': 1, 'Cancellation': 0}
        self.df['true_outcome_encoded'] = self.df['true_outcome'].map(outcome_mapping)
        self.df['predicted_outcome_encoded'] = self.df['predicted_outcome'].map(outcome_mapping)
        self.df['llm_decision_encoded'] = self.df['llm_decision'].map(outcome_mapping)
        if "user_decision" in self.df.columns:
            outcome_mapping = {'confirm_datapoint': 1, 'decline_datapoint': 0}
            self.df['user_decision_encoded'] = self.df['user_decision'].map(outcome_mapping)

    def analyze_combination(self, combination_id: int) -> Dict[str, float]:
        combo_data = self.df[self.df['combination_id'] == combination_id]

        if len(combo_data) == 0:
            return {}

        num_correct = len(combo_data[combo_data['true_outcome'] == combo_data['llm_decision']])
        percent_correct = (num_correct / len(combo_data)) * 100

        num_agree_ai = len(combo_data[combo_data['predicted_outcome'] == combo_data['llm_decision']])
        percent_agree_ai = (num_agree_ai / len(combo_data)) * 100

        # Correlations
        if combo_data['llm_decision_encoded'].std() == 0:
            corr_correct = 0
            corr_agree = 0
        else:
            corr_correct = combo_data['true_outcome_encoded'].corr(combo_data['llm_decision_encoded'])
            corr_agree = combo_data['predicted_outcome_encoded'].corr(combo_data['llm_decision_encoded'])

        if "user_decision_encoded" in combo_data.columns:
            num_user_correct = len(combo_data[combo_data['true_outcome_encoded'] == combo_data['user_decision_encoded']])
            num_user_agree_ai = len(combo_data[combo_data['predicted_outcome_encoded'] == combo_data['user_decision_encoded']])
            percent_user_correct = (num_user_correct / len(combo_data)) * 100
            percent_user_agree_ai = (num_user_agree_ai / len(combo_data)) * 100
            if combo_data['user_decision_encoded'].std() == 0:
                corr_user_llm = 0
                corr_user_correct = 0
            else:
                corr_user_llm = combo_data['user_decision_encoded'].corr(combo_data['llm_decision_encoded'])
                corr_user_correct = combo_data['user_decision_encoded'].corr(combo_data['true_outcome_encoded'])

        false_positive_rate = len(combo_data[(combo_data['true_outcome'] == 'Cancellation') & (combo_data['llm_decision'] == 'Check-Out')])
        false_negative_rate = len(combo_data[(combo_data['true_outcome'] == 'Check-Out') & (combo_data['llm_decision'] == 'Cancellation')])
        return_dic = {
            "combination_id": combination_id,
            "n_datapoints": len(combo_data),
            "percent_correct": percent_correct,
            "percent_agree": percent_agree_ai,
            "corr_correct": corr_correct,
            "corr_agree": corr_agree,
            "false_positive_rate": false_positive_rate/30,
            "false_negative_rate": false_negative_rate/30,
            # "decision_entropy": decision_entropy,
        }
        if "processing_time" in combo_data.columns:
            return_dic["avg_processing_time"] = combo_data['processing_time'].mean()
        # if "user_decision_encoded" in combo_data.columns:
        #     return_dic["corr_user_llm"] = corr_user_llm
        #     return_dic["corr_user_correct"] = corr_user_correct
        #     return_dic["percent_user_correct"] = percent_user_correct
        #     return_dic["percent_user_agree_ai"] = percent_user_agree_ai
        return return_dic

    def analyze_all_combinations(self) -> pd.DataFrame:
        results = []
        for combo_id in self.df['combination_id'].unique():
            analysis = self.analyze_combination(combo_id)
            if analysis:
                # Add parameter information
                combo_params = self.df[self.df['combination_id'] == combo_id].iloc[0]
                param_cols = [col for col in self.df.columns if col not in [
                    'experiment_id', 'combination_id', 'datapoint_idx', 'dataset_index',
                    'confidence', 'true_outcome', 'predicted_outcome', 'llm_decision',
                    'reasoning_length', 'processing_time', 'timestamp',
                    'true_outcome_encoded', 'predicted_outcome_encoded', 'llm_decision_encoded', "tokens_per_second", "total_tokens"
                ]]

                for col in param_cols:
                    analysis[col] = combo_params[col]
                results.append(analysis)

        return pd.DataFrame(results).drop("combination_id", axis=1)

    def filter_by_parameter(self, param_name: str, param_value: Any) -> 'ResultAnalyzer':
        filtered_df = self.df[self.df[param_name] == param_value]
        return ResultAnalyzer(filtered_df)

    def compare_parameters(self, param_name: str = None, include_fp_fn=False) -> pd.DataFrame:
        # Compare results across different values of a parameter
        comparison_results = []

        if param_name is None:
            analyzer = ResultAnalyzer(self.df)
            summary = analyzer.analyze_all_combinations()
            temp = {
                    "n_combinations": len(summary),
                    "krippendorff_alpha": calculate_krippendorff_alpha(self.df), }
            params = ["percent_correct", "percent_agree", "corr_correct", "corr_agree"]

            # if "user_decision" in self.df.columns:
            #     params += ["percent_user_correct", "percent_user_agree_ai", "corr_user_llm", "corr_user_correct"]
            if include_fp_fn:
                params += ["false_positive_rate", "false_negative_rate"]
            for col in params:
                temp[f"avg_{col}"] = f"{summary[col].mean():.2f}+-{summary[col].std():.2f}"
            comparison_results.append(temp)
            return pd.DataFrame(comparison_results)

        for param_value in self.df[param_name].unique():
            subset = self.df[self.df[param_name] == param_value]

            if len(subset) == 0:
                continue

            analyzer = ResultAnalyzer(subset)
            summary = analyzer.analyze_all_combinations()
            temp = {param_name: param_value,
                                  "n_combinations": len(summary),
                    "krippendorff_alpha": calculate_krippendorff_alpha(subset),}
            params = ["percent_correct", "percent_agree", "corr_correct", "corr_agree"]
            # if "user_decision" in self.df.columns:
            #     params += ["percent_user_correct", "percent_user_agree_ai", "corr_user_llm", "corr_user_correct"]
            if include_fp_fn:
                params += ["false_positive_rate", "false_negative_rate"]
            for col in params:
                temp[f"avg_{col}"] = f"{summary[col].mean():.2f}+-{summary[col].std():.2f}"
            comparison_results.append(temp)


        return pd.DataFrame(comparison_results)