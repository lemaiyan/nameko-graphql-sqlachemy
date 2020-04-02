from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from models import Ship, Race, Crew, Rank
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Create the fixtures
    vulcan = Race(name='Vulcan')
    db_session.add(vulcan)
    human = Race(name='Human')
    db_session.add(human)
    kelpien = Race(name='Kelpien')
    db_session.add(kelpien)
    synthetic = Race(name='Synthetic')
    db_session.add(synthetic)
    kelpien = Race(name='Kelpien')
    db_session.add(kelpien)
    synthetic = Race(name='Synthetic')
    db_session.add(synthetic)
    klingon = Race(name='Klingon')
    db_session.add(klingon)
    barzan = Race(name='Barzan')
    db_session.add(barzan)

    captain = Rank(name='Captain')
    db_session.add(captain)
    first_officer = Rank(name='First Officer')
    db_session.add(first_officer)
    chief_engineer = Rank(name='Chief Engineer')
    db_session.add(chief_engineer)
    science_officer = Rank(name='Science Officer')
    db_session.add(science_officer)
    chief_medical_officer = Rank(name='Chief Medical Officer')
    db_session.add(chief_medical_officer)
    communication_officer = Rank(name=' Communication Officer')
    db_session.add(communication_officer)
    ensign = Rank(name='Ensign')
    db_session.add(ensign)
    helmsman = Rank(name='Helmsman')
    db_session.add(helmsman)
    security_chief = Rank(name='Security Chief')
    db_session.add(security_chief)
    operations_officer = Rank(name='Operations Officer')
    db_session.add(operations_officer)
    transporter_chief = Rank(name='Transporter Chief')
    db_session.add(transporter_chief)

    discovery = Ship(name='U.S.S Discovery')
    db_session.add(discovery)
    enterprise = Ship(name='U.S.S. Enterprise')
    db_session.add(enterprise)

    jl = Crew(name='Jean-Luc Picard', ship=enterprise, race=human, rank=captain)
    db_session.add(jl)
    pike = Crew(name='Christopher Pike', ship=discovery, race=human, rank=captain)
    db_session.add(pike)
    lorca = Crew(name='Gabriel Lorca', ship=discovery, race=human, rank=captain)
    db_session.add(lorca)

    riker = Crew(name='William Riker', ship=enterprise, race=human, rank=first_officer)
    db_session.add(riker)
    saru = Crew(name='Saru', ship=discovery, race=kelpien, rank=first_officer)
    db_session.add(saru)

    la = Crew(name='Geordi La Forge', ship=enterprise, race=human, rank=chief_engineer)
    db_session.add(la)
    reno = Crew(name='Jett Reno', ship=discovery, race=human, rank=chief_engineer)
    db_session.add(reno)

    data = Crew(name='Data', ship=enterprise, race=synthetic, rank=science_officer)
    db_session.add(data)
    burn = Crew(name='Michael Burnham', ship=discovery, race=human, rank=science_officer)
    db_session.add(burn)

    b_crusher = Crew(name='Beverly Crusher', ship=enterprise, race=human, rank=chief_medical_officer)
    db_session.add(b_crusher)
    pulaski = Crew(name='Katherine Pulaski', ship=enterprise, race=human, rank=chief_medical_officer)
    db_session.add(pulaski)
    hugh = Crew(name='Hugh Culbe', ship=discovery, race=human, rank=chief_medical_officer)
    db_session.add(hugh)
    tracy = Crew(name='Tracy Pollard', ship=discovery, race=human, rank=chief_medical_officer)
    db_session.add(tracy)

    pend = Crew(name='Pendleton', ship=enterprise, race=human, rank=communication_officer)
    db_session.add(pend)
    ra = Crew(name='R.A. Bryce', ship=discovery, race=human, rank=communication_officer)
    db_session.add(ra)

    wc= Crew(name='Wesley Crusher', ship=enterprise, race=human, rank=helmsman)
    db_session.add(wc)
    keyla = Crew(name='Keyla Detmer', ship=discovery, race=human, rank=helmsman)
    db_session.add(keyla)

    worf = Crew(name='Worf', ship=enterprise, race=klingon, rank=security_chief)
    db_session.add(worf)
    nhan = Crew(name='Nhan', ship=discovery, race=barzan, rank=security_chief)
    db_session.add(nhan)

    data = Crew(name='Data', ship=enterprise, race=synthetic, rank=operations_officer)
    db_session.add(data)
    joann = Crew(name='Joann Owosekun', ship=discovery, race=human, rank=operations_officer)
    db_session.add(joann)

    miles= Crew(name='Miles O’Brien', ship=enterprise, race=human, rank=transporter_chief)
    db_session.add(miles)
    airiam = Crew(name='Airiam', ship=discovery, race=synthetic, rank=transporter_chief)
    db_session.add(airiam)

    w_c2 = Crew(name='Wesley Crusher', ship=enterprise, race=human, rank=ensign)
    db_session.add(w_c2)
    st = Crew(name='Sylvia Tilly', ship=discovery, race=human, rank=ensign)
    db_session.add(st)

    db_session.commit()
