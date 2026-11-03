from dotenv import load_dotenv
load_dotenv()

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from sklearn.metrics.pairwise import cosine_similarity
from google import genai

EMBEDDING_MODEL = "gemini-embedding-001"

client = genai.Client()

loader = UnstructuredMarkdownLoader("hotel_info.md")

docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=250,
    chunk_overlap=40,
)

chunks = splitter.split_documents(docs)

texts = [chunk.page_content for chunk in chunks]

result = client.models.embed_content(
    model=EMBEDDING_MODEL,
    contents=texts,
)

embedding = [item.values for item in result.embeddings]

questions = [
    "რამდენი ღირს ოთხი ადამიანისთვის განკუთვნილი ნომერი?",
    "საუზმე შედის ნომრის ფასში?",
    "შემიძლია თუ არა ჯავშნის გაუქმება ჩამოსვლამდე ერთი დღით ადრე?",
    "რომელ საათზე უნდა დავტოვო ნომერი?",
    "რა აქტივობებია ხელმისაწვდომი სტუმრებისთვის?",
    "რა პირობებია შინაური ცხოველის წამოყვანისთვის?",
    "რა მოხდება, თუ ჯავშნის გარეშე კი არა, დაჯავშნილი ნომრით საერთოდ არ მივალ?"
]

for question in questions:
    query_result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=question
    )

    embedding_query = query_result.embeddings[0].values

    similarity_scores = cosine_similarity([embedding_query], embedding)[0]

    results = sorted(zip(chunks, similarity_scores), key=lambda x: x[1], reverse=True)

    print("****************************")
    print(f"Question: {question}")

    for i, (chunk, score) in enumerate(results[:3]):  # მხოლოდ ტოპ 3 ყველაზე მსგავსი შედეგის ჩვენება
        print(f"Chunk {i + 1}:")
        print(f"Score: {score}")
        print(f"Data: {chunk.page_content}")
        print("\n")