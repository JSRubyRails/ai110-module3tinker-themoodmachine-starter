# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import re
from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


# Text emoticons we keep as single tokens so punctuation removal doesn't destroy them.
EMOTICONS = {":)", ":-)", ":(", ":-(", ":d", ":'(", ":/", ";)", "<3"}

# Words that flip the sentiment of the words that follow them.
NEGATIONS = {"not", "no", "never", "dont", "cant", "wont", "isnt", "aint"}

# Shallow sarcasm signals. When one of these appears, the literal sentiment of
# a short post is usually the OPPOSITE of what's intended ("I just love
# traffic"), so we invert the score. This catches marked sarcasm only; deadpan
# sarcasm with no cue ("Great service.") is out of reach for a rule based model.
SARCASM_EMOJIS = {"🙃", "🙄", "💀"}
SARCASM_CUE_PHRASES = {
    "yeah right",
    "oh great",
    "oh wonderful",
    "oh joy",
    "just love",
    "just great",
    "cant wait",
    "thanks a lot",
    "so much fun",
    "how lovely",
    "love getting",
    "love sitting",
    "love waiting",
    "love being",
}

# Unicode ranges covering most common emoji.
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001FAFF"  # symbols, pictographs, emoticons, supplemental
    "\U00002600-\U000027BF"  # misc symbols + dingbats
    "\U0001F1E6-\U0001F1FF"  # regional indicators (flags)
    "]"
)


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        TODO: Improve this method.

        Right now, it does the minimum:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Splits on spaces

        Ideas to improve:
          - Remove punctuation
          - Handle simple emojis separately (":)", ":-(", "🥲", "😂")
          - Normalize repeated characters ("soooo" -> "soo")
        """
        cleaned = text.strip().lower()

        # Put spaces around emoji so each one becomes its own token.
        cleaned = EMOJI_PATTERN.sub(r" \g<0> ", cleaned)

        tokens: List[str] = []
        for chunk in cleaned.split():
            # 1. Keep recognized text emoticons intact (":)", ":(").
            if chunk in EMOTICONS:
                tokens.append(chunk)
                continue

            # 2. Keep emoji as standalone tokens.
            if EMOJI_PATTERN.fullmatch(chunk):
                tokens.append(chunk)
                continue

            # 3. Strip surrounding punctuation, keeping letters, digits, apostrophes.
            word = re.sub(r"[^a-z0-9']", "", chunk)
            if not word:
                continue

            # 4. Normalize long runs of a repeated letter ("soooo" -> "soo").
            word = re.sub(r"(.)\1{2,}", r"\1\1", word)

            tokens.append(word)

        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.

        TODO: You must choose AT LEAST ONE modeling improvement to implement.
        For example:
          - Handle simple negation such as "not happy" or "not bad"
          - Count how many times each word appears instead of just presence
          - Give some words higher weights than others (for example "hate" < "annoyed")
          - Treat emojis or slang (":)", "lol", "💀") as strong signals
        """
        tokens = self.preprocess(text)

        score = 0
        # When > 0, the next few sentiment words have their meaning flipped.
        # This is the intentional enhancement: simple negation handling so that
        # "not happy" counts as negative and "not bad" counts as positive.
        negation_window = 0

        for token in tokens:
            if token in NEGATIONS:
                negation_window = 3  # affect the next few tokens
                continue

            value = 0
            if token in self.positive_words:
                value = 1
            elif token in self.negative_words:
                value = -1

            if value != 0 and negation_window > 0:
                value = -value

            score += value

            if negation_window > 0:
                negation_window -= 1

        # Sarcasm handling: if the post carries a common sarcasm marker, the
        # literal sentiment is usually inverted, so flip the score.
        if self._has_sarcasm_cue(tokens):
            score = -score

        return score

    def _has_sarcasm_cue(self, tokens: List[str]) -> bool:
        """
        Return True if the tokens contain a shallow sarcasm signal.

        Two kinds of cues:
          - Emoji cues (🙃, 🙄, 💀) appear as their own tokens.
          - Phrase cues ("yeah right", "oh great") are matched against the
            token stream with apostrophes removed so "can't" -> "cant".
        """
        if any(t in SARCASM_EMOJIS for t in tokens):
            return True

        joined = " ".join(t.replace("'", "") for t in tokens)
        return any(cue in joined for cue in SARCASM_CUE_PHRASES)

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        The default mapping is:
          - score > 0  -> "positive"
          - score < 0  -> "negative"
          - score == 0 -> "neutral"

        TODO: You can adjust this mapping if it makes sense for your model.
        For example:
          - Use different thresholds (for example score >= 2 to be "positive")
          - Add a "mixed" label for scores close to zero
        Just remember that whatever labels you return should match the labels
        you use in TRUE_LABELS in dataset.py if you care about accuracy.
        """
        score = self.score_text(text)

        # Look at the raw signals too. The net score alone can't tell apart
        # "neutral" (no sentiment words at all) from "mixed" (both positive and
        # negative words present that roughly cancel out).
        tokens = self.preprocess(text)
        has_positive = any(t in self.positive_words for t in tokens)
        has_negative = any(t in self.negative_words for t in tokens)

        # Mixed: genuine sentiment on both sides that stays close to zero.
        if has_positive and has_negative and abs(score) <= 1:
            return "mixed"

        if score > 0:
            return "positive"
        if score < 0:
            return "negative"
        return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        tokens = self.preprocess(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = 0

        for token in tokens:
            if token in self.positive_words:
                positive_hits.append(token)
                score += 1
            if token in self.negative_words:
                negative_hits.append(token)
                score -= 1

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )


# ---------------------------------------------------------------------
# Quick check: run `python3 mood_analyzer.py` to confirm tokenization.
# ---------------------------------------------------------------------

if __name__ == "__main__":
    analyzer = MoodAnalyzer()
    examples = [
        "I LOVE this!!!",
        "soooo tired :(",
        "  Mixed   spacing   here  ",
        "ok the sunset rn is actually kinda healing ✨",
        "no cap this is the best 😂😂",
    ]
    for text in examples:
        print(f"{text!r} -> {analyzer.preprocess(text)}")
