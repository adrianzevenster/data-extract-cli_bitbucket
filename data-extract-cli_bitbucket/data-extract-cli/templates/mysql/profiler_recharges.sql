SELECT
pr_subscribers.msisdn as "MSISDN",
pr_transactions.timestamp as "RECHARGE_DATE",
pr_transactions.transactionamount as "RECHARGE_AMOUNT"

FROM av_microservice_profiler.pr_transaction pr_transactions 

LEFT JOIN av_microservice_profiler.pr_subscriber pr_subscribers
ON pr_transactions.subscriberid = pr_subscribers.subscriberid

-- Recharges only
WHERE pr_transactions.transactiontype = 1     

AND pr_subscribers.msisdn IN 
(
	SELECT DISTINCT (_subscribers.msisdn)
	FROM av_microservice_lending.advance _advances FORCE INDEX(idx_loandate)

	INNER JOIN av_microservice_lending.subscriber _subscribers  -- inner join advance and subscriber table to get msisdn
	ON _advances.subscriberid = _subscribers.subscriberid

	-- Range start date in format 'YYYY-MM-DD'
	WHERE _advances.loandate >= %(loan_start_date)s    
	-- Range end date in format 'YYYY-MM-DD'
	AND _advances.loandate <= %(loan_end_date)s
	{% if tier_ids %}
		AND _advances.profiletierid IN %(tier_ids)s
	{% endif %}
	{% if msisdn_constraint %}
		AND _subscribers.msisdn LIKE %(msisdn_constraint)s
	{% endif %}                          -- optional filter
)
AND pr_transactions.timestamp >= %(historical_start_date)s                -- Advance range start date in format "YYYY-MM-DD"
AND pr_transactions.timestamp <= %(historical_end_date)s
