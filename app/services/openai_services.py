from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
import json
import os

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

class CommentSentiments(BaseModel):
    total_comments: int
    negative_comments: List[str]
    number_of_negative_comments: int
    positive_comments: List[str]
    number_of_positive_comments: int
    neutral_comments: List[str]
    number_of_neutral_comments: int

class ProblemIdentification(BaseModel):
    problems: str = Field( description="Title of the identified problem from the comments")
    suggetion: List[str] = Field( description="A list of actionable suggestions to improve engagement and address concerns")

class Suggestion(BaseModel):
    government_project_suggetions: List[ProblemIdentification]

class TopPositiveComments(BaseModel):
    positive_comments: str = Field( description="Top 5 positive comments from the list.")
    times_mentioned: int = Field( description="Number of times the positive comment was mentioned.")

class TopNegativeComments(BaseModel):
    negative_comments: str = Field( description="Top 5 negative comments from the list.")
    times_mentioned: int = Field( description="Number of times the negative comment was mentioned.")

class TopperComments(BaseModel):
    top_five_positive_comments: List[TopPositiveComments]
    top_five_negative_comments: List[TopNegativeComments]
    

async def get_comment_sentiments(comments: List[str]) -> CommentSentiments:
    prompt = (f"""
        You are an expert social media analyst for a government department. Given the following list of comments from users on a social media platform, identify and return only those comments that express negative, positive and neutral sentiment. A comment is considered negative if it contains criticism, complaints, A comment is considered positive if it contains praise, compliments, or favorable opinions. A comment is considered neutral if it is a statement of fact or unfavorable opinions. The sentiment can be sarcastic or indirect."""
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(comments)}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "comment_sentiments",
                "schema": CommentSentiments.model_json_schema()
            }
        }
    )

    data = json.loads(response.choices[0].message.content)
    return CommentSentiments(**data)

async def get_suggestion(comments: List[str]) -> List[str]:
    prompt = (f"""
        You are an expert social media analyst for a government department. Given the following list of comments from users on a social media platform identify the problem and provide actionable suggestions for improving engagement and addressing concerns.
    """)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(comments)}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "suggestion",
                "schema": Suggestion.model_json_schema()
            }
        }
    )

    data = json.loads(response.choices[0].message.content)
    return Suggestion(**data)

async def get_topper(comments: List[str]) -> List[str]:
    prompt = (f"""
        You are an expert social media analyst for a government department. Given the following list of comments from users on a social media platform identify the top 5 positive and top 5 negative comments, based it on the comment context. There may be comment that are similar in context count it as one. For the output return the list of comment and how many time it is mentioned.Count same thoughts as one.  
    """)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(comments)}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "topper_comments",
                "schema": TopperComments.model_json_schema()
            }
        }
    )

    data = json.loads(response.choices[0].message.content)
    return TopperComments(**data)