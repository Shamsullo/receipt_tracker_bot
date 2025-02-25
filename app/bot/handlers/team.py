# app/bot/handlers/team.py
import logging
from aiogram import Router, types
from aiogram.filters import Command

from app.services.team_service import TeamService

logger = logging.getLogger(__name__)


class TeamHandlers:
    def __init__(self, team_service: TeamService):
        self.team_service = team_service

    async def cmd_create_team(self, message: types.Message):
        try:
            args = message.get_args()
            if not args:
                await message.reply(
                    "Please provide a team name: /create_team team_name")
                return

            success, result_message = await self.team_service.create_team(
                telegram_id=message.from_user.id,
                team_name=args
            )

            await message.reply(result_message)

        except Exception as e:
            logger.error(f"Error creating team: {e}", exc_info=True)
            await message.reply("An error occurred while creating the team")

    async def cmd_invite(self, message: types.Message):
        try:
            args = message.get_args()
            if not args:
                await message.reply(
                    "Please provide a username: /invite @username")
                return

            username = args.lstrip('@')
            success, result_message = await self.team_service.invite_user(
                admin_telegram_id=message.from_user.id,
                username=username
            )

            await message.reply(result_message)

        except Exception as e:
            logger.error(f"Error inviting user: {e}", exc_info=True)
            await message.reply("An error occurred while inviting the user")


def setup_team_handlers(router: Router, team_service: TeamService):
    handlers = TeamHandlers(team_service)
    router.message.register(
        handlers.cmd_create_team,
        Command("create_team")
    )
    router.message.register(
        handlers.cmd_invite,
        Command("invite")
    )