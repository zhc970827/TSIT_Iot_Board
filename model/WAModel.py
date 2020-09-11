import asyncio
from gino import Gino

db = Gino()


class WaUser(db.Model):
    __tablename__ = 'users_table'

    id = db.Column(db.Integer(), primary_key=True)
    u_phone = db.Column(db.String)
    u_password = db.Column(db.String)
    u_password_salt = db.Column(db.String)
    username = db.Coulumn(db.String)
    verify_code = db.Column(db.String)


class WaUserMembership(db.Model):
    pass

async def main():
    await db.set_bind('postgresql://"localhost"/gino')
    await db.create_all()


    await db.pop_bind().close()
asyncio.get_event_loop().run_until_complete(main())
