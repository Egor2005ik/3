from . import add_user
from . import spam_manager
from . import join_to_chat
from . import info

blueprints = (
    add_user.user,
    spam_manager.user,
    join_to_chat.user,
    info.user,
)
