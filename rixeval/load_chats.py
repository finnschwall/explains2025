import sqlite3
import pandas as pd
from pathlib import Path
from pyalm import ConversationTracker
import numpy as np
import matplotlib.pyplot as plt
import ast


def extract_conversations_to_dataframe(db_path, table_name=None, user_table_name=None):
    conn = sqlite3.connect(db_path)

    try:
        if table_name is None:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            conversation_tables = [t[0] for t in tables if 'conversation' in t[0].lower()]

            if not conversation_tables:
                print("Available tables:")
                for table in tables:
                    print(f"  - {table[0]}")
                raise ValueError("No conversation table found. Please specify table_name parameter.")

            table_name = conversation_tables[0]
            print(f"Found conversation table: {table_name}")

        cursor = conn.cursor()

        if user_table_name is None:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            user_tables = [t[0] for t in tables if 'user' in t[0].lower() and 'auth' in t[0].lower()]
            if not user_tables:
                user_tables = [t[0] for t in tables if 'user' in t[0].lower()]

            if user_tables:
                user_table_name = user_tables[0]
                print(f"Found user table: {user_table_name}")
            else:
                print("Warning: Could not find user table.")

        if user_table_name:
            query = f"""
            SELECT
                c.id,
                u.username,
                c.tracker_yaml,
                c.timestamp,
                c.model_name,
                c.chat_mode
            FROM {table_name} c
            LEFT JOIN {user_table_name} u ON c.user_id = u.id
            """
        else:
            query = f"SELECT * FROM {table_name}"

        df = pd.read_sql_query(query, conn)

        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])


        return df

    finally:
        conn.close()


def match_chats_to_decisions(chat_df, decisions_df):
    # Sort both dataframes by timestamp
    chat_df = chat_df.sort_values('timestamp')
    decisions_df = decisions_df.sort_values('timestamp')

    # Initialize columns to store matched decision info
    matched_decisions = []

    # For each chat, find the next decision that comes after it
    for chat_idx, chat_row in chat_df.iterrows():
        # Find decisions that occur after this chat
        subsequent_decisions = decisions_df[decisions_df['timestamp'] > chat_row['timestamp']]

        if not subsequent_decisions.empty:
            # Get the first decision after this chat
            next_decision = subsequent_decisions.iloc[0]
            matched_decisions.append(next_decision.to_dict())
        else:
            # If no subsequent decisions, match with the last decision
            matched_decisions.append(decisions_df.iloc[-1].to_dict())

    # Create a dataframe from the matched decisions
    matched_decisions_df = pd.DataFrame(matched_decisions)

    # Combine with chat dataframe
    result_df = chat_df.reset_index(drop=True).join(matched_decisions_df.reset_index(drop=True), rsuffix='_decision')

    # Calculate statistics
    # Decisions without any chats are those that don't have any chats before them (except possibly the first one)
    all_decision_times = decisions_df['timestamp'].unique()
    chat_times = chat_df['timestamp'].unique()

    # Find decisions that don't have any chats before them
    decisions_without_chats = 0
    for i, decision_time in enumerate(all_decision_times):
        if i == 0:
            # First decision can't have chats before it
            has_prior_chat = False
        else:
            # Check if there are any chats between this decision and the previous one
            prev_decision_time = all_decision_times[i-1]
            has_prior_chat = ((chat_times > prev_decision_time) & (chat_times <= decision_time)).any()

        if not has_prior_chat:
            decisions_without_chats += 1

    percentage_without_chats = (decisions_without_chats / len(decisions_df)) * 100

    # Find the last datapoint index with a chat
    if not matched_decisions:
        last_datapoint_with_chat = None
    else:
        last_datapoint_with_chat = max([d['current_datapoint_index'] for d in matched_decisions])

    return result_df, percentage_without_chats, last_datapoint_with_chat


def split_conversation_tracker(tracker):
    if not tracker:
        return []

    splits = []
    current_segment = []

    for message in tracker:
        current_segment.append(message)

        # Check if this is a bot message with actual content (not just a code call)
        if (message.get('role') == 'assistant' and
            'content' in message and
            message['content'] is not None and
            message['content'].strip()):

            # End current segment here
            splits.append(current_segment[:])  # Make a copy
            current_segment = []

    # If there's a remaining segment that doesn't end with bot content, include it
    if current_segment:
        splits.append(current_segment)

    return splits



def load_chats(path, usernames_to_remove=[], chat_mode="anmol"):
    df = extract_conversations_to_dataframe(path)
    df = df[~df['username'].isin(usernames_to_remove)]
    df["tracker"] = df["tracker_yaml"].apply(lambda x: ConversationTracker.from_yaml(x))
    df["tracker_length"] = df["tracker"].apply(lambda x: len(x))
    df = df.drop("tracker_yaml", axis=1)
    df = df[df["chat_mode"] == chat_mode]
    df.drop("chat_mode", axis=1, inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    #add two hours to the timestamp
    df['timestamp'] = df['timestamp'] + pd.Timedelta(hours=2)
    return df

def load_answers(path, current_study_mode="chat"):

    answers = pd.read_csv(path, delimiter=";",
                          names=["timestamp", "current_study_mode", "username", "current_datapoint_index",
                                 "current_datapoint_id", "datapoint_choice", "answers"])
    print(answers["current_study_mode"].unique())
    answers = answers[answers["current_study_mode"] == current_study_mode].drop("current_study_mode", axis=1)
    answers['timestamp'] = pd.to_datetime(answers['timestamp'])
    return answers

def merge(chats, answers):
    data = []
    for username in chats["username"].unique():
        sub_df = chats[chats["username"] == username]
        sub_answers = answers[answers["username"] == username]
        if sub_df.empty or sub_answers.empty:
            continue
        sub_answers['parsed'] = sub_answers['answers'].apply(ast.literal_eval)
        for q in ['q1', 'q2', 'q3']:
            sub_answers[q] = sub_answers['parsed'].apply(lambda x: next((item['answer'] for item in x if item['id'] == q), None))

        sub_answers = sub_answers.drop(['answers', 'parsed'], axis=1)
        merged_df, pct_no_chat, last_dp = match_chats_to_decisions(sub_df, sub_answers)
        temp = {"username": username,
                "chats":sub_df, "answers": sub_answers, "merged": merged_df,
                "pct_no_chat": pct_no_chat, "last_dp": last_dp}
        data.append(temp)
    return data