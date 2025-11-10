from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Boolean, Text
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Mapped, mapped_column
from datetime import date

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///pet_clinic.db')
Session = sessionmaker(bind=engine)
session = Session()


class Owners(Base):
    """Owner model representing pet owners"""
    __tablename__ = 'owners'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Relationship to pets (one-to-many)
    pets: Mapped[list["Pets"]] = relationship("Pets", back_populates="owner")
    
    


class Pets(Base):
    """Pet model representing pets in the clinic"""
    __tablename__ = 'pets'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    species: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., "Dog", "Cat", "Bird"
    breed: Mapped[str] = mapped_column(String(100), nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('owners.id'), nullable=False)
    
    # Relationships
    owner: Mapped["Owners"] = relationship("Owners", back_populates="pets")
    appointments: Mapped[list["Appointments"]] = relationship("Appointments", back_populates="pet")
    
    


class Vets(Base):
    """Veterinarian model representing clinic veterinarians"""
    __tablename__ = 'vets'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialization: Mapped[str] = mapped_column(String(100), nullable=True)  # e.g., "General", "Surgery", "Dermatology"
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    
    # Relationships
    appointments: Mapped[list["Appointments"]] = relationship("Appointments", back_populates="vet", )
    
    


class Appointments(Base):
    """Appointment model representing pet appointments with veterinarians"""
    __tablename__ = 'appointments'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey('pets.id'), nullable=False)
    veterinarian_id: Mapped[int] = mapped_column(Integer, ForeignKey('vets.id'), nullable=False)
    appointment_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="Scheduled", nullable=False)  # "Scheduled", "Completed", "Cancelled"
    
    # Relationships
    pet: Mapped["Pets"] = relationship("Pets", back_populates="appointments")
    vet: Mapped["Vets"] = relationship("Vets", back_populates="appointments")
    




Base.metadata.create_all(engine)

# vet1 = Vets(name="Dr. Dizzy", specialization="Anesthesiologist", email="dylank@clinic.com")
# vet2 = Vets(name="Dr. James Brown", specialization="Surgery", email="james.brown@clinic.com")
# vet3 = Vets(name="Dr. Lisa Garcia", specialization="Dermatology", email="lisa.garcia@clinic.com")
# vet4 = Vets(name="Dr. Emily Wilson", specialization="General", email="emily.wilson@clinic.com")

# session.add_all([vet1,vet2,vet3,vet4])
# session.commit()
    