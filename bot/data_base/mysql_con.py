import mysql.connector
from create_bot import bot
import aiomysql
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to the MySQL database

# def db_start():
#     global base, cur
#     base = mysql.connector.connect(
#         # host="mysql",
#         user="mydatabaseuser",
#         password="12345",
#         database="mydatabase",
#         # auth_plugin='mysql_native_password'
#     )

async def db_start():
    global base, cur
    base = await aiomysql.connect(
        # host="mysql",
        # user=os.environ.get('DB_USER'),
        # password=os.environ.get('DB_PASSWORD'),
        # db=os.environ.get('DB_NAME'),
        password='12345',
        db='mydatabase',
        user='mydatabaseuser',
        autocommit=True,
        auth_plugin='mysql_native_password'
    )
    # Create a cursor object to execute queries
    cur = await base.cursor()
    if base:
        print('Data base connected OK')
    else:
        print('DB faile!')
    
    # await cur.execute("CREATE TABLE if not exists materials_telegram (img VARCHAR(100), name VARCHAR(100), description VARCHAR(1000))")
    # await base.commit()


async def write_user(message):
    answer = (
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
        3,
        0
    )
    await cur.execute("INSERT INTO telegram_like VALUES('%s', '%s', '%s', '%s', '%s', '%s')"%answer)
    await base.commit()


async def my_db_add_command(state):
    async with state.proxy() as data:
        res = tuple(data.values())
        await cur.execute("INSERT INTO materials_telegram VALUES ('%s', '%s', '%s')"%res)
        await base.commit()


async def my_db_read2():
    await cur.execute('SELECT * FROM materials_telegram')
    return cur.fetchall()


async def my_db_read(message):
    res = await my_db_read2()
    if len(await res) > 0:
        # for ret in await res:
        #     await bot.send_photo(message.from_user.id, ret[0], f'Name: {ret[1]}\nDescription:{ret[2]}')
        return await res
    else:    
        await bot.send_message(message.from_user.id, text="There are no courses yet.")


async def my_db_delete(data):
    await cur.execute("DELETE FROM materials_telegram WHERE name='%s'"%data)
    await base.commit()


async def my_db_read_lang(message):
    global res
    res = []
    await cur.execute('SELECT language FROM materials_language')
    # res.append(cur.fetchall())
    for i  in await cur.fetchall():
        res.append(i[0])
        await bot.send_message(message.from_user.id, f'Language: {i[0]}')
    

# Get description language by column name from db with class method get_desc()
# class Description():
#     def __init__(self, message, name):
#         self.message = message
#         self.name = name

#     async def get_desc(self):
#         await cur.execute("SELECT img, name, description FROM materials_telegram WHERE name=%s", (self.name,))
#         ret = await cur.fetchall()
#         await bot.send_photo(self.message.from_user.id, ret[0][0], f'Language: {ret[0][1]}\nDescription:{ret[0][2]}')


async def show_likes():
    await cur.execute("SELECT COUNT(res) FROM telegram_like WHERE res = '1'")
    likes = await cur.fetchall()
    await cur.execute("SELECT COUNT(res) FROM telegram_like WHERE res = '2'")
    dislikes = await cur.fetchall()
    # await bot.send_message(self.message.from_user.id , f'\U0001F44D {likes[0][0]}   \U0001F44E {dislikes[0][0]}')
    return likes, dislikes

class DbLike():
    def __init__(self, message) -> None:
        self.message = message

    async def write(self):
        await cur.execute("SELECT EXISTS(SELECT res FROM telegram_like WHERE user_id = '%s' AND res=3)"%(self.message.from_user.id))
        # cur.execute("SELECT user_id from telegram_like WHERE user_id = '%s'"%(self.message.from_user.id,))
        rep = await cur.fetchall()
        if rep[0][0] == 1:
            await cur.execute("UPDATE telegram_like SET res = '%s' WHERE user_id = '%s'"%(int(self.message.data.split('_')[1]), self.message.from_user.id))
            await base.commit()
            # await DbLike.show_likes(self)
        elif rep[0][0] == 0:
            await self.message.answer('You already chose')
            # await DbLike.show_likes(self)
    


    async def show_likes():
        await cur.execute("SELECT COUNT(res) FROM telegram_like WHERE res = '1'")
        likes = await cur.fetchall()
        await cur.execute("SELECT COUNT(res) FROM telegram_like WHERE res = '2'")
        dislikes = await cur.fetchall()
        # await bot.send_message(self.message.from_user.id , f'\U0001F44D {likes[0][0]}   \U0001F44E {dislikes[0][0]}')
        return (likes, dislikes)


class CourseData():
    # def __init__(self, message):
    #     self.message = message

    async def save_phone(message, phone):
        await cur.execute("SELECT EXISTS(SELECT * FROM telegram_like WHERE user_id = '%s')"%(message.from_user.id,))
        res = await cur.fetchall()
        if res[0][0] == 0:
            answer = (
                message.from_user.id,
                message.from_user.username,
                message.from_user.first_name,
                message.from_user.last_name,
                3,
                phone,
            )
            await cur.execute("INSERT INTO telegram_like VALUES('%s', '%s', '%s', '%s', '%s', '%s')"%answer)
            await base.commit()
        await cur.execute("UPDATE telegram_like SET phone = '%s' WHERE user_id = '%s'"%(phone, message.from_user.id))
        await base.commit()


    async def user_from_db(message):
        await cur.execute("SELECT * FROM telegram_like WHERE user_id ='%s'"%(message.from_user.id,))
        check = await cur.fetchall()
        return check

    async def uprowed_user_from_db(message):
        await cur.execute("SELECT is_approved, user_id, courses_id FROM materials_userprofile WHERE phone = (SELECT phone FROM telegram_like WHERE user_id ='%s')"%(message.from_user.id,))
        check = await cur.fetchall()
        return check
    
    async def course_from_db(course_id):
        await cur.execute("SELECT * FROM materials_course WHERE id = '%s'"%(course_id,))
        course = await cur.fetchall()
        await cur.execute("SELECT number, name, id FROM materials_lesson WHERE id in (SELECT lesson_id FROM materials_course_lesson1 WHERE course_id = '%s')"%(course_id,))
        lessons = await cur.fetchall()
        await cur.execute("SELECT * FROM materials_material WHERE id in (SELECT material_id FROM materials_lesson_materials WHERE lesson_id in (SELECT id FROM materials_lesson WHERE id in (SELECT lesson_id FROM materials_course_lesson1 WHERE course_id = '%s')))"%(course_id,))
        lesson_materials = await cur.fetchall()
        await cur.execute("SELECT * FROM materials_material WHERE id in (SELECT material_id FROM materials_course_materials WHERE course_id = '%s')"%(course_id,))
        addition_materials = await cur.fetchall()
        

        return course, lessons, lesson_materials, addition_materials

    async def addition_inf(course_id):
        await cur.execute("SELECT * FROM materials_material WHERE id in (SELECT material_id FROM materials_course_materials WHERE course_id = '%s')"%(course_id,))
        addition_materials = await cur.fetchall()
        return addition_materials

    async def new(course_id):
        # cur.execute("SELECT m.id, mlsm.lesson_id  FROM materials_material m inner join materials_lesson_materials mlsm on mlsm.material_id=m.id inner join materials_course_lesson1 mcl on mcl.course_id= '%s' AND mcl.lesson_id=mlsm.lesson_id"%(course_id,))
        await cur.execute("select materials_material.id as mat_id, \
                        materials_lesson_materials.lesson_id as less_id \
                        from materials_material inner join materials_lesson_materials \
                        on materials_material.id=materials_lesson_materials.material_id \
                        inner join materials_course_lesson1 on materials_lesson_materials.lesson_id=materials_course_lesson1.lesson_id \
                        and materials_course_lesson1.course_id='%s'"%(course_id,)
                        )
        res = await cur.fetchall()    
        return res
       

