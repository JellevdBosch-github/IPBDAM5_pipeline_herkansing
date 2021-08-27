from pipeline_components.staging_master import runner as staging


def run():
	staging.run_hourly()


run()

