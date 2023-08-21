Feature: Data Contracts
	Scenario: User runs a full data extract and wants to use specific columns
		Given a extract-request.json input file requesting a full extract
		When the `extract` CLI verb is called for data_contracts
		Then the CSV data conforms to the lending_advances contract
		Then the CSV data conforms to the lending_payments contract
		Then the CSV data conforms to the profiler_recharges contract

