from rixeval.setup import *
import datetime
class ResponseProcessor:
    @staticmethod
    def parse_decision(response: str) -> str:
        if response.endswith("#CANCELLATION#"):
            return "Cancellation"
        elif response.endswith("#CHECK-OUT#"):
            return "Check-Out"
        else:
            if "#CANCELLATION#" in response:
                return "Cancellation"
            elif "#CHECK-OUT#" in response:
                return "Check-Out"
            else:
                return "INVALID"

    @staticmethod
    def extract_reasoning(response: str) -> str:
        # Extract text before the final decision markers
        lines = response.split('\n')
        reasoning_lines = []
        for line in lines:
            if line.strip().endswith("#CANCELLATION#") or line.strip().endswith("#CHECK-OUT#"):
                break
            reasoning_lines.append(line)
        return '\n'.join(reasoning_lines).strip()


class DataCollector:
    def __init__(self, experiment_dir: str, verbose: bool = False):
        self.experiment_dir = Path(experiment_dir)
        self.experiment_dir.mkdir(parents=True, exist_ok=True)
        self.verbose = verbose
        self.results_file = self.experiment_dir / "results.parquet"
        self.raw_file = self.experiment_dir / "raw_responses.jsonl" if verbose else None

        # Initialize or load existing dataframe
        if self.results_file.exists():
            self.df = pd.read_parquet(self.results_file)
        else:
            self.df = pd.DataFrame()

    def add_result(self, experiment_id: str, combination_id: int, datapoint_idx: int,
                   parameters: Dict[str, Any], llm_response: str, xaidata,
                   processing_time: float, total_tokens: int, tokens_per_second: float,
                   username= None, user_decision= None, chat_id= None, tracker_len= None):


        decision = ResponseProcessor.parse_decision(llm_response)
        reasoning = ResponseProcessor.extract_reasoning(llm_response)
        if decision == "INVALID":
            with open(self.experiment_dir / "invalid_responses.log", 'a') as f:
                f.write(f"{'-'*40}\nInvalid response for combination {combination_id}, "
                        f"datapoint {datapoint_idx}:\nResponse:\n{'*'*10}\n{llm_response}\n{'-'*40}\n")

        # Get ground truth data
        datapoint = xaidata.datapoints[datapoint_idx]
        true_outcome = datapoint["actual_target"]
        predicted_outcome = datapoint["datapoint"]["predicted_target"]
        confidence = datapoint["datapoint"]["confidence_score"]
        dataset_index = datapoint["datapoint_id"]

        # Create result row
        result_row = {
            "experiment_id": experiment_id,
            "combination_id": combination_id,
            "datapoint_idx": datapoint_idx,
            "dataset_index": dataset_index,
            # "confidence": confidence,
            "true_outcome": true_outcome,
            "predicted_outcome": predicted_outcome,
            "llm_decision": decision,
            "reasoning_length": len(reasoning),
            "processing_time": processing_time,
            # "timestamp": time.time(),
            "total_tokens": total_tokens,
            "tokens_per_second": tokens_per_second
        }
        if username is not None:
            result_row["username"] = username
        if user_decision is not None:
            result_row["user_decision"] = user_decision
        if chat_id is not None:
            result_row["chat_id"] = chat_id
        if tracker_len is not None:
            result_row["tracker_len"] = tracker_len

        # Add all parameters as separate columns
        for param_name, param_value in parameters.items():
            if isinstance(param_value, dict):
                # Flatten dict parameters
                for k, v in param_value.items():
                    result_row[f"{param_name}_{k}"] = v
            elif isinstance(param_value, list):
                # Convert list to string representation
                result_row[param_name] = str(param_value)
            else:
                result_row[param_name] = param_value

        # Add to dataframe
        new_row_df = pd.DataFrame([result_row])
        self.df = pd.concat([self.df, new_row_df], ignore_index=True)

        # Save verbose data if enabled
        if self.verbose and self.raw_file:
            raw_data = {
                "experiment_id": experiment_id,
                "combination_id": combination_id,
                "datapoint_idx": datapoint_idx,
                "parameters": parameters,
                "llm_response": llm_response,
                "reasoning": reasoning,
                "timestamp": time.time()
            }
            with open(self.raw_file, 'a') as f:
                f.write(json.dumps(raw_data) + '\n')



    def save_results(self):
        self.df.to_parquet(self.results_file, index=False)

    def get_results(self) -> pd.DataFrame:
        return self.df.copy()


class ExperimentRunner:
    def __init__(self, config: ExperimentConfig, xaidata, llm, ignore_existing: bool = False):
        self.config = config
        self.xaidata = xaidata
        self.llm = llm

        # Create experiment directory
        self.experiment_dir = Path(config.output_dir) / f"{config.name}"
        if os.path.exists(self.experiment_dir / "results.parquet") and not ignore_existing:
            raise FileExistsError(f"Experiment directory {self.experiment_dir} already exists. "
                                  "Please choose a different name or delete the existing directory.")
        self.experiment_dir.mkdir(parents=True, exist_ok=True)

        # Save config
        with open(self.experiment_dir / "config.json", 'w') as f:
            config_dict = asdict(config)
            # Convert variation objects to serializable format
            variations_serializable = {}
            for name, var in config.variations.items():
                variations_serializable[name] = {
                    "type": var.__class__.__name__,
                    "name": var.name,
                    "values": var.generate_values()
                }
            config_dict["variations"] = variations_serializable
            json.dump(config_dict, f, indent=2)
        # Initialize components
        self.variation_generator = VariationGenerator(config.variations)
        self.prompt_builder = EnhancedPromptBuilder(xaidata, )
        self.data_collector = DataCollector(str(self.experiment_dir), config.verbose)


    @staticmethod
    def get_runstats(config, datapoints = 30, expected_min_time_per_prompt = 1.8, expected_max_time_per_prompt = 2.9):
        variation_generator = VariationGenerator(config.variations)
        combinations = variation_generator.generate_combinations()
        print(f"Total combinations: {len(combinations)}")
        print(f"Total expected runs: {len(combinations) * datapoints}")
        t1 = len(combinations) * datapoints * (expected_min_time_per_prompt)/ 60
        t2 = len(combinations) * datapoints * (expected_max_time_per_prompt) / 60
        print(f"This will take between {t1:.0f}-{t2:.0f} minutes / {t1/60:.2f}-{t2/60:.2f} hours.")


    def run(self):
        start_time = time.time()
        combinations = self.variation_generator.generate_combinations()
        with open(self.experiment_dir / "combinations.txt", 'a') as f:
            f.write(f"Generating {len(combinations)} for the following variations:\n")
            f.write(f"{combinations}")
            for combo_id, combination in enumerate(combinations):
                f.write(f"Combination {combo_id + 1}: {combination}\n\n\n")
        experiment_id = self.config.name
        combination_bar = tqdm(combinations, desc="Parameter Combinations")
        total_runs = 0
        avg_time_per_combination=-1
        minutes_elapsed = 0
        seconds_elapsed = 0
        for combo_id, combination in enumerate(combination_bar):
            combination_bar.set_description(f"Combo {combo_id + 1}/{len(combinations)}")
            if self.config.static_parameters:
                combination = {**combination, **self.config.static_parameters}
            self.prompt_builder.set_parameters(combination)

            datapoint_range = min(self.config.max_datapoints, len(self.xaidata.datapoints))
            datapoint_bar = tqdm(range(datapoint_range), desc="Datapoints")

            for datapoint_idx in datapoint_bar:

                # Build prompt and get LLM response
                llm_start_time = time.time()
                prompt = self.prompt_builder.build_prompt(datapoint_idx)
                if self.config.verbose:
                    print(f"Prompt for datapoint {datapoint_idx}:\n{'-'*40}\n{prompt}\n")
                if self.config.no_llm:
                    time.sleep(0.01)
                    llm_response = "Mock response for testing purposes." + np.random.choice([" #CANCELLATION#", " #CHECK-OUT#"])
                    total_tokens = 0
                else:
                    self.llm.reset_tracker() if hasattr(self.llm, 'reset_tracker') else None
                    llm_response = self.llm.create_completion(prompt)
                    if self.config.verbose or self.config.print_llm_responses:
                        print(f"LLM Response for datapoint {datapoint_idx}:\n{'-'*40}\n{llm_response}\n")
                    meta = self.llm.finish_meta
                    total_tokens = meta.get('tokens', {}).get('total_tokens', 0)

                processing_time = time.time() - llm_start_time
                tokens_per_second = total_tokens / processing_time if processing_time > 0 else 0

                # Collect result
                self.data_collector.add_result(
                    experiment_id=experiment_id,
                    combination_id=combo_id,
                    datapoint_idx=datapoint_idx,
                    parameters=combination,
                    llm_response=llm_response,
                    xaidata=self.xaidata,
                    processing_time=processing_time,
                    total_tokens=total_tokens,
                    tokens_per_second=tokens_per_second
                )

                # Save periodically
                if (datapoint_idx + 1) % 10 == 0:
                    self.data_collector.save_results()
                total_runs += 1
                current_time = time.time()
                seconds_elapsed = current_time - start_time
                minutes_elapsed = seconds_elapsed / 60
                avg_time_per_combination = seconds_elapsed / total_runs
                # datapoint_bar.set_description(f"Datapoint {datapoint_idx + 1}/{datapoint_range} "
                #                               f"(Time: {minutes_elapsed:.2f}m, Total runs: {total_runs})")

            # Save after each combination
            self.data_collector.save_results()

            with open(self.experiment_dir / "run.txt", 'w') as f:
                run_str = f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                run_str += f"Current run: {total_runs}/{len(combinations)*self.config.max_datapoints}\n"
                run_str += f"Total time elapsed: {minutes_elapsed:.2f}m, {seconds_elapsed:.2f}s\n"
                run_str += f"Avg. time per run: {avg_time_per_combination:.2f}s\n"
                run_str += f"Exp. time left: {(len(combinations)*self.config.max_datapoints - total_runs) * avg_time_per_combination / 60:.2f} minutes\n"
                f.write(run_str)


        return self.data_collector.get_results()


class ChatExperimentRunner:
    def __init__(self, config: ExperimentConfig, data, xaidata, llm, ignore_existing: bool = False):
        self.config = config
        self.data = data
        self.llm = llm
        self.xaidata = xaidata

        # Create experiment directory
        self.experiment_dir = Path(config.output_dir) / f"{config.name}"
        if os.path.exists(self.experiment_dir / "results.parquet") and not ignore_existing:
            raise FileExistsError(f"Experiment directory {self.experiment_dir} already exists. "
                                  "Please choose a different name or delete the existing directory.")
        self.experiment_dir.mkdir(parents=True, exist_ok=True)

        # Save config
        with open(self.experiment_dir / "config.json", 'w') as f:
            config_dict = asdict(config)
            # Convert variation objects to serializable format
            variations_serializable = {}
            for name, var in config.variations.items():
                variations_serializable[name] = {
                    "type": var.__class__.__name__,
                    "name": var.name,
                    "values": var.generate_values()
                }
            config_dict["variations"] = variations_serializable
            json.dump(config_dict, f, indent=2)
        # Initialize components
        self.variation_generator = VariationGenerator(config.variations)
        self.prompt_builder = EnhancedTrackerBuilder(xaidata)
        self.data_collector = DataCollector(str(self.experiment_dir), config.verbose)

    @staticmethod
    def get_runstats(config, chats, expected_min_time_per_prompt = 1.8, expected_max_time_per_prompt = 2.9):
        variation_generator = VariationGenerator(config.variations)
        combinations = variation_generator.generate_combinations()
        print(f"Total combinations: {len(combinations)}, Total chats: {len(chats)}")
        print(f"Total expected runs: {len(combinations) * len(chats)}")
        t1 = len(combinations) * len(chats) * expected_min_time_per_prompt / 60
        t2 = len(combinations) * len(chats) * expected_max_time_per_prompt / 60
        print(f"This will take between {t1:.0f}-{t2:.0f} minutes / {t1/60:.2f}-{t2/60:.2f} hours.")


    def run(self, max_chats=None):
        start_time = time.time()
        combinations = self.variation_generator.generate_combinations()
        with open(self.experiment_dir / "combinations.txt", 'a') as f:
            f.write(f"Generating {len(combinations)} for the following variations:\n")
            f.write(f"{combinations}")
            for combo_id, combination in enumerate(combinations):
                f.write(f"Combination {combo_id + 1}: {combination}\n\n\n")
        experiment_id = self.config.name
        combination_bar = tqdm(combinations, desc="Parameter Combinations")
        total_runs = 0
        avg_time_per_combination=-1
        minutes_elapsed = 0
        seconds_elapsed = 0
        if max_chats is None:
            max_chats = len(self.data)
        i=0
        for combo_id, combination in enumerate(combination_bar):
            combination_bar.set_description(f"Combo {combo_id + 1}/{len(combinations)}")
            if self.config.static_parameters:
                combination = {**combination, **self.config.static_parameters}
            self.prompt_builder.set_parameters(combination)

            data_bar = tqdm(self.data[:max_chats].iterrows(), desc="Chats", total=self.data.shape[0])
            for data in data_bar:
                data=data[1]
                llm_start_time = time.time()
                tracker = self.prompt_builder.build_prompt(data)

                if self.config.verbose:
                    print(f"\n\n{'-'*40}\nPrompt:\n{'-'*40}\n")
                    for message in tracker.tracker:
                        if "content" in message:
                            print(f"{message['role']}: {message['content']}")
                if self.config.no_llm:
                    time.sleep(0.01)
                    llm_response = "Mock response for testing purposes." + np.random.choice([" #CANCELLATION#", " #CHECK-OUT#"])
                    total_tokens = 0
                else:
                    self.llm.reset_tracker() if hasattr(self.llm, 'reset_tracker') else None
                    llm_response = self.llm.create_completion_plugin(tracker)
                    llm_response = llm_response[0].tracker[-1]["content"]
                    meta = self.llm.finish_meta
                    total_tokens = meta.get('tokens', {}).get('total_tokens', 0)

                processing_time = time.time() - llm_start_time
                tokens_per_second = total_tokens / processing_time if processing_time > 0 else 0

                # Collect result
                self.data_collector.add_result(
                    experiment_id=experiment_id,
                    combination_id=combo_id,
                    datapoint_idx=data["current_datapoint_index"],
                    parameters=combination,
                    llm_response=llm_response,
                    xaidata=self.xaidata,
                    processing_time=processing_time,
                    total_tokens=total_tokens,
                    tokens_per_second=tokens_per_second,
                    username=data["username"],
                    user_decision=data["datapoint_choice"],
                    tracker_len=data["tracker_length"],
                    chat_id=data["id"],

                )

                # Save periodically
                if i % 10 == 0:
                    self.data_collector.save_results()
                total_runs += 1
                current_time = time.time()
                seconds_elapsed = current_time - start_time
                minutes_elapsed = seconds_elapsed / 60
                avg_time_per_combination = seconds_elapsed / total_runs
                # datapoint_bar.set_description(f"Datapoint {datapoint_idx + 1}/{datapoint_range} "
                #                               f"(Time: {minutes_elapsed:.2f}m, Total runs: {total_runs})")
                i+=1

            # Save after each combination
            self.data_collector.save_results()

            with open(self.experiment_dir / "run.txt", 'w') as f:
                run_str = f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                run_str += f"Current run: {total_runs}/{len(combinations)*self.config.max_datapoints}\n"
                run_str += f"Total time elapsed: {minutes_elapsed:.2f}m, {seconds_elapsed:.2f}s\n"
                run_str += f"Avg. time per run: {avg_time_per_combination:.2f}s\n"
                run_str += f"Exp. time left: {(len(combinations)*self.config.max_datapoints - total_runs) * avg_time_per_combination / 60:.2f} minutes\n"
                f.write(run_str)


        return self.data_collector.get_results()
