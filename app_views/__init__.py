from os import path
from fastapi import FastAPI, Depends, FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from .models.model import db, engine
from .controllers import controller

db.metadata.create_all(bind=engine)

