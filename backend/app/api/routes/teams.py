from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.team import (
    create_team,
    get_team,
    get_teams,
    update_team,
)
from app.db.session import get_db
from app.schemas.team import (
    TeamCreate,
    TeamResponse,
    TeamUpdate,
)


router = APIRouter(
    prefix="/api/teams",
    tags=["Teams"]
)


@router.post(
    "/",
    response_model=TeamResponse
)
def create_team_route(
    team_data: TeamCreate,
    db: Session = Depends(get_db)
):
    return create_team(
        db,
        team_data
    )


@router.get(
    "/",
    response_model=list[TeamResponse]
)
def get_all_teams(
    db: Session = Depends(get_db)
):
    return get_teams(db)


@router.get(
    "/{team_id}",
    response_model=TeamResponse
)
def get_single_team(
    team_id: int,
    db: Session = Depends(get_db)
):
    team = get_team(
        db,
        team_id
    )

    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    return team


@router.patch(
    "/{team_id}",
    response_model=TeamResponse
)
def update_single_team(
    team_id: int,
    team_data: TeamUpdate,
    db: Session = Depends(get_db)
):
    team = update_team(
        db,
        team_id,
        team_data
    )

    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    return team