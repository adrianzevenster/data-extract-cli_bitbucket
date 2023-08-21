Feature: Run Extract
	Scenario: A Successfull Data Extract
		Given a valid extract-request.json input file
		When the `extract` CLI verb is called for run_extract
		Then I see a valid CSV data file on S3
