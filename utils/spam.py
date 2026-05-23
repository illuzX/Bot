SPAM = {}

def anti_spam(user_id):

    import time

    now = time.time()

    if user_id in SPAM:

        if now - SPAM[user_id] < 2:

            return False

    SPAM[user_id] = now

    return True
