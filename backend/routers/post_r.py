from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Post, Comment, Like
from schemas import PostCreate, PostResponse, CommentCreate, CommentResponse
from typing import List
from auth import get_current_user  # 인증 모듈 필요

router = APIRouter()

# 게시글 작성
@router.post("/posts/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    new_post = Post(title=post.title, content=post.content, author_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# 특정 게시글 조회
@router.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# 모든 게시글 조회 (페이징)
@router.get("/posts/", response_model=List[PostResponse])
def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts

# 게시글 수정
@router.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: PostCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    db_post = db.query(Post).filter(Post.id == post_id, Post.author_id == user_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")
    
    db_post.title = post.title # type: ignore
    db_post.content = post.content # type: ignore
    db.commit()
    db.refresh(db_post)
    return db_post

# 게시글 삭제
@router.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    db_post = db.query(Post).filter(Post.id == post_id, Post.author_id == user_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")
    
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}

# 좋아요 추가/삭제
@router.post("/posts/{post_id}/like")
def toggle_like(post_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    existing_like = db.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).first()
    if existing_like:
        db.delete(existing_like)
        db.commit()
        return {"message": "Like removed"}
    else:
        new_like = Like(post_id=post_id, user_id=user_id)
        db.add(new_like)
        db.commit()
        return {"message": "Like added"}

# 댓글 작성
@router.post("/posts/{post_id}/comments/", response_model=CommentResponse)
def create_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    new_comment = Comment(post_id=post_id, content=comment.content, author_id=user_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# 특정 게시글의 댓글 조회
@router.get("/posts/{post_id}/comments/", response_model=List[CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments

# 댓글 삭제
@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.author_id == user_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or not authorized")
    
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}
