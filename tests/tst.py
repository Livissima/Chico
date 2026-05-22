from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

db = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()


class Usuario(Base) :
    __tablename__ = 'usuarios'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String)
    email = Column('email', String)
    senha = Column('senha', String)
    ativo = Column('ativo', Boolean)

    def __init__(self, nome: str, email: str, senha: str, ativo: bool = True) :
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo

class Livro(Base) :
    __tablename__ = 'livros'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    título = Column('título', String)
    qtd_páginas = Column('qtd_paginas', Integer)
    dono = Column('dono', ForeignKey('usuarios.id'))

    def __init__(self, título, qtd_páginas, dono) :
        self.título = título
        self.qtd_páginas = qtd_páginas
        self.dono = dono


Base.metadata.create_all(bind=db)
