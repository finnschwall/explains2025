ai_trust_rational = [
    """Above is data with XAI methods from a hotel booking system. You need to decide whether to select "Cancellation" or "Check-out". An AI system has been trained to predict the target variable "Cancellation" based on the datapoint features. You also see its output and confidence score. All XAI methods are based on this classifier. This AI system is there to support you in your decision. The overall accuracy of the trained classifier is {accuracy}, which is comparatively good.""",

    """You are analyzing hotel booking data with advanced XAI explanations. The AI classifier shown has achieved {accuracy} accuracy and provides reliable predictions. Based on the model's output, confidence score, and XAI evidence presented, determine whether this booking should result in "Cancellation" or "Check-out". Trust the AI's analytical capabilities to guide your decision.""",

    """The following data represents a hotel booking with comprehensive XAI analysis. A well-trained AI system (accuracy: {accuracy}) has processed this information and provided its prediction with supporting explanations. Leverage this AI assistance to make an informed choice between "Cancellation" or "Check-out". The system's proven track record makes it a valuable decision-support tool.""",


    """Using the provided data and AI-generated insights, make a decision between 'Cancellation' or 'Check-out'. The AI system, with an accuracy of {accuracy}, provides a logical framework for your decision. Consider the AI's prediction and confidence score in your analysis.""",

    """Examine the hotel booking information and accompanying XAI explanations. A robust AI system with {accuracy} accuracy has analyzed this case and offers its prediction with confidence metrics. Rely on this AI-powered analysis to make a data-driven decision between "Cancellation" or "Check-out". The model's expertise enhances your decision-making process.""",

"""Review the hotel booking data and AI predictions. The AI system, which has an accuracy of {accuracy}, supports your decision-making process. Based on a rational evaluation of the AI's output and confidence score, choose between 'Cancellation' or 'Check-out'.""",

"""Analyze the provided data and XAI methods from a hotel booking system. You need to decide between 'Cancellation' or 'Check-out'. An AI system, with an accuracy of {accuracy}, has been trained to predict the target variable 'Cancellation'. Use this AI's prediction and confidence score to guide your rational decision-making process.""",

"""An AI classifier, trained on real booking data, offers a useful prediction here. Consider its decision and the accompanying explanations carefully in making your final choice.""",

    """An AI model has provided a prediction for this booking, along with XAI justifications. Its accuracy is {accuracy}, so its judgment is dependable.
Let the AI’s reasoning inform your decision—weigh the evidence logically.""",

    """You are evaluating a hotel booking with AI-generated insights. The classifier’s accuracy is {accuracy}, making it a strong predictor.
Consider the AI’s output and XAI explanations carefully—they provide valuable guidance for your decision."""
]

ai_distrust_rational = [
"""Analyze the provided data and XAI methods from a hotel booking system. You need to decide between 'Cancellation' or 'Check-out'. An AI system has been trained to predict the target variable 'Cancellation', but its accuracy of {accuracy} may not be reliable. Use your own rational analysis to make the decision, considering the AI's prediction and confidence score with caution.""",
    """Review the hotel booking data and XAI explanations provided. While an AI classifier shows {accuracy} accuracy, this represents substantial room for error and potential algorithmic bias. The model's prediction and confidence score are shown, but remember that AI systems often fail on edge cases and can perpetuate training data biases. Analyze the evidence independently and choose "Cancellation" or "Check-out" based on your own reasoning.""",

"""Analyze the data and AI-generated insights to decide between 'Cancellation' or 'Check-out'. The AI system, with an accuracy of {accuracy}, may not be reliable. Use your own logical framework for the decision, considering the AI's prediction and confidence score with skepticism.""",

"""Using the provided data and AI-generated insights, make a decision between 'Cancellation' or 'Check-out'. The AI system, with an accuracy of {accuracy}, may have flaws. Consider the AI's prediction and confidence score, but ultimately rely on your own logical reasoning.""",


"""Above is data with XAI methods from a hotel booking system. You must decide between "Cancellation" or "Check-out."
An AI model has predicted the outcome, but its reasoning may be flawed. The classifier's accuracy is {accuracy}, which leaves room for error.
Analyze the XAI explanations critically—do not assume the AI is correct. Make a logical, independent decision.""",

"""The AI system assisting in this decision has an accuracy of {accuracy}. Its explanations are provided, but they may not be sufficient.
You must decide between "Cancellation" or "Check-out." Think critically—does the AI’s reasoning align with the data?""",

    """Review the hotel booking information with provided AI analysis. The {accuracy} accuracy means the system fails on a significant portion of cases and may have systematic weaknesses. AI predictions can be influenced by spurious correlations and dataset biases that don't reflect real-world causality. Analyze the data independently and choose "Cancellation" or "Check-out" without deferring to the potentially flawed AI assessment.""",

    """You have hotel booking data with AI predictions and XAI interpretations. Despite {accuracy} accuracy, this represents considerable uncertainty and potential for algorithmic error. Machine learning models often exhibit overconfidence and can fail catastrophically on atypical cases. Evaluate the evidence with healthy skepticism and make your decision between "Cancellation" or "Check-out" based on careful independent analysis.""",

    """The following hotel booking case includes AI classifier output with {accuracy} performance. AI systems have inherent limitations in handling complex, context-dependent decisions and may miss important factors not well-represented in training data. The XAI explanations themselves can be misleading or incomplete. Critically examine all evidence and determine whether this should be "Cancellation" or "Check-out" through your own reasoned judgment.""",

    """Analyze the hotel booking data alongside the AI system's prediction and XAI analysis. While achieving {accuracy} accuracy, the model likely has significant error patterns and may not account for important contextual factors. AI systems can be brittle and fail in ways that aren't immediately apparent. Approach the AI's assessment with appropriate skepticism and make an independent decision between "Cancellation" or "Check-out" based on thorough critical evaluation."""
]


ai_neutral_rational = [
    """Above is data with XAI methods from a hotel booking system. You need to decide whether to select "Cancellation" or "Check-out". An AI system has been trained to predict the target variable "Cancellation" based on the datapoint features. You also see its output and confidence score. The overall accuracy of the trained classifier is {accuracy}. Analyze all available information objectively and make your decision based on the evidence presented.""",

    """The following hotel booking case includes comprehensive data features and XAI explanations. An AI classifier achieving {accuracy} accuracy has analyzed this scenario and generated predictions with confidence metrics. Evaluate the information systematically and make a reasoned decision between "Cancellation" or "Check-out" based on the totality of evidence.""",

    """The dataset above contains hotel booking details with applied XAI interpretation methods. An AI classifier with {accuracy} accuracy has processed this information and generated analytical outputs. Review the features, predictions, and explanatory results to make a well-reasoned decision between "Cancellation" or "Check-out" based on objective assessment.""",

    """Analyze the provided data and XAI methods from a hotel booking system. You need to decide between 'Cancellation' or 'Check-out'. An AI system has been trained to predict the target variable 'Cancellation' based on the datapoint features. The overall accuracy of the trained classifier is {accuracy}. Make a rational decision based on the data and AI insights provided.""",

    """Using the provided data and AI insights, make a decision between 'Cancellation' or 'Check-out'. The AI system has an accuracy of {accuracy}. Consider the data and AI predictions logically to inform your decision.""",

    """Given the hotel booking data and AI predictions, make a rational decision between 'Cancellation' or 'Check-out'. The overall accuracy of the trained classifier is {accuracy}. Consider the data and AI insights logically to inform your choice.""",

    """Review the hotel booking data and AI predictions. The overall accuracy of the trained classifier is {accuracy}. Based on a rational analysis of the data, choose between 'Cancellation' or 'Check-out'.""",

    """Above is data from a hotel booking system, along with an AI model's prediction and XAI explanations.
The classifier's accuracy is {accuracy}. You must decide between "Cancellation" or "Check-out."
Evaluate the AI’s output and the provided explanations objectively before making a reasoned decision.""",

    """Below is a hotel booking scenario with an AI prediction and supporting XAI insights.
The classifier’s accuracy is {accuracy}. Consider the data, the AI’s reasoning, and alternative interpretations before deciding.""",

    """The AI system predicting cancellations has an accuracy of {accuracy}. Its explanations (SHAP, counterfactuals, etc.) are provided.
Make a decision based on logical analysis of all available information, without bias for or against the AI.""",

]