from app.database import engine, Base
from app import models

print("Creating database...")
Base.metadata.create_all(bind=engine)
print("✅ All tables created!")
