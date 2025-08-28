import copy

import pandas as pd
import numpy as np
import json
import pickle
import itertools
import time
import os
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Union, Optional
from dataclasses import dataclass, asdict
from tqdm.notebook import tqdm
import random


@dataclass
class ExperimentConfig:
    name: str
    description: str
    variations: Dict[str, Any]
    max_datapoints: int = 30
    verbose: bool = False
    print_llm_responses: bool = False
    output_dir: str = "experiments"
    no_llm: bool = False
    static_parameters: Optional[Dict[str, Any]] = None


class BaseVariation(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def generate_values(self) -> List[Any]:
        pass


class NumericalRange(BaseVariation):
    def __init__(self, name: str, min_val: float, max_val: float, num_samples: int):
        super().__init__(name)
        self.min_val = min_val
        self.max_val = max_val
        self.num_samples = num_samples

    def generate_values(self) -> List[float]:
        return np.linspace(self.min_val, self.max_val, self.num_samples).tolist()


class UniformRange(BaseVariation):
    def __init__(self, name: str, min_val: float, max_val: float, num_samples: int):
        super().__init__(name)
        self.min_val = min_val
        self.max_val = max_val
        self.num_samples = num_samples

    def generate_values(self) -> List[float]:
        return [random.uniform(self.min_val, self.max_val) for _ in range(self.num_samples)]

class SequentialRange(BaseVariation):
    def __init__(self, name: str, start: float, end: float, num_samples: int, fake_decimals: bool = False, decimal_places :float =2):
        super().__init__(name)
        self.start = start
        self.end = end
        self.num_samples = num_samples
        self.fake_decimals = fake_decimals
        self.decimal_places = decimal_places

    def generate_values(self) -> List[float]:
        nums = np.linspace(self.start, self.end, self.num_samples)
        if self.fake_decimals:
            nums += np.random.uniform(-1, 1, self.num_samples)
            nums = [min(i, self.end) for i in nums]
            nums = np.round(nums, decimals=self.decimal_places)
        return list(nums)

class Exclusion(BaseVariation):
    def __init__(self, name: str, items: List[str]):
        super().__init__(name)
        self.items = items

    def generate_values(self) -> List[Dict[str, bool]]:
        results = []
        for i in range(len(self.items) + 1):
            for combo in itertools.combinations(self.items, i):
                item_dict = {item: item in combo for item in self.items}
                results.append(item_dict)
        return results


class CategoricalList(BaseVariation):
    def __init__(self, name: str, values: List[Any]):
        super().__init__(name)
        self.values = values

    def generate_values(self) -> List[Any]:
        return self.values.copy()


class NamedCategories(BaseVariation):
    def __init__(self, name: str, categories: Dict[str, List[Any]]):
        super().__init__(name)
        self.categories = categories

    def generate_values(self) -> List[Dict[str, Any]]:
        results = []
        for cat_name, values in self.categories.items():
            for value in values:
                results.append({"category": cat_name, "value": value})
        return results


class Permutation(BaseVariation):
    def __init__(self, name: str, items: List[str], max_perms: int = None):
        super().__init__(name)
        self.items = items
        self.max_perms = max_perms

    def generate_values(self) -> List[List[str]]:
        all_perms = list(itertools.permutations(self.items))
        if self.max_perms and len(all_perms) > self.max_perms:
            return random.sample(all_perms, self.max_perms)
        return [list(perm) for perm in all_perms]




class VariationGenerator:
    def __init__(self, variations: Dict[str, BaseVariation]):
        self.variations = variations

    def generate_combinations(self) -> List[Dict[str, Any]]:
        keys = list(self.variations.keys())
        value_lists = [var.generate_values() for var in self.variations.values()]

        combinations = []
        for combo in itertools.product(*value_lists):
            param_dict = dict(zip(keys, combo))
            combinations.append(param_dict)
        return combinations


class EnhancedPromptBuilder:
    def __init__(self, xaidata, base_prompts: Dict[str, str] = None):
        self.xaidata = xaidata
        self.base_prompts = base_prompts or {}
        self.current_params = {}

    def set_parameters(self, params: Dict[str, Any]):
        self.current_params = params

    def build_prompt(self, index: int) -> str:
        msg = ""

        # Handle preprompt variations
        if "preprompt_type" in self.current_params:
            msg += self._build_preprompt_variation(index)
        else:
            msg += self._build_default_preprompt(index)

        # Handle XAI method variations
        msg += self._build_xai_methods(index)
        if "final_prompt_type" in self.current_params:
            msg += self._build_final_prompt_variation()
        else:
            msg += self._build_default_final_prompt()

        return msg

    def _build_default_preprompt(self, index: int) -> str:
        datapoint = self.xaidata.datapoints[index]["datapoint"]
        confidence_score = datapoint["confidence_score"]
        if "confidence_score" in self.current_params:
            confidence_score = self.current_params["confidence_score"]


        predicted_class_str = datapoint["predicted_target"]
        if "predicted_target" in self.current_params:
            if isinstance(self.current_params["predicted_target"], str):
                predicted_class_str = self.current_params["predicted_target"]
        dpointstr = ""
        if confidence_score is not None:
            dpointstr += f"The confidence score of this datapoint is {confidence_score}%. "
            dpointstr += f"This means the model is {confidence_score}% confident that the booking will result in a {predicted_class_str.lower()}."
        dpointstr += "\nFeature values:\n"

        for feature in datapoint.keys():
            if feature in ["confidence_score", "predicted_target"]:
                continue
            dpointstr += f"- {feature}: {datapoint[feature]}\n"

        return dpointstr

    def _build_preprompt_variation(self, index: int) -> str:
        # Placeholder for preprompt variations
        return self._build_default_preprompt(index)

    def _build_xai_methods(self, index: int) -> str:
        local_methods = []
        global_methods = []

        # Handle exclusion variations

        if "xai_exclusion" in self.current_params:
            exclusion_dict = self.current_params["xai_exclusion"]
            local_methods = [k for k, v in exclusion_dict.items() if v and k in ["lime_explanation", "counterfactual1"]]
            global_methods = [k for k, v in exclusion_dict.items() if v and k in ["pdp", "shap"]]
        else:
            local_methods = ["lime_explanation", "counterfactual1"]
            global_methods = ["pdp", "shap", "histograms"]


        if "xai_excluded" in self.current_params:
            if self.current_params["xai_excluded"] == "yes":
                local_methods = []
                global_methods = []

        # Handle permutation variations
        if "method_order" in self.current_params:
            all_methods = self.current_params["method_order"]
            local_methods = [m for m in all_methods if m in local_methods]
            global_methods = [m for m in all_methods if m in global_methods]

        methods_content = []
        template = "### {key}\n {value}\n\n"

        for method in local_methods:
            if method in self.xaidata.datapoints[index]:
                methods_content.append(template.format(key=method, value=self.xaidata.datapoints[index][method]))

        for method in global_methods:
            if method in self.xaidata.global_methods:
                methods_content.append(template.format(key=method, value=self.xaidata.global_methods[method]))

        return "\n".join(methods_content)

    def _build_default_final_prompt(self) -> str:
        accuracy = self.current_params.get("accuracy", "84.34%")
        return f"""
Above is data with XAI methods from a hotel booking system. You need to decide whether or not to select "Cancellation" or "Check-out"
An AI system has been trained to predict the target variable "Cancellation" based on the datapoint features. You also see its output and its confidence score.
All XAI methods are based on this classifier.
This AI system is there to support you in your decision. However you should  not blindly follow its recommendation! The overall accuracy of the trained classifier is {accuracy}%.

Explain your decision whether to select "Cancellation" or "Check-out".

To automate this process end your last line with your choice with either
#CANCELLATION#
or
#CHECK-OUT#
"""

    def _build_final_prompt_variation(self) -> str:
        prompt_config = self.current_params["final_prompt_type"]
        category = prompt_config["category"]
        prompt_template = prompt_config["value"]

        accuracy = self.current_params.get("accuracy", 84.34)
        if isinstance(accuracy, str):
            return prompt_template.replace("{accuracy}", accuracy)
        if "bias" in self.current_params:
            bias = self.current_params["bias"]
            if bias["category"] != "None":
                prompt_template += "\n"+bias["value"]


        if "think_mode" in self.current_params:
            think_mode = self.current_params["think_mode"]
            prompt_template+= f"\n{think_mode['value']}"

        return prompt_template.replace("{accuracy}", f"{accuracy:.2f}")



class EnhancedTrackerBuilder(EnhancedPromptBuilder):
    def build_prompt(self, data) -> str:

        tracker = copy.deepcopy(data["tracker"])
        datapoint_index = data["current_datapoint_index"]

        if "system_message" in self.current_params:
            tracker.system_message = self.current_params["system_message"]

        if "include_datapoint_info" in self.current_params:
            if tracker.system_message is None:
                tracker.system_message = ""
            tracker.system_message += self._build_default_preprompt(datapoint_index)

        if "final_prompt_type" in self.current_params:
            tracker.add_entry(self._build_final_prompt_variation(), "user")
        else:
            tracker.add_entry(self._build_default_final_prompt(), "user")

        return tracker