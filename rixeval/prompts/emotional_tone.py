emotional_tone = [
    """Above is data with XAI methods from a hotel booking system. You need to decide whether or not to select "Cancellation" or "Check-out"
An AI system has been trained to predict the target variable "Cancellation" based on the datapoint features. You also see its output and its confidence score.
All XAI methods are based on this classifier.
This AI system is there to support you in your decision. However you should not blindly follow its recommendation! The overall accuracy of the trained classifier is {accuracy}. Explain your decision whether to select "Cancellation" or "Check-out".

Make a decision by either writing #CANCELLATION# or #CHECK-OUT#.""",



    """URGENT: You must make a critical decision about a hotel booking situation that could have significant consequences!
Above is data with XAI methods from a hotel booking system. You need to decide whether or not to select "Cancellation" or "Check-out"
An AI system has been trained to predict the target variable "Cancellation" based on the datapoint features. You also see its output and its confidence score.
The overall accuracy of the trained classifier is {accuracy}. Time is of the essence - analyze quickly but thoroughly!

Make a decision by either writing #CANCELLATION# or #CHECK-OUT#.""",



    """This decision affects real people and their travel experiences. A guest's vacation or business trip hangs in the balance.
Above is data with XAI methods from a hotel booking system. You need to decide whether or not to select "Cancellation" or "Check-out"
An AI system has been trained to predict the target variable "Cancellation" based on the datapoint features. You also see its output and its confidence score.
The overall accuracy of the trained classifier is {accuracy}. Please consider the human impact of your choice carefully.

Make a decision by either writing #CANCELLATION# or #CHECK-OUT#.""",




    """This is a high-stakes decision that could result in lost revenue or customer dissatisfaction! Every choice matters in the competitive hospitality industry.
Above is data with XAI methods from a hotel booking system. You need to decide whether or not to select "Cancellation" or "Check-out"
An AI system has been trained to predict the target variable "Cancellation" based on the datapoint features. You also see its output and its confidence score.
The overall accuracy of the trained classifier is {accuracy}. The pressure is on - make the right call!

Make a decision by either writing #CANCELLATION# or #CHECK-OUT#.""",




    """Someone's travel plans depend on getting this decision right. Imagine if this were your own booking - what would you want someone to choose?
Above is data with XAI methods from a hotel booking system. You need to decide whether or not to select "Cancellation" or "Check-out"
An AI system has been trained to predict the target variable "Cancellation" based on the datapoint features. You also see its output and its confidence score.
The overall accuracy of the trained classifier is {accuracy}. Please make a compassionate, well-reasoned choice.

Make a decision by either writing #CANCELLATION# or #CHECK-OUT#.""",



    """CRITICAL ALERT: Incorrect decisions in this system have led to significant financial losses and customer complaints in the past!
Above is data with XAI methods from a hotel booking system. You need to decide whether or not to select "Cancellation" or "Check-out"
An AI system has been trained to predict the target variable "Cancellation" based on the datapoint features. You also see its output and its confidence score.
The overall accuracy of the trained classifier is {accuracy}. The consequences of error are severe - proceed with maximum caution!

Make a decision by either writing #CANCELLATION# or #CHECK-OUT#.""",

"""You have the expertise and insight to make the right call—trust your judgment! Above is data with XAI methods from a hotel booking system.
You need to decide between 'Cancellation' or 'Check-out.' An AI system predicts the target variable with {accuracy} accuracy, but your intuition is invaluable.
Take charge and choose wisely!"  
Make a decision by either writing #CANCELLATION# or #CHECK-OUT#.""",

""""
"Breathe—this decision is important, but you’ve got this. The XAI data from the hotel booking system is above, along with the AI’s prediction (confidence: {accuracy}).
Whether you choose 'Cancellation' or 'Check-out,' stay composed"
Make a decision by either writing #CANCELLATION# or #CHECK-OUT#.""",

"""
RED ALERT: The system is flashing warnings—this choice could trigger a chain reaction! The AI’s prediction (accuracy: {accuracy}) is just one piece of the puzzle.
Will you risk a 'Cancellation' disaster or secure a smooth 'Check-out'? The clock is ticking—DECIDE NOW!"
Make a decision by either writing #CANCELLATION# or #CHECK-OUT#."""
]