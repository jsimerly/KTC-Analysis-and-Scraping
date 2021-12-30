from sqlalchemy import create_engine, engine
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import Column, Integer, String, TEXT

engine = create_engine('sqlite:///newdb.db', echo=True)
session = Session(engine)
Base = declarative_base()

class playerValues(Base):
    __tablename__ = 'Player Values'

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    pos = Column(String(25))
    age = Column(Integer)
    height = Column(String(6))
    weight = Column(Integer)
    drafted = Column(String(15))
    draftClass = Column(String(20))
    exp = Column(String(10))
    valueData = Column(TEXT)


    def addPlayer(self, id ,name, pos, age, height, weight, drafted, draftClass, exp, data):
        print(session)
        try:
            player = session.query(self).filter(self.id==id).one()
        except:
            player = None
       
        if player:
            player.name = name
            player.pos = pos
            player.age = age
            player.height = height
            player.weight = weight
            player.drafted = drafted
            player.draftClass = draftClass
            player.exp = exp
            player.valueData = data
        else:
            player = self(id=id, name=name, pos=pos, age=age, height=height, weight=weight, drafted=drafted, draftClass=draftClass, exp=exp, valueData=data)
        
        session.add(player)
            
    
    def commit():
        session.commit()

# #Base.metadata.create_all(engine)
# playerValues.addPlayer(playerValues, 1, 'testnew2', 'pos3', 22, '6"4', 220, '2.02', 2019, 'Rookie', r'2{324}')
# playerValues.addPlayer(playerValues, 5, 'Jacffob', 'pos', 22, '6"4', 220, '2.02', 2019, 'Rookie', r'{}')
# playerValues.commit()
