from langchain.serpapi import SerpAPIWrapper


def get_uid(flower: str) -> str:
    return SerpAPIWrapper().run(f'{flower}')
