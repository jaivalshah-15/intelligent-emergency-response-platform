from sqlalchemy.orm import Session

from app.models.team import Team
from app.schemas.team import TeamCreate, TeamUpdate


def create_team(
    db: Session,
    team_data: TeamCreate
):
    team = Team(
        name=team_data.name,
        team_type=team_data.team_type,
        status=team_data.status,
        latitude=team_data.latitude,
        longitude=team_data.longitude,
    )

    db.add(team)
    db.commit()
    db.refresh(team)

    return team


def get_teams(db: Session):
    return db.query(Team).all()


def get_team(
    db: Session,
    team_id: int
):
    return (
        db.query(Team)
        .filter(Team.id == team_id)
        .first()
    )


def update_team(
    db: Session,
    team_id: int,
    team_data: TeamUpdate
):
    team = get_team(
        db,
        team_id
    )

    if not team:
        return None

    data = team_data.model_dump(
        exclude_unset=True
    )

    for key, value in data.items():
        setattr(team, key, value)

    db.commit()
    db.refresh(team)

    return team