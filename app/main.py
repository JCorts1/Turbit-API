from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from typing import List
# --- ADD THIS IMPORT ---
from fastapi.middleware.cors import CORSMiddleware

from app.database import connect_to_mongo, close_mongo_connection, db
from app.models import Post, Comment, User, UserPostCount, PostWithCommentCount
from app import turbine_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()


app = FastAPI(
    title="Turbit API",
    description="API for accessing turbine data and JSONPlaceholder data stored in MongoDB",
    version="1.0.0",
    lifespan=lifespan
)

origins = [
    "http://localhost",
    "http://localhost:3000", # For create-react-app
    "http://localhost:5173", # For Vite
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------

# Include the turbine router
app.include_router(turbine_routes.router)


@app.get("/", tags=["Root"])
async def root():
    """Welcome endpoint."""
    return {
        "message": "Welcome to Turbit API",
        "description": "Turbine data and analytics platform",
        "endpoints": {
            "users": "/users",
            "posts": "/posts",
            "comments": "/comments",
            "user_post_counts": "/reports/user-post-counts",
            "post_comment_counts": "/reports/post-comment-counts",
            "turbines": "/turbines"
        }
    }


@app.get("/users", response_model=List[User], tags=["Users"])
async def get_users(skip: int = 0, limit: int = 100):
    """Get all users with pagination."""
    users = []
    cursor = db.database.users.find({}).skip(skip).limit(limit)
    async for user in cursor:
        user.pop('_id', None)
        users.append(user)
    return users


@app.get("/users/{user_id}", response_model=User, tags=["Users"])
async def get_user(user_id: int):
    """Get a specific user by ID."""
    user = await db.database.users.find_one({"id": user_id})
    if user:
        user.pop('_id', None)
        return user
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/posts", response_model=List[Post], tags=["Posts"])
async def get_posts(skip: int = 0, limit: int = 100, user_id: int = None):
    """Get all posts with optional filtering by user_id."""
    filter_query = {}
    if user_id is not None:
        filter_query["userId"] = user_id

    posts = []
    cursor = db.database.posts.find(filter_query).skip(skip).limit(limit)
    async for post in cursor:
        post.pop('_id', None)
        posts.append(post)
    return posts


@app.get("/posts/{post_id}", response_model=Post, tags=["Posts"])
async def get_post(post_id: int):
    """Get a specific post by ID."""
    post = await db.database.posts.find_one({"id": post_id})
    if post:
        post.pop('_id', None)
        return post
    raise HTTPException(status_code=404, detail="Post not found")


@app.get("/comments", response_model=List[Comment], tags=["Comments"])
async def get_comments(skip: int = 0, limit: int = 100, post_id: int = None):
    """Get all comments with optional filtering by post_id."""
    filter_query = {}
    if post_id is not None:
        filter_query["postId"] = post_id

    comments = []
    cursor = db.database.comments.find(filter_query).skip(skip).limit(limit)
    async for comment in cursor:
        comment.pop('_id', None)
        comments.append(comment)
    return comments


@app.get("/comments/{comment_id}", response_model=Comment, tags=["Comments"])
async def get_comment(comment_id: int):
    """Get a specific comment by ID."""
    comment = await db.database.comments.find_one({"id": comment_id})
    if comment:
        comment.pop('_id', None)
        return comment
    raise HTTPException(status_code=404, detail="Comment not found")


@app.get("/reports/user-post-counts", response_model=List[UserPostCount], tags=["Reports"])
async def get_user_post_counts():
    """Get the total number of posts for each user."""
    pipeline = [
        {"$group": {"_id": "$userId", "postCount": {"$sum": 1}}},
        {"$lookup": {"from": "users", "localField": "_id", "foreignField": "id", "as": "user"}},
        {"$unwind": "$user"},
        {"$project": {"userId": "$_id", "userName": "$user.name", "postCount": 1, "_id": 0}},
        {"$sort": {"userId": 1}}
    ]

    results = []
    async for doc in db.database.posts.aggregate(pipeline):
        results.append(UserPostCount(**doc))

    return results


@app.get("/reports/post-comment-counts", response_model=List[PostWithCommentCount], tags=["Reports"])
async def get_post_comment_counts(min_comments: int = 0):
    """Get the number of comments for each post."""
    pipeline = [
        {"$group": {"_id": "$postId", "commentCount": {"$sum": 1}}},
        {"$lookup": {"from": "posts", "localField": "_id", "foreignField": "id", "as": "post"}},
        {"$unwind": "$post"},
        {"$project": {"postId": "$_id", "postTitle": "$post.title", "userId": "$post.userId", "commentCount": 1, "_id": 0}},
        {"$match": {"commentCount": {"$gte": min_comments}}},
        {"$sort": {"commentCount": -1, "postId": 1}}
    ]

    results = []
    async for doc in db.database.comments.aggregate(pipeline):
        results.append(PostWithCommentCount(**doc))

    return results


@app.get("/health", tags=["Health"])
async def health_check():
    """Check if the API and database are healthy."""
    try:
        await db.database.command("ping")
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
