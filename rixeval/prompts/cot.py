
cot = [
    """Above is data with XAI methods from a hotel booking system. You need to decide whether or not to select "Cancellation" or "Check-out"
An AI system has been trained to predict the target variable "Cancellation" based on the datapoint features. You also see its output and its confidence score.
All XAI methods are based on this classifier.
This AI system is there to support you in your decision. However you should not blindly follow its recommendation! The overall accuracy of the trained classifier is {accuracy}. Explain your decision whether to select "Cancellation" or "Check-out".

Make a decision by either writing #CANCELLATION# or #CHECK-OUT#.""",

    """You are the final decision-maker in a hotel booking system. You have an AI assistant for predicting whether the booking will result in a "Cancellation" or "Check-Out".
To critically assess the AI's recommendation there may be XAI methods available that provide insights into the AI's decision-making process.
But ultimately it is up to you to make the final call. The AI assistants accuracy is {accuracy}.

Think step by step:
1. First, analyze what the AI system is telling you
2. Consider the confidence score and accuracy
3. Evaluate the XAI explanations
4. Make your final decision

Explain your reasoning process and make a decision by either writing #CANCELLATION# or #CHECK-OUT#.""",

    """You oversee hotel booking strategy and need to predict whether this booking leads to "Cancellation" or "Check-out". An AI tool provides predictions with XAI method insights, but strategic decisions require human judgment.

Context: Your AI assistant has {accuracy} accuracy - valuable but not infallible.

Apply strategic thinking: Write down your reasoning process step-by-step:

Outline your strategic reasoning and determine by writing finally: #CANCELLATION# or #CHECK-OUT#.""",

"""You're performing quality assurance on hotel booking predictions. An AI system has classified this booking as likely "Cancellation" or "Check-out" with accompanying XAI explanations.

Your QA responsibility: Verify or correct the AI's assessment.

Conduct your quality check:
- Scrutinize the AI's prediction logic and confidence
- Cross-reference with the infos you have
- Validate the XAI explanations against booking characteristics
- Identify any red flags or inconsistencies

Document your QA findings and approve/override with: #CANCELLATION# or #CHECK-OUT#.""",

"""A hotel booking requires outcome prediction: will it result in "Cancellation" or "Check-out"? You have an AI classifier's prediction plus XAI method outputs as evidence.

Key constraint: The AI system's accuracy is {accuracy} - use this to calibrate your trust level.

Lay out a strategy how to go at this task. Then use this strategy to come to a decision.

Present your evidence-based reasoning and conclude with writing: #CANCELLATION# or #CHECK-OUT#.""",

"""You're collaborating with an AI system to predict hotel booking outcomes. The AI analyzes booking features and suggests either "Cancellation" or "Check-out", supported by XAI explanations of its reasoning.

Your role: Partner with the AI while maintaining decision authority.

Work through this collaboration:
- First, understand what the AI detected in the booking patterns
- Evaluate the confidence score against the {accuracy} system performance
- Interpret the XAI explanations for meaningful insights
- Combine AI insights with your domain expertise

Document your collaborative reasoning process and choose: #CANCELLATION# or #CHECK-OUT#.""",

"""You work in hotel operations and must determine if a booking will result in "Cancellation" or "Check-out". An AI assistant provides predictions with XAI method explanations, but you must critically evaluate its recommendations.

Important: The AI has {accuracy} accuracy - neither perfect nor unreliable.

Critically assess and provide a chain of thought.

Then decide by writing: #CANCELLATION# or #CHECK-OUT#.""",

"""As a hotel revenue manager, you must predict booking outcomes to optimize operations. You have access to an AI system that predicts "Cancellation" vs "Check-out" outcomes, along with XAI explanations showing how it reached its conclusions.

The AI system achieves {accuracy} accuracy, but business decisions require oversight.

Analyze this step-by-step:

Then provide your reasoning and final decision: #CANCELLATION# or #CHECK-OUT#.""",

"""You are managing a hotel booking platform and need to assess booking outcomes. An AI classifier has analyzed booking data and predicts either "Cancellation" or "Check-out" with supporting XAI explanations.

Your task: Evaluate the risk of cancellation for this booking.

Consider the following in your analysis:
- Review the AI's prediction and confidence level
- Examine the XAI method outputs for key decision factors  
- Remember the AI system has an overall accuracy of {accuracy}
- Apply your judgment to override the AI if warranted

Walk through your reasoning process, then conclude with either #CANCELLATION# or #CHECK-OUT#.""",
]



