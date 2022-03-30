from operator import mod
from typing import List, Optional
from fastapi import status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import outerjoin, true
from sqlalchemy.sql.functions import current_user, func
from starlette.responses import Response
from ..database import get_db
from ..schemas import Post, PostOut, PostResponse
from .. import models
from ..import oauth2
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
    )

@router.get("/test")
def root(): return "hellow Subarata"

@router.get("/", response_model=List[PostOut])
#@router.get("/")
def get_post(db: Session = Depends(get_db),
current_user:any = Depends(oauth2.get_current_user),
limit:int=2, skip:int = 0, search:Optional[str] = ""): # limit and skip is the query parameter 

    post_response = db.query(models.Post).filter(
        models.Post.title.contains(search)
        ).limit(limit).offset(skip).all()

    '''SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, 
        posts.published AS posts_published, posts.created_at AS posts_created_at, 
        posts.user_id AS posts_user_id, count(votes.post_id) AS total_post
       FROM posts LEFT OUTER JOIN votes ON votes.post_id = posts.id GROUP BY posts.id'''

    result = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)
        ).limit(limit).offset(skip).all()

    print(result)
    return result


@router.get("/{id}", response_model=PostOut)
def get_post(id: int, db: Session = Depends(get_db),
current_user:any = Depends(oauth2.get_current_user)):
    # cr.execute("""SELECT * FROM posts where id = %s """, (str(id),))
    # post_response = cr.fetchone()
    # if not post_response:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} was not found")
    # post_response = db.query(models.Post).filter(models.Post.id == id).first()ss
    
    post_response = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()
    
    if not post_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} was not found")

    return post_response

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db),
current_user:int = Depends(oauth2.get_current_user)):
    # cr.execute("""DELETE FROM posts where id = %s RETURNING * """, (str(id),))
    # deleted_post = cr.fetchone()
    # con.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")

    if post.user_id == current_user.id:
        post_query.delete(synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User not unauthorized {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # cr.execute("""UPDATE posts SET title = %s WHERE id = %s RETURNING * """, (post.title, str(id),))
    # updated_post = cr.fetchone()
    # con.commit()
    update_query = db.query(models.Post).filter(models.Post.id == id)

    if update_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")

    update_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return update_query.first()


# @router.get("/test_table/test")
# def get_levels(): 
#     labels = (1,2,3,4,5)
#     updatequery='update test_table set id= id + 2 where label= %s'
#     for label in labels:
#         tuplee=(label)
#         print(tuplee)
#         cr.execute(updatequery,str(tuplee),)
#         con.commit()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def save_post(post:Post, 
db: Session = Depends(get_db),
current_user:int = Depends(oauth2.get_current_user)): 
    # cr.execute("""INSERT INTO posts(title, content, published) values(%s, %s, %s) RETURNING * """, 
    # (post.title, post.content, post.published))

    # new_post = cr.fetchone()
    # con.commit() # Save data into the DB

    # Create post
    # new_post = models.Post(title=post.title, content = post.content, published = post.published)
    # Or
    print(current_user.id)
    new_post = models.Post(user_id=current_user.id,**post.dict()) # pass forign key value as user id
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # Return SQL query result to new_post variable
    
    return new_post