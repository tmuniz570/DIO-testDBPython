from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, inspect, select
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship("Address", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_address = Column(String(40), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="address")

    def __repr__(self):
        return f"Address(id={self.id}, email_address={self.email_address})"


engine = create_engine("sqlite://")

Base.metadata.create_all(engine)

insp = inspect(engine)

print(insp.get_table_names())

with Session(engine) as session:
    thiago = User(
        name='Thiago',
        fullname='Thiago Brandao',
        address=[Address(email_address='tmuniz570@gmail.com')]
    )

    heloisa = User(
        name='Heloisa',
        fullname='Heloisa Seabra',
        address=[Address(email_address='helo@gmail.com'),
                 Address(email_address='mister@g.uk')]
    )

    julieta = User(
        name='Julieta',
        fullname='Julieta Juliao'
    )

    # Add to DB
    session.add_all([thiago, heloisa, julieta])
    session.commit()

stmt_user = select(User).where(User.name.in_(['Thiago']))
for user in session.scalars(stmt_user):
    print(user)

stmt_address = select(Address).where(Address.user_id.in_([2]))
for address in session.scalars(stmt_address):
    print(address)

stmt_order = select(User).order_by(User.name.desc())
for result in session.scalars(stmt_order):
    print(result)

stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)
connection = engine.connect()
for result in connection.execute(stmt_join):
    print(result)
