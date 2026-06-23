# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

You may complete this model card for whichever version you used, or compare both if you explored them.

## 1. Model Overview

**Model type:**  
Describe whether you used the rule based model, the ML model, or both.  
Example: “I used the rule based model only” or “I compared both models.”

- I compared both models.

**Intended purpose:**  
What is this model trying to do?  
Example: classify short text messages as moods like positive, negative, neutral, or mixed.

- Classify short social-media style posts as positive, negative, neutral, or mixed

**How it works (brief):**  
For the rule based version, describe the scoring rules you created.  
For the ML version, describe how training works at a high level (no math needed).


- Rule-based tokenizes text, scores +1/−1 per sentiment word, handles negation and sarcasm, then maps the score to a label. ML converts posts to bag-of-words counts and fits logistic regression to learn word→label associations.



## 2. Data

**Dataset description:**  
Summarize how many posts are in `SAMPLE_POSTS` and how you added new ones.


- 6 posts were originally in `SAMPLE_POSTS` before I added 8 new posts. I created the new posts based on a separate `BREAKER_POSTS` I created that deals with tricky cases 


**Labeling process:**  
Explain how you chose labels for your new examples.  
Mention any posts that were hard to label or could have multiple valid labels.


- Labels were based on its intended tone, where sentences such as "idk how I feel" or "passed the exam but my bank account is crying" can be interpreted as neutral or mixed

**Important characteristics of your dataset:**  
Examples you might include:  

- Contains slang or emojis  
- Includes sarcasm  
- Some posts express mixed feelings  
- Contains short or ambiguous messages


- The dataset contains slang such as "no cap" and "lowkey", emojis, sarcasm, and mixed-emotion posts 

**Possible issues with the dataset:**  
Think about imbalance, ambiguity, or missing kinds of language.

- The dataset is very small (only has 14 rows), and lots of slang that isn't covered in the word lists 

## 3. How the Rule Based Model Works (if used)

**Your scoring rules:**  
Describe the modeling choices you made.  
Examples:  

- How positive and negative words affect score  
- Negation rules you added  
- Weighted words  
- Emoji handling  
- Threshold decisions for labels


- ±1 per matched word; negation flips the next ~3 words ("not happy" → negative); sarcasm cues invert the score; mixed when both sides present and the absolute value of score  ≤ 1. 

**Strengths of this approach:**  
Where does it behave predictably or reasonably well?

- The scoring rule is fully transparent as you can see exactly why each prediction happend and its reasoning 

**Weaknesses of this approach:**  
Where does it fail?  
Examples: sarcasm, subtlety, mixed moods, unfamiliar slang.


- It fails at words that isn't in the vocabulary and fails at some aspects of slang

## 4. How the ML Model Works (if used)

**Features used:**  
Describe the representation.  
Example: “Bag of words using CountVectorizer.”

**Training data:**  
State that the model trained on `SAMPLE_POSTS` and `TRUE_LABELS`.

**Training behavior:**  
Did you observe changes in accuracy when you added more examples or changed labels?

**Strengths and weaknesses:**  
Strengths might include learning patterns automatically.  
Weaknesses might include overfitting to the training data or picking up spurious cues.

## 5. Evaluation

**How you evaluated the model:**  
Both versions can be evaluated on the labeled posts in `dataset.py`.  
Describe what accuracy you observed.

- Both models were evaluated based on the labeled posts. Rule-based was 9/14 while the ML is 14/14

**Examples of correct predictions:**  
Provide 2 or 3 examples and explain why they were correct.

- "I love this class so much" is correct as positive and "wow I just LOVE sitting in traffic for two hours" is correct as negative due to the sarcasm detected 

**Examples of incorrect predictions:**  
Provide 2 or 3 examples and explain why the model made a mistake.  
If you used both models, show how their failures differed.

- "Lowkey exhausted but we move" and "the best day of my life" is incorrectly neutral because it has unknown words

## 6. Limitations

Describe the most important limitations.  
Examples:  

- The dataset is small  
- The model does not generalize to longer posts  
- It cannot detect sarcasm reliably  
- It depends heavily on the words you chose or labeled

- The dataset is small, it can't reliably detect sarcasm or unfamiliar slang, and the rule-based depends on the word list that I choose 

## 7. Ethical Considerations

Discuss any potential impacts of using mood detection in real applications.  
Examples: 

- Misclassifying a message expressing distress  
- Misinterpreting mood for certain language communities  
- Privacy considerations if analyzing personal messages

- Slang and dialect differences mean the model may work worse for some communities, and misreading a distress mesage as neutral or positive is harmful 

## 8. Ideas for Improvement

List ways to improve either model.  
Possible directions:  

- Add more labeled data  
- Use TF IDF instead of CountVectorizer  
- Add better preprocessing for emojis or slang  
- Use a small neural network or transformer model  
- Improve the rule based scoring method  
- Add a real test set instead of training accuracy only


- The model could be improved by adding more labeled data, and doing a better job of handling emoji and slang