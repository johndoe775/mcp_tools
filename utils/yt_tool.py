import re
from youtube_transcript_api import YouTubeTranscriptApi
from deep_translator import GoogleTranslator

class YouTubeTranscriptTranslator:
    # Regex to extract YouTube video IDs
    YOUTUBE_REGEX = re.compile(
        r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/|v/|shorts/|live/)|youtube\.com.*[?&]v=)([A-Za-z0-9_-]{11})"
    )

    def __init__(self, url: str, target_lang: str = "en"):
        self.url = url
        self.target_lang = target_lang
        self.video_id = self.extract_video_id()
        self.transcript_api = YouTubeTranscriptApi()
        self.translated_text = self.process()
        self.result=self.translate_in_chunks(self.translated_text)

    # --------------------------
    # Extract YouTube ID
    # --------------------------
    def extract_video_id(self):
        match = self.YOUTUBE_REGEX.search(self.url)
        if not match:
            raise ValueError("Invalid YouTube URL: Could not extract video ID.")
        return match.group(1)

    # --------------------------
    # Main processing pipeline
    # --------------------------
    def process(self):
        transcript_list = self.transcript_api.list(self.video_id)

        # Pick manually created → generated → auto-translated transcript
        transcript_obj = (
            transcript_list.find_transcript(
                transcript_list._manually_created_transcripts.keys()
                or transcript_list._generated_transcripts.keys()
            )
        )

        # Fetch transcript text
        transcript = transcript_obj.fetch()
        full_text = " ".join([entry.text for entry in transcript])

        # Translate in 2000-char chunks
        return full_text

    # --------------------------
    # Translate large text safely
    # --------------------------
    def translate_in_chunks(self, text, chunk_size=2000):
        translated_chunks = []
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
            translated_chunk = GoogleTranslator(
                source="auto",
                target=self.target_lang
            ).translate(chunk)
            translated_chunks.append(translated_chunk)
        return " ".join(translated_chunks)
