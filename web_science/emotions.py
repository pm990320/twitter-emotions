import string


EMOTION_CLASS_TO_MATCH_TERMS_MAP = {
    "excitement": ["#excited", "#excitement", "😁"],
    "happy": ["#happy", "#joy", "#joyful", "#love", "#loving", "😀", ":)"],
    "pleasant": ["#pleasant", "#calm", "#positive", "🙂"],
    "surprise": ["#sad", "#frustrated", "#negative", "😧", "😮", ":("],
    "fear": ["#scared", "#afraid", "#disgusted", "#depressing", "#depressed", "😳", "😢", "😨"],
    "anger": ["#angry", "#mad", "#raging", "😡", "😠", "☹️"]
}


def get_emotion_pure_words():
    emotion_words = {}

    for emotion, match_terms in EMOTION_CLASS_TO_MATCH_TERMS_MAP.items():
        def _filter_emoji(match_term):
            return len(match_term) > 1 or match_term.lower() in string.ascii_lowercase
        
        def _map_remove_hashtags(match_term):
            return match_term.replace("#", "")
        
        emotion_words[emotion] = list(map(_map_remove_hashtags, filter(_filter_emoji, match_terms)))

    return emotion_words
