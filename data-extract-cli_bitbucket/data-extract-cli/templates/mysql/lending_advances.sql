SELECT
subscribers.msisdn AS "MSISDN",
advances.advanceid AS "ADVANCE_ID",
advances.channelid AS "CHANNEL_ID",
advances.loandate AS "LOAN_DATE",
advances.loanamt AS "LOAN_AMOUNT",
advances.servicefee AS "SERVICE_FEE",
advances.statusid AS "STATUS_ID",
advances.profiletierid AS "PROFILE_TIER_ID"

-- Join advance to subscriberid to obtain the MSISDN
FROM av_microservice_lending.advance advances
LEFT JOIN av_microservice_lending.subscriber subscribers 
ON advances.subscriberid = subscribers.subscriberid 

WHERE subscribers.subscriberid IN 
(
	SELECT DISTINCT (_advances.subscriberid)
	FROM av_microservice_lending.advance _advances FORCE INDEX(idx_loandate)
	-- Range start date in YYYY-MM-DD format
	WHERE _advances.loandate >= %(loan_start_date)s  
	-- Range end date in YYYY-MM-DD       
	AND _advances.loandate <= %(loan_end_date)s        
	{% if tier_ids %}
		AND _advances.profiletierid IN %(tier_ids)s
	{% endif %}
)
{% if msisdn_constraint %}
	AND subscribers.msisdn LIKE %(msisdn_constraint)s
{% endif %}
AND advances.loandate >= %(historical_start_date)s                -- Advance range start date in format "YYYY-MM-DD"
AND advances.loandate <= %(historical_end_date)s
