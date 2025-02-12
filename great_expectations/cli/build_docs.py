from typing import List, Optional

from great_expectations import DataContext
from great_expectations.cli import toolkit
from great_expectations.cli.cli_logging import logger
from great_expectations.cli.pretty_printing import cli_message


def build_docs(
    context: DataContext,
    site_names: Optional[List[str]] = None,
    view: bool = True,
    assume_yes: bool = False,
) -> None:
    """Build documentation in a context"""
    logger.debug("Starting cli.datasource.build_docs")

    index_page_locator_infos = context.build_data_docs(
        site_names=site_names, dry_run=True
    )
    msg: str = "\nThe following Data Docs sites will be built:\n\n"
    for site_name, index_page_locator_info in index_page_locator_infos.items():
        msg += " - <cyan>{}:</cyan> ".format(site_name)
        msg += "{}\n".format(index_page_locator_info)

    cli_message(msg)
    if not assume_yes:
        toolkit.confirm_proceed_or_exit()

    cli_message("\nBuilding Data Docs...\n")
    context.build_data_docs(site_names=site_names)

    cli_message("Done building Data Docs")

    if view and site_names:
        for site_to_open in site_names:
            context.open_data_docs(site_name=site_to_open, only_if_exists=True)
