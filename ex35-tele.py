import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

bear_room = False
evil_room = False
gold_room = False
start_room = False
bear_moved = False

def reset():
    global bear_room 
    global evil_room 
    global gold_room 
    global start_room
    global bear_moved
    bear_room = False
    evil_room = False
    gold_room = False
    start_room = False
    bear_moved = False

def bear_room_state():
    global bear_room 
    global evil_room 
    global gold_room 
    global start_room
    global bear_moved
    bear_room = True
    evil_room = False
    gold_room = False
    start_room = False
    bear_moved = False

def bear_room_state_bear_moved():
    global bear_room 
    global evil_room 
    global gold_room 
    global start_room
    global bear_moved
    bear_room = True
    evil_room = False
    gold_room = False
    start_room = False
    bear_moved = True

def evil_room_state():
    global bear_room 
    global evil_room 
    global gold_room 
    global start_room
    global bear_moved
    bear_room = False
    evil_room = True
    gold_room = False
    start_room = False
    bear_moved = False

def gold_room_state():
    global bear_room 
    global evil_room 
    global gold_room 
    global start_room
    global bear_moved
    bear_room = False
    evil_room = False
    gold_room = True
    start_room = False
    bear_moved = False

def start_room_state():
    global bear_room 
    global evil_room 
    global gold_room 
    global start_room
    global bear_moved
    bear_room = False
    evil_room = False
    gold_room = False
    start_room = True
    bear_moved = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_room_state()
    msg = """You are in a dark room.
There is a door to your right and left.
Which one do you take?"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

async def story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    

    skip = False
    choice = update.message.text
    if "left" in choice and "right" in choice and start_room:
        msg = "You can't go both ways! It's either left or right."
    
    elif "left" in choice and "right" not in choice and start_room:
        bear_room_state()
        msg = """There is a bear here.
The bear has a bunch of honey.
The fat bear is in front of another door.
How are you going to move the bear?"""
        bear = True
    
    elif choice == "take honey" and bear_room and not bear_moved:
        msg = "The bear looks at you then slaps your face off."
        reset()
    
    elif choice == "taunt bear" and bear_room and not bear_moved:
        bear_room_state_bear_moved()
        msg = """The bear has moved from the door.
You can go through it now."""
        choice = ""
    
    elif choice == "taunt bear" and bear_moved:
        msg = "The bear gets pissed off and chews your leg off."
        reset()
   
    elif choice == "open door" and bear_moved:
        gold_room_state()
        msg = "This room is full of god.  How much do you take?"
    
    elif gold_room:
        try:
            how_much = int(choice)
            if how_much < 50:
                msg = "Nice, you're not greedy, you win!"
                #reset()
            else:
                msg = "You greedy bastard!"
                #reset()
        except:
            msg = "Man, learn to type a number."
            #reset()

    elif bear_moved or bear_room:
        msg = "I have no idea what that means."

    elif "right" in choice and "left" not in choice and start_room:
        evil_room_state()
        msg = """Here you see the great evil Cthulhu.
He, it, whatever stares at you and you go insane.
Do you flee for your life or eat your head?"""
    
    elif "right" not in choice and "left" not in choice and start_room:
        msg = "You stumble around the room until you starve."
        reset()
    
    elif "flee" in choice and evil_room:
        start_room_state()
        msg = """You are in a dark room.
There is a door to your right and left.
Which one do you take?"""

    elif "head" in choice and evil_room:
        msg = "Well that was tasty! Good job!"
        reset()
    
    else:
        skip = True

    if not skip:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

if __name__ == '__main__':
    application = ApplicationBuilder().token('TOKEN').build()

    start_handler = CommandHandler('start', start)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), story)
    
    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()
