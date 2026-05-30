from collections import Counter

class JobTextAnalytics:
    def __init__(self):
        pass

    def get_top_keywords(self, documents: list[str], top_n: int = 10) -> list[tuple[str, int]]:
        if not documents:
            return []
            
        all_words = []
        for doc in documents:
            if doc:
                words = [word.lower() for word in doc.split() if len(word) > 1]
                all_words.extend(words)
                
        counter = Counter(all_words)
        return counter.most_common(top_n)