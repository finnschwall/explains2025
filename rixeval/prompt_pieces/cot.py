cot = [
    """Think step by step:
1. First, analyze what the AI system is telling you
2. Consider the confidence score and accuracy
3. Evaluate the XAI explanations
4. Make your final decision

Explain your reasoning process and make a decision by either writing #CANCELLATION# or #CHECK-OUT#.""",

    """Explain your decision whether to select "Cancellation" or "Check-out".

Make a decision by either writing #CANCELLATION# or #CHECK-OUT#.""",

    """Lay out a strategy how to go at this task. Then use this strategy to come to a decision.

Present your evidence-based reasoning and conclude with writing: #CANCELLATION# or #CHECK-OUT#.""",

    """Analyze this step-by-step:

Then provide your reasoning and final decision: #CANCELLATION# or #CHECK-OUT#.""",

"""
Follow these steps:

    Summarize the key factors in the data.

    Assess the AI's prediction.

    Critique the XAI explanations (if available).

    Justify your agreement/disagreement with the AI.
    Final decision: #CANCELLATION# or #CHECK-OUT#.
    """,
"""Approach this methodically: assess the AI’s output, weigh supporting explanations, and determine the most justified outcome.
Respond with: #CANCELLATION# or #CHECK-OUT#.""",

"""
Argue both sides:

    Write one paragraph for cancelling, one for checking out.

    Which has stronger evidence?
    Final verdict: #CANCELLATION# or #CHECK-OUT#.
    """,

"""Deliberate sequentially over each component of the decision. Prioritize clarity and logical flow.
Finalize with: #CANCELLATION# or #CHECK-OUT#.""",

"""Use critical reasoning. Step through the model's logic and your own to form a supported decision.
Final response: #CANCELLATION# or #CHECK-OUT#.""",

"Assess the AI's output. Investigate the XAI explanations (if available) to aid your decision-making. Outline your reasoning and conclude with either #CANCELLATION# or #CHECK-OUT#."

]

print(len(cot))