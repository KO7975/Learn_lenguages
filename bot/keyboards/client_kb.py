from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton#, ReplyKeyboardRemove
from create_bot import dp


#emojis
teacher_em =u'\U0001F469'
arr_down_em = u'\U00002b07'
arr_right_em =u'\U000027a1'
arr_left_em = u'\U00002b05'
arr_up_em = u'\U000023EB'

#inline buttons created
inkb = InlineKeyboardMarkup(row_width=1)
inb1 = InlineKeyboardButton(text='🇬🇧󠁧󠁢󠁥󠁮🇺🇸  English  🇺🇸🇬🇧',  callback_data='en')
inb2 = InlineKeyboardButton(text=f'🇪🇸 Spanish  🇪🇸', callback_data='sp')
inb3 = InlineKeyboardButton(text=f'🇵🇱  Polish  🇵🇱', callback_data='ps')
inb4 = InlineKeyboardButton(text=f'🇬🇧\U00002693  English for seamen  \U00002693🇬🇧', callback_data='en_s')
x = [
    InlineKeyboardButton(text='Read_more', callback_data='rm'),
    InlineKeyboardButton(text='facebook', url='https://www.facebook.com/staciewhite22', callback_data='fb'),
    InlineKeyboardButton(text='My website', callback_data='web' )
    ]

inkb.add(inb1).add(inb2).add(inb3).add(inb4).row(*x)
inlkb = InlineKeyboardMarkup(row_width=1)\
    .add(InlineKeyboardButton(text='like', callback_data='ln_1'))\
    .add(InlineKeyboardButton(text='dislike', callback_data='ln_2'))
# inkb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Press me', callback_data='www'))
to_teacher=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Write Your question', url='https://t.me/@Pirat17'))

#Keybourd buttons
b1 = KeyboardButton('/Working_time⌚')
b2 = KeyboardButton('/Course_list\U0001F4D1')
b3 = KeyboardButton('/All_Courses\U0001F4DA')
b4 = KeyboardButton('/contacts💬')
# b5 = KeyboardButton('/sent my position', request_location=True)
# b6 = KeyboardButton('/sent my number', request_contact=True)
b7 = KeyboardButton('/💰price')
b8  =KeyboardButton('get_contact',  request_contact=True)
b9 = KeyboardButton('/like')
b10 = KeyboardButton('/update')
b11 = KeyboardButton('/Your_course_data')
kb_client1 = ReplyKeyboardMarkup() #(resize_keyboard=True, one_time_keyboard=True)

# kb_client.add(b1).add(b2).insert(b3).insert(b4)
# kb_client.row(b1, b2, b3, b4)
kb_client1.add(b10).row(b1,b4,b7).row(b2, b3).row(b9)#.row(b5,b6)
kb_client2 = ReplyKeyboardMarkup()
kb_client2.add(b10).row(b1,b4,b7).row(b2, b3).row(b9).add(b11)

#Inline buttons links
# inb = InlineKeyboardMarkup(row_width=1)
# inb1 = InlineKeyboardButton(text='English')
# inb2 = InlineKeyboardButton(text='Spanish')
# inb3 = InlineKeyboardButton(text='Polish')
# inb4 = InlineKeyboardButton(text='English for seamen')
# x = [InlineKeyboardButton(text='Read_more', url='localhost'), InlineKeyboardButton(text='facebook', url='https://www.facebook.com/staciewhite22')]

# inb.add(inb1, inb2, inb3, inb4).row(*x)


#course inline_buttons
def courses(lesson, number, cbdt):
    les = InlineKeyboardMarkup(row_width=1)
    lesson_btn = InlineKeyboardButton(text=f'Lesson {lesson} № {number}', callback_data=cbdt)
    les.add(lesson_btn)
    return les

def material_kb(title, callbac_data):
    mat = InlineKeyboardMarkup(row_width=1)
    mat_btn = InlineKeyboardButton(text=f'{title}', callback_data=callbac_data)
    return mat.add(mat_btn)

    




