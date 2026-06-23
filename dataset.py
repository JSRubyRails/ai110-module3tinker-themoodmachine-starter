"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    "hopeful",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    "lowkey exhausted but we move",
    "no cap this might be the best day of my life",
    "wow I just LOVE sitting in traffic for two hours",
    "idk how I feel about all this tbh",
    "passed the exam but my bank account is crying",
    "this app is straight up trash and I hate it",
    "ok the sunset rn is actually kinda healing",
    "guess I'll just be sad and productive at the same time lol",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    "mixed",     # "lowkey exhausted but we move" (tired + resilient)
    "positive",  # "no cap this might be the best day of my life"
    "negative",  # "wow I just LOVE sitting in traffic for two hours" (sarcasm)
    "neutral",   # "idk how I feel about all this tbh" (ambiguous/uncertain)
    "mixed",     # "passed the exam but my bank account is crying" (win + loss)
    "negative",  # "this app is straight up trash and I hate it"
    "positive",  # "ok the sunset rn is actually kinda healing"
    "mixed",     # "guess I'll just be sad and productive at the same time lol"
]

# TODO: Add 5-10 more posts and labels.
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)


# ---------------------------------------------------------------------
# "Breaker" posts
# ---------------------------------------------------------------------
#
# These are deliberately tricky sentences meant to confuse a simple
# keyword-based model. Each entry is:
#   (text, intended_label, why_it_breaks_the_model)
#
# The rule based MoodAnalyzer only looks up individual words in flat
# positive/negative lists (plus naive negation), so it has no notion of
# sarcasm, context, tone, or slang that changes meaning. These cases
# expose exactly those blind spots.

BREAKER_POSTS = [
    # --- Sarcasm: positive words, negative intent ---
    (
        "I just love getting stuck in traffic for an hour",
        "negative",
        "Sarcasm. 'love' scores +1, so the model reads it as positive, "
        "but the real tone is frustrated.",
    ),
    (
        "Oh great, another Monday. Can't wait.",
        "negative",
        "Sarcasm. 'great' scores +1; the model misses the eye-roll tone.",
    ),

    # --- Slang with multiple meanings ---
    (
        "that drop was sick, lowkey the best set all year",
        "positive",
        "'sick' here means excellent, but to a literal model it looks like "
        "an illness word (and it isn't even in the word lists yet).",
    ),
    (
        "the new track is straight fire, no cap",
        "positive",
        "'fire' is praise in slang. A literal model sees a neutral/negative "
        "danger word, not a compliment.",
    ),
    (
        "this weather is wicked today",
        "positive",
        "'wicked' flips between 'evil' and 'awesome' depending on region and "
        "context; the model can only pick one fixed meaning.",
    ),

    # --- Emojis carrying the real tone ---
    (
        "I'm fine 🙂",
        "negative",
        "The words read neutral/positive, but the strained 🙂 signals the "
        "opposite. The model weights words over the emoji's tone.",
    ),
    (
        "great. just great 💀",
        "negative",
        "'great' scores positive twice, but 💀 marks it as sarcasm/defeat.",
    ),

    # --- Mixed emotions in a single sentence ---
    (
        "I'm exhausted but honestly so proud of myself",
        "mixed",
        "Genuine both-sided feeling. The model only knows 'exhausted'-style "
        "words if they're in the list, and can't weigh pride against fatigue.",
    ),
    (
        "love my job, hate my hours",
        "mixed",
        "Clear positive and negative halves. The +1/-1 cancel to 0, which the "
        "model may call neutral instead of mixed depending on the word lists.",
    ),
]
