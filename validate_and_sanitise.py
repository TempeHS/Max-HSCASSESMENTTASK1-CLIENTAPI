from flask import Flask, redirect, render_template
import bcrypt
import sqlite3 as sql
import userManagement as dbHandler

def validate_password(password):
    if len(password) < 8:
        return False
    return True