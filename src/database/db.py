from src.database.config import supabase

import bcrypt

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(),bcrypt.gensalt()).decode()


def check_pass(pwd,hash_pwd):
    return bcrypt.checkpw(pwd.encode(),hash_pwd.encode())


def check_teacher_exist(username):
    # checks for duplicate username
    response=supabase.table("teachers").select("username").eq("username",username).execute()
    return len(response.data)>0


def create_teacher(username,password,name):
    data={"username":username,"password":hash_pass(password),"name":name}

    response=supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username,password):
    response=supabase.table("teachers").select("*").eq("username",username).execute()

    if response.data:
        teacher=response.data[0]
        if check_pass(password,teacher['password']):
            return teacher
    return None

def get_all_students():
    response=supabase.get("students").select("*").execute()

    return response.data
