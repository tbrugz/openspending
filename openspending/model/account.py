import colander
import uuid

from openspending.model import meta as db
from openspending.model.dataset import Dataset

REGISTER_NAME_RE = r"^[a-zA-Z0-9_\-]{3,255}$"

def make_uuid():
    return unicode(uuid.uuid4())


account_dataset_table = db.Table('account_dataset', db.metadata,
        db.Column('dataset_id', db.Integer, db.ForeignKey('dataset.id'),
            primary_key=True),
        db.Column('account_id', db.Integer, db.ForeignKey('account.id'),
            primary_key=True)
    )


class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255), unique=True)
    fullname = db.Column(db.Unicode(2000))
    email = db.Column(db.Unicode(2000))
    password = db.Column(db.Unicode(2000))
    api_key = db.Column(db.Unicode(2000), default=make_uuid)
    admin = db.Column(db.Boolean, default=False)
    
    datasets = db.relationship(Dataset,
            secondary=account_dataset_table,
            backref=db.backref('managers', lazy='dynamic'))

    def __init__(self):
        pass

    @classmethod
    def by_name(cls, name):
        return db.session.query(cls).filter_by(name=name).first()
    
    @classmethod
    def by_api_key(cls, api_key):
        return db.session.query(cls).filter_by(api_key=api_key).first()

    def as_dict(self):
        return {
            'name': self.name,
            'fullname': self.fullname,
            'email': self.email,
            'admin': self.admin
            }

class AccountRegister(colander.MappingSchema):
    name = colander.SchemaNode(colander.String(),
                               validator=colander.Regex(REGISTER_NAME_RE))

    fullname = colander.SchemaNode(colander.String())
    email = colander.SchemaNode(colander.String(),
                                validator=colander.Email())
    password1 = colander.SchemaNode(colander.String(),
                                    validator=colander.Length(min=4))
    password2 = colander.SchemaNode(colander.String(),
                                    validator=colander.Length(min=4))


class AccountSettings(colander.MappingSchema):
    fullname = colander.SchemaNode(colander.String())
    email = colander.SchemaNode(colander.String(),
                                validator=colander.Email())
    password1 = colander.SchemaNode(colander.String(),
                                missing=None, default=None)
    password2 = colander.SchemaNode(colander.String(),
                                missing=None, default=None)
