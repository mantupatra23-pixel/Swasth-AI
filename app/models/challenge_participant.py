from sqlalchemy import Column, Integer, Float, ForeignKey, Boolean
from app.core.database import Base

class ChallengeParticipant(Base):
    __tablename__ = "challenge_participants"

    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("fitness_challenges.id"))
    user_id = Column(Integer, ForeignKey("health_profiles.id"))
    progress = Column(Float, default=0)
    completed = Column(Boolean, default=False)
