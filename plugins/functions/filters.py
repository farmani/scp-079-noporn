# SCP-079-NOPORN - Auto delete NSFW media messages
# Copyright (C) 2019 SCP-079 <https://scp-079.org>
#
# This file is part of SCP-079-NOPORN.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

from pyrogram import Filters, Message

from .. import glovar
from .ids import init_group_id


# Enable logging
logger = logging.getLogger(__name__)


def is_class_c(_, message: Message) -> bool:
    try:
        uid = message.from_user.id
        gid = message.chat.id
        init_group_id(gid)
        if uid in glovar.admin_ids.get(gid, set()) or uid in glovar.bot_ids or message.from_user.is_self:
            return True
    except Exception as e:
        logger.warning(f"Is class c error: {e}", exc_info=True)

    return False


def is_class_d(_, message: Message) -> bool:
    try:
        uid = message.from_user.id
        if uid in glovar.bad_ids["users"]:
            return True

        if message.forward_from_chat:
            cid = message.forward_from_chat.id
            if cid in glovar.bad_ids["channels"]:
                return True
    except Exception as e:
        logger.warning(f"Is class d error: {e}", exc_info=True)


def is_class_e(_, message: Message) -> bool:
    try:
        uid = message.from_user.id
        if uid in glovar.except_ids["users"]:
            return True

        if message.forward_from_chat:
            cid = message.forward_from_chat.id
            if cid in glovar.except_ids["channels"]:
                return True
    except Exception as e:
        logger.warning(f"Is class e error: {e}", exc_info=True)

    return False


def is_exchange_channel(_, message: Message) -> bool:
    cid = message.chat.id
    if cid == glovar.exchange_channel_id:
        return True

    return False


def is_new_group(_, message: Message) -> bool:
    new_users = message.new_chat_members
    for user in new_users:
        if user.is_self:
            return True

    return False


def is_test_group(_, message: Message) -> bool:
    cid = message.chat.id
    if cid == glovar.test_group_id:
        return True

    return False


class_c = Filters.create(
    name="Class C",
    func=is_class_c
)

class_d = Filters.create(
    name="Class D",
    func=is_class_d
)

class_e = Filters.create(
    name="Class E",
    func=is_class_e
)

exchange_channel = Filters.create(
    name="Exchange Channel",
    func=is_exchange_channel
)

new_group = Filters.create(
    name="New Group",
    func=is_new_group
)

test_group = Filters.create(
    name="Test Group",
    func=is_test_group
)