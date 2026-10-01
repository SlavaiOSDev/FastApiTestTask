from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AnalyzeBody(BaseModel): 
    words: list[str]

class AnalyzeResponse(BaseModel):
    total: int
    unique: int
    words: list[str]
    frequency: dict[str, int]
    by_length: dict[int, list[str]]
    most_frequent: list[str]

@app.post("/analyze", response_model = AnalyzeResponse)
async def analyze(body: AnalyzeBody):
   normalized_words: list[str] = normalize_words(body.words)
   return analyze_words(normalized_words)

def normalize_words(arr: list[str]):
    '''
    Удаляет проблеы
    Приводит к нижнему регистру
    Возвращает не пустые строки
    '''
    return [stripped.lower() for word in arr if (stripped := word.strip())]

def analyze_words(arr: list[str]):

    total = len(arr)
    unique_list = set(arr)
    unique = len(unique_list)
    words = sorted(unique_list)
    frequency = analyze_frequency(arr)
    by_length = analyze_by_length(arr)
    most_frequent = analyze_most_frequent(frequency)

    return {
        "total": total,
        "unique": unique,
        "words": words,
        "frequency": frequency,
        "by_length": by_length,
        "most_frequent": most_frequent
    }

def analyze_frequency(arr: list[str]):
    frequency: dict[str, int] = {}

    for word in arr: 
        frequency[word] = frequency.setdefault(word, 0) + 1

    return frequency

def analyze_by_length(arr: list[str]):
    by_length: dict[int, list[str]] = {}

    for word in arr: 
        by_length.setdefault(len(word), []).append(word)

    for value in by_length.values():
        value[:] = sorted(set(value))

    return by_length

def analyze_most_frequent(frequency:  dict[str, int]):
    if not frequency:
        return []

    max_count = max(frequency.values())
    return sorted([key for key, value in frequency.items() if value == max_count])




# total — количество слов после очистки, включая повторения;
# unique — количество уникальных слов;
# words — уникальные слова, отсортированные по алфавиту;
# frequency — сколько раз встречается каждое слово;
# by_length — уникальные слова, сгруппированные по длине. Внутри каждой группы слова должны быть отсортированы;
# most_frequent — все слова с максимальным количеством повторений, отсортированные по алфавиту.