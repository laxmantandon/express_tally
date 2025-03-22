import click

from express_tally.setup import after_install as setup


def after_install():
	try:
		print("Setting up Express Tally...")
		setup()

		click.secho("Thank you for installing Express Tally!", fg="green")

	except Exception as e:
		BUG_REPORT_URL = "https://github.com/efeone/express_tally/issues/new"
		click.secho(
			"Installation for Express Tally app failed due to an error."
			" Please try re-installing the app or"
			f" report the issue on {BUG_REPORT_URL} if not resolved.",
			fg="bright_red",
		)
		raise e
