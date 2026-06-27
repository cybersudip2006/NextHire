from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy object
db = SQLAlchemy()


class ResumeData(db.Model):
    __tablename__ = "resume_data"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        nullable=False
    )

    phone = db.Column(
        db.String(25),
        nullable=False
    )

    def __repr__(self):
        return f"<ResumeData {self.name}>"
