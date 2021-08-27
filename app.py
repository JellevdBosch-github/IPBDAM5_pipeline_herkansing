from pipeline_components.staging_master import runner as stream
from pipeline_components.staging_master import run_batch as batch


def run():
	# batch.run()
	stream.run_staging()


run()

