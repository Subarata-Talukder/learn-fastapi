from os import stat
from fastapi import status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from ..database import get_db
from .. import models
from ..import oauth2
from ..schemas import Vote

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
    )

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:Vote, 
db: Session = Depends(get_db),
current_user:int = Depends(oauth2.get_current_user)): 

    check_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not check_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post {vote.post_id} does not exit')

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, 
    models.Votes.user_id == current_user.id)

    print("this is the vote query", vote_query)

    f_vote = vote_query.first()

    if(vote.dir == 1):
        if f_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="you voted already")
        
        s_vote = models.Votes(post_id = vote.post_id, user_id= current_user.id)
        db.add(s_vote)
        db.commit()

        return {"msg": "Voted successfully"}
    else:
        if not f_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="you vote already")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"msg": "Voted successfully"}