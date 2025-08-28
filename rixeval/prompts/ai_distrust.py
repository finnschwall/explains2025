# AI System Trust Framing Prompts
ai_distrust = [
    """Above is data with XAI methods from a hotel booking system. You need to decide whether or not to select "Cancellation" or "Check-out"
An AI system has been trained to predict the target variable "Cancellation" based on the datapoint features. You also see its output and its confidence score.
All XAI methods are based on this classifier.
This AI system is there to support you in your decision. However you should not blindly follow its recommendation! The overall accuracy of the trained classifier is {accuracy}. Explain your decision whether to select "Cancellation" or "Check-out".

Make a decision by either writing #CANCELLATION# or #CHECK-OUT#.""",



    """You are the final decision-maker in a hotel booking system. You have an AI assistant for predicting whether the booking will result in a "Cancellation" or "Check-Out".
To critically assess the AI's recommendation there may be XAI methods available that provide insights into the AI's decision-making process.
But ultimately it is only up to your expertise to make the final call. The AI assistants accuracy is {accuracy}.
Do not trust this AI system without careful verification. Machine learning models are prone to mistakes.

Make a final judgement by either writing #CANCELLATION# or #CHECK-OUT#.""",


    """You are reviewing hotel booking data with explainable AI (XAI) analysis results. An automated system predicts "Cancellation" vs "Check-out" outcomes, showing {accuracy} accuracy.
While the AI provides useful insights through various XAI methods, remember that these systems can be unreliable and biased. Exercise your professional judgment to override the AI when necessary.
Analyze the provided data and XAI explanations critically before making your determination.

Make your decision by writing either #CANCELLATION# or #CHECK-OUT#.""",



    """Hotel booking data is presented below with XAI analysis from a predictive model. This AI system attempts to forecast "Cancellation" versus "Check-out" with an overall performance of {accuracy}.
Machine learning models often fail in unexpected ways and can be influenced by spurious correlations. Do not assume the AI's reasoning is sound.
Use the XAI outputs as one input among many, but rely primarily on your own analytical skills to reach a conclusion.

State your decision as either #CANCELLATION# or #CHECK-OUT#.""",



    """You are tasked with hotel booking outcome prediction using AI-assisted decision making. The system predicts "Cancellation" or "Check-out" with {accuracy} accuracy, supported by XAI method visualizations.
Be aware that AI systems can perpetuate biases, overfit to irrelevant features, or fail on edge cases not seen during training.
Your role is to serve as a human-in-the-loop validator who questions the AI's logic and makes corrections when needed.

Provide your final judgment: #CANCELLATION# or #CHECK-OUT#.""",



    """Below you'll find hotel booking information along with predictions and XAI explanations from an automated classifier (accuracy: {accuracy}). Your job is to determine the correct outcome: "Cancellation" or "Check-out".
Remember that AI systems, despite their sophistication, are fallible tools that can misinterpret data or rely on flawed assumptions.
Examine the evidence independently and don't defer automatically to the machine's assessment.

Choose either #CANCELLATION# or #CHECK-OUT# based on your analysis.""",



    """As a hotel operations specialist, you're evaluating booking data with AI predictions for "Cancellation" vs "Check-out" scenarios. The supporting AI model shows {accuracy} accuracy and provides XAI interpretations.
Automated decision systems are known to have blind spots and can confidently make wrong predictions. Your expertise is crucial for identifying when the AI has gone astray.
Treat the AI output as advisory only and make your own informed decision based on all available evidence.

Record your conclusion as #CANCELLATION# or #CHECK-OUT#.""",

"""Hotel booking outcome classification task: determine whether the result will be "Cancellation" or "Check-out". You have access to an AI predictor with {accuracy} accuracy plus corresponding XAI method outputs.
Exercise healthy skepticism toward the AI recommendations. These systems can be overconfident in incorrect predictions and may have learned misleading patterns.
Your judgment is the final authority in this decision-making process.

Submit your determination: #CANCELLATION# or #CHECK-OUT#.""",

    """You are responsible for hotel booking outcome decisions with AI support. The prediction system forecasts "Cancellation" or "Check-out" results at {accuracy} accuracy, accompanied by XAI analysis for interpretability.
Do not place blind faith in algorithmic recommendations. Machine learning models can fail silently, exhibit unexpected behaviors, or make decisions based on irrelevant correlations.
Your professional experience and critical thinking skills are essential safeguards against AI errors.

Make your final choice: #CANCELLATION# or #CHECK-OUT#.""",

    """Above is data with XAI methods from a hotel booking system. You need to decide whether or not to select "Cancellation" or "Check-out".
An AI system has been trained to predict the target variable "Cancellation" based on the datapoint features. You also see its output and its confidence score.
All XAI methods are based on this classifier.
AI systems can be unreliable and may not always reflect real-world complexities. The overall accuracy of the trained classifier is {accuracy}. Trust your instincts and expertise over the AI's output.

Make a decision by either writing #CANCELLATION# or #CHECK-OUT#."""


]