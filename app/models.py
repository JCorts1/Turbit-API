from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str

    class Config:
        json_schema_extra = {
            "example": {
                "userId": 1,
                "id": 1,
                "title": "Sample Post Title",
                "body": "This is the body of the post"
            }
        }


class Comment(BaseModel):
    postId: int
    id: int
    name: str
    email: str
    body: str

    class Config:
        json_schema_extra = {
            "example": {
                "postId": 1,
                "id": 1,
                "name": "Comment Name",
                "email": "commenter@example.com",
                "body": "This is a comment"
            }
        }


class User(BaseModel):
    id: int
    name: str
    username: str
    email: str
    address: dict
    phone: str
    website: str
    company: dict

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "username": "johndoe",
                "email": "john@example.com",
                "address": {
                    "street": "123 Main St",
                    "suite": "Apt. 1",
                    "city": "New York",
                    "zipcode": "10001",
                    "geo": {
                        "lat": "40.7128",
                        "lng": "-74.0060"
                    }
                },
                "phone": "1-234-567-8900",
                "website": "johndoe.com",
                "company": {
                    "name": "Acme Corp",
                    "catchPhrase": "Innovation at its best",
                    "bs": "synergize scalable solutions"
                }
            }
        }


class UserPostCount(BaseModel):
    userId: int
    userName: str
    postCount: int


class PostWithCommentCount(BaseModel):
    postId: int
    postTitle: str
    userId: int
    commentCount: int
