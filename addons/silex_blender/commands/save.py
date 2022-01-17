import logging

from silex_client.action.command_base import CommandBase
from silex_client.action.action_query import ActionQuery


class Save(CommandBase):
    """
    Save current scene with context as path
    """

    parameters = {
        "file_path": {"label": "filename", "type": str},
    }

    @CommandBase.conform_command()
    async def __call__(
        self,
        parameters,
        action_query: ActionQuery,
        logger: logging.Logger,
    ):
        print("Executing save")
