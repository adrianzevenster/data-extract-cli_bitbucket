SELECT
subscribers.msisdn AS "MSISDN",
payments.indate AS "IN_DATE" ,
payments.rechargeamt AS "PAYMENT_AMOUNT" ,
payments.advanceid AS "ADVANCE_ID",
advances.channelid AS "CHANNEL_ID",
advances.loandate AS "LOAN_DATE",
advances.loanamt AS "LOAN_AMOUNT",
advances.servicefee AS "SERVICE_FEE",
advances.statusid AS "STATUS_ID",
advances.profiletierid AS "PROFILE_TIER_ID"

FROM av_microservice_lending.payment payments

INNER JOIN av_microservice_lending.advance advances 
ON payments.advanceid = advances.advanceid

INNER JOIN av_microservice_lending.subscriber subscribers
ON advances.subscriberid = subscribers.subscriberid

WHERE subscribers.subscriberid IN 
(
	SELECT DISTINCT (_advances.subscriberid)
	FROM av_microservice_lending.advance _advances FORCE INDEX(idx_loandate)
	-- Range start date in YYYY-MM-DD format
	WHERE _advances.loandate >= %(loan_start_date)s  
	-- Range end date in YYYY-MM-DD format
	AND _advances.loandate <= %(loan_end_date)s        
	{% if tier_ids %}
		AND _advances.profiletierid IN %(tier_ids)s
	{% endif %}
)
{% if msisdn_constraint %}
	AND subscribers.msisdn LIKE %(msisdn_constraint)s
{% endif %}
AND payments.indate >= %(historical_start_date)s                -- Advance range start date in format "YYYY-MM-DD"
AND payments.indate <= %(historical_end_date)s



