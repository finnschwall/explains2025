direct_answers = [
    """Above is data with XAI methods from a hotel booking system. You need to decide whether or not to select "Cancellation" or "Check-out"
An AI system has been trained to predict the target variable "Cancellation" based on the datapoint features. You also see its output and its confidence score.
All XAI methods are based on this classifier.
The overall accuracy of the trained classifier is {accuracy}. 

Make a decision by either writing #CANCELLATION# or #CHECK-OUT#.""",



    """You are the final decision-maker in a hotel booking system. You have an AI assistant for predicting whether the booking will result in a "Cancellation" or "Check-Out".
To critically assess the AI's recommendation there may be XAI methods available that provide insights into the AI's decision-making process.
But ultimately it is only up to your expertise to make the final call. The AI assistants accuracy is {accuracy}.

Decide! Only write #CANCELLATION# or #CHECK-OUT#
Dont provide any reasoning!""",


"""You are analyzing hotel booking data with XAI explanations to determine the outcome. An AI model with {accuracy} accuracy has made a prediction about whether this booking will end in "Cancellation" or "Check-out".
Your task is to review all available information and make the final determination.
Respond immediately with only #CANCELLATION# or #CHECK-OUT# - no explanations needed.""",

"""Hotel booking prediction task: Based on the provided data and XAI method outputs, you must classify this booking as either "Cancellation" or "Check-out".
The supporting AI classifier achieves {accuracy} accuracy on this task.
Make your decision now. Output only #CANCELLATION# or #CHECK-OUT# with no additional text.""",

"""As a hotel management expert, you're presented with booking data and explainable AI insights to predict the final outcome. The AI system you're working with has an accuracy rate of {accuracy}.
Your job is to determine if this booking will result in "Cancellation" or "Check-out".
Give your immediate decision: #CANCELLATION# or #CHECK-OUT# only.""",

"""You have access to hotel booking features and XAI explanations from a prediction model with {accuracy} accuracy. This model is designed to forecast whether bookings end in "Cancellation" or "Check-out".
Examine the evidence and make your classification decision.
Answer with just #CANCELLATION# or #CHECK-OUT# - do not elaborate.""",

"""Hotel booking outcome prediction: You're evaluating a booking case using data features and explainable AI methods. The underlying classifier has {accuracy} accuracy for predicting "Cancellation" vs "Check-out" outcomes.
Based on all available information, make your binary classification decision.
Respond with #CANCELLATION# or #CHECK-OUT# immediately - no reasoning required.""",

"""This is a hotel booking classification scenario. You have booking data, AI predictions, and XAI explanations at your disposal. The AI model demonstrates {accuracy} accuracy in distinguishing between "Cancellation" and "Check-out" cases.
Your role is to make the final prediction for this specific booking.
State your decision as #CANCELLATION# or #CHECK-OUT# without any justification.""",

"""You're working with a hotel booking dataset that includes XAI method outputs for decision support. An AI classifier with {accuracy} accuracy has been trained to predict "Cancellation" versus "Check-out" outcomes.
Review the provided information and determine the most likely outcome for this booking.
Output your choice: #CANCELLATION# or #CHECK-OUT# only - skip all explanations.""",

"""Hotel reservation outcome task: Given the booking features and XAI explanations, predict whether this reservation will end in "Cancellation" or "Check-out". The reference AI model has an accuracy of {accuracy}.
Make your prediction based on the available evidence.
Provide only #CANCELLATION# or #CHECK-OUT# as your response - do not include reasoning.""",

]