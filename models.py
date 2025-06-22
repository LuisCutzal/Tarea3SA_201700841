from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class CIType(Base):
    __tablename__ = "CIType"  # Respetar el nombre exacto (mayúsculas)
    Id = Column(Integer, primary_key=True)
    Name = Column(String(100), unique=True)

class CI(Base):
    __tablename__ = "CI"
    Id = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)
    Description = Column(Text)
    SerialNumber = Column(String(100))
    Version = Column(String(50))
    AcquisitionDate = Column(Date)
    CurrentStatus = Column(String(50))
    PhysicalLocation = Column(String(255))
    Owner = Column(String(100))
    SecurityLevel = Column(String(50))
    Compliance = Column(String(50))
    ConfigStatus = Column(String(50))
    LicenseNumber = Column(String(100))
    ExpirationDate = Column(Date)
    TypeId = Column(Integer, ForeignKey("CIType.Id"))
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow)

    type = relationship("CIType")
