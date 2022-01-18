from os import path
from fastapi import FastAPI, Depends, FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from .controllers import controller

