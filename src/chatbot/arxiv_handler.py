from typing import List
import requests

class ArxivHandler:
    BASE_URL = "http://export.arxiv.org/api/query?"

    def fetch_paper(self, paper_id: str) -> dict:
        query = f"id:{paper_id}"
        response = requests.get(self.BASE_URL + f"search_query={query}")
        if response.status_code == 200:
            return self.parse_response(response.text)
        else:
            raise Exception("Error fetching paper from arXiv")

    def parse_response(self, response_text: str) -> dict:
        # Parse the arXiv API response and extract relevant information
        # This is a placeholder for actual parsing logic
        return {"title": "Sample Title", "summary": "Sample Summary"}

    def summarize_paper(self, paper_id: str) -> str:
        paper_data = self.fetch_paper(paper_id)
        return paper_data.get("summary", "No summary available.")

    def get_paper_metadata(self, paper_id: str) -> dict:
        paper_data = self.fetch_paper(paper_id)
        return {
            "title": paper_data.get("title"),
            "authors": paper_data.get("authors", []),
            "published": paper_data.get("published"),
        }